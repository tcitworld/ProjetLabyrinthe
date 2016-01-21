import random

# classe représentant un joueur
class Joueur(object):
	def __init__(self):
		self.tresors = []
		self.position = (None, None)
	#
	# Retourne la liste des trésors pour un joueur.
	# @return [int]
	#
	def getTresors(self):
		return self.tresors

	#
	# Retourne le tuple position pour un joueur.
	# @return (int,int)
	#
	def getPosition(self):
		return self.position
	
	#
	# Ajoute un trésor à la liste des trésors d'un joueur.
	# @param int tresor
	#
	def setTresor(self, tresor):
		self.tresors.append(tresor)
	
	#
	# Change la position d'un joueur.
	# @param (int,int) 
	#
	def setPosition(self, position):
		self.position = position
	
	#
	# Retourne le prochain trésor pour un joueur.
	# @return int
	#
	def prochainTresor(self):
		prochain = None
		
		if len(self.tresors) > 0:
			prochain = self.tresors[0]
		
		return prochain
	
	#
	# Retourne le nombre de trésors restants pour un joueur.
	# @return int
	#

	def nbTresorsRestants(self):
		return len(self.tresors)
	
	#
	# Supprime le trésor à trouver et renvoie le nombre de trésor restant
	# @return None|int
	#

	def tresorTrouve(self):
		nb = None
		
		if len(self.tresors) > 0:
			del self.tresors[0]
			nb = self.nbTresorsRestants()

		return nb
	
			
# classe permettant d'initialiser et de maintenir une liste de joueurs
class Joueurs(object):
	def __init__(self, nbJoueurs = 2, nbTresors = 24, nbTresorMax = 0):
		assert(nbJoueurs >= 2 and nbJoueurs <= 4)
		assert(nbTresors > 0)
		assert(nbTresorMax >= 0)
		
		self.listeJoueurs = []
		self.nbJoueurs = nbJoueurs
		self.nbTresors = nbTresors
		self.nbTresorMax = nbTresorMax
		
		for i in range(nbJoueurs):
			self.listeJoueurs.append(Joueur())
		
		self.initTresor()
	
	#
	# Initie les trésors sur les joueurs
	#
	def initTresor(self):
		listeTresorsDejaDistribues = set()
		for i in range(self.nbJoueurs):
			n = self.nbTresorMax if self.nbTresorMax != 0 else (self.nbTresors // len(self.listeJoueurs))
			j = 0
			while (j < n):
				idTresorADistribuer = random.randint(0, self.nbTresors - 1)
				if (idTresorADistribuer not in listeTresorsDejaDistribues):
					listeTresorsDejaDistribues.add(idTresorADistribuer)
					self.listeJoueurs[i].setTresor(idTresorADistribuer)
					j += 1