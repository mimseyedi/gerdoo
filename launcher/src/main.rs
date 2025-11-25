mod gui;
mod setup;
mod server;
mod config;
mod update;

use egui::Key::A;
use config::{
    AppConfig,
};


#[tokio::main]
async fn main() -> eframe::Result<()> {
    let cfg = AppConfig::load()
        .unwrap_or_else( |e| {
            eprintln!("Error: {}", e);
            AppConfig::default()
        });
    gui::run_gui(cfg).await
}