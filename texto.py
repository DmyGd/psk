# -*- coding: utf-8 -*-

from base import *
from arbol import *

# Creaa un objetos que recibe un texto y lo procesa por medio de spacy (nlp está definido en base.py)
# el texto procesado con spacy se encuentra en el atributo linea y es un arreglo de Palabras sin clasificar
# ver base.py

class Texto:
	def __init__(self, texto):
		self.linea = []
		texto.strip('\n')
		texto = nlp(texto)
		for token in texto:
			palabra = Palabra(token.text,token.lemma_,token.pos_)
			self.linea.append(palabra)
		#temp_row_list.append(token.lemma_+'/'+token.pos_)

	def __str__(self):
		r = ""
		for p in self.linea:
			r = r+"{0:25}\t{1:20}\t{2:10}\t{3:10}\t{4:10}\n".format(p.palabra, p.lemma, p.pos, p.tipo, p.idTipo)
		return r


class TextoAnalizado(Texto):

	def __init__(self, txt):
		self.vd = Arbol('vd.txt')
		self.vnd = Arbol('vnd.txt')
		self.nexo = Arbol('nexo.txt')
		self.termino = Arbol('terminos.txt',1)
		#self.vd.imprimeExpresiones()

		
		Texto.__init__(self,txt)






if __name__ == '__main__':
	# 0 -cualquiera
	# 1 - vd
	# 2 - vnd
	# 3 - nx
	# 4 - t
	# 5 - d
	vDef = 1
	vNoDef = 2
	nx = 3
	t = 4
	#s = "1844. A mast cell is a leukocyte that produces inflammatory molecules, such as histamine, in response to large pathogens.         A basophil is a leukocyte that, like a neutrophil, releases chemicals to stimulate the inflammatory response as illustrated in [link].       Basophils are also involved in allergy and hypersensitivity responses and induce specific types of inflammatory responses. "
	#s= "1844. A mast cell is a leukocyte that produces inflammatory molecules"
	s = "that primarily which states that Hello Dog some these are called which states that monitors and causes which states that Hello Dog these are called which states that that primarily"
	analisis1 = TextoAnalizado(s)
	#print(str(analisis1.linea))
	analisis1.vd.buscarTermino(analisis1.linea,vDef)


	print(analisis1)
#t = Texto("1542.         When blood glucose levels decline below normal levels, for example between meals or when glucose is utilized rapidly during exercise, the hormone glucagon is released from the alpha cells of the pancreas.       Glucagon raises blood glucose levels, eliciting what is called a hyperglycemic effect, by stimulating the breakdown of glycogen to glucose in skeletal muscle cells and liver cells in a process called glycogenolysis.")
#print(t)


