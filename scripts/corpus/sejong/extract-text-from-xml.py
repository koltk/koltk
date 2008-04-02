#!/usr/bin/python
# $Id$
from xml.sax.handler import ContentHandler
import xml.sax
import sys

class textHandler(ContentHandler):
	def characters(self, ch):
		sys.stdout.write(ch.encode("utf-8"))

parser = xml.sax.make_parser()
handler = textHandler()
parser.setContentHandler(handler)
parser.parse(sys.argv[1])
