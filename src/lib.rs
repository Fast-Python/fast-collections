pub mod trie;

#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

#[cfg(feature = "pyo3")]
#[pymodule]
fn fast_collections(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<trie::Trie>()?;
    Ok(())
}
