import random

#-----------------------------------------
# contructeur et accesseurs
#-----------------------------------------

#crée une matrice de nbLignes lignes sur nbColonnes colonnes en mettant valeurParDefaut
# dans chacune des cases
class Matrice(object):
      def __init__(self,nbLignes,nbColonnes,valeurParDefaut=0):
          self.taille=nbLignes*nbColonnes
          liste=[]
          for i in range(self.taille):
              liste.append(valeurParDefaut)
          self.lignes=nbLignes
          self.colonnes=nbColonnes
          self.valeurs=liste
#print(Matrice(7,7,0))
    

# retourne le nombre de ligne de la matrice
      def getNbLignes(self):
          return self.lignes

#print(getNbLignes(Matrice(7,7,0)))
    
    

#retourne le nombre de colonnes de la matrice
      def getNbColonnes(self):
          return self.colonnes
#print(getNbColonnes(Matrice(7,7,0)))

# retourne la valeur qui se trouve à la ligne et la colonne passées en paramètres
      def getVal(self,ligne,colonne):
          valeur=self.valeurs[(self.getNbColonnes()*ligne)+colonne]
          return valeur
#print(getVal(Matrice(7,7,0),2,1))

# place la valeur à l'emplacement ligne colonne de la matrice
      def setVal(self,ligne,colonne,valeur):
          self.valeurs[(self.getNbColonnes()*ligne)+colonne]=valeur
#print(setVal(Matrice(7,7,0),2,1,-1))



# fonction utilitataire
      def afficheLigneSeparatrice(self,tailleCellule=4):
          print()
          for i in range(self.getNbColonnes()+1):
              print('-'*tailleCellule+'+', end="")
          print()

# fonction d'affichage d'une matrice
      def afficheMatrice(self,tailleCellule=4):
          nbColonnes=self.getNbColonnes()
          nbLignes=self.getNbLignes()
          print(' '*tailleCellule+'|',end='')
          for i in range(nbColonnes):
              print(str(i).center(tailleCellule)+'|',end='')
          self.afficheLigneSeparatrice(tailleCellule)
          for i in range(nbLignes):
              print(str(i).rjust(tailleCellule)+'|',end='')
              for j in range(nbColonnes):
                  print(str(self.getVal(i,j)).rjust(tailleCellule)+'|',end='')
              self.afficheLigneSeparatrice(tailleCellule)
          print()
#afficheMatrice(Matrice(7,7,0),tailleCellule=4)

#------------------------------------------        
# decalages A IMPLEMENTER
#------------------------------------------

# decale la ligne numLig d'une case vers la gauche en insérant la nouvelleValeur
# dans la case ainsi libérée
# la fonction retourne la valeur de la case "ejectée" par le décalage
      def decalageLigneAGauche(self, numLig, nouvelleValeur=0):
          valeurRecuperee=self.getVal(numLig,0)
          for i in range(self.getNbColonnes() - 1):
              nouvelleV=self.getVal(numLig,i+1)
              self.setVal(numLig,i,nouvelleV)
          self.setVal(numLig,self.getNbColonnes()- 1,nouvelleValeur)
          return valeurRecuperee
        

# dans la case ainsi libérée
# la fonction retourne la valeur de la case "ejectée" par le décalage
      def decalageLigneADroite(self, numLig, nouvelleValeur=0):
          valeurRecup=self.getVal(numLig,self.getNbColonnes()-1)
          for i in range(self.getNbColonnes()-1,0,-1):
              nouvelleVal=self.getVal(numLig,i-1)
              self.setVal(numLig,i,nouvelleVal)
          self.setVal(numLig,0,nouvelleValeur)
          return valeurRecup


# decale la colonne numCol d'une case vers le haut en insérant la nouvelleValeur
# dans la case ainsi libérée
# la fonction retourne la valeur de la case "ejectée" par le décalage
      def decalageColonneEnHaut(self, numCol, nouvelleValeur=0):
          valARecup=self.getVal(0,numCol)
          for j in range(self.getNbLignes()-1):
              nouvelleVal=(self.getVal(j+1,numCol))
              self.setVal(j,numCol,nouvelleVal)
          self.setVal(self.getNbLignes()-1,numCol,nouvelleValeur)
          return valARecup



# decale la colonne numCol d'une case vers le haut en insérant la nouvelleValeur
# dans la case ainsi libérée
# la fonction retourne la valeur de la case "ejectée" par le décalage
      def decalageColonneEnBas(self, numCol, nouvelleValeur=0):
          valeurRecup=self.getVal(self.getNbLignes()-1,numCol)
          for j in range(0,self.getNbLignes()-1, 1):
              nouvelleVal= self.getVal(j,numCol)
              self.setVal(j-1,numCol,nouvelleVal)
          self.setVal(0,numCol,nouvelleValeur)
          return valeurRecup

matriceTemp = Matrice(7,7,0)
matriceTemp.setVal(0,1,5)#juste pour tester
matriceTemp.afficheMatrice()

print("decalageLigneAGauche")
print(matriceTemp.decalageLigneAGauche(0,3))
matriceTemp.afficheMatrice()

print("decalageLigneADroite")
print(matriceTemp.decalageLigneADroite(0,6))
matriceTemp.afficheMatrice()

print("decalageColonneEnHaut")
print(matriceTemp.decalageColonneEnHaut(0,9))
matriceTemp.afficheMatrice()

print("decalageColonneEnBas")
print(matriceTemp.decalageColonneEnBas(0,6))    
matriceTemp.afficheMatrice()

         