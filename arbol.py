# -*- coding: utf-8 -*-
import spacy 
import sys
from base import *
from texto import *
from enum import Enum

sys.stdout.reconfigure(encoding='utf-8')

idNodo = 0

from enum import Enum

class TipoNodo(Enum):
	Lemma = 1
	POS = 2
	Palabra = 3
	Termino = 4

class Nodo:
	def __init__(self,palabra):
		global idNodo
		self.palabra = palabra
		self.hojas = []
		self.terminal = False
		self.id = idNodo
		self.idExpresion = -1
		idNodo += 1
		return

	def __str__(self):
		res = '('+str(self.palabra)+' '+str(self.id)+'->{'
		for h in self.hojas:
			res = res + h.palabra.palabra+','
		res = res+'}'
		return res


	def comparaConNodo(self,hoja,palabra):
		pass

	def crearNodo(self,palabra):
		pass		

	# busca el nodo correspondiente a la palabra dada como parámetro
	# si existe regresa el nodo si no regresa None
	def buscarNodo(self,palabra):
		for hoja in self.hojas:
			if self.comparaConNodo(hoja,palabra):
				return hoja
		return None	

	def obtenerHoja(self,palabra):
		#print('=>',str(palabra),end='')
		nodo = self.buscarNodo(palabra)
		#print('-->',end='')
		if (nodo==None):
			#print(' -new- ')
			nodo = self.crearNodo(palabra)
			self.hojas.append(nodo)
			return nodo
		#print(' * ')
		return nodo

class NodoLemma(Nodo):
	def crearNodo(self,palabra):
		return NodoLemma(palabra)

	def comparaConNodo(self,hoja,palabra):
		return hoja.palabra.lemma==palabra.lemma


class NodoPOS(Nodo):
	def crearNodo(self,palabra):
		return NodoPOS(palabra)

	def comparaConNodo(self,hoja,palabra):
		return hoja.palabra.pos==palabra.pos


class NodoPalabra(Nodo):
	def crearNodo(self,palabra):
		return NodoPalabra(palabra)

	def comparaConNodo(self,hoja,palabra):
		return hoja.palabra.palabra==palabra.palabra


class Arbol:
	def __init__(self,nombre='',tipoNodo = TipoNodo.Lemma,tipoArbol = 0):
		self.tipoNodo = tipoNodo
		if tipoNodo == TipoNodo.Lemma:
			self.raiz = NodoLemma('-Lemas-')
		elif tipoNodo == TipoNodo.Palabra: 
			self.raiz = NodoPalabra('-Palabras-')
		else:
			self.raiz = NodoPOS('-POS-')



		self.expresiones = dict()
		if len(nombre) > 0:
			if tipoArbol == 0:
				self.cargaArchivo(nombre)
			else:
				self.cargaArchivoTerminos(nombre)




	def agregarLista(self,palabras,raiz,id=0):
		if raiz == self.raiz:
			# agrega la expresion a el diccionario de expresiones
			self.expresiones[id] = palabras
		if len(palabras)==0:
			raiz.terminal = True
			raiz.idExpresion = id
			return
		hoja = raiz.obtenerHoja(palabras[0])
		self.agregarLista(palabras[1:],hoja,id)
		return

	def imprimeListaHojas(self,lista):
		print("[{},".format(str(lista[0])),end='')
		for hoja in lista[1:]:
			print(str(hoja),end='')
		print("]")

	#funcion usada por imprime
	def recorre(self,raiz,lista):
		lista = lista[:]
		lista.append(raiz)
		if raiz.terminal:
			self.imprimeListaHojas(lista)	
		for h in raiz.hojas:
			self.recorre(h,lista)
		return 		

	def imprime(self):
		self.recorre(self.raiz,[])
		return

	def imprimeExpresiones(self):
		for k,v in self.expresiones.items():
			print(str(k)+'->',end='')
			for s in v:
				print(s,end = '')
			print()


# revisa si en los hijos de la raíz proporcionada se encuantra la palabra buscada
# regresa la hoja donde encontró la palabra o None si no la encontró
	def buscarHoja(self,raiz,palabra):
		for hoja in raiz.hojas:
			if hoja.palabra.pos == palabra.pos:
				return hoja
		return None

#regresa la hoja

	def buscarLista(self,raiz,palabras):
		if len(palabras)==0:
			return None
		hoja = self.buscarHoja(raiz,palabras[0])
		if hoja == None:
			return None
		if len(palabras) == 1:
			#si solo restaba una palabar y la hoja correspondiente es terminal regresa la hoja
			# regresa None si solo había una palabra y no se encontro una hoja terminal
			if hoja.terminal:
				return hoja
			return None

		if hoja.terminal:
			#si en la lista hay más de una palabra y la hoja actual es terminal entonces continua buscando
			#para ver si la siguiente palabra esta dentro de esa rama
			if self.buscarHoja(hoja,palabras[1]) == None:
				return hoja
		return self.buscarLista(hoja,palabras[1:])

	def buscarTermino(self,palabras,tipo):
		#vervosEncontrados = []
		for k in range(len(palabras)):
			#print(palabras[k])
			h = self.buscarHoja(self.raiz,palabras[k])

			if h != None:
				hoja = self.buscarLista(h,palabras[k+1:])
				if hoja!=None:
					palabras[k].tipo = tipo
					palabras[k].idTipo = hoja.idExpresion
					#print(">>>>>>>> [{},{}]".format(hoja.palabra,hoja.idExpresion))
					#print(type(self.expresiones[hoja.idExpresion]))
					longitud = len(self.expresiones[hoja.idExpresion])
					print("longitud: {} ".format(longitud))
					for j in range(longitud):
						
						print("cambiando el valor de "+str(palabras[k+j]))
						print("idExpresion: " + str(hoja.idExpresion))
						palabras[k+j].tipo = tipo
						#palabras[k+j].idTipo = hoja.idExpresion
						palabras[k+j].idTipo = hoja.idExpresion
						print("valor modificado: {}".format(palabras[k+j].idTipo))
					
					
				else:
					#vervosEncontrados.append([h.palabra.palabra,k,k])
					#vervosEncontrados.append([str(h.palabra),k,k])
					palabras[k].tipo = tipo
					print(">>>>>>>> [{},{}]".format(h.palabra,h.idExpresion))
					palabras[k].idTipo = h.idExpresion

		#return palabras

		


	def imprimeHojas(self,raiz):
		if raiz.terminal:
			print(raiz.id,' ',raiz.idExpresion,' -> ',end='')
			for palabra in self.expresiones[raiz.idExpresion]:
				print(palabra,end='')
			print()
		for h in raiz.hojas:
			self.imprimeHojas(h)
		return 

	def cargaArchivo(self,nombre):
		k = 0
		with open(nombre, encoding="utf_8") as f:
			for linea in f:
				linea = linea.rstrip(' \n')
				if len(linea)==0:
					continue
				t = Texto(linea)
				k = k+1
				self.agregarLista(t.linea,self.raiz,k)

	def cargaArchivoTerminos(self,nombre):
		k = 0
		with open(nombre, encoding="utf_8") as f:
			for linea in f:
				linea = linea.rstrip(' \n')
				if len(linea)==0:
					continue
				t = Texto(linea)
				for p in t.linea:
					p.pos = p.palabra
					p.lemma = p.palabra
				k = k+1
				self.agregarLista(t.linea,self.raiz,k)


class ArbolLemma(Arbol):
	def buscarHoja(self,raiz,palabra):
		for hoja in raiz.hojas:

			if hoja.palabra.palabra == palabra.palabra:
				return hoja
		return None


if __name__ == "__main__":
	vd = Arbol('nexo.txt',TipoNodo.Termino)

	#print("-"*30)
	vd.imprime()
	#print('*'*30)
	vd.imprimeExpresiones()



# is know
# is known as
# it is know in that 
# in which

