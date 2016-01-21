#-------------------------------
# Fichier : 	carte.py
# Fonction : 	implémente la structure des cartes dans le jeu du labyrinthe ainsi que leur gestion
#-------------------------------

import random

'''
structure carte
dictionnaire
	"direction" : list(bool) True == Mur, False == Passage
	"pion" : list de pion (int)
	"tresor" : identifiant trésor (int)
'''

# la liste des caractère semi-graphiques correspondants aux différentes cartes
# l'indice du caractère dans la liste correspond au codage des murs sur la carte
# le caractère 'Ø' indique que l'indice ne correspond pas à une carte
listeCartes=['Ø','╦','╣','╗','╩','═','╝','Ø','╠','╔','║','Ø','╚','Ø','Ø','Ø']
 
# permet de créer une carte:
# les quatre premiers paramètres sont des booléens indiquant s'il y a un mur ou non dans chaque direction
# tresor est le numéro du trésor qui se trouve sur la carte (0 s'il n'y a pas de trésor)
# pions donne la liste des pions qui seront posés sur la carte (un pion est un entier entre 1 et 4)
def Carte( nord, est, sud, ouest, tresor, pions):
    return {'direction':[nord,est,sud,ouest],'tresor':tresor,'pions':pions}
 
# retourne un booléen indiquant si la carte est valide ou non c'est à dire qu'elle a un ou deux murs
def estValide(c):
    return 0 < sum([c['direction'][0],c['direction'][1],c['direction'][2],c['direction'][3]]) <=2
 
# retourne un booléen indiquant si la carte possède un mur au nord
def murNord(c):
    return c['direction'][0]
 
# retourne un booléen indiquant si la carte possède un mur au sud
def murSud(c):
    return c['direction'][2]
 
# retourne un booléen indiquant si la carte possède un mur à l'est
def murEst(c):
    return c['direction'][1]
 
# retourne un booléen indiquant si la carte possède un mur à l'ouest
def murOuest(c):
    return c['direction'][3]
 
# retourne la liste des pions se trouvant sur la carte
def getListePions(c):
    return c['pions']
 
# retourne le nombre de pions se trouvant sur la carte
def getNbPions(c):
    return len(c['pions'])
 
# retourne un booléen indiquant si la carte possède le pion passé en paramètre
def possedePion(c,pion):
    return pion in c['pions']
 
# retourne le codage de la liste des pions
def getPions(c):
    return type(c['pions'])
 
# affecte les pions de la cartes en utilisant directement le codage de la liste des pions
def setPions(c,pions):
    c['pions'] = pions
 
# retourne la valeur du trésor qui se trouve sur la carte (0 si pas de trésor)
def getTresor(c):
    #print('carte',c)
    return c.get('tresor',0)
 
# enlève le trésor qui se trouve sur la carte et retourne la valeur de ce trésor
def prendreTresor(c):
    tresor = c.get('tresor',0)
    c['tresor'] = 0
    return tresor
 
# met le trésor passé en paramètre sur la carte et retourne la valeur de l'ancien trésor
def mettreTresor(c,tresor):
    oldTresor = c.get('tresor',0)
    c['tresor'] = tresor
    return oldTresor
 
# enlève le pion passé en paramètre de la carte. Si le pion n'y était pas ne fait rien
def prendrePion(c, pion):
    if pion in c['pions']:
        c['pions'].remove(pion)
 
# pose le pion passé en paramètre sur la carte. Si le pion y était déjà ne fait rien
def poserPion(c, pion):
    if pion not in c['pions']:
        c['pions'].append(pion)
 
# fait tourner la carte dans le sens horaire
def tournerHoraire(c):
    print('tourne')
    c['direction'].insert(0,c['direction'][3])
    c['direction'].pop(-1)
   
# fait tourner la carte dans le sens anti horaire
def tournerAntiHoraire(c):
    c['direction'].insert(4,c['direction'][0])
    c['direction'].pop(0)
 
# faire tourner la carte dans nombre de tour aléatoire
def tourneAleatoire(c):
    for i in range(randint(0,4)):
        tournerHoraire(c)
 
# code les murs sous la forme d'un entier dont le codage binaire
# est de la forme bNbEbSbO où bN, bE, bS et bO valent
#      soit 0 s'il n'y a pas de mur dans dans la direction correspondante
#      soit 1 s'il y a un mur dans la direction correspondante
# bN est le chiffre des unité, BE des dizaine, etc...
# le code obtenu permet d'obtenir l'indice du caractère semi-graphique
# correspondant à la carte dans la liste listeCartes au début de ce fichier
def coderMurs(c):
    #print(int(c['direction'][3]),int(c['direction'][2]),int(c['direction'][1]),int(c['direction'][0]))
    return int(str(int(c['direction'][3]))+str(int(c['direction'][2]))+str(int(c['direction'][1]))+str(int(c['direction'][0])),2)
 
# positionne les mur d'une carte en fonction du code décrit précédemment
def decoderMurs(c,code):
    for i in range(len(code)):
        c['direction'][i] = bool(int(code[i]))
       
# fournit le caractère semi graphique correspondant à la carte (voir la variable listeCartes au début de ce script)
def toChar(c):
    #print(int(coderMurs(c),2))
    return listeCartes[coderMurs(c)]
 
# suppose que la carte2 est placée au nord de la carte1 et indique
# s'il y a un passage entre ces deux cartes en passant par le nord
def passageNord(carte1,carte2):
    return not carte1['direction'][0] and not carte2['direction'][2]
 
# suppose que la carte2 est placée au sud de la carte1 et indique
# s'il y a un passage entre ces deux cartes en passant par le sud
def passageSud(carte1,carte2):
    return not carte1['direction'][2] and not carte2['direction'][0]
 
# suppose que la carte2 est placée à l'ouest de la carte1 et indique
# s'il y a un passage entre ces deux cartes en passant par l'ouest
def passageOuest(carte1,carte2):
    return not carte1['direction'][3] and not carte2['direction'][1]
 
# suppose que la carte2 est placée à l'est de la carte1 et indique
# s'il y a un passage entre ces deux cartes en passant par l'est
def passageEst(carte1,carte2):
    return not carte1['direction'][1] and not carte2['direction'][3]