use clap::{
    Parser,
    Subcommand,
};


#[derive(Parser)]
#[command(name="Gerdoo Launcher")]
#[command(about="Gerdoo Launcher", long_about=None)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Commands,
}


#[derive(Subcommand)]
pub enum Commands {
    Server {
        #[command(subcommand)]
        action: ServerAction,
    },
    Update {
        #[command(subcommand)]
        action: UpdateAction,
    },
    Install {
        #[command(subcommand)]
        action: InstallAction,
    },
}


#[derive(Subcommand)]
pub enum ServerAction {
    Start,
    Stop,
    CheckPid,
}


#[derive(Subcommand)]
pub enum UpdateAction {
    Check,
    Update,
}


#[derive(Subcommand)]
pub enum InstallAction {
    Check,
    Install,
    CreateUser {
        #[arg(short, long)]
        username: String,

        #[arg(short, long)]
        email: String,

        #[arg(short, long)]
        password: String,
    },
}
