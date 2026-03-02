class Trie:
    """
    A prefix tree (trie) data structure for efficient string storage and retrieval.

    Provides O(k) operations for insert, search, and prefix matching,
    where k is the length of the input string.

    All string operations are case-sensitive and operate on Unicode characters.

    Examples:
        >>> t = Trie()
        >>> t.insert("hello")
        >>> t.search("hello")
        True
        >>> t.starts_with("he")
        True
        >>> len(t)
        1
        >>> "hello" in t
        True
    """

    def __init__(self) -> None:
        """Initialize an empty trie."""
        ...

    def insert(self, word: str) -> None:
        """
        Insert a word into the trie.

        If the word already exists, the trie remains unchanged
        (duplicate insertions are idempotent).

        Args:
            word: The string to insert. Must not be None.

        Raises:
            TypeError: If word is None.

        Complexity: O(k) where k = len(word)

        Examples:
            >>> t = Trie()
            >>> t.insert("hello")
            >>> "hello" in t
            True
        """
        ...

    def search(self, word: str) -> bool:
        """
        Check if a word has been inserted into the trie.

        Args:
            word: The string to search for. Must not be None.

        Returns:
            True if the exact word exists in the trie, False otherwise.

        Raises:
            TypeError: If word is None.

        Complexity: O(k) where k = len(word)

        Examples:
            >>> t = Trie()
            >>> t.insert("apple")
            >>> t.search("apple")
            True
            >>> t.search("app")
            False
        """
        ...

    def starts_with(self, prefix: str) -> bool:
        """
        Check if any inserted word starts with the given prefix.

        Args:
            prefix: The prefix to check. Must not be None.
                   An empty prefix always returns True.

        Returns:
            True if at least one word in the trie has the given prefix,
            False otherwise.

        Raises:
            TypeError: If prefix is None.

        Complexity: O(k) where k = len(prefix)

        Examples:
            >>> t = Trie()
            >>> t.insert("apple")
            >>> t.starts_with("app")
            True
        """
        ...

    def delete(self, word: str) -> bool:
        """
        Delete a word from the trie.

        Only removes the exact word; other words sharing the same prefix
        are not affected. The trie is compacted if possible (nodes with
        no remaining children and not marking a word end are removed).

        Args:
            word: The string to delete. Must not be None.

        Returns:
            True if the word was found and deleted, False if the word
            was not present in the trie.

        Raises:
            TypeError: If word is None.

        Complexity: O(k) where k = len(word)

        Examples:
            >>> t = Trie()
            >>> t.insert("apple")
            >>> t.delete("apple")
            True
        """
        ...

    def word_count(self) -> int:
        """
        Return the total number of words stored in the trie.

        Returns:
            The count of distinct inserted words.

        Complexity: O(n) where n is the total number of nodes in the trie.

        Examples:
            >>> t = Trie()
            >>> t.insert("apple")
            >>> t.word_count()
            1
        """
        ...

    def collect_words(self) -> list[str]:
        """
        Return all words stored in the trie, sorted lexicographically.

        The words are collected via depth-first traversal, which naturally
        produces lexicographic order.

        Returns:
            A list of all inserted strings in lexicographic order.
            Returns an empty list if the trie is empty.

        Complexity: O(m) where m is the total number of characters
        across all stored words.

        Examples:
            >>> t = Trie()
            >>> t.insert("apple")
            >>> t.insert("banana")
            >>> t.collect_words()
            ['apple', 'banana']
        """
        ...

    def __contains__(self, word: str) -> bool:
        """
        Check if a word exists in the trie (enables the ``in`` operator).

        Equivalent to ``search()``.

        Examples:
            >>> t = Trie()
            >>> t.insert("apple")
            >>> "apple" in t
            True
            >>> "app" in t
            False
        """
        ...

    def __len__(self) -> int:
        """
        Return the number of words in the trie (enables the ``len()`` function).

        Equivalent to ``word_count()``.

        Examples:
            >>> t = Trie()
            >>> t.insert("a")
            >>> t.insert("b")
            >>> len(t)
            2
        """
        ...
