from carte import *
from matrice import *
from astar import *
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
	
	if 1 < len(joueurs) < 5:
		joueurs[0]['position'] = (0,0)
		joueurs[1]['position'] = (0,6)
		if len(joueurs) >= 3:
			joueurs[2]['position'] = (6,0)
		if len(joueurs) == 4:
			joueurs[3]['position'] = (6,6)

	tresors = [i for i in range(nbTresors)]
	cptTresorsAttr = 0
	def initTresorsCarte(cptTresorsAttr):
		if random.randint(0,6) == 0 and cptTresorsAttr < len(tresors):
			cptTresorsAttr+=1
			return tresors[cptTresorsAttr-1]
		else:
			return 0


	# cartes fixes
	pions = [x for x in range(len(joueurs))]
	#ligne 1
	setVal(plateau,0,0,Carte(True,False,False,True,0,[1]))
	setVal(plateau,0,2,Carte(True,False,False,False,initTresorsCarte(cptTresorsAttr)))
	setVal(plateau,0,4,Carte(True,False,False,False,initTresorsCarte(cptTresorsAttr)))
	setVal(plateau,0,6,Carte(True,True,False,False,0,[2]))
	#ligne 2
	setVal(plateau,2,0,Carte(False,False,False,True,initTresorsCarte(cptTresorsAttr)))
	setVal(plateau,2,2,Carte(False,False,False,True,initTresorsCarte(cptTresorsAttr)))
	setVal(plateau,2,4,Carte(True,False,False,False,initTresorsCarte(cptTresorsAttr)))
	setVal(plateau,2,6,Carte(False,True,False,False,initTresorsCarte(cptTresorsAttr)))
	#ligne 3
	setVal(plateau,4,0,Carte(False,False,False,True,initTresorsCarte(cptTresorsAttr)))
	setVal(plateau,4,2,Carte(False,False,True,False,initTresorsCarte(cptTresorsAttr)))
	setVal(plateau,4,4,Carte(False,True,False,False,initTresorsCarte(cptTresorsAttr)))
	setVal(plateau,4,6,Carte(False,True,False,False,initTresorsCarte(cptTresorsAttr)))
	# ligne 4
	setVal(plateau,6,0,Carte(False,False,True,True,0,[3] if len(joueurs)>=3 else []))
	setVal(plateau,6,2,Carte(False,True,False,False,initTresorsCarte(cptTresorsAttr)))
	setVal(plateau,6,4,Carte(False,True,False,False,initTresorsCarte(cptTresorsAttr)))
	setVal(plateau,6,6,Carte(False,True,True,False,0,[4] if len(joueurs)==3 else []))



	# remplir plateau avec cartes
	# construire toutes les cartes 
	
	listeCartesAmovibles,carteAmovible2 = creerCartesAmovibles(cptTresorsAttr,nbTresors)
	k = 0
	for i in range(7):
		for j in range(7):
			if i%2==1:
				setVal(plateau,i,j,listeCartesAmovibles[k])
				k+=1
			elif i%2 == 0 and j%2==1:
				setVal(plateau,i,j,listeCartesAmovibles[k])
				k+=1
	carteAmovible = Carte(carteAmovible2[0],carteAmovible2[1],carteAmovible2[2],carteAmovible2[3])
	#print('carteAmovible',carteAmovible)
	#print('affiche plateau')
	#afficheMatrice(plateau)
	joueurCourant = 1
	phaseCourante = 1
		
	return {"joueurs" : joueurs, "nbJoueurs" : len(joueurs), "plateau" : plateau, "trésors" : tresors, "nbTrésors" : len(tresors), "joueurCourant" : joueurCourant, "phaseCourante" : phaseCourante, "carteAmovible" : carteAmovible, "directionInterdite" : None}

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
	tresorTrouve(getLesJoueurs(labyrinthe), getJoueurCourant(labyrinthe)["idJoueur"])
	prendreTresor(getVal(labyrinthe, getJoueurCourant(labyrinthe)["position"][0], getJoueurCourant(labyrinthe)["position"][1]))

# retourne le nombre de trésors restant à trouver pour le joueur numJoueur
def nbTresorsRestantsJoueur(labyrinthe,numJoueur):
	return nbTresorsRestants(getLesJoueurs(labyrinthe), numJoueur)

# enlève le trésor numTresor sur la carte qui se trouve sur la case lin,col du plateau
# si le trésor ne s'y trouve pas la fonction ne fait rien
def prendreTresorL(labyrinthe,lin,col,numTresor):
	#print('coucou',getVal(labyrinthe['plateau'], lin, col))
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
	nbCartes = 34
	listeCartesAmovibles = []
	carteAmovible = None
	
	# les cartes amovibles aléatoires doivent respecter les règles suivantes
	# pas de cartes à 4 murs
	# pas de cartes à 0 murs
	# donc les cartes doivent avoir entre 1 et 3 murs
	
	# on va initialiser de façon aléatoire les murs grace à une conversion d'entier décimaux en binaire
	# en sachant que 0 correspond à un passage et 1 un mur 
	# alors on peut générer un entier aléatoire compris entre 1 et 14 inclus (1 = 0001b et 14 = 1110b)
	# et utiliser ses bits pour initialiser les murs de la carte
	
	for i in range(nbCartes):
		
		r = random.randint(1, 12)
		
		# 7 = 0111b, 11 = 1011b
		while r == 7 or r == 11:
			r = random.randint(1, 12)
			
		murs_s = "{0:04b}".format(r)
		murs = [int(x) for x in murs_s]
		listeCartesAmovibles.append(Carte(bool(murs[0]), bool(murs[1]), bool(murs[2]), bool(murs[3]), (i + tresorDebut) if (i + tresorDebut) < nbTresors else 0))
		
	carteAmovible = [int(x) for x in "{0:04b}".format(random.randint(1, 3))]
	
	def rand(item):
		return random.randint(0, nbCartes - 1)
	
	return (sorted(listeCartesAmovibles, key = rand), carteAmovible)

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
	return labyrinthe["trésors"][getTresorCourant(labyrinthe)]

# retourne sous la forme d'un couple (lin,col) la position dule joueur courant sur le plateau
def getCoordonneesJoueurCourant(labyrinthe):
	return getLesJoueurs(labyrinthe)[labyrinthe["joueurCourant"]]["position"]

# prend le pion numJoueur sur sur la carte se trouvant en position lin,col du plateau
def prendrePionL(labyrinthe,lin,col,numJoueur):
	if possedePion(getVal(labyrinthe['plateau'], lin, col), numJoueur):
		prendrePion(getVal(labyrinthe['plateau'], lin, col), numJoueur)

# pose le pion numJoueur sur sur la carte se trouvant en position lin,col du plateau
def poserPionL(labyrinthe,lin,col,joueur):
	if possedePion(getVal(labyrinthe['plateau'], lin, col), joueur):
		poserPion(getVal(labyrinthe['plateau'], lin, col), joueur)

def accessibleDist(labyrinthe,linD,colD,linA,colA):
	depart = (linD,colD)
	arrivee = (linA,colA)
	chemin = AStar(labyrinthe['plateau'],depart,arrivee)
	print(chemin)
	return chemin




# exécute une action de jeu de la phase 1
# si action vaut 'T' => faire tourner la carte à jouer
# si action est une des lettres N E S O et rangee est un des chiffre 1,3,5 
# => insèrer la carte à jouer à la direction action sur la rangée rangee
# le retour de la fonction est un entier qui vaut
# 0 si l'action demandée était valide et s'est bien effectuée
# 2 si l'action est interdite car l'opposée de l'action précédente
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
		    		changerPhase(labyrinthe)
		    		return 1
		    else:
		    	assert('action inconnue')
		    	return 3
	else:
		return 2

# verifie si le joueur courant peut accéder la case ligA,colA
# si c'est le cas la fonction retourne une liste représentant un chemin possible
# sinon ce n'est pas le cas, la fonction retourne None
def accessibleDistJoueurCourant(labyrinthe, ligA,colA):
     return accessibleDist(labyrinthe,getLesJoueurs(labyrinthe)[getJoueurCourant(labyrinthe)]['position'][0],getLesJoueurs(labyrinthe)[getJoueurCourant(labyrinthe)]['position'][1],ligA,colA)

# vérifie si le le joueur courant vient de trouver un trésor (si oui fait le nécessaire)
# vérifie si la partie est terminée, si ce n'est pas le cas passe au joueur suivant
# le retour de la fonction est un entier qui vaut
# 0 si le joueur courant n'a pas trouvé de trésor
# 1 si le joueur courant a trouvé un trésor mais la partie n'est pas terminée
# 2 si le joueur courant a trouvé son dernier trésor (la partie est donc terminée)
def finirTour(labyrinthe):
    if prochainTresor(labyrinthe['joueurs'],labyrinthe['joueurCourant']) == None:
    	return 2
    #if 


#-----------------------------------------
# tests
#-----------------------------------------