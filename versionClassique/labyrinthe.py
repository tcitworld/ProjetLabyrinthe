from carte import *
from matrice import *
from joueur import *
import random
import os

'''
structure labyrinthe
dictionnaire
	"joueurs" : liste des joueurs
	"nbJoueurs" : nombre de joueurs
	"plateau" : matrice du plateau
	"trésors" : liste des trésors
	"nbTrésors" : nombre de trésors sur le plateau
	"joueurCourant" : joueur courant
	"phaseCourante" : phase courante
	"carteAmovible" : la carte amovible
	"directionInterdite" : direction interdite
	"rangéeInterdite" : rangée interdite si direction interdite
'''


# permet de créer un labyrinthe avec nbJoueurs joueurs, nbTresors trésors
# chacun des joueurs aura au plus nbTresorMax à trouver
# si ce dernier paramètre est à 0, on distribuera le maximum de trésors possible 
# à chaque joueur en restant équitable
# un joueur courant est choisi et la phase est initialisée
def Labyrinthe(nbJoueurs=2,nbTresors=24, nbTresorMax=0):
	joueurs = Joueurs(nbJoueurs, nbTresors, nbTresorMax)
	plateau = Matrice(7, 7)
	
	tresors = [i for i in range(nbTresors)]
	cptTresorsAttr = 0
	def initTresorsCarte():
		if random.randint(0,11) == 0 and cptTresorsAttr < len(tresors):
			cptTresorsAttr+=1
			return tresors[cptTresorsAttr-1]


	# cartes fixes
	pions = [x for x in range(len(joueurs))]
	#ligne 1
	setVal(plateau,0,0,Carte(1,0,0,1,0,[1]))
	setVal(plateau,0,2,Carte(1,0,0,0,initTresorsCarte()))
	setVal(plateau,0,4,Carte(1,0,0,0,initTresorsCarte()))
	setVal(plateau,0,6,Carte(1,1,0,0,0,[2]))
	#ligne 2
	setVal(plateau,2,0,Carte(0,0,0,1,initTresorsCarte()))
	setVal(plateau,2,2,Carte(0,0,0,1,initTresorsCarte()))
	setVal(plateau,2,4,Carte(1,0,0,0,initTresorsCarte()))
	setVal(plateau,2,6,Carte(0,1,0,0,initTresorsCarte()))
	#ligne 3
	setVal(plateau,4,0,Carte(0,0,0,1,initTresorsCarte()))
	setVal(plateau,4,2,Carte(0,0,1,0,initTresorsCarte()))
	setVal(plateau,4,4,Carte(0,1,0,0,initTresorsCarte()))
	setVal(plateau,4,6,Carte(0,1,0,0,initTresorsCarte()))
	# ligne 4
	setVal(plateau,6,0,Carte(0,1,0,1,0,[3] if len(joueurs)>=3 else []))
	setVal(plateau,6,2,Carte(0,1,0,0,initTresorsCarte()))
	setVal(plateau,6,4,Carte(0,1,0,0,initTresorsCarte()))
	setVal(plateau,6,6,Carte(0,1,1,0,0,[4] if len(joueurs)==3 else []))



	# remplir plateau avec cartes
	# construire toutes les cartes 
	
	creerCartesAmovibles(cptTresorsAttr,nbTresors)
	
	joueurCourant = 1
	phaseCourante = 1
		
	return {"joueurs" : joueurs, "nbJoueurs" : len(joueurs), "plateau" : plateau, "trésors" : tresors, "nbTrésors" : len(tresors), "joueurCourant" : joueurCourant, "phaseCourante" : phaseCourante}

# retourne la matrice représentant le plateau de jeu
def getPlateau(labyrinthe):
	return labyrinthe["plateau"]

# retourne le nombre de joueurs engagés dans la partie
def getNbJoueurs(labyrinthe):
	return len(labyrinthe["joueurs"])

# indique quel est le joueur courant (celui qui doit jouer)
def getJoueurCourant(labyrinthe):
	return labyrinthe["joueurCourant"]

# change de joueur courant
def changerJoueurCourant(labyrinthe):
	labyrinthe["joueurCourant"] = 1 if labyrinthe["joueurCourant"] == labyrinthe["nbJoueurs"] - 1 else labyrinthe["joueurCourant"] + 1

# retourne la phase du jeu
def getPhase(labyrinthe):
	return labyrinthe["phaseCourante"]

# change la phase de jeu
def changerPhase(labyrinthe):
	labyrinthe["phaseCourante"] = (labyrinthe["phaseCourante"] % 2) + 1

# indique combien de trésors il reste dans le labyrinthe
def getNbTresors(labyrinthe):
	return labyrinthe["nbTrésors"]

# retourne la structures qui gèrent les joueurs et leurs trésors
def getLesJoueurs(labyrinthe):
	return labyrinthe["joueurs"]

# diminue le nombre de trésors de 1
def decTresor(labyrinthe):
	labyrinthe["nbTrésors"] -= 1

# met à jour la structure qui gère les joueurs en enlevant le trésor qui le joueur
# courant vient de trouver
def joueurCourantTrouveTresor(labyrinthe):
	pass

# retourne le nombre de trésors restant à trouver pour le joueur numJoueur
def nbTresorsRestantsJoueur(labyrinthe,numJoueur):
	return nbTresorsRestants(getLesJoueurs(labyrinthe), numJoueur)

# enlève le trésor numTresor sur la carte qui se trouve sur la case lin,col du plateau
# si le trésor ne s'y trouve pas la fonction ne fait rien
def prendreTresorL(labyrinthe,lin,col,numTresor):
	if getTresor(getVal(labyrinthe['plateau'], lin, col)) == numTresor:
		prendreTresor(getVal(labyrinthe['plateau'], lin, col))

# enlève le joueur courant de la carte qui se trouve sur la case lin,col du plateau
# si le joueur ne s'y trouve pas la fonction ne fait rien
def prendreJoueurCourant(labyrinthe,lin,col):
	prendrePionL(labyrinthe, lin, col, labyrinthe['joueurCourant'])

# pose le joueur courant de la carte qui se trouve sur la case lin,col du plateau
# si le joueur s'y trouve déjà la fonction ne fait rien
def poserJoueurCourant(labyrinthe,lin,col):
	poserPionL(labyrinthe, lin, col, labyrinthe['joueurCourant'])

# retourne la carte amovible supplémentaire que le joueur courant doit joueur
def getCarteAJouer(labyrinthe):
	return labyrinthe["carteAmovible"]

# fonction utilitaire qui permet de créer les cartes amovibles du jeu en y positionnant
# aléatoirement nbTresor trésors
# la fonction retourne la liste, mélangée aléatoirement, des cartes ainsi créées
def creerCartesAmovibles(tresorDebut,nbTresors):
    pass

# fonction qui retourne True si le coup proposé correspond au coup interdit
# elle retourne False sinon
def coupInterdit(labyrinthe,direction,rangee):
	#return True if rangee % 2 == 0 else False
	return True if ((rangee % 2 == 0) or (labyrinthe['directionInterdite'] == direction and labyrinthe['rangéeInterdite'] == rangee)) else False
	
# fonction qui joue la carte amovible dans la direction et sur la rangée passées 
# en paramètres. Cette fonction
#      - met à jour le plateau du labyrinthe
#      - met à jour la carte à jouer
#      - met à jour la nouvelle direction interdite
def jouerCarte(labyrinthe,direction,rangee):
	if direction == 'N':
		labyrinthe['carteAmovible'] = decalageColonneEnHaut(labyrinthe['plateau'],rangee,labyrinthe['carteAmovible'])
		labyrinthe['directionInterdite'] = 'S'
	elif direction == 'O':
		labyrinthe['carteAmovible'] = decalageLigneAGauche(labyrinthe['plateau'],rangee,labyrinthe['carteAmovible'])
		labyrinthe['directionInterdite'] = 'E'
	elif direction == 'S':
		labyrinthe['carteAmovible'] = decalageColonneEnBas(labyrinthe['plateau'],rangee,labyrinthe['carteAmovible'])
		labyrinthe['directionInterdite'] = 'N'
	elif direction == 'E':
		labyrinthe['carteAmovible'] = decalageLigneADroite(labyrinthe['plateau'],rangee,labyrinthe['carteAmovible'])
		labyrinthe['directionInterdite'] = 'O'
	else:
		assert('direction inconnue')

# Cette fonction tourne la carte à jouer dans le sens indiqué 
# en paramètre (H horaire A antihoraire)
def tournerCarte(labyrinthe,sens='H'):
	if (sens == 'H'):
		tournerHoraire(labyrinthe["carteAmovible"])
	elif (sens == 'A'):
		tournerAntiHoraire(labyrinthe["carteAmovible"])
	else:
		assert("sens de rotation inconnu")

# retourne le numéro du trésor à trouver pour le joueur courant
def getTresorCourant(labyrinthe):
	return prochainTresor(labyrinthe["joueurs"],labyrinthe["joueurCourant"])

# retourne sous la forme d'un couple (lin,col) la position du trésor à trouver 
# pour le joueur courant sur le plateau
def getCoordonneesTresorCourant(labyrinthe):
	return labyrinthe["trésors"][getTresorCourant(labyrinthe)]["position"]

# retourne sous la forme d'un couple (lin,col) la position dule joueur courant sur le plateau
def getCoordonneesJoueurCourant(labyrinthe):
	return getLesJoueurs(labyrinthe)[labyrinthe["joueurCourant"]]["position"]

# prend le pion numJoueur sur sur la carte se trouvant en position lin,col du plateau
def prendrePionL(labyrinthe,lin,col,numJoueur):
	if possedePion(getVal(labyrinthe['plateau'], lin, col), numJoueur):
		prendrePion(getVal(labyrinthe['plateau'], lin, col), numJoueur)

# pose le pion numJoueur sur sur la carte se trouvant en position lin,col du plateau
def poserPionL(labyrinthe,lin,col,joueur):
	if possedePion(getVal(labyrinthe['plateau'], lin, col), numJoueur):
		poserPion(getVal(labyrinthe['plateau'], lin, col), numJoueur)
	
# indique si il y a un chemin entre la case ligD,colD et la case ligA,colA du labyrinthe
def accessible(labyrinthe,ligD,colD,ligA,colA):
    pass

# indique si il y a un chemin entre la case ligD,colD et la case ligA,colA du labyrinthe
# mais la valeur de retour est None s'il n'y a pas de chemin, sinon c'est un chemin possible entre ces deux cases
def accessibleDist(labyrinthe,ligD,colD,ligA,colA):
    if not accessible(labyrinthe,ligD,colD,ligA,colA):
    	return None
    else:
    	pass

# exécute une action de jeu de la phase 1
# si action vaut 'T' => faire tourner la carte à jouer
# si action est une des lettres N E S O et rangee est un des chiffre 1,3,5 
# => insèrer la carte à jouer à la direction action sur la rangée rangee
# le retour de la fonction est un entier qui vaut
# 0 si l'action demandée était valide et s'est bien effectuée
# 1 si l'action est interdite car l'opposée de l'action précédente
# 2 si action et rangee sont des entiers positifs
# 3 dans tous les autres cas
def executerActionPhase1(labyrinthe,action,rangee):
	if action != labyrinthe['directionInterdite']:
		if type(action) == 'int' and type(rangee) == 'int':
			return 2
		else:
		    if action == 'T':
		    	tournerCarte(labyrinthe)
		    	return 0
		    elif action in ['N','E','S','O'] and rangee in [1,3,5] :
		    		jouerCarte(labyrinthe,action,rangee)
		    		return 0
		    else:
		    	assert('action inconnue')
		    return 3
	else:
		return 1

# verifie si le joueur courant peut accéder la case ligA,colA
# si c'est le cas la fonction retourne une liste représentant un chemin possible
# sinon ce n'est pas le cas, la fonction retourne None
def accessibleDistJoueurCourant(labyrinthe, ligA,colA):
    pass

# vérifie si le le joueur courant vient de trouver un trésor (si oui fait le nécessaire)
# vérifie si la partie est terminée, si ce n'est pas le cas passe au joueur suivant
# le retour de la fonction est un entier qui vaut
# 0 si le joueur courant n'a pas trouvé de trésor
# 1 si le joueur courant a trouvé un trésor mais la partie n'est pas terminée
# 2 si le joueur courant a trouvé son dernier trésor (la partie est donc terminée)
def finirTour(labyrinthe):
    pass
    

#-----------------------------------------
# tests
#-----------------------------------------