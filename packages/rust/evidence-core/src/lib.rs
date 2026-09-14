//! Safe deterministic helpers for evidence aggregation.
pub fn mean_confidence(values: &[f64]) -> f64 { if values.is_empty() { 0.0 } else { values.iter().sum::<f64>() / values.len() as f64 } }
#[cfg(test)]
mod tests { use super::mean_confidence; #[test] fn empty_is_zero() { assert_eq!(mean_confidence(&[]), 0.0); } #[test] fn computes_mean() { assert!((mean_confidence(&[0.2,0.8]) - 0.5).abs() < f64::EPSILON); } }
