import random

#-----------------------------------------
# contructeur et accesseurs
#-----------------------------------------

#crée une matrice de nbLignes lignes sur nbColonnes colonnes en mettant valeurParDefaut
# dans chacune des cases
def Matrice(nbLignes,nbColonnes,valeurParDefaut=0):
    taille=nbLignes*nbColonnes
    liste=[]
    for i in range(taille):
        liste.append(valeurParDefaut)
        matrice={'Lignes':nbLignes,'Colonnes':nbColonnes,'valeurs': liste}
    return matrice
#print(Matrice(7,7,0))
    

# retourne le nombre de ligne de la matrice
def getNbLignes(matrice):
    NbLignes=matrice['Lignes']
    return NbLignes

#print(getNbLignes(Matrice(7,7,0)))
    
    

#retourne le nombre de colonnes de la matrice
def getNbColonnes(matrice):
    NbColonnes=matrice['Colonnes']
    return NbColonnes
#print(getNbColonnes(Matrice(7,7,0)))

# retourne la valeur qui se trouve à la ligne et la colonne passées en paramètres
def getVal(matrice,ligne,colonne):
    valeur=matrice['valeurs'][(getNbColonnes(matrice)*ligne)+colonne]
    return valeur
#print(getVal(Matrice(7,7,0),2,1))

# place la valeur à l'emplacement ligne colonne de la matrice
def setVal(matrice,ligne,colonne,valeur):
    matrice['valeurs'][(getNbColonnes(matrice)*ligne)+colonne]=valeur
#print(setVal(Matrice(7,7,0),2,1,-1))



# fonction utilitataire
def afficheLigneSeparatrice(matrice,tailleCellule=4):
    print()
    for i in range(getNbColonnes(matrice)+1):
        print('-'*tailleCellule+'+', end="")
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
#afficheMatrice(Matrice(7,7,0),tailleCellule=4)

#------------------------------------------        
# decalages A IMPLEMENTER
#------------------------------------------

# decale la ligne numLig d'une case vers la gauche en insérant la nouvelleValeur
# dans la case ainsi libérée
# la fonction retourne la valeur de la case "ejectée" par le décalage
def decalageLigneAGauche(matrice, numLig, nouvelleValeur=0):
    valeurRecuperee=getVal(matrice,numLig,0)
    for i in range(getNbColonnes(matrice) - 1):
        nouvelleV=getVal(matrice,numLig,i+1)
        setVal(matrice,numLig,i,nouvelleV)
    setVal(matrice,numLig,getNbColonnes(matrice) - 1,nouvelleValeur)
    return valeurRecuperee
        

# dans la case ainsi libérée
# la fonction retourne la valeur de la case "ejectée" par le décalage
def decalageLigneADroite(matrice, numLig, nouvelleValeur=0):
    valeurRecup=getVal(matrice,numLig,getNbColonnes(matrice)-1)
    for i in range(getNbColonnes(matrice)-1,0,-1):
        nouvelleVal=getVal(matrice,numLig,i-1)
        setVal(matrice,numLig,i,nouvelleVal)
    setVal(matrice,numLig,0,nouvelleValeur)
    #print(matrice)#pour voir ma matrice apres le changement
    return valeurRecup


# decale la colonne numCol d'une case vers le haut en insérant la nouvelleValeur
# dans la case ainsi libérée
# la fonction retourne la valeur de la case "ejectée" par le décalage
def decalageColonneEnHaut(matrice, numCol, nouvelleValeur=0):
    valARecup=getVal(matrice,0,numCol)
    for j in range(getNbLignes(matrice)-1):
        nouvelleVal=(getVal(matrice,j+1,numCol))
        setVal(matrice,j,numCol,nouvelleVal)
    setVal(matrice,getNbLignes(matrice)-1,numCol,nouvelleValeur)
    #print(matrice)
    return valARecup



# decale la colonne numCol d'une case vers le haut en insérant la nouvelleValeur
# dans la case ainsi libérée
# la fonction retourne la valeur de la case "ejectée" par le décalage
def decalageColonneEnBas(matrice, numCol, nouvelleValeur=0):
    #afficheMatrice(matrice)
    valeurRecup=getVal(matrice,getNbLignes(matrice)-1,numCol)
    
    for j in range(0,getNbLignes(matrice)-1, 1):
        nouvelleVal= getVal(matrice,j,numCol)
        setVal(matrice,j-1,numCol,nouvelleVal)
        
        
    setVal(matrice,0,numCol,nouvelleValeur)
    return valeurRecup

'''matriceTemp = Matrice(7,7,0)
setVal(matriceTemp,0,1,5)#juste pour tester
afficheMatrice(matriceTemp)

print("decalageLigneAGauche")
print(decalageLigneAGauche(matriceTemp,0,3))
afficheMatrice(matriceTemp)

print("decalageLigneADroite")
print(decalageLigneADroite(matriceTemp,0,6))
afficheMatrice(matriceTemp)

print("decalageColonneEnHaut")
print(decalageColonneEnHaut(matriceTemp,0,9))
afficheMatrice(matriceTemp)

print("decalageColonneEnBas")
print(decalageColonneEnBas(matriceTemp,0,6))    
afficheMatrice(matriceTemp)'''

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
