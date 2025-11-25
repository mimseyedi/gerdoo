use std::path::{PathBuf, Path};
use std::cmp::Ordering;
use std::process::Command;
use std::fs;
use serde::Deserialize;
use reqwest;
use serde_json;
use tokio::time::{self, Duration};


#[derive(
    Debug,
    Clone,
    PartialEq,
)]
pub enum UpdateStatus {
    Checking,
    CheckingInternet,
    CheckingForUpdates,
    UpdateAvailable(String),
    NoUpdate,
    Downloading(f32),
    Installing,
    Complete,
    Error(String),
}


#[derive(
    Debug,
    Deserialize,
)]
pub struct RemoteManifest {
    pub version: String,
    pub description: String,
}


pub struct UpdateManager {
    app_base_path: PathBuf,
    current_version: String,
    remote_manifest_url: String,
    pub status: UpdateStatus,
    pub update_available: bool,
    pub remote_manifest: Option<RemoteManifest>,
    pub check_complete: bool,
    pub download_success: bool,
    pub error_message: Option<String>,
}


pub fn version_cmp(v1: &str, v2: &str) -> bool {
    let mut v1_iter = v1
        .split('.')
        .filter_map(|s| s.parse::<u32>().ok());
    let v1_major = v1_iter.next().unwrap_or(0);
    let v1_minor = v1_iter.next().unwrap_or(0);
    let v1_patch = v1_iter.next().unwrap_or(0);

    let mut v2_iter = v2
        .split('.')
        .filter_map(|s| s.parse::<u32>().ok());
    let v2_major = v2_iter.next().unwrap_or(0);
    let v2_minor = v2_iter.next().unwrap_or(0);
    let v2_patch = v2_iter.next().unwrap_or(0);

    if v2_major > v1_major { return true ; }
    if v2_major < v1_major { return false; }

    if v2_minor > v1_minor { return true ; }
    if v2_minor < v1_minor { return false; }

    if v2_patch > v1_patch { return true ; }

    false
}


async fn run_sparse_checkout(app_base_path: &Path, temp_path: &Path) -> Result<(), String> {
    const GIT_REPO_URL: &str = "https://github.com/mimseyedi/gerdoo.git";
    const APP_DIR_NAME: &str = "app";

    if temp_path.exists() {
        let _ = fs::remove_dir_all(temp_path);
    }
    fs::create_dir(temp_path)
        .map_err(|e| format!("Failed to create temp dir: {}", e))?;

    let output = Command::new("git")
        .arg("clone")
        .arg("--no-checkout")
        .arg(GIT_REPO_URL)
        .arg(temp_path)
        .output()
        .map_err(|e| format!("Failed to run git clone: {}", e))?;

    if !output.status.success() {
        return Err(format!("Git Clone failed: {}", String::from_utf8_lossy(&output.stderr)));
    }

    let output = Command::new("git")
        .arg("sparse-checkout")
        .arg("init")
        .current_dir(temp_path)
        .output()
        .map_err(|e| format!("Failed to init sparse-checkout: {}", e))?;

    if !output.status.success() {
        return Err(format!("Git Sparse Init failed: {}", String::from_utf8_lossy(&output.stderr)));
    }

    let output = Command::new("git")
        .arg("sparse-checkout")
        .arg("set")
        .arg(APP_DIR_NAME)
        .current_dir(temp_path)
        .output()
        .map_err(|e| format!("Failed to set sparse-checkout path: {}", e))?;

    if !output.status.success() {
        return Err(format!("Git Sparse Set failed: {}", String::from_utf8_lossy(&output.stderr)));
    }

    let output = Command::new("git")
        .arg("checkout")
        .current_dir(temp_path)
        .output()
        .map_err(|e| format!("Failed to run git checkout: {}", e))?;

    if !output.status.success() {
        return Err(format!("Git Checkout failed: {}", String::from_utf8_lossy(&output.stderr)));
    }

    Ok(())
}


impl UpdateManager {
    const DEFAULT_MANIFEST_URL: &'static str = "https://raw.githubusercontent.com/Gerdoo/gerdoo-repo/main/update_manifest.json";
    const TEMP_DIR_NAME: &'static str = "gerdoo_update_temp";
    const APP_SUB_DIR: &'static str = "app";

    pub fn new(app_base_path: PathBuf, current_version: String) -> Self {
        UpdateManager {
            app_base_path,
            current_version,
            remote_manifest_url: Self::DEFAULT_MANIFEST_URL.to_owned(),
            status: UpdateStatus::Checking,
            update_available: false,
            remote_manifest: None,
            check_complete: false,
            download_success: false,
            error_message: None,
        }
    }

    pub async fn check_for_update(&mut self) {
        self.status = UpdateStatus::CheckingForUpdates;
        time::sleep(Duration::from_millis(500)).await;
        let client = reqwest::Client::new();

        let response = match client.get(&self.remote_manifest_url).send().await {
            Ok(res) => res,
            Err(e) => {
                self.status = UpdateStatus::Error(format!("Network error: {}", e));
                self.check_complete = true;
                return;
            }
        };

        let remote_manifest_json = match response.json::<RemoteManifest>().await {
            Ok(manifest) => manifest,
            Err(e) => {
                self.status = UpdateStatus::Error(format!("Failed to parse remote manifest: {}", e));
                self.check_complete = true;
                return;
            }
        };

        let remote_version = &remote_manifest_json.version.clone();

        match version_cmp(&self.current_version, remote_version) {
            true => {
                self.update_available = true;
                self.remote_manifest = Some(remote_manifest_json);
                self.status = UpdateStatus::UpdateAvailable(remote_version.to_string());
            }
            false => {
                self.update_available = false;
                self.status = UpdateStatus::NoUpdate;
                self.check_complete = true;
            }
        }
    }

    pub async fn start_download_and_install(&mut self) {
        let temp_dir_path = self.app_base_path.join(Self::TEMP_DIR_NAME);
        self.status = UpdateStatus::Downloading(0.0);

        match run_sparse_checkout(&self.app_base_path, &temp_dir_path).await {
            Ok(_) => {
                self.status = UpdateStatus::Downloading(0.9);

                self.status = UpdateStatus::Installing;

                let old_app_path = self.app_base_path.join(Self::APP_SUB_DIR);
                let new_app_path = temp_dir_path.join(Self::APP_SUB_DIR);

                if old_app_path.exists() {
                    let _ = fs::remove_dir_all(&old_app_path);
                }

                match fs::rename(&new_app_path, &old_app_path) {
                    Ok(_) => {
                        let _ = fs::remove_dir_all(&temp_dir_path);
                        self.status = UpdateStatus::Complete;
                        self.download_success = true;
                    }
                    Err(e) => {
                        self.status = UpdateStatus::Error(format!("Installation failed: {}", e));
                    }
                }
            }
            Err(e) => {
                self.status = UpdateStatus::Error(format!("Download failed (Git error): {}", e));
            }
        }
        self.check_complete = true;
    }
}