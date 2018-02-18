#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import division

import re

from flask import Flask, request
from goose import Goose
from requests import get

# it looks like a clusterfuck but it's really just a list of punctuation
# if you add more, make sure it's escaped for regex
PUNCTUATION = re.compile(r'[,.\\<>/\?;:\'"\[\]\{\}!@#\$%\^\&\*\(\)_\+=\-|]')

biased_words = set()
with open('wordlist.txt') as f:
    for line in f:
        biased_words.add(line.strip().lower())

app = Flask(__name__)

@app.route('/')
def index():
    url = request.args.get('url')
    if url is None or not url:
        return 'specify a ?url=', 400

    response = get(url)
    extractor = Goose()
    article = extractor.extract(raw_html=response.content)
    text =  article.cleaned_text

    words = text.split()
    count = sum(PUNCTUATION.sub('', word.lower()) in biased_words for word in words)
    return str(count / len(words) * 100) + '% of the words are biased'

if __name__ == "__main__":
	app.run()