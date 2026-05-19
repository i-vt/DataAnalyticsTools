"""Tests for data_analytics_tools.cleanup.tokenizer."""

import hashlib

import pytest

from data_analytics_tools.cleanup.tokenizer import (
    int_to_token,
    str_to_sha512,
    tokenize_array,
)


# ── str_to_sha512 ──────────────────────────────

class TestStrToSha512:
    def test_empty_string_returns_empty(self):
        assert str_to_sha512("") == ""

    def test_known_value(self):
        expected = hashlib.sha512(b"hello").hexdigest()
        assert str_to_sha512("hello") == expected

    def test_unicode(self):
        result = str_to_sha512("café")
        assert len(result) == 128  # SHA-512 hex length


# ── int_to_token ────────────────────────────────

class TestIntToToken:
    def test_zero(self):
        assert int_to_token(0, 3) == "aaa"

    def test_one(self):
        assert int_to_token(1, 3) == "aab"

    def test_twenty_six(self):
        assert int_to_token(26, 3) == "aba"

    def test_single_letter(self):
        assert int_to_token(0, 1) == "a"
        assert int_to_token(25, 1) == "z"

    def test_negative_raises(self):
        with pytest.raises(ValueError, match="negative"):
            int_to_token(-1)

    def test_overflow_raises(self):
        with pytest.raises(ValueError, match="overflow"):
            int_to_token(26, 1)  # max is 25 for 1-letter

    def test_boundary_max(self):
        # max for 2 letters is 26^2 - 1 = 675
        assert int_to_token(675, 2) == "zz"


# ── tokenize_array ──────────────────────────────

class TestTokenizeArray:
    def test_empty(self):
        assert tokenize_array([]) == []

    def test_token_method(self):
        result = tokenize_array(["x", "y", "z"], "token")
        assert len(result) == 3
        originals = [r[0] for r in result]
        assert originals == ["x", "y", "z"]
        # Each token should be a lowercase alpha string
        for _, tok in result:
            assert tok.isalpha() and tok.islower()

    def test_hash_method(self):
        result = tokenize_array(["hello"], "hash")
        assert result[0][0] == "hello"
        assert result[0][1] == str_to_sha512("hello")

    def test_duplicates_raise(self):
        with pytest.raises(ValueError, match="duplicates"):
            tokenize_array(["a", "a"])

    def test_invalid_method_raises(self):
        with pytest.raises(ValueError, match="invalid method"):
            tokenize_array(["a"], "bad")

    def test_unique_tokens(self):
        items = [f"item{i}" for i in range(100)]
        result = tokenize_array(items, "token")
        tokens = [t for _, t in result]
        assert len(set(tokens)) == 100
