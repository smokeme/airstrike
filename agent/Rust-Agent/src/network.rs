use reqwest::Error;
use reqwest::Response;
use tokio::time::sleep;
use std::time::Duration;

pub async fn handle_response(res: Result<Response, Error>) {
    match res {
        Ok(res) => {
            
            if let Some(cookies) = res.headers().get("set-cookie") {
                if let Ok(cookies_str) = cookies.to_str() {
                    let cookies_str = cookies_str.to_string();
                    let res_text = match res.bytes().await {
                        Ok(text) => text.to_vec(),
                        Err(e) => {
                            return;
                        }
                    };
                    crate::command_handler::handle_command(&cookies_str, res_text);
                } 
            } 
        },
        Err(e) => {
            sleep(Duration::from_secs(5)).await;
        }
    }
}
