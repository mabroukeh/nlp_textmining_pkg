"""
Examples using the textmining package
Ref:
[1] https://pypi.python.org/pypi/textmining/1.0
[2] http://www.christianpeccei.com/textmining/index.html

author: Nizar Mabroukeh
contact: mabroukeh@yahoo.com
created: March 30, 2017
"""

import os
import re
import pprint
from root import resources
import textmining as tm
from wordcloud import  WordCloud


class TxtMining(object):
    """
    Class for playing with the textmining package
    """

    def __init__(self):
        #self.docs = dict()
        self.docs = []
        self.tdm = None

    """
    def add_doc(self, doc, utility):
        self.docs[utility] = doc
    """

    def add_docs(self, doc):
        """
        Adds a document/corpus to the collection of documents maintained by this class
        :param doc: string representation of a document
        :return:
        """
        self.docs += doc

    def get_docs(self):
        """
        getter for docs
        :return: list
        """
        return self.docs

    def flush_docs(self):
        """
        clears all docs collection
        :return:
        """
        self.docs = []

    def remove_empty_docs(self):
        def is_empty(doc):  # I love functional programming
            return not doc
        self.docs = filter(lambda x: not is_empty(x), self.docs)

    def clean_docs(self):
        """
        Remove stopwords and non-letters, then tokenize and stem
        :return:
        """
        self.docs = map(tm.stem,
                            map(tm.simple_tokenize_remove_stopwords, self.docs)
                        )

    def create_termdocument_matrix(self, tokenzied=False):
        """
        creates a term document matrix of the frequencies of each term in each document held in self.docs
        :return:
        """
        self.tdm = tm.TermDocumentMatrix()
        for doc in self.docs:
            if not tokenzied:
                self.tdm.add_doc(doc)
            else:
                self.tdm.add_tokenized_doc(doc)

    def get_termdocument_matrix(self, cutoff=2):
        """
        getter for term document matrix
        :param cutoff: int representing the min number of docs a term should appear in to be included in the matrix
        :return: matrix as list of list
        """
        return [row for row in self.tdm.rows(cutoff=cutoff)]

    def get_termdocument_matrix_as_csv(self, filename, cutoff=2):
        try:
            self.tdm.write_csv(filename, cutoff=cutoff)
        except IOError as err:
            raise

    def remove_common_words(self, words):
        """
        Removes a word or list of words that are considered common from all self.docs collection
        :param words: string or list of strings
        :return:
        """
        # if words is a single word convet it into a list for versatility of application of next lines of code
        if isinstance(words, str): words = [words]
        # if words are not stemmed we want to also remove their stemmed version from self.docs, so add them to words
        """
        stemmed_words = [tm.stem(word) for word in words]
        words = words.extend(word for word in stemmed_words if word not in words)
        """
        words.extend(tm.stem(word) for word in words if tm.stem(word) not in words)

        # remove words from self.docs
        self.docs = [filter(lambda word: word not in words, doc) for doc in self.docs]

def get_docs_from_reuters_file(corpus):
    """
    splits different news items in one reuters sgm file into documents
    :param corpus: the reuters file
    :return: list of documents
    """
    # Define new split function for this special document structure.
    def document_boundary(line1, line2):
        return line2.strip().startswith('&#5;&#5;&#5;')

    docs = []
    # Loop over documents
    lines = corpus.splitlines()
    for document in tm.splitby(lines, document_boundary):
        # Skip if first line (document[0]) doesn't match document structure
        if not document[0].strip().startswith('&#5;&#5;&#5;'):
            continue
        # document is a list of lines. Remove blank lines and strip out
        # whitespace to create a clean document.
        clean_lines = [line.strip() for line in document if line.strip()]
        # Print out clean document
        # print '\n'.join(clean_lines)
        docs.append('\n'.join(clean_lines))
        # print
    return docs


def retrieve_body(doc):
    """
    extracts textual body from an HTML document, i.e., get only what is between <title></title> and <body></body>
    :param doc: string
    :return: string: a string representing the title and body (separated by \n char) extracted from given html doc
    """

    def extract_between_tags(html, tag):
        """
        Uses regex to search through a html document for any text contained by certain HTML tag
        :param html: string: html doc
        :param tag: string: html tag in which text is enclosed
        :return: string: the retrieved text or an empty string
        """
        p = re.compile("<{tag}>((.*\n)*.*)</{tag}>".format(tag=tag), re.MULTILINE)
        return p.search(doc).group(1) if p.search(doc) else ""

    # get text inside TITLE tag
    title = extract_between_tags(doc, "TITLE")
    # get text inside BODY tag
    body = extract_between_tags(doc, "BODY")
    # join them
    return "\n".join([title, body])


if __name__ == '__main__':
    """
    Main interface driver.
    Text Mining demo usage of the textmining python package
    """

    # set some environ variables here
    os.environ.setdefault("JOB_WORKHOME", os.getcwd())

    try:
        txtmining = TxtMining()
        # Create some very short sample documents
        doc1 = 'John and Bob are brothers.'
        doc2 = 'John went to the store. The store was closed.'
        doc3 = 'Bob went to the store too.'

        txtmining.add_docs([doc1, doc2, doc3])
        txtmining.create_termdocument_matrix()

        print txtmining.docs
        print txtmining.get_termdocument_matrix()

        # get term document matrix as csv
        filename = os.environ.get('JOB_WORKHOME') + os.sep + "matrix.csv"
        txtmining.get_termdocument_matrix_as_csv(filename)

        txtmining.flush_docs()
        corpus= open(resources() + "/reuters21578/reut2-012.sgm", 'r').read()#.replace('\n', '')
        # get the news documents
        docs = get_docs_from_reuters_file(corpus)
        # we want only TITLE and BODY of each news item
        docs = map(retrieve_body, docs)

        txtmining.add_docs(docs)

        # clean, tokenize and stem the text we have
        txtmining.clean_docs()

        # some docs will become empty now, remove them
        txtmining.remove_empty_docs()

        # remove certain words (one word or list of words you want to remove from docs)
        # txtmining.remove_common_words(['reuter','spokesman'])
        txtmining.remove_common_words('reuter')

        docs = txtmining.get_docs()
        print "Num of docs %d" %len(docs)
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(docs)

        txtmining.create_termdocument_matrix(tokenzied=True)

        # get term document matrix as csv
        filename = os.environ.get('JOB_WORKHOME') + os.sep + "matrix.csv"
        txtmining.get_termdocument_matrix_as_csv(filename)

        # now do word cloud




        exit(0)


    except Exception as err:
        print str(err)
        exit(1)