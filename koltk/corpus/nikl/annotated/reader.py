"""NIKL Annotated Corpus Reader
"""

import os

try: 
    import simplejson as json
except ImportError:
    import json

from .object import Corpus, CorpusMetadata, DocumentList, Document

class NiklansonReader:
    """NIKL ANnotated corpus JSON format file reader.

    Wrap file contents into a corpus. The top level object of a file may be a
    corpus or a doucment.

    """
    def __init__(self, filename):
        self.__filename = filename
        with open(filename) as file:
            self.__data = json.load(file)
            
            if 'document' in self.__data:
                self.__toplevel = 'corpus'
                self.__corpus = Corpus.from_dict(self.__data)
            elif 'sentence' in self.__data:
                self.__toplevel = 'document'
                self.__document = Document.from_dict(self.__data)
            else:
                self.__toplevel = None

    @property
    def filename(self):
        return self.__filename
    
    @property
    def basename(self):
        return os.path.basename(self.__filename)

    @property
    def toplevel(self):
        return self.__toplevel
        
    @property
    def corpus(self):
        if self.toplevel == 'corpus' :
            return self.__corpus
        else:
            raise Exception('The top level object is not a corpus.')

    @property
    def document(self):
        if self.toplevel == 'document':
            return self.__document
        else:
            raise Exception('The top level object is not a document.')

    @property
    def document_list(self):
        if self.toplevel == 'corpus' :
            return self.corpus.document_list
        elif self.toplevel == 'document' :
            return [self.document]
            
    def __repr__(self):
        return 'NiklansonReader(filename={}, toplevel={})'.format(self.filename, self.toplevel)



class NiklansonCorpusReader:
    """NIKL Annotated Corpus JSON Reader.
    
    Read a NIKL annotated corpus JSON file.
    """
    def __init__(self, filename):
        self.filename = filename
        with open(filename) as file:
            self.data = json.load(file)
        
    @property
    def corpus(self):
        return Corpus.from_dict(self.data) 

class NiklansonDocumentReader:
    """NIKL ANnotated corpus JSON Document file Reader.

    Read NIKL annotated document JSON files
    """
    def __init__(self, filename):
        self.filename = filename
        with open(filename) as file:
            self.data = json.load(file)

    @property
    def document(self):
        return Document.from_dict(self.data)

    



