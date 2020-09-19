"""NIKL Annotated Corpus Reader
"""

import os

try: 
    import simplejson as json
except ImportError:
    import json

from .object import Corpus, CorpusMetadata, DocumentList

class NiklansonReader:
    """NIKL ANnotated corpus JSON format file reader.

    Wrap file contents into a corpus. The top level object of a file may be a
    corpus, a doucment, or a sentence.

    """
    def __init__(self, filename):
        self.__filename = filename
        with open(filename) as file:
            self.__data = json.load(file)
        
        self.__level = None

    @property
    def filename(self):
        return self.__filename
    
    @property
    def basename(self):
        return os.path.basename(self.__filename)

    @property
    def level(self):
        if 'document' in self.__data:
            self.__level = 'corpus'
        elif 'sentence' in self.__data:
            self.__level = 'document'
        elif 'form' in self.__data:
            self.__level = 'sentence'

        return self.__level
        
    @property
    def corpus(self):
        if self.level == 'corpus' :
            corpus= self.__data
        elif self.level == 'document' :
            corpus = { 'id' : '', 'metadata' : {}, 'document' : [ self.__data ] }
        elif self.level == 'sentence' :
            doc = { 'id' : '', 'metadata' : {}, 'sentence' : [ self.__data ]  }
            corpus = { 'id' : '', 'metadata' : {}, 'document' : doc }

        return Corpus(corpus)

    @property
    def document_list(self):
        if self.level == 'corpus' :
            doclist = self.__data['document']
        elif self.level == 'document' :
            doclist = [ self.__data ]
        elif self.level == 'sentence' :
            doc = { 'id' : '', 'metadata' : {}, 'sentence' : [ self.__data ]  }
            doclist= [ doc ]

        return DocumentList(doclist)
    
    def __repr__(self):
        return self.filename + ' ' + self.level



class NiklansonCorpusReader:
    """NIKL Annotated Corpus JSON Reader.
    
    Read a NIKL annotated corpus JSON file.
    """
    def __init__(self, filename):
        self.filename = filename
        with open(filename) as file:
            self.__data = json.load(file)
        
    @property
    def corpus(self):
        return Corpus(self.__data) 

    @property
    def document_list(self):
        return DocumentList(self.__data['document'])


class NiklansonDocumentReader:
    """NIKL ANnotated corpus JSON Document file Reader.

    Read NIKL annotated document JSON files
    """
    def __init__(self, filenames):
        pass

class NiklansonSentenceReader:
    """NIKL ANnotated Corpus Sentence file Reader.

    Read NIKL annotated sentence JSON files
    """
    def __init__(self, filenames):
        pass
    
     
if __name__ == '__main__':
    import sys
    nr = NiklansonReader(sys.argv[1])
    print(nr)
    



