# -*- coding: utf-8 -*-

import spacy 
import sys

sys.stdout.reconfigure(encoding='utf-8')
nlp = spacy.load('en_core_web_sm')

class Palabra:
	def __init__(self, palabra, lemma, pos):
		self.palabra = palabra
		self.pos = pos
		self.lemma = lemma
		# 0 -cualquiera
		# 1 - vd
		# 2 - vnd
		# 3 - nx
		# 4 - t
		# 5 - d
		self.tipo = 0
		self.idTipo = -1
		return

	def __str__(self):
		return "[({}),({}),({})]".format(self.palabra,self.lemma,self.pos)

	# def __eq__(self,otraPalabra):
	# 	assert isinstance(otraPalabra,Palabra),"Se intenta comparar palabra con algo que no es una palabra"
	# 	r = self.lemma == otraPalabra.lemma
	# 	print(self.lemma,otraPalabra.lemma,'?',r)
	# 	return r

if __name__ == '__main__':
	p1 = Palabra('a','alemma','apos')
	p2 = Palabra('b','alemma','bpos')
	if p1==p2:
		print("iguales")
	else:
		print("diferentes")

