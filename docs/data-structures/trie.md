# Trie — prefix tree

A **Trie** (prefix tree) is a data structure for efficient string storage and retrieval. `Insert`, `search`, and `prefix` matching all run in `O(k)`, where `k` is the length of the string.

---

## Quick start

```python
from fast_collections import Trie

t = Trie()

t.insert("hello")
t.insert("world")
t.insert("help")

assert t.search("hello") == True
assert t.search("hell") == False

assert t.starts_with("he") == True
assert t.starts_with("wo") == True
assert t.starts_with("xyz") == False

assert "hello" in t
assert "hell" not in t

assert len(t) == 3
assert t.word_count() == 3

t.delete("hello")
assert "hello" not in t
assert len(t) == 2

words = t.collect_words()
assert words == ["help", "world"]
```

---

## Full API

### `Trie()`

Creates an empty prefix tree.

```python
t = Trie()
```

---

### `insert(word: str) -> None`

Inserts a word into the trie. If the word already exists, the trie remains unchanged (duplicate insertions are idempotent).

| Parameter | Type | Description |
|-----------|------|-------------|
| `word` | `str` | The string to insert. Must not be `None`. |

**Raises:** `TypeError` if `word` is `None`.

**Complexity:** O(k), where k = len(word)

```python
t = Trie()
t.insert("apple")
t.insert("apple")
```

---

### `search(word: str) -> bool`

Checks if a word has been inserted into the trie.

| Parameter | Type | Description |
|-----------|------|-------------|
| `word` | `str` | The string to search for. Must not be `None`. |

**Returns:** `True` if the exact word exists in the trie, `False` otherwise.

**Raises:** `TypeError` if `word` is `None`.

**Complexity:** O(k), where k = len(word)

```python
t = Trie()
t.insert("apple")
assert t.search("apple") == True
assert t.search("app")   == False
```

---

### `starts_with(prefix: str) -> bool`

Checks if any inserted word starts with the given prefix.

| Parameter | Type | Description |
|-----------|------|-------------|
| `prefix` | `str` | The prefix to check. Must not be `None`. An empty prefix always returns `True`. |

**Returns:** `True` if at least one word in the trie has the given prefix, `False` otherwise.

**Raises:** `TypeError` if `prefix` is `None`.

**Complexity:** O(k), where k = len(prefix)

```python
t = Trie()
t.insert("apple")
t.insert("application")
assert t.starts_with("app")  == True
assert t.starts_with("appl") == True
assert t.starts_with("banana") == False
assert t.starts_with("") == True
```

---

### `delete(word: str) -> bool`

Deletes an exact word from the trie. Other words sharing the same prefix are not affected. The trie is compacted if possible (nodes with no remaining children and not marking a word end are removed).

| Parameter | Type | Description |
|-----------|------|-------------|
| `word` | `str` | The string to delete. Must not be `None`. |

**Returns:** `True` if the word was found and deleted; `False` if the word was not present in the trie.

**Raises:** `TypeError` if `word` is `None`.

**Complexity:** O(k), where k = len(word)

```python
t = Trie()
t.insert("apple")
t.insert("app")

assert t.delete("apple") == True
assert t.delete("apple") == False
assert t.search("app")   == True
```

---

### `word_count() -> int`

Returns the total number of words stored in the trie.

**Returns:** The count of distinct inserted words.

**Complexity:** O(n), where n is the total number of nodes in the trie.

```python
t = Trie()
assert t.word_count() == 0

t.insert("a")
t.insert("b")
t.insert("c")
assert t.word_count() == 3
```

---

### `collect_words() -> list[str]`

Returns all words stored in the trie, sorted lexicographically. The words are collected via depth-first traversal, which naturally produces lexicographic order.

**Returns:** A list of all inserted strings in lexicographic order. Returns an empty list if the trie is empty.

**Complexity:** O(m), where m is the total number of characters across all stored words.

```python
t = Trie()
t.insert("banana")
t.insert("apple")
t.insert("cherry")

assert t.collect_words() == ["apple", "banana", "cherry"]
```

---

### `__contains__(word: str) -> bool`

Enables the `in` operator. Equivalent to `search()`.

```python
t = Trie()
t.insert("apple")

assert "apple" in t
assert "app" not in t
```

---

### `__len__() -> int`

Enables the `len()` function. Equivalent to `word_count()`.

```python
t = Trie()
t.insert("a")
t.insert("b")
assert len(t) == 2
```

---
