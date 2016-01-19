from matrice import *
from carte import *
from functools import *

def GetDir(i):
	dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
	return dirs[i]

def Heuristique(v1, v2):
	return abs(v1[0] - v2[0]) + abs(v1[1] - v2[1])

def ReconstruireChemin(chemin, depart, arrivee):
	courant = arrivee
	chemin_ = [courant]
	
	while courant !=  depart:
		courant = chemin[courant]
		chemin_.append(courant)

	return list(reversed(chemin_))

def AStar(plateau, depart, arrivee):
	visites = set()
	traces = {}
	poids = {depart : 0}
	heuristique = {depart : Heuristique(depart, arrivee)}
	pile = [(heuristique[depart], depart)]
	
	while len(pile) > 0:
		pos_courante = pile.pop()[1]
		
		if pos_courante == arrivee:
			return ReconstruireChemin(traces, depart, arrivee)
		
		visites.add(pos_courante)
		
		for i in range(4):
			d = GetDir(i)
			
			pos_v = (pos_courante[0] + d[0], pos_courante[1] + d[1])
			poids_elem = poids[pos_courante] + Heuristique(pos_courante, pos_v)
			if pos_v[0] >= 0 and pos_v[0] < getNbLignes(plateau) and pos_v[1] >= 0 and pos_v[1] < getNbColonnes(plateau):
				if pos_v in visites and poids_elem >= poids.get(pos_v, 0):
					continue
				else:
					passage = False
					
					c_courante = getVal(plateau, pos_courante[0], pos_courante[1])
					c_voisin = getVal(plateau, pos_v[0], pos_v[1])
					
					if (d == (-1, 0)):
						if (passageNord(c_courante, c_voisin)):
							passage = True
					elif (d == (0, 1)):
						if (passageEst(c_courante, c_voisin)):
							passage = True
					elif (d == (1, 0)):
						if (passageSud(c_courante, c_voisin)):
							passage = True
					else: # (0, -1)
						if (passageOuest(c_courante, c_voisin)):
							passage = True
					
					if passage:
						if  poids_elem < poids.get(pos_v, 0) or pos_v not in [i[1] for i in pile]:
							traces[pos_v] = pos_courante
							poids[pos_v] = poids_elem
							heuristique[pos_v] = poids_elem + Heuristique(pos_v, arrivee)
							pile.append((heuristique[pos_v], pos_v))
					else:
						continue
			else: # position en dehors du plateau
				continue

#-------------------------------
# TEST
#-------------------------------

import random

# fonction utilitataire
def afficheLigneSeparatrice(matrice,tailleCellule=4):
	print()
	for i in range(getNbColonnes(matrice)+1):
		print('-'*tailleCellule+'+', end="")
	print()

# fonction d'affichage d'une matrice
def drawMat(matrice,tailleCellule=4):
	nbColonnes=getNbColonnes(matrice)
	nbLignes=getNbLignes(matrice)
	print(' '*tailleCellule+'|',end='')
	for i in range(nbColonnes):
		print(str(i).center(tailleCellule)+'|',end='')
	afficheLigneSeparatrice(matrice,tailleCellule)
	for i in range(nbLignes):
		print(str(i).rjust(tailleCellule)+'|',end='')
		for j in range(nbColonnes):
			#print(str(getVal(matrice,i,j)).rjust(tailleCellule)+'|',end='')
			dN = "N" if getVal(matrice,i,j)['direction'][0] == False else "-"
			dE = "E" if getVal(matrice,i,j)['direction'][1] == False else "-"
			dS = "S" if getVal(matrice,i,j)['direction'][2] == False else "-"
			dO = "O" if getVal(matrice,i,j)['direction'][3] == False else "-"
			print((dN+dE+dS+dO).rjust(tailleCellule)+'|',end='')
		afficheLigneSeparatrice(matrice,tailleCellule)
	print()

# TESTS

'''
plat = Matrice(7,7)
for i in range(getNbLignes(plat)):
	for j in range(getNbColonnes(plat)):
		setVal(plat, i, j, Carte(bool(0),bool(0),bool(0),bool(0)))

drawMat(plat)

dep = (0, 0)
arr = (6, 6)
chem = AStar(plat, dep, arr)
print('chem', chem)
'''