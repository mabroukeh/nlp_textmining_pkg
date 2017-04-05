"""
Examples wuign the textmining package
Ref:
[1] https://pypi.python.org/pypi/textmining/1.0
[2] http://www.christianpeccei.com/textmining/index.html

"""

import textmining as tm
import os
import re
from root import resources


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

    def add_doc(self, doc):
        """
        Adds a document/corpus to the collection of documents maintained by this class
        :param doc: string representation of a document
        :return:
        """
        self.docs += doc

    def flush_docs(self):
        """
        clears all docs collection
        :return:
        """
        self.docs = []

    def create_termdocument_matrix(self):
        """
        creates a term document matrix of the frequencies of each term in each document held in self.docs
        :return:
        """
        self.tdm = tm.TermDocumentMatrix()
        for doc in self.docs:
            self.tdm.add_doc(doc)

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

        txtmining.add_doc([doc1, doc2, doc3])
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
        # clean the text we have
        docs = map(clean_text, docs)  # MAY BE WE CAN DO THIS AFTER txtmining.add_doc bby utilizing the lib in textmining for this purpose
        exit()

        txtmining.add_doc([retrieve_body(doc) for doc in get_docs_from_reuters_file(corpus)])



        corpus = resources() + "/feldman-cia-worldfactbook-data.txt"
        txtmining.flush_docs()
        # load documents from reuters news
        for i in xrange(5):
            news_file = open(resources() + "/reuters21578/reut2-00{num}.sgm".format(num=i), 'r')
            doc = news_file.read().replace('\n', '')
            print doc
            exit()
            txtmining.add_doc(doc)

        txtmining.create_termdocument_matrix()

        # get term document matrix as csv
        filename = os.environ.get('JOB_WORKHOME') + os.sep + "matrix.csv"
        txtmining.get_termdocument_matrix_as_csv(filename)




        exit(0)


    except Exception as err:
        print str(err)
        exit(1)