#-------------------------------
# Fichier : 	astar.py
# Fonction : 	implementation de l'algorithme de recherche de chemin
#				ici l'algorithme A* (A Star) a été implementé en raison de ses multiples avantage par rapport
#				à l'algorithme de l'inondation (compléxité en O(b^d), avec b = 4 car il y a au maximum 4 voisins dans notre cas)
#-------------------------------

from matrice import *
from carte import *

# Structure d'un noeud
'''
dict Noeud = {
	"x" : int
	"y" : int
	"poids" : int
	"heuristique" : int
}
'''

# défini un Noeud (utilisé dans l'algoritme A*)
def Noeud(x, y, poids, heuristique):
	return {"x" : x, "y" : y, "poids" : poids, "heuristique" : heuristique}

# renvoie un vecteur directionnel suivant une direction donnée (N = 0, E = 1, S = 2, W = 3)
def GetDir(i):
	dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
	return dirs[i]

# calcul une valeur heuristique entre deux position du plateau (utilisé pour l'algorithme A*)
def Heuristique(n1, n2):
	return abs(n1[0] - n2[0]) + abs(n1[1] - n2[1])

# permet de reconstruire le chemin à partir des traces retenues par l'algorithme A*, les traces sont un dictionnaire dont
# les positions sont les clefs et leur valeur une position ayant un passage commun
def ReconstruireChemin(traces, depart, arrivee):
	courant = arrivee
	chemin_ = [courant]
	
	# tant que la position de départ n'a pas été atteinte on continu de remonter le chemin
	while courant !=  depart:
		courant = traces[courant]
		chemin_.append(courant)

	# on retourne la liste inversée pour obtenir le chemine
	return list(reversed(chemin_))

# permet de rechercher un noeud dans la pile de noeud à traiter
def RechercheNoeudDansPile(pile, pos):
	l = [x for x in pile if (x["x"], x["y"]) == pos]
	
	noeud = None
	
	# si on obtient un élément dans la liste on le retourne
	if len(l) > 0:
		noeud = l[0]
	else: # sinon on retourne un noeud virtuel avec un poids de 0 pour nos calculs d'heuristique
		noeud = Noeud(None, None, 0, None)
	
	return noeud
	
def InsererNoeudDansPile(pile, noeud):
	i = 0
	while i < len(pile) and noeud["heuristique"] < pile[i]["heuristique"]:
		i += 1
		
	pile.insert(i, noeud)
		
# fonction principale executant l'algorithme A* 
def AStar(plateau, depart, arrivee):
	# ensemble des position des cases visitées (on utilise un ensemble car une recherche sur un ensemble est O(1) alors qu'une liste est O(n))
	visites = set()
	# trace des passages visités avec leurs connections
	traces = {}
	
	cheminTrouve = False
	
	# on créer le noeud initial avec la position de départ et on le place sur la pile
	ndep = Noeud(depart[0], depart[1], Heuristique(depart, arrivee), 0)
	pile = [ndep]
	
	# tant que la pile n'est pas vide (un pile vide correspond à tout les points accessibles traités et aucun chemin vers la destination)
	while len(pile) > 0 and not cheminTrouve:
	
		# on récupère et consume le noeud au sommet de notre pile pour le traiter
		courant = pile.pop(0)
		
		# on récupère la position référencée par notre noeud à traiter
		pos_courante = (courant["x"], courant["y"])
		
		# si la position du noeud à traiter correspond à l'objectif on sort car on est assuré d'un chemin (pas forcément le plus court)
		if pos_courante == arrivee:
			cheminTrouve = True
			continue
		
		# on ajoute la position référencée par le noeud en cours de traitement à l'ensemble des noeuds visités
		visites.add(pos_courante)
		
		# on vérifie les quatres cases voisines
		for i in range(4):
			
			# on obtient le vecteur représentant la direction à analyser
			d = GetDir(i)
			
			# position et poids de la case voisine dans la direction recherchée
			pos_v = (pos_courante[0] + d[0], pos_courante[1] + d[1])
			poids_v = courant["poids"] + Heuristique(pos_courante, pos_v)
			
			# on s'assure que la case voisine est dans les bornes du plateau
			if pos_v[0] >= 0 and pos_v[0] < getNbLignes(plateau) and pos_v[1] >= 0 and pos_v[1] < getNbColonnes(plateau):
				# on cherche si un noeud présent dans la pile existe pour notre position
				n = RechercheNoeudDansPile(pile, pos_v)
				
				# si la position à déjà été traitée ou bien que le poids du voisin est supérieur on passe (car le chemin est moins intéressant dû au poids)
				if pos_v in visites and poids_v >= n["poids"]:
					continue
				else:
					passage = False
					
					# on récupère la carte de notre position courante et celle de la case voisine à analyser dans notre plateau
					c_courante = getVal(plateau, pos_courante[0], pos_courante[1])
					c_voisin = getVal(plateau, pos_v[0], pos_v[1])
					
					# vérification d'un passage existant entre ces deux cartes
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
					
					# si un passage existe on effectue le traitement
					if passage:
						# si le poids est intéressant ou que la destination n'a pas encore été traitée
						# on enregistre ce passage dans traces et on créer un nouveau noeud sur la pile pour traitement ultérieurs
						if  poids_v < n["poids"] or pos_v not in [(k["x"], k["y"]) for k in pile]:
							traces[pos_v] = pos_courante
							n2 = Noeud(pos_v[0], pos_v[1], poids_v, poids_v + Heuristique(pos_v, arrivee))
							#pile.append(n2)
							InsererNoeudDansPile(pile, n2)
					else:
						continue
			else: # position en dehors du plateau
				continue
	
	# on renvoie le chemin si il existe
	chemin = None
	if cheminTrouve:
		chemin = ReconstruireChemin(traces, depart, arrivee)
	return chemin
#-------------------------------
# TEST
#-------------------------------

'''
# Fonctions pour tester A*
import random

# fonction utilitataire
def afficheLigneSeparatrice(matrice,tailleCellule=4):
	print()
	for i in range(getNbColonnes(matrice)+1):
		print('-'*tailleCellule+'+', end="")
	print()

# fonction d'affichage d'une matrice modifiée
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

def genereRandomLab():
	plat = Matrice(7,7)
	for i in range(getNbLignes(plat)):
		for j in range(getNbColonnes(plat)):
			setVal(plat, i, j, Carte(bool(random.randint(0, 1)),bool(random.randint(0, 1)),bool(random.randint(0, 1)),bool(random.randint(0, 1)), 0, []))
	return plat

dep = (0, 0)
arr = (6, 6)
chem = None

print('création d\'un labyrinthe valide pour le test en cours ...')
# ensure working path for debugging
while chem == None:
	plat = genereRandomLab()
	chem = AStar(plat, dep, arr)	

drawMat(plat)
print('chem', chem)
'''