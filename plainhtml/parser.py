from dataclasses import dataclass
from functools import cached_property

from lxml import etree
from lxml.html import HTMLParser
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
        # TODO
        return Cleaner()

    @cached_property
    def tree(self):
        body = self.html.strip().replace("\x00", "").encode("utf-8")
        parser = HTMLParser(recover=True, encoding="utf-8")
        tree = etree.fromstring(body, parser=parser)
        return self.cleaner.clean_html(tree)

    def extract(self) -> str:
        self.chunks = []
        self.context = Context(DOUBLE_NEWLINE)
        self.traverse(self.tree)
        return "".join(self.chunks).strip()

    def traverse(self, tree):
        self.add_newlines(tree.tag)
        self.add_text(tree.text)
        for child in tree:
            self.traverse(child)
        self.add_newlines(tree.tag)

    def add_newlines(self, tag):
        if not self.context.previous_tag is DOUBLE_NEWLINE:
            if tag in DOUBLE_NEWLINE_TAGS:
                self.chunks.append("\n" if self.context.previous_tag is NEWLINE else "\n\n")
                self.context.previous_tag = DOUBLE_NEWLINE
            elif tag in NEWLINE_TAGS:
                if not self.context.previous_tag is NEWLINE:
                    self.chunks.append("\n")
                self.context.previous_tag = NEWLINE

    def add_text(self, text: str):
        if (text := utils.normalize_whitespace(text)) :
            space = self.space_between(text, self.context.previous_tag)
            self.chunks.extend([space, text])
            self.context.previous_tag = text

    def space_between(self, text, previous_tag):
        if text:
            return " " if self.should_add_space(text, previous_tag) else ""
        else:
            return " "

    @staticmethod
    def should_add_space(text, previous_tag):
        # TODO: find other name
        if previous_tag in {NEWLINE, DOUBLE_NEWLINE}:
            return False
        if not utils.has_trailing_whitespace(previous_tag):
            if utils.has_punctuation_after(text) or utils.has_open_bracket_before(previous_tag):
                return False
        return True
