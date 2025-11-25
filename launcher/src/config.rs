use dirs;
use std::path::{
    PathBuf,
};
use directories::{
    ProjectDirs,
};
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
        let gerdoo_path = get_gerdoo_app_path();
        Self {
            server_pid: None,
            current_version: "0.0.0".to_owned(),
            app_path: PathBuf::from(gerdoo_path),
        }
    }
}


fn get_gerdoo_app_path() -> PathBuf {
    let mut home_dir = dirs::home_dir().unwrap();
    home_dir.push("gerdoo");
    home_dir.push("app");
    home_dir
}