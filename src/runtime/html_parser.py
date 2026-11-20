"""Parseo de HTML estático con el parser incluido en Python."""

from bs4 import BeautifulSoup


def parse_html(html):
    return BeautifulSoup(html, "html.parser")
