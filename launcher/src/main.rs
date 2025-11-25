use eframe::{self, NativeOptions};
use std::sync::{Arc, Mutex};


mod gui;
mod setup;
mod server;
mod config;
mod update;
mod updater;


use config::AppConfig;
use update::UpdateManager;
use updater::UpdaterApp;
use gui::run_gui;


#[tokio::main]
async fn main() -> eframe::Result<()> {
    let initial_config = AppConfig::load()
        .unwrap_or_else( |e| {
            eprintln!("Error: {}", e);
            AppConfig::default()
        });

    let update_manager = UpdateManager::new(
        initial_config.app_path.clone(),
        initial_config.current_version.clone(),
    );

    let updater_options = eframe::NativeOptions {
        centered: true,
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([400.0, 100.0])
            .with_resizable(false)
            .with_title("Gerdoo Updater")
            .with_always_on_top(),
        ..Default::default()
    };

    eframe::run_native(
        "Gerdoo Updater",
        updater_options,
        Box::new(|_cc| {
            Ok(Box::new(UpdaterApp::new(update_manager)))
        }),
    )?;

    let final_config = AppConfig::load()
        .unwrap_or_else( |e| {
            eprintln!("Error: {}", e);
            initial_config
        });

    gui::run_gui(final_config).await
}