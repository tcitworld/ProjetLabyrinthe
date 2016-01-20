from matrice import *
from carte import *

# classe noeud
class Noeud(object):
	def __init__(self, x, y, poids, heuristique):
		self.x = x
		self.y = y
		self.poids = poids
		self.heuristique = heuristique
		
	def getHeuristique(self):
		return self.heuristique
		
	def getPoids(self):
		return self.poids
		
	def getPosition(self):
		return (self.x, self.y)
		
	def setHeuristique(self, heuristique):
		self.heuristique = heuristique
	
	def setPoids(self, poids):
		self.poids = poids
	
	def setPosition(self, position):
		self.position = position
	
	def __str__(self):
		return "Noeud(" + str(self.x) + ", " + str(self.y) + ", " + str(self.poids) + ", " + str(self.heuristique) + ")"

# fonction utilitaire
def GetDir(i):
	dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
	return dirs[i]

def Heuristique(n1, n2):
	return abs(n1[0] - n2[0]) + abs(n1[1] - n2[1])

def RechercheNoeudDansPile(pile, pos):
	l = [x for x in pile if x.getPosition() == pos]
	if len(l) > 0:	
		return l[0]
	else:
		return Noeud(None, None, 0, None) # on retourne un noeud virtuel avec un poids 0
		

# classe AStar
class AStar(object):
	def __init__(self, plateau, depart, arrivee):
		self.plateau = plateau
		self.depart = Noeud(depart[0], depart[1], Heuristique(depart, arrivee), 0)
		self.arrivee = Noeud(arrivee[0], arrivee[1], None, None)
		self.traces = {}
		self.cheminTrouve = False
		
	# Reconstruit le chemin si celui ci existe
	def ReconstruireChemin(self):
		if self.cheminTrouve == False:
			return None
			
		courant = self.arrivee.getPosition()
		chemin = [courant]
		
		while courant != self.depart.getPosition():
			courant = self.traces[courant]
			chemin.append(courant)
			
		return list(reversed(chemin))
	
	def Calculer(self):
		visites = set()
		pile = [self.depart]
		
		while (len(pile)) > 0:
			courant = pile.pop()
			if courant.getPosition() == self.arrivee.getPosition():
				self.cheminTrouve = True
				return self.cheminTrouve
			
			visites.add(courant.getPosition())
			
			for i in range(4):
				d = GetDir(i)
				# valeur de la case voisine dans la direction souhaitée
				pos_v = (courant.getPosition()[0] + d[0], courant.getPosition()[1] + d[1])
				poids_v = courant.getPoids() + Heuristique(courant.getPosition(), pos_v)
				
				if pos_v[0] >= 0 and pos_v[0] < self.plateau.getNbLignes() and pos_v[1] >= 0 and pos_v[1] < self.plateau.getNbColonnes():
					n = RechercheNoeudDansPile(pile, pos_v)
					if pos_v in visites and poids_v >= n.getPoids():
						continue
					else:
						passage = False
						
						c_courant = self.plateau.getVal(courant.getPosition()[0], courant.getPosition()[1])
						c_voisin = self.plateau.getVal(pos_v[0], pos_v[1])
						
						if (d == (-1, 0)):
							if (c_courant.passageNord(c_voisin)):
								passage = True
						elif (d == (0, 1)):
							if (c_courant.passageEst(c_voisin)):
								passage = True
						elif (d == (1, 0)):
							if (c_courant.passageSud(c_voisin)):
								passage = True
						else: # (0, -1)
							if (c_courant.passageOuest(c_voisin)):
								passage = True
						
						
						if passage:
							if poids_v < n.getPoids() or pos_v not in [k.getPosition() for k in pile]:
								self.traces[pos_v] = courant.getPosition()
								n2 = Noeud(pos_v[0], pos_v[1], poids_v, poids_v + Heuristique(pos_v, self.arrivee.getPosition()))
								pile.append(n2)
				else: # position en dehors du plateau
					continue


#-------------------------------
# TEST
#-------------------------------
'''
import random

# fonction d'affichage d'une matrice modifiée pour le test de l'algoritme a star
def drawMat(matrice,tailleCellule=4):
	nbColonnes=matrice.getNbColonnes()
	nbLignes=matrice.getNbLignes()
	print(' '*tailleCellule+'|',end='')
	for i in range(nbColonnes):
		print(str(i).center(tailleCellule)+'|',end='')
	matrice.afficheLigneSeparatrice(tailleCellule)
	for i in range(nbLignes):
		print(str(i).rjust(tailleCellule)+'|',end='')
		for j in range(nbColonnes):
			#print(str(matrice.getVal(i,j)).rjust(tailleCellule)+'|',end='')
			dN = "N" if matrice.getVal(i,j).murNord() == False else "-"
			dE = "E" if matrice.getVal(i,j).murEst() == False else "-"
			dS = "S" if matrice.getVal(i,j).murSud() == False else "-"
			dO = "O" if matrice.getVal(i,j).murOuest() == False else "-"
			print((dN+dE+dS+dO).rjust(tailleCellule)+'|',end='')
		matrice.afficheLigneSeparatrice(tailleCellule)
	print()

plat = Matrice(7,7)
for i in range(plat.getNbLignes()):
	for j in range(plat.getNbColonnes()):
		plat.setVal(i, j, Carte(bool(random.randint(0, 1)),bool(random.randint(0, 1)),bool(random.randint(0, 1)),bool(random.randint(0, 1)), 0, []))

#plat.setVal(1, 0, Carte(bool(1), bool(1), bool(1), bool(0), 0, []))

drawMat(plat)

dep = (0, 0)
arr = (1, 2)
astar = AStar(plat, dep, arr)
astar.Calculer()
print('traces', astar.traces)
print('chem', astar.ReconstruireChemin())
'''
