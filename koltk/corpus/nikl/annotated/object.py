r"""NIKL ANnotated Corpus JSON (Niklanson) Objects

.. code-block::

  Corpus
    CorpusMetadata
    DocumentList
      Document
        DocumentMetadata
        SentenceList
          Sentence
            WordList, Word
            MorphemeList, Morpheme
            WSDList, WSD
            NEList, NE
            DPList, DP
            SRLList, SR
        ZAList, ZA
        CRList, CR



"""


from __future__ import annotations
from .base import Niklanson
import re
import json

class CorpusMetadata(Niklanson):
    def __init__(self, iterable=(), **extra):
        self.title = None
        self.creator = None
        self.distributor = None
        self.year = None
        self.category = None
        self.annotation_level = []
        self.sampling = None
        
        super().__init__(iterable)
        self.update(extra)
    
class Corpus:
    """Corpus: the top level object.

    - id
    - :class:`.CorpusMetadata`
    - :class:`.DocumentList`

    JSON:
    
    .. code-block:: json
      
      {
        "id" : "",
        "metadata" : {},
        "document" : []
      }
    
    Args:
        corpus (Corpus) : corpus
    

    Example:
    
    .. code-block:: python

        Corpus({ "id" : "", "metadata" : {}, "document" : [] })
        Corpus(id='', metadata=None, document=[])

    """
    def __init__(self, *args, **kwargs):
        if args == [] and kwargs == {}:
            self.__init_empty()
        elif len(args) == 1 and kwargs == {}:
            corpus = args[0]
            if type(corpus) is Corpus:
                # TODO: implement clone
                raise NotImplementedError 
            elif type(corpus) is dict:
                self.__init_from_dict(corpus)
            else:
                raise TypeError
        elif args == [] and len(kwargs) > 0:
            self__init_from_kwargs(kwargs)

    def __init_empty(self):
        self.id = ''
        self.metadata = None
        self.__document_list = []
        
    def __init_from_dict(self, corpus):
        #self.__json = corpus
        self.id = corpus['id']
        self.metadata = CorpusMetadata(corpus['metadata'])
        self.__document_list = DocumentList(corpus['document'])

    def __init_from_kwargs(self, kwargs):
        self.id = kwargs['id']
        self.metadata = kwargs['metadata']
        self.__document_list = kwargs['document']
        

    @property
    def document_list(self):
        """ :class:`.DocumentList`
        """
        if self.__document_list is None:
            self.__document_list = DocumentList(self.__json['document'])

        return self.__document_list

    def __repr__(self):
        return 'Corpus(id={})'.format(self.id)


class DocumentList(list):
    def __init__(self, document_list):
        if type(document_list) is DocumentList:
            # TODO: implement clone
            raise NotImplementedError
        elif type(document_list) is list:
            self.__init_from_json(document_list)

    def __init_from_json(self, document_list):
        self.__json = document_list

        for doc in document_list:
            list.append(self, Document(doc))
                    


class DocumentMetadata(Niklanson):
    def __init__(self, iterable=(), **extra):
        self.title = None
        self.author = None
        self.publisher = None
        self.date = None
        self.topic = None
        self.url = None
        
        super().__init__(iterable)
        self.update(extra)
    

class Document:
    """
    Document(id, metadata=DocumentMetadata(), sentence=[])

    ::

        >>> d = Document('X200818')
        >>> print(d)
        {
          "id": "X200818",
          "metadata": {
            "title": "",
            "author": "",
            "publisher": "",
            "date": "",
            "topic": "",
            "url": ""
          },
          "sentence": [],
          "ZA" : [],
          "CR" : []
        }
       
    """
    # def __init__(self, id=None, metadata=DocumentMetadata(), sentence = [], cr = [], za = []):
    def __init__(self, document):
        if type(document) is Document:
            # TODO: implement clone
            raise NotImplementedError
        elif type(document) is dict:
           self.__init_from_json(document) 

    def __init_from_json(self, document):
        self.__json = document
        self.id = document['id']
        self.metadata = DocumentMetadata(document['metadata'])
        self.__sentence_list = None
        self.__za_list = None
        self.__cr_list = None

    @property
    def sentence_list(self):
        if self.__sentence_list is None:
            self.__sentence_list = SentenceList(self.__json['sentence'])

        return self.__sentence_list
        
    def __repr__(self):
        return 'Document(id={})'.format(self.id)
    
    def __str__(self):
        return json.dumps(self.__json, ensure_ascii=False)
    
class SentenceList(list):
    def __init__(self, sentence_list):
        if type(sentence_list) is SentenceList:
            # TODO: implement clone
            raise NotImplementedError
        elif type(sentence_list) is list:
            self.__init_from_json(sentence_list)

    def __init_from_json(self, sentence_list):
        self.__json = sentence_list

        for s in sentence_list:
            list.append(self, Sentence(s))
    
class Sentence:
    """
    Sentence(id, form)

    ::

        >>> s = Sentence('X200818', '아이들이 책을 읽는다.')
        >>> print(s)
        {
          "id": "X200818",
          "form": "아이들이 책을 읽는다.",
          "word": [
              {
                "id": 1,
                "form": "아이들이",
                "begin": 0,
                "end": 4
              },
              {
                "id": 2,
                "form": "책을",
                "begin": 5,
                "end": 7
              },
              {
                "id": 3,
                "form": "읽는다.",
                "begin": 8,
                "end": 12
              }
          ]
        }    

    """
    #def __init__(self, id: str, form: str, word: list(Word) = None):
    def __init__(self, sentence):
        if type(sentence) is Sentence:
            # TODO: implement clone
            raise NotImplementedError
        elif type(sentence) is dict:
           self.__init_from_json(sentence)

    def __init_from_json(self, sentence):
        self.__json = sentence
        self.id = sentence['id']
        self.form = sentence['form']
        self.__word_list = None 
        self.__morpheme_list = None
        self.__wsd_list = None
        self.__ne_list = None
        self.__dp_list = None
        self.__srl_list = None

    @property
    def word_list(self):
        if self.__word_list is None:
            self.__word_list = WordList(self.__json['word'])

        return self.__word_list
    
    @property
    def morpheme_list(self):
        if self.__morpheme_list is None:
            self.__morpheme_list = MorphemeList(self.__json['morpheme'])
            
        return self.__morpheme_list
    
    @property
    def wsd_list(self):
        if self.__wsd_list is None:
            self.__wsd_list = WSDList(self.__json['WSD'])
            
        return self.__wsd_list
        
    @property
    def ne_list(self):
        if self.__ne_list is None:
            self.__ne_list = NEList(self.__json['NE'])
            
        return self.__ne_list
  
    @property
    def dp_list(self):
        if self.__dp_list is None:
            self.__dp_list = DPList(self.__json['DP'])
            
        return self.__dp_list
  
    @property
    def srl_list(self):
        if self.__srl_list is None:
            self.__srl_list = SRLList(self.__json['SRL'])
            
        return self.__srl_list
  
    @property
    def za_list(self):
        if self.__za_list is None:
            self.__za_list = ZAList(self.__json['ZA'])
            
        return self.__za_list
  
    @property
    def cr_list(self):
        if self.__cr_list is None:
            self.__cr_list = CRList(self.__json['CR'])
            
        return self.__cr_list
  

    def __init_word_list_from_sentence_form(self):
        self.__word_list = []
        beg = 0
        i = 0
       
        for tok in re.split('(\s+)', self.form):
            if tok == '' : continue
            elif re.match('\s', tok[0]) : beg += len(tok)
            else:
                i += 1
                self.word.append(Word(i, tok, beg, beg + len(tok))) 
                beg += len(tok)
    @property
    def fwid(self):
        toks = self.id.split(".")
        if len(toks) == 2:
            docid, sentnum = toks
            fw_sid = "{}-{:05d}".format(docid, int(sentnum))
        elif len(toks) == 4:
            corpusid, docnum, paranum, sentnum = toks
            fw_sid = "{}-{:04d}-{:05d}-{:05d}".format(corpusid, int(docnum), int(paranum), int(sentnum))
        else:
            sys.exit(sid)

        return fw_sid

    def __repr__(self):
        return json.dumps(self.__json, ensure_ascii=False)
        

class WordList(list):
    def __init__(self, word_list):
        if type(word_list) is WordList:
            # TODO: implement clone
            raise NotImplementedError
        elif type(word_list) is list:
            self.__init_from_json(word_list)

    def __init_from_json(self, word_list):
        self.__json = word_list
        
        for w in word_list:
            list.append(self, Word(w))
            
        
    
        
class Word(Niklanson):
    """
    Word
    """
    #def __init__(self, id : int, form : str, begin : int, end : int):
    def __init__(self, word):
        if type(word) is Word:
            # TODO: implement clone
            raise NotImplementedError
        elif type(word) is dict:
            self.__init_from_json(word)
            
    def __init_from_json(self, word):
        super().__init__(word)

    @property
    def slice(self):
        return slice(self.begin, self.end) 

    @property
    def slice_str(self):
       return '{}:{}'.format(self.begin, self.end) 


class MorphemeList(list):
    def __init__(self, morpheme_list):
        if type(morpheme_list) is MorphemeList:
            # TODO: implement clone
            raise NotImplementedError
        elif type(morpheme_list) is list:
            self.__init_from_json(morpheme_list)

    def __init_from_json(self, morpheme_list):
        self.__json = morpheme_list
        
        for w in morpheme_list:
            list.append(self, Morpheme.from_dict(w))
            
 
class Morpheme(Niklanson):
    """Morpheme
    """
    def __init__(self,
                 id : int = None,
                 form: str = None,
                 label : str = None,
                 word_id : int = None,
                 position : int = None):
        self.id = id
        self.form = form
        self.label = label
        self.word_id = word_id
        self.position = position
        self.__str = None

    @classmethod
    def strict(cls, id, form, label, word_id, position):
        return cls(id, form, label, word_id, position)

    @property
    def str(self):
        if self.__str is None:
            self.__str = self.form + '/' + self.label

        return self.__str


class WSDList(list):
    def __init__(self, wsd_list):
        if type(wsd_list) is WSDList:
            # TODO: implement clone
            raise NotImplementedError
        elif type(wsd_list) is list:
            self.__init_from_json(wsd_list)

    def __init_from_json(self, wsd_list):
        self.__json = wsd_list
        
        for w in wsd_list:
            list.append(self, WSD(w))
 
class WSD(Niklanson):
    """
    WSD (Word Sense Disambiguation)
    """
    #def __init__(self, word: str, sense_id: int, pos : str, begin: int, end: int):
    def __init__(self, wsd):
        if type(wsd) is WSD:
            pass
        elif type(wsd) is dict:
            self.__init_from_json(wsd)

            
    def __init_from_json(self, wsd):
        super().update(wsd)
        # self.word = word
        # self.sense_id = sense_id
        # self.pos = pos
        # self.begin = begin
        # self.end = end

    def __str__(self):
        return '{}__{:03d}/{}'.format(self.word, self.sense_id, self.pos)

    @property
    def slice(self):
        return slice(self.begin, self.end)

    @property
    def slice_str(self):
        return '{}:{}'.format(self.begin, self.end)
    
        
class NEList(list):
    def __init__(self, ne_list):
        if type(ne_list) is NEList:
            # TODO: implement clone
            raise NotImplementedError
        elif type(ne_list) is list:
            self.__init_from_json(ne_list)

    def __init_from_json(self, ne_list):
        self.__json = ne_list
        
        for w in ne_list:
            list.append(self, NE(w))
 
class NE(Niklanson):
    """
    NE (Named Entity)
    """
    #def __init__(self, id: int, form: str, label: str, begin:int, end: int):
    def __init__(self, ne):
        if type(ne) is NE:
            pass
        elif type(ne) is dict:
            self.__init_from_json(ne)

            
    def __init_from_json(self, ne):
        super().update(ne)
 
        # self.id = id
        # self.form = form
        # self.label = label
        # self.begin = begin
        # self.end = end

    @property
    def slice_str(self):
        return '{}:{}'.format(self.begin, self.end)

    @property
    def slice(self):
        return slice(self.begin, self.end)

    def __str__(self):
        return '{}/{}'.format(self.form, self.label)

class DPList(list):
    def __init__(self, dp_list):
        if type(dp_list) is DPList:
            # TODO: implement clone
            raise NotImplementedError
        elif type(dp_list) is list:
            self.__init_from_json(dp_list)

    def __init_from_json(self, dp_list):
        self.__json = dp_list
        
        for w in dp_list:
            list.append(self, DP(w))
 

class DP(Niklanson):
    """
    DP (Denpendency Parsing)
    """
    #def __init__(self, word_id: int, word_form: str, head: int, label: str, depdendent: list[int]):
    def __init__(self, dp):
        if type(dp) is DP:
            pass
        elif type(dp) is dict:
            self.__init_from_json(dp)

            
    def __init_from_json(self, dp):
        super().update(dp)
 
        # self.word_id = word_id
        # self.word_form = word_form
        # self.head = head
        # self.label = label
        # self.dependent = dependent
    
class SRLList(list):
    def __init__(self, srl_list):
        if type(srl_list) is SRLList:
            # TODO: implement clone
            raise NotImplementedError
        elif type(srl_list) is list:
            self.__init_from_json(srl_list)

    def __init_from_json(self, srl_list):
        self.__json = srl_list
        
        for srl in srl_list:
            list.append(self, SRL(srl))
        
class SRLPredicate(Niklanson):
    def __init__(self, form: str, begin: int, end: int, lemma: str, sense_id: int):
        self.form = form
        self.begin = begin
        self.end = end
        self.lemma = lemma
        self.sense_id = sense_id

class SRLArgument(Niklanson):
    def __init__(self, form: str, label: str, begin: int, end: int):
        self.form = form
        self.label = label
        self.begin = begin
        self.end = end

class SRL(Niklanson):
    """
    SRL (Semantic Role Labeling)
    
    consists of a predicate and a list of arguments::
    
        >>> SRL(SRLPredicate(), [SRLArgument()])
    """
    def __init__(self, predicate: SRLPredicate, argument: []):
        """
        :param argument: list(SRLArgument)
        
        ``argument`` is a list of Argument.
        """
        self.predicate = predicate
        self.argument = argument

class CRList(list):
    def __init__(self, cr_list):
        if type(cr_list) is crList:
            # TODO: implement clone
            raise NotImplementedError
        elif type(cr_list) is list:
            self.__init_from_json(cr_list)

    def __init_from_json(self, cr_list):
        self.__json = cr_list
        
        for cr in cr_list:
            list.append(self, CR(cr))
  

class CRMention(Niklanson):
    def __init__(self, form : str, NE_id : int, sentence_id : int, begin : int, end : int):
        self.form = form
        self.NE_id = NE_id
        self.sentence_id = sentence_id
        self.begin = begin
        self.end = end

class CR(Niklanson):
    """
    CR (Cross Reference)
    """
    def __init__(self, mention: list(CRMention)):
        """
        """
        self.mention = mention
    
class ZAList(list):
    def __init__(self, za_list):
        if type(za_list) is ZAList:
            # TODO: implement clone
            raise NotImplementedError
        elif type(za_list) is list:
            self.__init_from_json(za_list)

    def __init_from_json(self, za_list):
        self.__json = za_list
        
        for w in za_list:
            list.append(self, ZA(w))
 

class ZAPredicate(Niklanson):
    def __init__(self, form: str, sentence_id: int, begin: int, end: int):
        self.form = form
        self.sentence_id = sentence_id
        self.begin = begin
        self.end = end

class ZAAntecedent(Niklanson):
    def __init__(self, type: str, form: str, sentence_id: int, begin: int, end: int):
        self.type = type
        self.form = form
        self.sentence_id = sentence_id
        self.begin = begin
        self.end = end
        
class ZA(Niklanson):
    def __init__(self, predicate: ZAPredicate, antecedent: list(ZAAntecedent)):
       self.predicate = predicate
       self.antecedent = antecedent
