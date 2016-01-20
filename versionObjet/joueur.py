import random

# classe représentant un joueur
class Joueur(object):
	def __init__(self):
		self.tresors = []
		self.position = (None, None)
	
	def getTresors(self):
		return self.tresors
	
	def getPosition(self):
		return self.position
	
	def setTresor(self, tresor):
		print('trésor : ',tresor)
		self.tresors.append(tresor)
	
	def setPosition(self, position):
		self.position = position
	
	def prochainTresor(self):
		prochain = None
		
		if len(self.tresors) > 0:
			prochain = self.tresors[0]
		
		return prochain
	
	def nbTresorsRestants(self):
		return len(self.tresors)
		
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