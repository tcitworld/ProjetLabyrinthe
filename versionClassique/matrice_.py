import random

#-----------------------------------------
# contructeur et accesseurs
#-----------------------------------------

#crée une matrice de nbLignes lignes sur nbColonnes colonnes en mettant valeurParDefaut
# dans chacune des cases
def Matrice(nbLignes,nbColonnes,valeurParDefaut=0):
	donnees = []
	for i in range(nbLignes):
		donnees.append([valeurParDefaut] * nbColonnes)
			
	return {"nbLignes" : nbLignes, "nbColonnes": nbColonnes, "donnees" : donnees}

# retourne le nombre de ligne de la matrice
def getNbLignes(matrice):
	return matrice["nbLignes"]

#retourne le nombre de colonnes de la matrice
def getNbColonnes(matrice):
	return matrice["nbColonnes"]

# retourne la valeur qui se trouve à la ligne et la colonne passées en paramètres
def getVal(matrice,ligne,colonne):
	assert(ligne >= 0 and ligne < getNbLignes(matrice) and colonne >= 0 and colonne < getNbColonnes(matrice))
	return matrice["donnees"][ligne][colonne]


# place la valeur à l'emplacement ligne colonne de la matrice
def setVal(matrice,ligne,colonne,valeur):
	assert(ligne >= 0 and ligne < getNbLignes(matrice) and colonne >= 0 and colonne < getNbColonnes(matrice))
	matrice["donnees"][ligne][colonne] = valeur
	
	



#------------------------------------------        
# decalages A IMPLEMENTER
#------------------------------------------

# decale la ligne numLig d'une case vers la gauche en insérant la nouvelleValeur
# dans la case ainsi libérée
# la fonction retourne la valeur de la case "ejectée" par le décalage
def decalageLigneAGauche(matrice, numLig, nouvelleValeur=0):
	
	#on sauvegarde la valeur éjectée
	valeurEjectee = getVal(matrice, numLig, 0)
	
	#on effectue le décalage vers la gauche
	for i in range(1, getNbColonnes(matrice)):
		setVal(matrice, numLig, i - 1, getVal(matrice, numLig, i))
		
	#on insère la nouelle valeur
	setVal(matrice, numLig, getNbColonnes(matrice) - 1, nouvelleValeur)
	
	return valeurEjectee

# decale la ligne numLig d'une case vers la droite en insérant la nouvelleValeur
# dans la case ainsi libérée
# la fonction retourne la valeur de la case "ejectée" par le décalage
def decalageLigneADroite(matrice, numLig, nouvelleValeur=0):
	valeurEjectee = getVal(matrice, numLig, getNbColonnes(matrice) - 1)
	
	for i in range(getNbColonnes(matrice) - 1):
		setVal(matrice, numLig, i + 1, getVal(matrice, numLig, i))
		
	setVal(matrice, numLig, 0, nouvelleValeur)
	return valeurEjectee

# decale la colonne numCol d'une case vers le haut en insérant la nouvelleValeur
# dans la case ainsi libérée
# la fonction retourne la valeur de la case "ejectée" par le décalage
def decalageColonneEnHaut(matrice, numCol, nouvelleValeur=0):
	valeurEjectee = getVal(matrice, 0, numCol)
	
	for i in range(1, getNbLignes(matrice)):
		setVal(matrice, i - 1, numCol, getVal(matrice, i, numCol))
		
	setVal(matrice, getNbLignes(matrice) - 1, numCol, nouvelleValeur)
	return valeurEjectee


# decale la colonne numCol d'une case vers le haut en insérant la nouvelleValeur
# dans la case ainsi libérée
# la fonction retourne la valeur de la case "ejectée" par le décalage
def decalageColonneEnBas(matrice, numCol, nouvelleValeur=0):
	valeurEjectee = getVal(matrice, getNbLignes(matrice) - 1, numCol)
	
	for i in range(getNbLignes(matrice) - 1):
		setVal(matrice, i + 1, numCol, getVal(matrice, i, numCol))
		
	setVal(matrice, 0, numCol, nouvelleValeur)
	return valeurEjectee


#-----------------------------------------
# entrées sorties
#-----------------------------------------
#sauvegarde une matrice en mode texte 
# ATTENTION NE MARCHE QUE POUR DES MATRICE CONTENANT DES TYPES SIMPLES
def sauveMatrice(matrice,nomFic):
    fic=open(nomFic,'w')
    ligne=str(getNbLignes(matrice))+','+str(getNbColonnes(matrice))+'\n'
    fic.write(ligne)
    for i in range(getNbLignes(matrice)):
        ligne=''
        for j in range(getNbColonnes(matrice)-1):
            val=getVal(matrice,i,j)
            if val==None:
                ligne+=','
            else:
                ligne+=str(val)+','
        val=getVal(matrice,i,j+1)
        if val==None:
            ligne+='\n'
        else:
            ligne+=str(val)+'\n'
        fic.write(ligne)
    fic.close()

# construit une matrice à partir d'un fichier texte 
# ATTENTION NE MARCHE QUE POUR DES MATRICE CONTENANT DES TYPES SIMPLES
def chargeMatrice(nomFic,typeVal='int'):
    fic=open(nomFic,'r')
    ligneLinCol=fic.readline()
    listeLinCol=ligneLinCol.split(',')
    matrice=Matrice(int(listeLinCol[0]),int(listeLinCol[1]))
    i=0
    for ligne in fic:
        listeVal=ligne.split(",")
        j=0
        for elem in listeVal:
            if elem=="" or elem=="\n":
                setVal(matrice,i,j,None)
            elif typeVal=='int':
                setVal(matrice,i,j,int(elem))
            elif typeVal=='float':
                setVal(matrice,i,j,float(elem))
            elif typeVal=='bool':
                setVal(matrice,i,j,bool(elem))
            else:
                matrice.setVal(i,j,elem)
            j+=1
        i+=1
    return matrice

# fonction utilitataire
def afficheLigneSeparatrice(matrice,tailleCellule=4):
    print()
    for i in range(getNbColonnes(matrice)+1):
        print('-'*tailleCellule+'+',end='')
    print()

# fonction d'affichage d'une matrice
def afficheMatrice(matrice,tailleCellule=4):
    nbColonnes=getNbColonnes(matrice)
    nbLignes=getNbLignes(matrice)
    print(' '*tailleCellule+'|',end='')
    for i in range(nbColonnes):
        print(str(i).center(tailleCellule)+'|',end='')
    afficheLigneSeparatrice(matrice,tailleCellule)
    for i in range(nbLignes):
        print(str(i).rjust(tailleCellule)+'|',end='')
        for j in range(nbColonnes):
            print(str(getVal(matrice,i,j)).rjust(tailleCellule)+'|',end='')
        afficheLigneSeparatrice(matrice,tailleCellule)
    print()
    

#-----------------------------------------
# tests
#-----------------------------------------
'''mat = Matrice(7, 8)
afficheMatrice(mat)
print(getNbColonnes(mat))
print(getNbLignes(mat))
setVal(mat, 1, 1, 8)
print(getVal(mat, 1, 1))
afficheMatrice(mat)'''