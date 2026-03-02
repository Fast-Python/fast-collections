from fast_collections import Trie


def test_create_trie():
    Trie()


def test_trie_insert():
    t = Trie()
    t.insert("hello")
    assert "hello" in t, "insert(hello)"
    t.insert("world")
    assert "world" in t, "insert(world)"


def test_trie_remove():
    t = Trie()
    t.insert("hello")
    assert "hello" in t, "insert(hello)"
    t.delete("hello")
    assert "hello" not in t, "remove(hello)"


def test_trie_contains():
    t = Trie()
    t.insert("hello")
    assert "hello" in t, "insert(hello)"
    assert "world" not in t, "contains(world)"


def test_trie_starts_with():
    t = Trie()
    t.insert("hello")
    assert t.starts_with("hello"), "starts_with(hello)"
    assert not t.starts_with("world"), "starts_with(world)"


def test_trie_search():
    t = Trie()
    t.insert("hello")
    assert t.search("hello"), "search(hello)"
    assert not t.search("world"), "search(world)"


def test_trie_size():
    t = Trie()
    t.insert("hello")
    assert len(t) == 1, "len()"


def test_trie_collect_words():
    t = Trie()
    t.insert("hello")
    assert t.collect_words() == ["hello"], "collect_words()"
