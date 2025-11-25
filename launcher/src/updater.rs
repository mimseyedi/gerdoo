use eframe::{self, egui, App, Frame};
use tokio::sync::{Mutex, MutexGuard};
use std::sync::{Arc,};
use std::thread;
use crate::update::UpdateManager;
use std::time::Duration;


pub struct UpdaterApp {
    manager: Arc<Mutex<UpdateManager>>,
    should_close: bool,
}


impl UpdaterApp {
    pub fn new(manager: UpdateManager) -> Self {
        let manager_arc = Arc::new(Mutex::new(manager));
        let manager_clone = manager_arc.clone();

        tokio::spawn(async move {
            let update_needed;
            {
                let mut mgr = manager_clone.lock().await;
                mgr.check_for_update().await;
                update_needed = mgr.update_available;
            }
            if update_needed {
                let mut mgr = manager_clone.lock().await;
                mgr.start_download_and_install().await;
            }
        });

        UpdaterApp {
            manager: manager_arc,
            should_close: false,
        }
    }
}

impl App for UpdaterApp {
    fn update(&mut self, ctx: &egui::Context, frame: &mut Frame) {
        let mgr = match self.manager.try_lock() {
            Ok(mgr_guard) => mgr_guard,
            Err(_) => {
                ctx.request_repaint();
                return;
            }
        };

        egui::CentralPanel::default().show(ctx, |ui| {
            ui.label(format!("Status: {:?}", mgr.status));
            if let crate::update::UpdateStatus::Downloading(progress) = mgr.status {
                ui.add(egui::ProgressBar::new(progress).show_percentage());
            }
            if let Some(err) = &mgr.error_message {
                ui.label(egui::RichText::new(format!("Error: {}", err)).color(egui::Color32::RED));
            }
        });

        if mgr.check_complete { self.should_close = true; }

        if self.should_close {
            let ctx = ctx.clone();
            thread::spawn(move || {
                ctx.send_viewport_cmd(egui::ViewportCommand::Close);
            });
            self.should_close = false;
        }

        ctx.request_repaint();
    }

    fn on_exit(&mut self, _gl: Option<&eframe::glow::Context>) {
        self.should_close;
    }
}