use qni_core_rs::prelude::c_api::ConsoleArcCtx;
use std::slice;
use std::str;

use log::error;

#[no_mangle]
pub extern "C" fn qni_program_init() {
    pretty_env_logger::init();
}

#[no_mangle]
pub unsafe extern "C" fn qni_program_start(
    ctx: ConsoleArcCtx,
    addr: *const u8,
    addr_len: usize,
) -> i32 {
    let addr = str::from_utf8_unchecked(slice::from_raw_parts(addr, addr_len));

    match qni_connector_ws_rs::start_connector(&*ctx, addr) {
        Ok(_) => 0,
        Err(err) => {
            error!("ws err: {}", err);
            -1
        }
    }
}
