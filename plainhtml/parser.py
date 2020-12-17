from dataclasses import dataclass
from functools import cached_property

from lxml import etree
from lxml.html import HtmlElement, HTMLParser
from lxml.html.clean import Cleaner

from plainhtml import utils
from plainhtml.utils import DOUBLE_NEWLINE_TAGS, NEWLINE_TAGS, Context, DoubleNewline, Newline

DOUBLE_NEWLINE = DoubleNewline()
NEWLINE = Newline()


@dataclass
class Parser:
    html: str

    @cached_property
    def cleaner(self) -> Cleaner:
        """[summary]

        Returns
        -------
        Cleaner
            [description]
        """
        return Cleaner(
            javascript=False,
            page_structure=False,
            forms=False,
            annoying_tags=False,
            remove_unknown_tags=False,
            safe_attrs_only=False,
        )

    @cached_property
    def tree(self) -> HtmlElement:
        """[summary]

        Returns
        -------
        HtmlElement
            [description]
        """
        body = self.html.strip().replace("\x00", "").encode("utf-8")
        parser = HTMLParser(recover=True, encoding="utf-8")
        tree = etree.fromstring(body, parser=parser)
        return self.cleaner.clean_html(tree)

    def extract(self) -> str:
        """[summary]

        Returns
        -------
        str
            [description]
        """
        self.chunks = []
        self.context = Context(DOUBLE_NEWLINE)
        self.traverse(self.tree)
        return "".join(self.chunks).strip()

    def traverse(self, tree: HtmlElement):
        """[summary]

        Parameters
        ----------
        tree : HtmlElement
            [description]
        """
        self.add_newlines(tree.tag)
        self.add_text(tree.text)
        for child in tree:
            self.traverse(child)
        self.add_newlines(tree.tag)

    def add_newlines(self, tag: str):
        """[summary]

        Parameters
        ----------
        tag : str
            [description]
        """
        if not self.context.previous is DOUBLE_NEWLINE:
            if tag in DOUBLE_NEWLINE_TAGS:
                self.chunks.append("\n" if self.context.previous is NEWLINE else "\n\n")
                self.context.previous = DOUBLE_NEWLINE
            elif tag in NEWLINE_TAGS:
                if not self.context.previous is NEWLINE:
                    self.chunks.append("\n")
                self.context.previous = NEWLINE

    def add_text(self, text: str):
        """[summary]

        Parameters
        ----------
        text : str
            [description]
        """
        if (text := utils.normalize_whitespace(text)) :
            space = self.space_between(text)
            self.chunks.extend([space, text])
            self.context.previous = text

    def space_between(self, text: str) -> str:
        """[summary]

        Parameters
        ----------
        text : str
            [description]

        Returns
        -------
        str
            [description]
        """
        if text:
            return " " if self.should_add_space(text) else ""
        else:
            return " "

    def should_add_space(self, text: str) -> bool:
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
        # TODO: find other name
        if self.context.previous in {NEWLINE, DOUBLE_NEWLINE}:
            return False
        if not utils.has_trailing_whitespace(self.context.previous):
            if utils.has_punctuation_after(text) or utils.has_open_bracket_before(
                self.context.previous
            ):
                return False
        return True
