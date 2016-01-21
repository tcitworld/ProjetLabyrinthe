#-----------------------------------------
# contructeur et accesseurs
#-----------------------------------------

class Matrice(object):
	def __init__(self, nbLignes, nbColonnes, valeurParDefaut = 0):
		taille = nbLignes * nbColonnes
		liste = []
		
		for i in range(taille):
			liste.append(valeurParDefaut)
		
		self.lignes = nbLignes
		self.colonnes = nbColonnes
		self.valeurs = liste.copy() # assure contre la perte du pointeur sur la liste
		
	def getNbLignes(self):
		return self.lignes
	
	def getNbColonnes(self):
		return self.colonnes
		
	def getVal(self, ligne, colonne):
		return self.valeurs[(self.colonnes * ligne) + colonne]
	
	def setVal(self, ligne, colonne, valeur):
		self.valeurs[(self.colonnes * ligne) + colonne] = valeur
		
	def afficheLigneSeparatrice(self, tailleCellule = 4):
		print()
		for i in range(self.getNbColonnes() + 1):
			print('-' * tailleCellule + '+', end = "")
		print()
		
	def afficheMatrice(self, tailleCellule = 4):
		nbCol = self.getNbColonnes()
		nbLig = self.getNbLignes()
		print(' ' * tailleCellule + '|', end = '')
		for i in range(nbCol):
			print(str(i).center(tailleCellule) + '|', end = '')
		self.afficheLigneSeparatrice(tailleCellule)
		for i in range(nbLig):
			print(str(i).rjust(tailleCellule) + '|', end = '')
			for j in range(nbCol):
				print(str(self.getVal(i, j)).rjust(tailleCellule) + '|', end  = '')
			self.afficheLigneSeparatrice(tailleCellule)
		print()
		
	def decalageLigneAGauche(self, numLig, nouvelleValeur = 0):
		valeurEjectee = self.getVal(numLig, 0)
		
		for i in range(self.getNbColonnes() - 1):
			valeurACopier = self.getVal(numLig, i + 1)
			self.setVal(numLig, i, valeurACopier)
		
		self.setVal(numLig, self.getNbColonnes() - 1, nouvelleValeur)
		return valeurEjectee
		
	def decalageLigneADroite(self, numLig, nouvelleValeur = 0):
		valeurEjectee = self.getVal(numLig, self.getNbColonnes() - 1)
		
		for i in range(self.getNbColonnes() - 1, 0, -1):
			valeurACopier = self.getVal(numLig, i - 1)
			self.setVal(numLig, i, valeurACopier)
		
		self.setVal(numLig, 0, nouvelleValeur)
		return valeurEjectee
	
	def decalageColonneEnHaut(self, numCol, nouvelleValeur = 0):
		valeurEjectee = self .getVal(0, numCol)
		
		for i in range(self.getNbLignes() - 1):
			valeurACopier = self.getVal(i + 1, numCol)
			self.setVal(i, numCol, valeurACopier)
		
		self.setVal(self.getNbLignes() - 1, numCol, nouvelleValeur)
		return valeurEjectee
	
	def decalageColonneEnBas(self, numCol, nouvelleValeur = 0):
		valeurEjectee = self.getVal(self.getNbLignes() - 1, numCol)
		
		for i in range(self.getNbLignes() - 1, 0, -1):
			valeurACopier = self.getVal(i - 1, numCol)
			self.setVal(i, numCol, valeurACopier)
		
		self.setVal(0, numCol, nouvelleValeur)
		return valeurEjectee
		
#-----------------------
# TEST
#-----------------------
'''
mat = Matrice(7, 7, 0)
mat.setVal(2, 0, 5)
mat.setVal(1, 0, 7)
mat.setVal(3, 0, 4)
mat.afficheMatrice()
print(mat.getVal(2, 0))
print(mat.getVal(1, 0))
print(mat.getVal(3, 0))
print("mat.decalageLigneAGauche(0, 3)", mat.decalageLigneAGauche(0, 3))
mat.afficheMatrice()
print("mat.decalageLigneADroite(0, 6)", mat.decalageLigneADroite(0, 6))
mat.afficheMatrice()
print("mat.decalageColonneEnHaut(0, 9)", mat.decalageColonneEnHaut(0, 9))
mat.afficheMatrice()
print("mat.decalageColonneEnBas(0, 12)",mat.decalageColonneEnBas(0, 12))
mat.afficheMatrice()
'''