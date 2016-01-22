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
# un joueur courant est choisi et la phase est initialisée$
class Labyrinthe():
	def __init__(self,nbJoueurs,nbTresors=24, nbTresorMax=4):
		self.nbTresors = nbTresors
		self.nbTresorMax = nbTresorMax
		self.joueurs = Joueurs(nbJoueurs, self.nbTresors, self.nbTresorMax)
		self.nbJoueurs = nbJoueurs
		self.plateau = Matrice(7, 7)
		
		# Initialisation des joueurs aux 4 coins du jeu
		if self.getNbJoueurs() > 1 and self.getNbJoueurs() < 5:
			self.joueurs.listeJoueurs[0].setPosition((0,0))
			self.joueurs.listeJoueurs[1].setPosition((0,6))
			if self.getNbJoueurs() >= 3:
				self.joueurs.listeJoueurs[2].setPosition((6,0))
			if self.getNbJoueurs() == 4:
				self.joueurs.listeJoueurs[3].setPosition((6,6))

		self.tresors = [i for i in range(self.nbTresors)]
		self.tresorsPos = {}


		# initialisation des cartes fixes
		self.pions = [x for x in range(self.getNbJoueurs())]
		#ligne 1
		self.plateau.setVal(0,0,Carte(True,False,False,True,0,[1]))
		self.plateau.setVal(0,2,Carte(True,False,False,False,1,[]))
		self.plateau.setVal(0,4,Carte(True,False,False,False,2,[]))
		self.plateau.setVal(0,6,Carte(True,True,False,False,0,[2]))
		#ligne 2
		self.plateau.setVal(2,0,Carte(False,False,False,True,3,[]))
		self.plateau.setVal(2,2,Carte(False,False,False,True,4,[]))
		self.plateau.setVal(2,4,Carte(True,False,False,False,5,[]))
		self.plateau.setVal(2,6,Carte(False,True,False,False,6,[]))
		#ligne 3
		self.plateau.setVal(4,0,Carte(False,False,False,True,7,[]))
		self.plateau.setVal(4,2,Carte(False,False,True,False,8,[]))
		self.plateau.setVal(4,4,Carte(False,True,False,False,9,[]))
		self.plateau.setVal(4,6,Carte(False,True,False,False,10,[]))
		# ligne 4
		self.plateau.setVal(6,0,Carte(False,False,True,True,0,[3] if self.getNbJoueurs()>=3 else []))
		self.plateau.setVal(6,2,Carte(False,True,False,False,11,[]))
		self.plateau.setVal(6,4,Carte(False,True,False,False,12,[]))
		self.plateau.setVal(6,6,Carte(False,True,True,False,0,[4] if self.getNbJoueurs()==4 else []))



		# remplir plateau avec cartes
		# construire toutes les cartes 
		
		# Création des cartes amovibles

		listeCartesAmovibles,carteAmovible2 = self.creerCartesAmovibles(13)
		k = 0
		for i in range(7):
			for j in range(7):
				if i % 2 == 1:
					self.plateau.setVal(i,j,listeCartesAmovibles[k])
					self.tresorsPos[listeCartesAmovibles[k].getTresor()] = (i,j)
					k+=1
				elif i % 2 == 0 and j % 2 == 1:
					self.plateau.setVal(i,j,listeCartesAmovibles[k])
					self.tresorsPos[listeCartesAmovibles[k].getTresor()] = (i,j)
					k+=1
		self.carteAmovible = Carte(bool(carteAmovible2[0]),bool(carteAmovible2[1]),bool(carteAmovible2[2]),bool(carteAmovible2[3]),0,[])

		# Paramètres
		self.joueurCourant = 1
		self.phaseCourante = 1
		self.directionInterdite = None
		self.rangéeInterdite = None
		
	# retourne la matrice représentant le plateau de jeu
	def getPlateau(self):
		return self.plateau

	# retourne le nombre de joueurs engagés dans la partie
	def getNbJoueurs(self):
		return len(self.joueurs.listeJoueurs)

	# indique quel est le joueur courant (celui qui doit jouer)
	def getJoueurCourant(self):
		return self.joueurCourant

	# change de joueur courant
	def changerJoueurCourant(self):
		self.joueurCourant = 1 if self.joueurCourant == self.nbJoueurs else self.joueurCourant + 1

	# retourne la phase du jeu
	def getPhase(self):
		return self.phaseCourante

	# change la phase de jeu
	def changerPhase(self):
		self.phaseCourante = (self.phaseCourante % 2) + 1

	# indique combien de trésors il reste dans le labyrinthe
	def getNbTresors(self):
		return self.nbTresors

	# retourne la structures qui gèrent les joueurs et leurs trésors
	def getLesJoueurs(self):
		return self.joueurs.listeJoueurs

	# diminue le nombre de trésors de 1
	def decTresor(self):
		self.nbTresors -= 1

	# met à jour la structure qui gère les joueurs en enlevant le trésor qui le joueur
	# courant vient de trouver
	def joueurCourantTrouveTresor(self):
		self.getLesJoueurs()[self.getJoueurCourant()-1].tresorTrouve()
		self.plateau.getVal(self.getCoordonneesJoueurCourant()[0], self.getCoordonneesJoueurCourant()[1]).prendreTresor()
		self.decTresor()

	# retourne le nombre de trésors restant à trouver pour le joueur numJoueur
	def nbTresorsRestantsJoueur(self,numJoueur):
		return self.joueurs.listeJoueurs[numJoueur-1].nbTresorsRestants()

	# enlève le trésor numTresor sur la carte qui se trouve sur la case lin,col du plateau
	# si le trésor ne s'y trouve pas la fonction ne fait rien
	def prendreTresorL(self,lin,col,numTresor):
		if self.plateau.getVal(lin, col).getTresor() == numTresor:
			self.plateau.getVal(lin, col).prendreTresor()

	# enlève le joueur courant de la carte qui se trouve sur la case lin,col du plateau
	# si le joueur ne s'y trouve pas la fonction ne fait rien
	def prendreJoueurCourant(self,lin,col):
		self.prendrePionL(lin, col, self.joueurCourant)

	# pose le joueur courant de la carte qui se trouve sur la case lin,col du plateau
	# si le joueur s'y trouve déjà la fonction ne fait rien
	def poserJoueurCourant(self,lin,col):
		self.poserPionL(lin, col, self.joueurCourant)

	# retourne la carte amovible supplémentaire que le joueur courant doit joueur
	def getCarteAJouer(self):
		return self.carteAmovible

	# fonction utilitaire qui permet de créer les cartes amovibles du jeu en y positionnant
	# aléatoirement nbTresor trésors
	# la fonction retourne la liste, mélangée aléatoirement, des cartes ainsi créées
	def creerCartesAmovibles(self,tresorDebut):
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
			listeCartesAmovibles.append(Carte(bool(murs[0]), bool(murs[1]), bool(murs[2]), bool(murs[3]), (i + tresorDebut) if (i + tresorDebut) < self.nbTresors else 0, []))
			
		carteAmovible = [int(x) for x in "{0:04b}".format(random.randint(1, 3))]
		
		def rand(item):
			return random.randint(0, nbCartes - 1)
		
		return (sorted(listeCartesAmovibles, key = rand), carteAmovible)

	# fonction qui retourne True si le coup proposé correspond au coup interdit
	# elle retourne False sinon
	def coupInterdit(self,direction,rangee):
		return True if ((rangee % 2 == 0) or (self.directionInterdite == direction and self.rangéeInterdite == rangee)) else False
		
	# fonction qui joue la carte amovible dans la direction et sur la rangée passées 
	# en paramètres. Cette fonction
	#      - met à jour le plateau du labyrinthe
	#      - met à jour la carte à jouer
	#      - met à jour la nouvelle direction interdite
	def jouerCarte(self,direction,rangee):
		if direction == 'N':
			self.carteAmovible = self.plateau.decalageColonneEnHaut(rangee,self.carteAmovible)
			self.directionInterdite = 'S'
			self.rangéeInterdite = rangee

		elif direction == 'O':
			self.carteAmovible = self.plateau.decalageLigneAGauche(rangee,self.carteAmovible)
			self.directionInterdite = 'E'
			self.rangéeInterdite = rangee

		elif direction == 'S':
			self.carteAmovible = self.plateau.decalageColonneEnBas(rangee,self.carteAmovible)
			self.directionInterdite = 'N'
			self.rangéeInterdite = rangee

		elif direction == 'E':
			self.carteAmovible = self.plateau.decalageLigneADroite(rangee,self.carteAmovible)
			self.directionInterdite = 'O'
			self.rangéeInterdite = rangee

		else:
			assert('direction inconnue')

	# Cette fonction tourne la carte à jouer dans le sens indiqué 
	# en paramètre (H horaire A antihoraire)
	def tournerCarte(self,sens='H'):
		if (sens == 'H'):
			self.carteAmovible.tournerHoraire()
		elif (sens == 'A'):
			self.carteAmovible.tournerAntiHoraire()
		else:
			assert("sens de rotation inconnu")

	# retourne le numéro du trésor à trouver pour le joueur courant
	def getTresorCourant(self):
		return self.getLesJoueurs()[self.getJoueurCourant()-1].prochainTresor()

	# retourne sous la forme d'un couple (lin,col) la position du trésor à trouver 
	# pour le joueur courant sur le plateau
	def getCoordonneesTresorCourant(self):
		coord = None
		for i in range(self.plateau.getNbLignes()):
			for j in range(self.plateau.getNbColonnes()):
				if self.plateau.getVal(i,j).getTresor() == self.getTresorCourant():
					coord = i,j
		return coord

	# retourne sous la forme d'un couple (lin,col) la position dule joueur courant sur le plateau
	def getCoordonneesJoueurCourant(self):
		coord = None
		for i in range(self.plateau.getNbLignes()):
			for j in range(self.plateau.getNbColonnes()):
				if self.getJoueurCourant() in self.plateau.getVal(i,j).getListePions():
					coord = i,j
		return coord

	# prend le pion numJoueur sur sur la carte se trouvant en position lin,col du plateau
	def prendrePionL(self,lin,col,numJoueur):
		if self.plateau.getVal(lin, col).possedePion(numJoueur):
			self.plateau.getVal(lin, col).prendrePion(numJoueur)

	def mettrePionL(self,x,y,numJoueur):
		self.poserPionL(x,y,numJoueur)

	# pose le pion numJoueur sur sur la carte se trouvant en position lin,col du plateau
	def poserPionL(self,lin,col,joueur):
		self.plateau.getVal(lin, col).poserPion(joueur)

	def accessibleDist(self,linD,colD,linA,colA):
		depart = (linD,colD)
		arrivee = (linA,colA)
		chemin = AStar(self.plateau,depart,arrivee)
		chemin.Calculer()
		return chemin.ReconstruireChemin()




	# exécute une action de jeu de la phase 1
	# si action vaut 'T' => faire tourner la carte à jouer
	# si action est une des lettres N E S O et rangee est un des chiffre 1,3,5 
	# => insèrer la carte à jouer à la direction action sur la rangée rangee
	# le retour de la fonction est un entier qui vaut
	# 0 si l'action demandée était valide et s'est bien effectuée
	# 2 si l'action est interdite car l'opposée de l'action précédente
	# 2 si action et rangee sont des entiers positifs
	# 3 dans tous les autres cas
	def executerActionPhase1(self,action,rangee):
		coderetour = 2
		if not (action == self.directionInterdite and rangee == self.rangéeInterdite):
			if not type(action) == 'int' and not type(rangee) == 'int':
			    if action == 'T':
			    	self.tournerCarte()
			    	coderetour = 0
			    elif action in ['N','E','S','O'] and rangee in [1,3,5] :
		    		self.jouerCarte(action,rangee)
		    		self.changerPhase()
		    		coderetour = 1
			    else:
			    	coderetour = 3
		return coderetour

	# verifie si le joueur courant peut accéder la case ligA,colA
	# si c'est le cas la fonction retourne une liste représentant un chemin possible
	# sinon ce n'est pas le cas, la fonction retourne None
	def accessibleDistJoueurCourant(self, ligA,colA):
		chemin = None
		if self.getCoordonneesJoueurCourant() != None:
			x, y = self.getCoordonneesJoueurCourant()
			chemin = self.accessibleDist(x, y, ligA, colA)
		return chemin

	# vérifie si le le joueur courant vient de trouver un trésor (si oui fait le nécessaire)
	# vérifie si la partie est terminée, si ce n'est pas le cas passe au joueur suivant
	# le retour de la fonction est un entier qui vaut
	# 0 si le joueur courant n'a pas trouvé de trésor
	# 1 si le joueur courant a trouvé un trésor mais la partie n'est pas terminée
	# 2 si le joueur courant a trouvé son dernier trésor (la partie est donc terminée)
	def finirTour(self):
		coderetour = 0
		if self.getCoordonneesJoueurCourant() == self.getCoordonneesTresorCourant():
			self.joueurCourantTrouveTresor()
			if self.joueurs[self.joueurCourant].prochainTresor() == None:
				coderetour = 2
			else:
				self.changerJoueurCourant()
				self.changerPhase()
				coderetour = 1
		else:
			self.changerPhase()
			self.changerJoueurCourant()
			coderetour = 0
		return coderetour


	#-----------------------------------------
	# tests
	#-----------------------------------------