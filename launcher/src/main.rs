mod gui;
mod setup;
mod server;
mod config;
mod update;


use config::{
    LauncherConfig,
};


#[tokio::main]
async fn main() -> eframe::Result<()> {
    let cfg = LauncherConfig::load()
        .unwrap_or_else( |e| {
            eprintln!("Error: {}", e);
            LauncherConfig::default()
        });
    gui::run_gui(cfg).await
}