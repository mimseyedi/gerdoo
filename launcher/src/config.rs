use dirs;
use std::fs;
use std::path::{
    Path,
    PathBuf,
};
use directories::{
    ProjectDirs,
};
use serde_json;
use serde::{
    Deserialize,
    Serialize,
};


#[derive(
    Debug,
    Clone,
    Serialize,
    Deserialize,
)]
pub struct AppConfig {
    pub server_pid: Option<u32>,
    pub current_version: String,
    pub app_path: PathBuf,
}


impl AppConfig {
    const QUA: &'static str = "app";
    const ORG: &'static str = "Gerdoo";
    const APP: &'static str = "Launcher";

    pub fn load() -> Result<Self, String> {
        let path = Self::prepare()?;
        if !path.exists() {
            let default_config = Self::default();
            default_config.save()?;
            return Ok(default_config);
        }
        let file_content = std::fs::read_to_string(path)
            .map_err(|e| format!("Error: {}", e))?;
        serde_json::from_str(&file_content)
            .map_err(|e| format!("Error: {}", e))
    }

    pub fn save(&self) -> Result<(), String> {
        let path = Self::prepare()?;
        let json_content = serde_json::to_string_pretty(self)
            .map_err(|e| format!("Error: {}", e))?;
        std::fs::write(path, json_content)
            .map_err(|e| format!("Error: {}", e))
    }

    fn prepare() -> Result<PathBuf, String> {
        let launcher_dir = Self::get_launcher_sys_path()?;
        let config_dir = launcher_dir.config_dir();
        std::fs::create_dir_all(config_dir)
            .map_err(|e| format!("Error: {}", e))?;
        Ok(config_dir.join("config.json"))
    }

    fn get_launcher_sys_path() -> Result<ProjectDirs, String> {
        ProjectDirs::from(
            Self::QUA,
            Self::ORG,
            Self::APP,
        ).ok_or_else(|| "Not found!".to_owned())
    }
}


impl Default for AppConfig {
    fn default() -> Self {
        Self {
            server_pid: None,
            current_version: first_version().to_owned(),
            app_path: PathBuf::from(get_gerdoo_app_path()),
        }
    }
}


fn first_version() -> String {
    let fallback_version = "0.1.0".to_owned();

    let mut manifest = get_gerdoo_app_path();
    manifest.push("update_manifest.json");
    if !Path::new(&manifest).exists() {
        return fallback_version;
    }

    let content = match fs::read_to_string(&manifest) {
        Ok(c) => c,
        Err(e) => {
            eprintln!("{}", e);
            return fallback_version;
        }
    };

    let value: serde_json::Value = match serde_json::from_str(&content) {
        Ok(v) => v,
        Err(e) => {
            eprintln!("{}", e);
            return fallback_version;
        }
    };

    if let Some(version_str) = value["version"].as_str() {
        return version_str.to_owned();
    }
    fallback_version
}


fn get_gerdoo_app_path() -> PathBuf {
    let mut home_dir = dirs::home_dir().unwrap();
    home_dir.push("gerdoo");
    home_dir.push("app");
    home_dir
}