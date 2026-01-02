```rust
#[target_feature(enable = "neon")]
pub unsafe fn hash_events_neon(
    events: &[crate::core::activity_ledger::OntoEvent],
) -> Result<Vec<u64>, super::SimdError> {
    use std::arch::aarch64::*;
    let mut hashes = Vec::with_capacity(events.len());
    for event in events {
        let bytes = serde_json::to_vec(event).map_err(|_| super::SimdError::InvalidData)?;
        let mut state = vdupq_n_u8(0);
        for chunk in bytes.chunks(16) {
            let mut pad = [0u8; 16];
            pad[..chunk.len()].copy_from_slice(chunk);
            let vec = vld1q_u8(pad.as_ptr());
            state = veorq_u8(state, vec);
        }
        let result = vgetq_lane_u64(vreinterpretq_u64_u8(state), 0);
        hashes.push(result);
    }
    Ok(hashes)
}
```
