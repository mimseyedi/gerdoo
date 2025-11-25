use opener;
use std::time::Duration;
use chrono::{
    Local,
};
use eframe::{
    self,
    App,
    Frame,
    CreationContext,
};
use egui::{
    self,
    Color32,
    Context,
    RichText,
    TextStyle,
    ScrollArea,
    CentralPanel,
};
use std::sync::{
    Arc,
    Mutex,
};
use tokio::time;
use tokio::sync::mpsc::{
    self,
    Sender,
    Receiver,
};
use crate::{
    server,
};
use crate::config::{
    AppConfig,
};
use crate::server::{
    ConsoleMessage,
};


const WINDOW_ICON_BYTES: &[u8] = include_bytes!(
    "../assets/icons/gerdoo-launcher-logo.png"
);


pub struct LauncherApp {
    config: Arc<Mutex<AppConfig>>,
    console_output: String,
    status_message: String,
    tx: Sender<ConsoleMessage>,
    rx: Receiver<ConsoleMessage>,
    scroll_to_bottom: bool,
}


impl LauncherApp {
    pub fn new(cc: &CreationContext<'_>, initial_config: AppConfig) -> Self {
        let (tx, rx) = mpsc::channel(100);

        let mut style = (*cc.egui_ctx.style()).clone();
        style.visuals.window_fill = Color32::from_gray(30);
        cc.egui_ctx.set_style(style);

        Self {
            config: Arc::new(Mutex::new(initial_config)),
            console_output: "".to_owned(),
            status_message: "Launcher is ready.\n".to_owned(),
            tx,
            rx,
            scroll_to_bottom: true,
        }
    }
}


pub async fn run_gui(initial_config: AppConfig) -> eframe::Result<()> {
    let window_icon = eframe::icon_data::from_png_bytes(WINDOW_ICON_BYTES)
        .expect("Error: Failed to load the windows icon.");

    let viewport = egui::ViewportBuilder::default()
        .with_inner_size([600.0, 450.0])
        .with_resizable(false);

    let options = eframe::NativeOptions {
        centered: true,
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([600.0, 450.0])
            .with_resizable(false)
            .with_icon(Arc::new(window_icon)),
        ..Default::default()
    };

    eframe::run_native(
        "Gerdoo Launcher",
        options,
        Box::new(|cc| Ok(Box::new(LauncherApp::new(cc, initial_config)))),
    )
}


impl App for LauncherApp {
    fn update(&mut self, ctx: &Context, _frame: &mut Frame) {
        while let Ok(message) = self.rx.try_recv() {
            let timestamp = Local::now().format("%H:%M:%S").to_string();
            let formatted_line = match message {
                ConsoleMessage::System(msg) => format!("{}\n", msg),
                ConsoleMessage::Stdout(msg) => format!("{}\n", msg),
                ConsoleMessage::Stderr(msg) => format!("{}\n", msg),
            };

            self.console_output.push_str(&formatted_line);
            self.scroll_to_bottom = true;
        }

        CentralPanel::default().show(ctx, |ui| {
            let mut config_lock = self.config.lock().unwrap();
            let is_running = config_lock.server_pid.is_some();

            ui.horizontal(|ui| {
                ui.spacing_mut().item_spacing.x = 10.0;

                let start_button = ui.add_enabled_ui(!is_running, |ui| {
                    ui.button(RichText::new("▶ Start Server").strong().size(18.0))
                }).inner;

                let stop_button = ui.add_enabled_ui(is_running, |ui| {
                    ui.button(RichText::new("◼ Stop Server").strong().size(18.0).color(Color32::RED))
                }).inner;

                if start_button.clicked() {
                    self.status_message = "Starting server...\n".to_owned();
                    let tx_clone = self.tx.clone();
                    let config_arc_clone = self.config.clone();

                    let server_url = "http://127.0.0.1:8000";

                    tokio::spawn(async move {
                        let mut current_config_clone = config_arc_clone.lock().unwrap().clone();
                        let result = crate::server::start_server(&mut current_config_clone, tx_clone).await;

                        if result.is_ok() {
                            time::sleep(Duration::from_secs(2)).await;
                            if let Err(e) = opener::open_browser(server_url) {
                                eprintln!("Failed to open browser: {}", e);
                            }
                            let _ = current_config_clone.save();
                            let mut main_config_lock = config_arc_clone.lock().unwrap();
                            *main_config_lock = current_config_clone;
                        }
                    });
                }

                if stop_button.clicked() {
                    self.status_message = "Stopping server...".to_owned();
                    let tx_clone = self.tx.clone();
                    let config_arc_clone = self.config.clone();

                    tokio::spawn(async move {
                        let mut current_config_clone = config_arc_clone.lock().unwrap().clone();
                        let result = crate::server::stop_server(&mut current_config_clone, tx_clone).await;

                        if result.is_ok() {
                            let _ = current_config_clone.save();
                            let mut main_config_lock = config_arc_clone.lock().unwrap();
                            *main_config_lock = current_config_clone;
                        }
                    });
                }
            });

            ui.add_space(12.0);
            ui.label(RichText::new(&self.status_message).italics());
            ui.separator();

            ui.label("Server Logs:");

            let available_size = ui.available_size();
            let available_height = available_size.y;

            ScrollArea::vertical().max_height(f32::INFINITY).show(ui, |ui| {
                ui.add(
                    egui::TextEdit::multiline(&mut self.console_output)
                        .min_size(egui::vec2(available_size.x, available_height))
                        .font(TextStyle::Monospace)
                        .desired_width(f32::INFINITY)
                        .interactive(false)
                );

                if self.scroll_to_bottom {
                    ui.scroll_to_cursor(Some(egui::Align::BOTTOM));
                    self.scroll_to_bottom = false;
                }
            });
            ctx.request_repaint();
        });
    }

    fn on_exit(&mut self, _gl: Option<&eframe::glow::Context>) {
        let mut config_snapshot = match crate::config::AppConfig::load() {
            Ok(cfg) => cfg,
            Err(_) => return,
        };
        server::main_thread_stop_server(&mut config_snapshot);
        let _ = config_snapshot.save();
    }
}