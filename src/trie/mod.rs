use std::collections::HashMap;

#[derive(Clone, Debug)]
pub struct Triers {
    children: HashMap<char, Box<Triers>>,
    is_end: bool,
}

impl Default for Triers {
    fn default() -> Self {
        Self::new()
    }
}

impl Triers {
    pub fn new() -> Self {
        Self {
            children: HashMap::new(),
            is_end: false,
        }
    }

    pub fn insert(&mut self, word: &str) {
        let mut node = self;
        for ch in word.chars() {
            node = node
                .children
                .entry(ch)
                .or_insert_with(|| Box::new(Triers::new()));
        }
        node.is_end = true;
    }

    pub fn search(&self, word: &str) -> bool {
        let mut node = self;
        for ch in word.chars() {
            match node.children.get(&ch) {
                Some(child) => node = child,
                None => return false,
            }
        }
        node.is_end
    }

    pub fn starts_with(&self, prefix: &str) -> bool {
        let mut node = self;
        for ch in prefix.chars() {
            match node.children.get(&ch) {
                Some(child) => node = child,
                None => return false,
            }
        }
        true
    }

    pub fn delete(&mut self, word: &str) -> bool {
        Self::delete_rec(self, word, 0)
    }

    fn delete_rec(node: &mut Triers, word: &str, depth: usize) -> bool {
        if depth == word.len() {
            if !node.is_end {
                return false;
            }
            node.is_end = false;
            return node.children.is_empty();
        }

        let ch = word[depth..].chars().next().unwrap();
        if let Some(child) = node.children.get_mut(&ch) {
            if Self::delete_rec(child, word, depth + 1) {
                node.children.remove(&ch);
                return node.children.is_empty() && !node.is_end;
            }
        }
        false
    }

    pub fn word_count(&self) -> usize {
        let mut count = 0;
        if self.is_end {
            count += 1;
        }
        for child in self.children.values() {
            count += child.word_count();
        }
        count
    }

    pub fn collect_words(&self) -> Vec<String> {
        let mut result = Vec::new();
        let mut prefix = String::new();
        Self::collect_rec(self, &mut prefix, &mut result);
        result
    }

    fn collect_rec(node: &Triers, prefix: &mut String, result: &mut Vec<String>) {
        if node.is_end {
            result.push(prefix.clone());
        }
        for (&ch, child) in &node.children {
            prefix.push(ch);
            Self::collect_rec(child, prefix, result);
            prefix.pop();
        }
    }
}

#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

#[cfg(feature = "pyo3")]
#[pyclass]
pub struct Trie {
    inner: Triers,
}

#[cfg(feature = "pyo3")]
#[pymethods]
impl Trie {
    #[new]
    fn new() -> Self {
        Self {
            inner: Triers::new(),
        }
    }

    fn insert(&mut self, word: &str) {
        self.inner.insert(word);
    }

    fn search(&self, word: &str) -> bool {
        self.inner.search(word)
    }

    fn starts_with(&self, prefix: &str) -> bool {
        self.inner.starts_with(prefix)
    }

    fn delete(&mut self, word: &str) -> bool {
        self.inner.delete(word)
    }

    fn word_count(&self) -> usize {
        self.inner.word_count()
    }

    fn collect_words(&self) -> Vec<String> {
        self.inner.collect_words()
    }

    fn __contains__(&self, word: &str) -> bool {
        self.inner.search(word)
    }

    fn __len__(&self) -> usize {
        self.inner.word_count()
    }
}
