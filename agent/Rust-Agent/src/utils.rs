
pub fn xor(buf: &mut [u8]) {
    for byte in buf.iter_mut() {
        *byte ^= 0xfa;
    }
}