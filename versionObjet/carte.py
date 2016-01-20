import random

'''
structure carte
dictionnaire
	"direction" : list(bool) True == Mur, False == Passage
	"pion" : list de pion (int)
	"tresor" : identifiant trésor (int)
'''

# permet de créer une carte:
# les quatre premiers paramètres sont des booléens indiquant s'il y a un mur ou non dans chaque direction
# tresor est le numéro du trésor qui se trouve sur la carte (0 s'il n'y a pas de trésor)
# pions donne la liste des pions qui seront posés sur la carte (un pion est un entier entre 1 et 4)
class Carte:
    def __init__(self,nord,est,sud,ouest,tresor,pions):
        self.nord = nord
        self.est = est
        self.sud = sud
        self.ouest = ouest
        self.tresor = tresor
        self.pions = pions
        # la liste des caractère semi-graphiques correspondants aux différentes cartes
        # l'indice du caractère dans la liste correspond au codage des murs sur la carte
        # le caractère 'Ø' indique que l'indice ne correspond pas à une carte
        self.listeCartes=['Ø','╦','╣','╗','╩','═','╝','Ø','╠','╔','║','Ø','╚','Ø','Ø','Ø']
 
    # retourne un booléen indiquant si la carte est valide ou non c'est à dire qu'elle a un ou deux murs
    def estValide(self):
        return 0 < sum([self.nord,self.est,self.sud,self.ouest]) <=2
     
    # retourne un booléen indiquant si la carte possède un mur au nord
    def murNord(self):
        return self.nord
     
    # retourne un booléen indiquant si la carte possède un mur au sud
    def murSud(self):
        return self.sud
     
    # retourne un booléen indiquant si la carte possède un mur à l'est
    def murEst(self):
        return self.est
     
    # retourne un booléen indiquant si la carte possède un mur à l'ouest
    def murOuest(self):
        return self.ouest
     
    # retourne la liste des pions se trouvant sur la carte
    def getListePions(self):
        return self.pions
     
    # retourne le nombre de pions se trouvant sur la carte
    def getNbPions(self):
        return len(self.pions)
     
    # retourne un booléen indiquant si la carte possède le pion passé en paramètre
    def possedePion(self,pion):
        return pion in self.pions
     
    # retourne le codage de la liste des pions
    def getPions(self):
        return type(self.pions)
     
    # affecte les pions de la cartes en utilisant directement le codage de la liste des pions
    def setPions(self,pions):
        self.pions = pions
     
    # retourne la valeur du trésor qui se trouve sur la carte (0 si pas de trésor)
    def getTresor(self):
        #print('carte',c)
        return self.tresor if self.tresor != None else 0
     
    # enlève le trésor qui se trouve sur la carte et retourne la valeur de ce trésor
    def prendreTresor(self):
        tresor = self.tresor if self.tresor != None else 0
        self.tresor = 0
        return tresor
     
    # met le trésor passé en paramètre sur la carte et retourne la valeur de l'ancien trésor
    def mettreTresor(self,tresor):
        oldTresor = self.tresor if self.tresor != None else 0
        self.tresor = tresor
        return oldTresor
     
    # enlève le pion passé en paramètre de la carte. Si le pion n'y était pas ne fait rien
    def prendrePion(self, pion):
        if pion in self.pions:
            self.pions.remove(pion)
     
    # pose le pion passé en paramètre sur la carte. Si le pion y était déjà ne fait rien
    def poserPion(self, pion):
        if pion not in self.pions:
            self.pions.append(pion)
     
    # fait tourner la carte dans le sens horaire
    def tournerHoraire(self):
        directions = [self.nord,self.est,self.sud,self.ouest]
        directions.insert(0,directions[3])
        directions.pop(-1)
        [self.nord,self.est,self.sud,self.ouest] = directions
       
    # fait tourner la carte dans le sens anti horaire
    def tournerAntiHoraire(self):
        directions = [self.nord,self.est,self.sud,self.ouest]
        directions.insert(4,directions[0])
        directions.pop(0)
        [self.nord,self.est,self.sud,self.ouest] = directions
     
    # faire tourner la carte dans nombre de tour aléatoire
    def tourneAleatoire(self):
        for i in range(randint(0,4)):
            self.tournerHoraire()
     
    # code les murs sous la forme d'un entier dont le codage binaire
    # est de la forme bNbEbSbO où bN, bE, bS et bO valent
    #      soit 0 s'il n'y a pas de mur dans dans la direction correspondante
    #      soit 1 s'il y a un mur dans la direction correspondante
    # bN est le chiffre des unité, BE des dizaine, etc...
    # le code obtenu permet d'obtenir l'indice du caractère semi-graphique
    # correspondant à la carte dans la liste listeCartes au début de ce fichier
    def coderMurs(self):
        #print(int(c['direction'][3]),int(c['direction'][2]),int(c['direction'][1]),int(c['direction'][0]))
        return int(str(int(self.ouest))+str(int(self.sud))+str(int(self.est))+str(int(self.nord)),2)
     
    # positionne les mur d'une carte en fonction du code décrit précédemment
    def decoderMurs(self,code):
        self.nord = bool(int(code[0]))
        self.est = bool(int(code[1]))
        self.sud = bool(int(code[2]))
        self.ouest = bool(int(code[3]))
           
    # fournit le caractère semi graphique correspondant à la carte (voir la variable listeCartes au début de ce script)
    def toChar(self):
        #print(int(coderMurs(c),2))
        return self.listeCartes[self.coderMurs()]
     
    # suppose que la carte2 est placée au nord de la carte1 et indique
    # s'il y a un passage entre ces deux cartes en passant par le nord
    def passageNord(self, carte2):
        return not self.nord and not carte2.sud
     
    # suppose que la carte2 est placée au sud de la carte1 et indique
    # s'il y a un passage entre ces deux cartes en passant par le sud
    def passageSud(self, carte2):
        return not self.sud and not carte2.nord
     
    # suppose que la carte2 est placée à l'ouest de la carte1 et indique
    # s'il y a un passage entre ces deux cartes en passant par l'ouest
    def passageOuest(self, carte2):
        return not self.ouest and not carte2.est
     
    # suppose que la carte2 est placée à l'est de la carte1 et indique
    # s'il y a un passage entre ces deux cartes en passant par l'est
    def passageEst(self, carte2):
        return not self.est and not carte2.ouest
