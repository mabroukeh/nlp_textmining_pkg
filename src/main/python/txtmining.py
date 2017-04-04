"""
Examples wuign the textmining package
Ref:
[1] https://pypi.python.org/pypi/textmining/1.0
[2] http://www.christianpeccei.com/textmining/index.html

"""

import textmining as tm
import os

# set some environ variables here
os.environ.setdefault("JOB_WORKHOME", os.getcwd())


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


if __name__ == '__main__':
    """
    Main interface driver.
    Text Mining demo usage of the textmining python package
    """
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

        exit(0)


    except Exception as err:
        print str(err)
        exit(1)