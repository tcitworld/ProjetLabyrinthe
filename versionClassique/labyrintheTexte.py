from labyrinthe import *
from ansiColor import *
import sys
import time

# création d'une vue de labyrinthe en mode texte
def LabyrintheTexte():
    return {"labyrinthe":None}

# association d'un jeu de labyrinthe à la vue mode texte
def setLabyrinthe(lmt,labyrinthe):
    lmt["labyrinthe"]=labyrinthe

# retourne le labyrinthe associé à la vue mode texte
def getLabyrinthe(lmt):
    return lmt["labyrinthe"]

# affiche une carte du labyrinthe
def afficheCarte(lmt, carte,pion=1,tresor=-1):
        coulFond=NORMAL
        coulCar=NORMAL
        style=AUCUN
        if getTresor(carte)==tresor:
            coulFond=GRIS
            coulCar=NOIR
        lesPions=getListePions(carte)
        if len(lesPions)>0:
            if len(lesPions)>1:
                style=GRAS
            if possedePion(carte,pion):
                coulCar=pion
            else:  
                coulCar=lesPions[0]
        pcouleur(toChar(carte),coulCar,coulFond,style)
 
# affiche le labyrinthe en mode texte
# le message passé en paramètre sera affiché au dessus du plateau
def afficheLabyrinthe(lmt,message="",sauts=0):
    clearscreen();
    print(message)
    print('Cartes restantes :',end='')
    labyrinthe=getLabyrinthe(lmt)
    for i in range(1,getNbJoueurs(labyrinthe)+1):
        pcouleur('Joueur '+str(i)+' '+str(nbTresorsRestantsJoueur(labyrinthe,i))+' ',i)
    print()
    print("C'est au tour du ",end='')
    pcouleur('Joueur '+str(getJoueurCourant(labyrinthe))+ " de jouer",getJoueurCourant(labyrinthe))
    print()
    tresor=getTresorCourant(labyrinthe)
    print("Le trésor recherché est :",tresor, "caché ",end='')
    coord=getCoordonneesTresorCourant(labyrinthe)
    if coord==None:
        print("sur la carte à jouer")
    else:
        print("en",coord)
    print()
    print(' ',sep='',end='')
    plateau=getPlateau(labyrinthe)
    remplissage=' '*30
    print(remplissage,end='')
    for i in range(1,7,2):
        print(" "+str(i),sep='',end='')
    print()
    for i in range(getNbLignes(plateau)):
        print(remplissage,end='')            
        if i%2==0:
            print(' ',sep='',end='')
        else:
            print(str(i),sep='',end='')
        for j in range(getNbColonnes(plateau)):
            afficheCarte(lmt,getVal(plateau,i,j),getJoueurCourant(labyrinthe),tresor)
        if i%2==0:
            print(' ',sep='',end='')
        else:
            print(str(i),sep='',end='')            
        print()
    print(' ',sep='',end='')
    print(remplissage,end='')        
    for i in range(1,7,2):
        print(" "+str(i),sep='',end='')
    print()
    print("Carte à jouer: ",end='')
    afficheCarte(lmt,getCarteAJouer(labyrinthe),tresor)
    for i in range(sauts):
        print()
    print()

# déplace un joueur suvant un chemin passé en paramètre
def animationChemin(lmt,chemin, joueur,pause=0.1):
    (xp,yp)=chemin.pop(0)
    for (x,y) in chemin:
        prendrePionL(getLabyrinthe(lmt),xp,yp,joueur)
        poserPionL(getLabyrinthe(lmt),x,y,joueur)
        afficheLabyrinthe(lmt,sauts=1)
        time.sleep(pause)
        xp,yp=x,y
    return xp,yp

# -------------------------------------------
# fonctions de saisie des actions des joueurs
# ces fonctions sont à  implémenter
# -------------------------------------------

# permet de saisir soit l'ordre de tourner la carte à jouer
#                  soit l'ordre d'insérer la carte à jouer
# la fonction vérifie la validité de l'ordre. On ne sort de la fonction que si
# l'ordre est valide et on retourne cet ordre sous la forme d'un couple (x,y)
# où x est un caractère valant un des cinq caractères 'T','N','E','S','O'
# dans le cas où x vaut 'T' la valeur de y n'est pas utilisée,
# dans le cas où x vaut une des quatre autres valeur, y doit valoir 1, 3 ou 5
# c'est à dire le numéro de la ligne ou de la colonne où insérer la carte
def saisirOrdre(lmt):
    pass
 
# permet de saisir les coordonées de la case de destination choisie par le joueur courant
# on ne sort de la fonction qui ces coordonées sont valides et que le déplacement est possible
# la fonction retourne le chemin entre la case où se trouve le joueur courant et la case de 
# destination qu'il a choisi
def saisirDeplacement(lmt):
    pass
        
# demarre la partie en mode texte
def demarrer(lmt):
    afficheLabyrinthe(lmt)
    labyrinthe=getLabyrinthe(lmt)
    fini=False
    while not fini:
        while(getPhase(labyrinthe)==1):
            x,y=saisirOrdre(lmt)
            res=executerActionPhase1(labyrinthe,x,y)
            if res==0:
                message="La carte a été tournée"
            elif res==1:
                message="La carte a bien été insérée"
            elif res==2:
                message="Ce coup est interdit car l'opposé du précédent"
            elif res==3:
                message="Vous devez insérer la carte avant de vous déplacer"
            else:
                afficheLabyrinthe(lmt,"Veuillez soit tourner la carte soit l'insérer")    
            afficheLabyrinthe(lmt,message)
            
        chemin=saisirDeplacement(lmt)
        jc=getJoueurCourant(labyrinthe)
        xA,yA=animationChemin(lmt,chemin,jc)
        t=getTresorCourant(labyrinthe)
        res2=finirTour(labyrinthe)
        message=""
        if res2==2:
            message="Le joueur "+str(jc)+" a gagné"
            fini=True
        elif res2==1:
            message="Le joueur "+str(jc)+" vient de trouver le trésor "+str(t)
        afficheLabyrinthe(lmt,message)

    print("Merci au revoir")


# programme principal
print("Bienvenue dans le jeu du labyrinthe")
# saisie du nombre de joueurs
nbJoueurs=input("Combien de joueurs? ")
while nbJoueurs not in ['1','2','3','4']:
    print("Le nombre de joueurs doit être compris entre 1 et 4")
    nbJoueurs=input("Combien de joueurs? ")

# saisie du nombre de trésors par joueur
nbTresors=input("Combien de trésors à trouver par joueur (0 pour le maximum possible)?")
ok=True
try:
    nbTresorsInt=int(nbTresors)
except:
    nbTresorsInt=0
    print("Le nombre maximum de trésor a été choisi")
#initialisation du labyrinthe
l=Labyrinthe(int(nbJoueurs),nbTresorMax=nbTresorsInt)
#initialisation de l'affichage
g=LabyrintheTexte(l)
#démarrage de la partie
demarrer(g)
