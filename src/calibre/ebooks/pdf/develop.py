#!/usr/bin/env python2
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2019, Kovid Goyal <kovid at kovidgoyal.net>

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

from PyQt5.Qt import QApplication, QUrl, QPageLayout, QPageSize, QMarginsF
from PyQt5.QtWebEngineWidgets import QWebEnginePage

from calibre.gui2 import load_builtin_fonts, must_use_qt
from calibre.utils.podofo import get_podofo

OUTPUT = '/t/dev.pdf'


class Renderer(QWebEnginePage):

    def do_print(self, ok):
        p = QPageLayout(QPageSize(QPageSize(QPageSize.A6)), QPageLayout.Portrait, QMarginsF(10, 10, 10, 10))
        self.printToPdf(self.print_finished, p)

    def print_finished(self, pdf_data):
        with open(OUTPUT, 'wb') as f:
            f.write(pdf_data)
        QApplication.instance().exit(0)
        podofo = get_podofo()
        doc = podofo.PDFDoc()
        doc.load(pdf_data)
        from pprint import pprint
        pprint(doc.extract_anchors())


def main():
    must_use_qt()
    load_builtin_fonts()
    renderer = Renderer()
    renderer.setUrl(QUrl.fromLocalFile(sys.argv[-1]))
    renderer.loadFinished.connect(renderer.do_print)
    QApplication.instance().exec_()
    print('Output written to:', OUTPUT)


if __name__ == '__main__':
    main()