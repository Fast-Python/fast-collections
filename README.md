# fast-collections

[![Docs](https://img.shields.io/badge/docs-mkdocs-blue)](https://github.com/Fast-Python/fast-collections/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![test](https://github.com/Fast-Python/fast-collections/actions/workflows/test.yml/badge.svg)](https://github.com/Fast-Python/fast-collections/actions/workflows/test.yml)
[![GitHub stars](https://img.shields.io/github/stars/Fast-Python/fast-collections?style=social)](https://github.com/Fast-Python/fast-collections/)
[![Python Version](https://img.shields.io/pypi/pyversions/fast-collections.svg)](https://pypi.org/project/fast-collections/)

**Blazing-fast data structures and algorithms you've been missing** — written in Rust, usable from Python.

---

## Why this exists

Python's standard library lacks many fundamental data structures and algorithms (which is not necessarily bad). Whenever you need a `trie`, a `B‑tree`, a `suffix array`, or anything beyond what's provided, you either copy a slow pure‑Python implementation from GitHub or write your own dangerous version.

**fast-collections** fills those gaps with Rust implementations. You get production-ready data structures and algorithms that are orders of magnitude faster than anything you could write in pure Python — with compact memory layout and full type annotations.


## Why not write it yourself in Python?

Writing such data structures from scratch is **hard**.
Even if you know the theory, it's easy to miss edge cases or introduce subtle bugs. And pure‑Python implementations are often slow anyway.

We've already done the work for you — **fast‑collections** provides well‑tested, Rust‑optimized versions of these structures.
Just import and use them with confidence.


## Who is this for?

- Anyone who has ever needed a data structure or algorithm that isn't in the standard library.
- Anyone who wants Rust performance without leaving Python.


## Quickstart

```bash
pip install fast-collections
```

```python
from fast_collections import Trie

t = Trie()
t.insert("hello")
t.insert("world")

assert "hello" in t
assert t.starts_with("he")
```

See the [full documentation](https://github.com/Fast-Python/fast-collections/) for all available data structures, algorithms, and their APIs.