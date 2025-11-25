use std::process::{
    Stdio,
};
use tokio::process::{
    Command,
};
use tokio::sync::mpsc::{
    Sender,
};
use tokio::io::{
    AsyncBufReadExt,
    BufReader,
};
use crate::config::{
    AppConfig,
};


type ServerResult<T> = Result<T, String>;


#[derive(Debug)]
pub enum ConsoleMessage {
    Stdout(String),
    Stderr(String),
    System(String),
}


pub async fn start_server(
    config: &mut AppConfig,
    tx: Sender<ConsoleMessage>
) -> ServerResult<String> {

    if config.server_pid.is_some() {
        return Ok("Error: Server is already running.".to_owned());
    }

    let gerdoo_path = &config.app_path;
    if !gerdoo_path.exists() {
        let err_msg = format!(
            "Error: The 'Gerdoo' app was not found in '{}'",
            gerdoo_path.display()
        );
        let _ = tx.send(ConsoleMessage::System(err_msg.clone())).await;
        return Err(err_msg);
    }

    let _ = tx.send(
        ConsoleMessage::System(
        "Preparing server process...".to_owned()
        )
    ).await;

    let mut command = if cfg!(target_os = "windows") {
        let mut cmd = Command::new("cmd");
        cmd.args(["/C", "python", "manage.py", "runserver", "--noreload"]);
        cmd
    } else {
        let mut cmd = Command::new("python");
        cmd.args(["manage.py", "runserver", "--noreload"]);
        cmd
    };

    command.current_dir(gerdoo_path)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .kill_on_drop(false);

    match command.spawn() {
        Ok(mut child) => {
            let pid = child.id().ok_or_else(
                || "Failed to get process PID.".to_owned()
            )?;

            config.server_pid = Some(pid);
            config.save()
                .map_err(|e| format!("Error: Failed to save settings in '{}'", e))?;

            let _ = tx.send(
                ConsoleMessage::System(
                    format!("Server with PID {}: started.", pid)
                )
            ).await;

            let tx_clone = tx.clone();
            let stdout_reader = BufReader::new(child.stdout.take().unwrap());
            tokio::spawn(read_output(stdout_reader, tx_clone, ConsoleMessage::Stdout));

            let tx_clone_err = tx.clone();
            let stderr_reader = BufReader::new(child.stderr.take().unwrap());
            tokio::spawn(read_output(stderr_reader, tx_clone_err, ConsoleMessage::Stderr));

            let tx_clone_wait = tx.clone();
            tokio::spawn(async move {
                let status = child.wait().await;
                let _ = tx_clone_wait.send(ConsoleMessage::System(
                    format!("The server with PID {}: stopped with code '{:?}'.", pid, status)
                )).await;
            });

            Ok(format!("Server with PID {}: started successfully.", pid))
        }
        Err(e) => {
            let _ = tx.send(
                ConsoleMessage::System(
                    format!("Error: Failure to execute the command. '{}'", e)
                )
            ).await;
            Err(format!("Error: Failure to execute the command (python). '{}'", e))
        }
    }
}


async fn read_output<R>(
    reader: BufReader<R>,
    tx: Sender<ConsoleMessage>,
    msg_type_constructor: fn(String) -> ConsoleMessage
) where R: tokio::io::AsyncRead + Unpin {
    let mut lines = reader.lines();
    while let Ok(Some(line)) = lines.next_line().await {
        let _ = tx.send(msg_type_constructor(line)).await;
    }
}


pub async fn stop_server(config: &mut AppConfig, tx: Sender<ConsoleMessage>) -> ServerResult<String> {
    let pid = match config.server_pid {
        Some(p) => p,
        None => return Ok("Server is currently down.".to_owned()),
    };

    let _ = tx.send(ConsoleMessage::System(format!("Sending stop signal to PID: {}", pid))).await;

    let kill_result = if cfg!(target_os = "windows") {
        Command::new("taskkill")
            .args(["/F", "/PID", &pid.to_string()])
            .status()
            .await
    } else {
        Command::new("kill")
            .arg(pid.to_string())
            .status()
            .await
    };

    let success = kill_result.is_ok() && kill_result.as_ref().unwrap().success();

    if success {
        config.server_pid = None;
        config.save()
            .map_err(|e| format!("Error: Failed to save settings. '{}'", e))?;

        let msg = format!("Server with PID {}: stopped successfully.", pid);
        let _ = tx.send(ConsoleMessage::System(msg.clone())).await;
        Ok(msg)
    } else {
        config.server_pid = None;
        config.save()
            .map_err(|e| format!("Failed to save settings after stop failure: {}", e))?;

        let msg = format!("Failed to stop process PID {}. PID was manually cleared.", pid);
        let _ = tx.send(ConsoleMessage::System(msg.clone())).await;
        Err(msg)
    }
}


pub fn is_server_running(config: &AppConfig) -> bool {
    config.server_pid.is_some()
}


pub fn main_thread_stop_server(config: &mut crate::config::AppConfig) {
    let pid = match config.server_pid {
        Some(p) => p,
        None => return,
    };

    let pid_str = pid.to_string();
    let kill_result = if cfg!(target_os = "windows") {
        std::process::Command::new("taskkill").args(["/F", "/PID", &pid_str]).status()
    } else {
        std::process::Command::new("kill").args(["-9", &pid_str]).status()
    };

    match kill_result {
        Ok(status) if status.success() => {
            eprintln!("[SYNC KILL] Successfully killed process: {}", pid);
        }
        Ok(status) => {
            eprintln!("[SYNC KILL] Failed to kill process {}. Status: {}", pid, status);
        }
        Err(e) => {
            eprintln!("[SYNC KILL] Error executing kill command for {}: {}", pid, e);
        }
    }
    config.server_pid = None;
}