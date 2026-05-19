"""Tokenization utilities for anonymising and encoding data."""

from __future__ import annotations

import hashlib
import math
from typing import List, Literal, Tuple


def str_to_sha512(value: str) -> str:
    """Return the SHA-512 hex digest of *value*.

    Parameters
    ----------
    value:
        The string to hash.  An empty string returns ``""``.

    Returns
    -------
    str
        Hex-encoded SHA-512 hash, or ``""`` for empty input.
    """
    if not value:
        return ""
    return hashlib.sha512(value.encode("utf-8")).hexdigest()


def int_to_token(n: int, max_letters: int = 3) -> str:
    """Encode a non-negative integer as a lower-case alphabetic token.

    The encoding is bijective base-26 (a–z) zero-padded to
    *max_letters* characters.

    Parameters
    ----------
    n:
        Non-negative integer to encode.
    max_letters:
        Width of the resulting token.

    Returns
    -------
    str
        Alphabetic token of length *max_letters*.

    Raises
    ------
    ValueError
        If *n* is negative or exceeds ``26 ** max_letters - 1``.
    """
    if n < 0:
        raise ValueError(f"int_to_token does not accept negative integers ({n})")
    if n >= 26 ** max_letters:
        raise ValueError(
            f"int_to_token overflow: {n} >= 26^{max_letters} ({26 ** max_letters})"
        )
    chars: list[str] = []
    remaining = n
    for _ in range(max_letters):
        chars.append(chr(97 + remaining % 26))
        remaining //= 26
    return "".join(reversed(chars))


def tokenize_array(
    items: List[str],
    method: Literal["token", "hash"] = "token",
) -> List[Tuple[str, str]]:
    """Map each unique item to a token or hash.

    Parameters
    ----------
    items:
        List of **unique** strings to tokenize.
    method:
        ``"token"`` for short alphabetic tokens, ``"hash"`` for SHA-512.

    Returns
    -------
    list[tuple[str, str]]
        Pairs of ``(original, token)``.

    Raises
    ------
    ValueError
        If *items* contains duplicates or *method* is invalid.
    """
    if not items:
        return []
    if len(items) != len(set(items)):
        raise ValueError("tokenize_array: input list contains duplicates")
    if method not in ("token", "hash"):
        raise ValueError(f"tokenize_array: invalid method '{method}'")

    result: List[Tuple[str, str]] = []
    if method == "token":
        max_letters = max(1, math.ceil(math.log(max(len(items), 2), 26)))
        for idx, item in enumerate(items):
            result.append((item, int_to_token(idx, max_letters)))
    else:
        for item in items:
            result.append((item, str_to_sha512(item)))
    return result
