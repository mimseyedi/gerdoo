use std::fs;
use std::path::PathBuf;
use serde::{
    Serialize,
    Deserialize,
};
use crate::output::Response;


#[derive(Deserialize)]
struct Manifest {
    version: String,
}


pub enum ConfigAttr {
    Version(String),
    LastPid(Option<u32>),
}


#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Config {
    pub version: String,
    pub last_pid: Option<u32>,
}


impl Config {
    fn get_path() -> PathBuf {
        let mut path = dirs::config_dir().unwrap_or_else(|| PathBuf::from("."));
        path.push("gerdoo");
        if !path.exists() {
            let _ = fs::create_dir_all(&path);
        }
        path.push("config.json");
        path
    }

    pub fn load() -> Self {
        let path = Self::get_path();

        let mut config = if let Ok(content) = fs::read_to_string(&path) {
            serde_json::from_str::<Self>(&content)
                .unwrap_or_else(|_| Self::default())
        } else {
            Self::default()
        };

        if let Ok(mut manifest_path) = Self::app_path() {
            manifest_path.push("update_manifest.json");

            if let Ok(manifest_content) = fs::read_to_string(manifest_path) {
                if let Ok(manifest) = serde_json::from_str::<Manifest>(
                    &manifest_content
                ) {
                    if config.version != manifest.version {
                        config.version = manifest.version;
                        let _ = config.save();
                    }
                }
            }
        }
        config
    }

    pub fn save(&self) -> Result<(), std::io::Error> {
        let path = Self::get_path();
        let content = serde_json::to_string_pretty(self)?;
        fs::write(path, content)
    }

    pub fn update(&mut self, attr: ConfigAttr) {
        match attr {
            ConfigAttr::Version(version) =>
                self.version = version,
            ConfigAttr::LastPid(last_pid) =>
                self.last_pid = last_pid,
        }
        let _ = self.save();
    }

    pub fn app_path() -> Result<PathBuf, Response> {
        match dirs::home_dir() {
            Some(mut path) => {
                path.push(".gerdoo");
                path.push("app");
                Ok(path)
            },
            None => Err(
                Response::err("Could not find home directory")
            )
        }
    }

    fn default() -> Self {
        Self {
            version: String::from("0.1.0"),
            last_pid: None,
        }
    }
}