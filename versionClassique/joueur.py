import random

# Structure interne du joueur
# Joueur
# 		{
#			"idJoueur" : int 
#			"trésors" : list
#			"position" : (int, int)
#		}

# attribue effectivement les trésors de manière aléatoire
def initTresor(joueurs, nbTresors, nbTresorMax):
	listeTresorsDejaDistribues = []
	for i in range(1,len(joueurs)+1):
		n = nbTresorMax if nbTresorMax != 0 else (nbTresors // len(joueurs))
		j = 0
		while (j < n):
			idTresorADistribuer = random.randint(1, nbTresors-1)
			if (idTresorADistribuer not in listeTresorsDejaDistribues):
					listeTresorsDejaDistribues.append(idTresorADistribuer)
					joueurs[i-1]["trésors"].append(idTresorADistribuer)
					j += 1

# permet de créer entre deux et quatre joueurs et leur distribue de manière équitable
# les trésors compris entre 1 et nbTresor avec au plus nbMaxTresor chacun
# si nbMaxTresor vaut 0, la fonction distribue le maximum de trésors possible
def Joueurs(nbJoueurs=2, nbTresors=24, nbTresorMax=0):
	listeJoueurs = []
	
	assert(nbJoueurs >= 2 and nbJoueurs <= 4)
	assert(nbTresors > 0)
	assert(nbTresorMax >= 0)
	
	for i in range(1,nbJoueurs+1):
		listeJoueurs.append({
			"idJoueur" : i,
			"trésors" : [],
			"position" : (None, None)
		})
	
	initTresor(listeJoueurs, nbTresors, nbTresorMax)
	return listeJoueurs						

# retourne le numéro du prochain trésor à trouver pour la joueur numJoueur
# None s'il n'y a pas de prochain trésor
def prochainTresor(joueurs,numJoueur):
	if (len(joueurs[numJoueur-1]["trésors"]) <= 0):
		prochain = None
	else:
		prochain = joueurs[numJoueur-1]["trésors"][0]
	return prochain

# retourne le nombre de trésors qu'il reste à trouver pour le joueur numJoueur
def nbTresorsRestants(joueurs,numJoueur):
	nbTres = 0
	for joueur in joueurs:
		if joueur['idJoueur'] == numJoueur:
			nbTres = len(joueur['trésors'])
	
	return nbTres
	
# enlève le trésor courant du joueur numJoueur et retourne le nombre de trésor
# qu'il reste à trouver pour ce joueur
def tresorTrouve(joueurs,numJoueur):
	if (len(joueurs[numJoueur-1]["trésors"]) <= 0):
		nb = None
	else:
		del joueurs[numJoueur-1]["trésors"][0]
		nb = nbTresorsRestants(joueurs, numJoueur)
		
	return nb


'''print(Joueurs())
print(Joueurs(4, 24, 3))
joueurs = Joueurs(4, 24, 3)
print(joueurs)
print(prochainTresor(joueurs, 0))
print(prochainTresor(joueurs, 1))
print(tresorTrouve(joueurs, 0))
print(prochainTresor(joueurs, 0))
print(nbTresorsRestants(joueurs, 0))'''