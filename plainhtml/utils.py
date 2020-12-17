import re
from dataclasses import dataclass
from typing import Optional, Union

NEWLINE_TAGS = {
    "article",
    "aside",
    "br",
    "dd",
    "details",
    "div",
    "dt",
    "fieldset",
    "figcaption",
    "footer",
    "form",
    "header",
    "hr",
    "legend",
    "li",
    "main",
    "nav",
    "table",
    "tr",
}
DOUBLE_NEWLINE_TAGS = {
    "blockquote",
    "dl",
    "figure",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "ol",
    "p",
    "pre",
    "title",
    "ul",
}
WHITESPACE = re.compile(r"\s+")
TRAILING_WHITESPACE = re.compile(r"\s$")
PUNCTUATION_AFTER = re.compile(r'^[,:;.!?")]')
OPEN_BRACKET_BEFORE = re.compile(r"\($")


def has_trailing_whitespace(text: str) -> bool:
    """[summary]

    Parameters
    ----------
    text : str
        [description]

    Returns
    -------
    bool
        [description]
    """
    if TRAILING_WHITESPACE.search(text):
        return True
    else:
        return False


def has_punctuation_after(text: str) -> bool:
    """[summary]

    Parameters
    ----------
    text : str
        [description]

    Returns
    -------
    bool
        [description]
    """
    if PUNCTUATION_AFTER.search(text):
        return True
    else:
        return False


def has_open_bracket_before(text: str) -> bool:
    """[summary]

    Parameters
    ----------
    text : str
        [description]

    Returns
    -------
    bool
        [description]
    """
    if OPEN_BRACKET_BEFORE.search(text):
        return True
    else:
        return False


def normalize_whitespace(text: Optional[str]) -> str:
    """[summary]

    Parameters
    ----------
    text : Optional[str]
        [description]

    Returns
    -------
    str
        [description]
    """
    if text:
        return WHITESPACE.sub(" ", text.strip())
    else:
        return ""


class DoubleNewline:
    pass


class Newline:
    pass


@dataclass
class Context:
    previous: Union[DoubleNewline, Newline]
