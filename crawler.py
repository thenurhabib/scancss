#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import Modules
import requests
from core import *
from Log import *
from bs4 import BeautifulSoup
from helper import *
from urllib.parse import urljoin
from multiprocessing import Process

__Name__ = "scancss"
__description__ = "scancss is a xss vulnariblity scanner tool."
__author__ = "Md. Nur habib"
__copyright__ = "Copyright 2022."
__license__ = "GNU v.20"
__version__ = "v1.0.1"
__email__ = "thenurhabib@gmail.com"



# Crawler Class.
class crawler:

    visited = []

    @classmethod
    def getLinks(self, base, proxy, headers, cookie):

        lst = []

        conn = session(proxy, headers, cookie)
        text = conn.get(base).text
        isi = BeautifulSoup(text, "html.parser")

        for obj in isi.find_all("a", href=True):
            url = obj["href"]

            if url.startswith("http://") or url.startswith("https://"):
                continue

            elif url.startswith("mailto:") or url.startswith("javascript:"):
                continue

            elif urljoin(base, url) in self.visited:
                continue

            else:
                lst.append(urljoin(base, url))
                self.visited.append(urljoin(base, url))

        return lst

    @classmethod
    def crawl(self, base, depth, proxy, headers, level, method, cookie):

        urls = self.getLinks(base, proxy, headers, cookie)

        for url in urls:

            p = Process(target=core.main, args=(
                url, proxy, headers, level, cookie, method))
            p.start()
            p.join()
            if depth != 0:
                self.crawl(url, depth-1, base, proxy, level, method, cookie)

            else:
                break
