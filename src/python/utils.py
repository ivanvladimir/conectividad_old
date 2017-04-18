#!/usr/bin/env python3
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Analyses texts
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2017/IIMAS/UNAM
# ----------------------------------------------------------------------

# System libraries
import io
from subprocess import call
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.pdfdevice import TagExtractor
from pdfminer.converter import PDFLayoutAnalyzer
from pdfminer.layout import LAParams
from pdfminer.utils import set_debug_logging
from pdfminer.layout import LTContainer, LTPage, LTText, LTLine, LTRect, LTCurve
from pdfminer.layout import LTFigure, LTImage, LTChar, LTTextLine
from pdfminer.layout import LTTextBox, LTTextBoxVertical, LTTextGroup


from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups


def search_regexp(regexp,tokens):
    return [w for w in tokens if re.search(regexp, w)]

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Tópico #{0}:".format(topic_idx))
        print(" ".join([feature_names[i]
                for i in topic.argsort()[:-n_top_words - 1:-1]]))
        print()

def extract_topics(documents, n_features = 2000,n_topics =30, n_top_words = 20,sws="english"):
    tfidf_vectorizer = TfidfVectorizer(min_df=0.1,
                                   max_features=n_features,
                                   stop_words=sws)

    tfidf = tfidf_vectorizer.fit_transform(documents)
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=43)
    lda.fit(tfidf)

    tf_feature_names = tfidf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words)


def extract_text_from_pdf(file_in,file_out):
    call(["pdftotext", "-layout",file_in,file_out])


class TextExtractor(PDFLayoutAnalyzer):
    def __init__(self, rsrcmgr, pageno=1, laparams=None,
                 showpageno=False):
        PDFLayoutAnalyzer.__init__(self, rsrcmgr, pageno=pageno, laparams=laparams)
        self.showpageno = showpageno
        self.text=""

    def save_text(self, text):
        self.text+=text

    def receive_layout(self, ltpage):
        def render(item):
            if isinstance(item, LTContainer):
                for child in item:
                    render(child)
            elif isinstance(item, LTText):
                self.save_text(item.get_text())
            if isinstance(item, LTTextBox):
                self.save_text('\n')
        if self.showpageno:
            self.save_text('Page %s\n' % ltpage.pageid)
        render(ltpage)
        self.save_text('\f')

    # Some dummy functions to save memory/CPU when all that is wanted is text.
    # This stops all the image and drawing ouput from being recorded and taking
    # up RAM.
    def render_image(self, name, stream):
        pass
    def paint_path(self, gstate, stroke, fill, evenodd, path):
        pass


def pdf2text(filename):
    rsrcmgr = PDFResourceManager()
    device = TextExtractor(rsrcmgr)
    fp = io.open(filename, 'rb')
    process_pdf(rsrcmgr, device, fp)
    fp.close()
    device.close()
    return device.text


       


