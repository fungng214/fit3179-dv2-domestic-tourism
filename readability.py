"""Limit authored prose to twelve whitespace-separated words per line.

Explicit breaks retain the limit at every viewport size; narrow screens may
wrap earlier. Inline emphasis and links remain intact. No browser script needed.
"""
from html.parser import HTMLParser
import re


class ProseLines(HTMLParser):
    blocks = {'p', 'h1', 'h2', 'h3', 'h4', 'li', 'div', 'section',
              'article', 'header', 'footer', 'main', 'ul', 'ol'}

    def __init__(self, limit=12):
        super().__init__(convert_charrefs=False)
        self.limit, self.words, self.hidden = limit, 0, 0
        self.output = []

    def handle_starttag(self, tag, attrs):
        if tag in self.blocks or tag == 'br':
            self.words = 0
        if tag in {'script', 'style', 'head'}:
            self.hidden += 1
        self.output.append(self.get_starttag_text())

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in self.blocks:
            self.words = 0
        if tag in {'script', 'style', 'head'}:
            self.hidden -= 1
        self.output.append('</' + tag + '>')

    def handle_data(self, text):
        if self.hidden:
            self.output.append(text)
            return
        for part in re.findall(r'\s+|\S+', text):
            if not part.isspace():
                if self.words == self.limit:
                    self.output.append('<br class="prose-break">')
                    self.words = 0
                self.words += 1
            self.output.append(part)
            # Prefer sentence endings over arbitrary twelve-word chunks.
            # Decimal values contain a dot internally, so remain intact.
            if not part.isspace() and re.search(r'[.!?][)”’\"\']?$', part):
                self.output.append('<br class="prose-break">')
                self.words = 0

    def handle_entityref(self, name):
        self.output.append('&' + name + ';')

    def handle_charref(self, name):
        self.output.append('&#' + name + ';')

    def handle_decl(self, decl):
        self.output.append('<!' + decl + '>')

    def handle_comment(self, text):
        self.output.append('<!--' + text + '-->')


def limit_prose_lines(page):
    parser = ProseLines()
    parser.feed(page)
    return ''.join(parser.output)
