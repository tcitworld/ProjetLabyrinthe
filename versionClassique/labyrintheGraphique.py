from labyrinthe import *
import pygame
import time
import sys
import os

       
AUCUNE=0
ALPHA=1
NUMERIQUE=2

class LabyrintheGraphique(object):
    """Classe simple d'affichage et d'interaction pour le labyrinthe."""

    def __init__(self, labyrinthe, titre='Labyrinthe des IUT', size=(1000, 800), couleur=(209,238,238),prefixeImage="./images"):
        """Method docstring."""
        self.messageInfo=None
        self.imgInfo=None
        self.labyrinthe=labyrinthe
        self.fini=False
        self.couleurTexte=couleur
        self.laMatrice=getPlateau(labyrinthe)
        self.nbCol=getNbColonnes(self.laMatrice)
        self.nbLig=getNbLignes(self.laMatrice)
        self.titre=titre
        self.getImages(prefixeImage)
        pygame.init()
        pygame.display.set_icon(self.icone)
        fenetre = pygame.display.set_mode(size,pygame.RESIZABLE|pygame.DOUBLEBUF)
        pygame.display.set_caption(titre)
        self.surface=pygame.display.get_surface()
        self.miseAjourParametres()
        self.afficheJeu()
        
        

    def getImages(self,prefixImage="./images"):
        self.imagesCartes=[]
        for i in range(16):
            if os.path.isfile(os.path.join(prefixImage,'Carte'+str(i)+'.jpeg')):
                s=pygame.image.load(os.path.join(prefixImage,'Carte'+str(i)+'.jpeg'))
            else:
                s=None
            self.imagesCartes.append(s)
        self.imagesPions=[]
        for i in range(1,5):
            s=pygame.image.load(os.path.join(prefixImage,'pion'+str(i)+'.png'))
            self.imagesPions.append(s)
        self.imagesTresors=[]
        for i in range(38):
            s=pygame.image.load(os.path.join(prefixImage,'tresor'+str(i)+'.jpeg'))
            self.imagesTresors.append(s)
        random.shuffle(self.imagesTresors)
        self.icone=pygame.image.load(os.path.join(prefixImage,'logo.jpeg'))
        self.bousole=pygame.image.load(os.path.join(prefixImage,'boussole.gif'))
                                             
    def miseAjourParametres(self):
        self.surface=pygame.display.get_surface()
        self.hauteur=self.surface.get_height()*2//3
        self.largeur=self.hauteur
        self.deltah=self.hauteur//(self.nbLig+2)
        self.deltal=self.largeur//(self.nbCol+2)
        self.finh=self.deltah*(self.nbLig+2)
        self.finl=self.deltal*(self.nbCol+2)
        self.tailleFont=min(self.deltah,self.deltal)*2//3

    def surfaceCarte(self,carte):
        t=getTresor(carte)
        p=getListePions(carte)
        img=self.imagesCartes[coderMurs(carte)]
        if img==None:
            return None
        
        surfCarte=pygame.transform.smoothscale(img,(self.deltal,self.deltah))
        if t!=0:
            surfTresor=pygame.transform.smoothscale(self.imagesTresors[t-1],(self.deltal//2,self.deltah//2))
            surfCarte.blit(surfTresor,(self.deltal//4,self.deltah//4))
        dist=10
        coord=[(dist,dist),(dist,self.deltah-(self.deltah//4+dist)),(self.deltal-(self.deltal//4+dist),self.deltah-(self.deltah//4+dist)),(self.deltal-(self.deltal//4+dist),dist)]
        for pion in p:
            surfPion=pygame.transform.smoothscale(self.imagesPions[pion-1],(self.deltal//4,self.deltah//4))
            surfCarte.blit(surfPion,coord.pop(0))
        return surfCarte

    def surfaceFleche(self,direction='O',couleur=(209,238,238)):
        res=pygame.Surface((self.deltal,self.deltah))
        pygame.draw.polygon(res, couleur, [(self.deltal//2,self.deltah//3),(self.deltal-self.deltal//8,self.deltah//2),(self.deltal//2, self.deltah*2//3)], 0)
        if direction=='N':
            res=pygame.transform.rotate(res,-90.0)
        elif direction=='E':
            res=pygame.transform.rotate(res,180.0)
        elif direction=='S':
            res=pygame.transform.rotate(res,90.0)
        return res
        
    def surfacePion(self,pion):
        res=pygame.Surface((self.deltal,self.deltah))
        surfPion=pygame.transform.smoothscale(self.imagesPions[pion-1],(self.deltal//2,self.deltah//2))
        res.blit(surfPion,(self.deltal//4,self.deltah//4))
        return res
        
    def surfaceTresor(self,tresor):
        res=pygame.Surface((self.deltal,self.deltah))
        surfTresor=pygame.transform.smoothscale(self.imagesTresors[tresor-1],(self.deltal//2,self.deltah//2))
        res.blit(surfTresor,(self.deltal//4,self.deltah//4))
        return res

    def afficheMessage(self,ligne,texte,images=[],couleur=None):
        font = pygame.font.Font(None, self.tailleFont)
        if couleur==None:
            couleur=self.couleurTexte        
        posy=self.finh+self.deltah*(ligne-1)
        posx=self.deltal//3

        #self.surface.fill((0,0,0),(0,posy,self.surface.get_width(),posy+self.deltah))

        listeTextes=texte.split('@img@')
        for msg in listeTextes:
            if msg!='':
                texte=font.render(msg,1,couleur)
                textpos=texte.get_rect()
                textpos.y=posy
                textpos.x=posx
                self.surface.blit(texte,textpos)
                posx+=textpos.width#+(self.deltal//3)
            if images!=[]:
                surface=images.pop(0)
                debuty= posy-(self.deltah//3)
                self.surface.blit(surface,(posx,debuty))
                posx+=surface.get_width()#+(self.deltal//3)

    def afficheScore(self,numLigne=3):
        texte="Nb trésors restants:"
        img=[]
        for i in range(getNbJoueurs(self.labyrinthe)):
            texte+=" @img@ "+str(nbTresorsRestantsJoueur(self.labyrinthe,i+1))
            img.append(self.surfacePion(i+1))
        self.afficheMessage(numLigne,texte,img)
    
    def afficheMessageInfo(self,numLigne=4):
        if self.messageInfo!=None:
            self.afficheMessage(numLigne,self.messageInfo,self.imgInfo)
        self.messageInfo=None
        self.imgInfo=None
        
    def afficheCarteAJouer(self):
        self.surface.blit(self.surfaceCarte(getCarteAJouer(self.labyrinthe)),(self.finl+self.deltal//2,self.finh//2))
    
    def dessineGrille(self,couleur=(255,0,0)):
        self.surface.fill((0,0,0))
        font = pygame.font.Font(None, self.tailleFont)
        flecheO=self.surfaceFleche('O')
        flecheE=self.surfaceFleche('E')
        flecheN=self.surfaceFleche('N')
        flecheS=self.surfaceFleche('S')        
        for i in range(1,self.nbLig,2):
            self.surface.blit(flecheO,(0,(i+1)*self.deltah))
            self.surface.blit(flecheE,(self.deltal*(self.nbCol+1),(i+1)*self.deltah))

        for i in range(1,self.nbCol,2):
            self.surface.blit(flecheN,((i+1)*self.deltal,0))
            self.surface.blit(flecheS,((i+1)*self.deltah,self.deltah*(self.nbLig+1)))
            
    def afficheGrille(self):
        font = pygame.font.Font(None, self.tailleFont)
        for i in range(self.nbLig):
            for j in range(self.nbCol):
                try:
                    carte=getVal(self.laMatrice,i,j)
                    s=self.surfaceCarte(carte)
                    if s==None:
                        self.surface.fill((0,0,0),((j+1)*self.deltal,(i+1)*self.deltah,self.deltal,self.deltah))
                    else:
                        self.surface.blit(s,((j+1)*self.deltal,(i+1)*self.deltah))
                except:
                    pass
                
    def animationChemin(self,chemin, joueur,pause=0.1):
        (xp,yp)=chemin.pop(0)
        for (x,y) in chemin:
            prendrePionL(self.labyrinthe,xp,yp,joueur)
            mettrePionL(self.labyrinthe,x,y,joueur)
            self.afficheJeu()
            time.sleep(pause)
            xp,yp=x,y
        getLesJoueurs(self.labyrinthe)[getJoueurCourant(self.labyrinthe)-1]['position'] = xp,yp
        return xp,yp

    def getCase(self,pos):
        if self.finl+self.deltal//2<=pos[0]<=self.finl+self.deltal//2+self.deltal and self.finh//2<=pos[1]<=self.finh//2+self.deltah:
            return ('T','T')
        if pos[0]<0 or pos[0]>self.finl or pos[1]<0 or pos[1]>self.finh:
            return (-1,-1)
        
        x=pos[1]//self.deltah
        y=pos[0]//self.deltal
        if x==0 and y in [2,4,6]:
            return ('S',y-1)
        if x==self.nbCol+1 and y in [2,4,6]:
            return ('N',y-1)
        if y==0 and x in [2,4,6]:
            return ('E',x-1)
        if y==self.nbLig+1 and x in [2,4,6]:
            return ('O',x-1)
        if x==0 or x==self.nbCol+1 or y==0 or y==self.nbLig+1:
            return (-1,-1)
        return (x-1,y-1)

    def afficheJeu(self):
        self.dessineGrille()
        self.afficheGrille()
        if not self.fini:
            self.afficheMessage(2,"C'est au joueur @img@ de jouer. Trésor à trouver @img@",[self.surfacePion(getJoueurCourant(self.labyrinthe)),self.surfaceTresor(getTresorCourant(self.labyrinthe))])
        self.afficheScore(3)
        self.afficheMessageInfo(4)
        self.afficheCarteAJouer()        
        pygame.display.flip()

    # démarre l'écoute des événements souris 
    def demarrer(self):
        self.phase=1
        pygame.time.set_timer(pygame.USEREVENT+1,100)
        while(True):
            ev=pygame.event.wait()
            if ev.type in (pygame.QUIT, pygame.KEYDOWN):
                break
            if ev.type==pygame.USEREVENT+1:
                pygame.display.flip()
            if ev.type==pygame.VIDEORESIZE:
                fenetre=pygame.display.set_mode(ev.size,pygame.RESIZABLE|pygame.DOUBLEBUF)
                self.miseAjourParametres()
                self.afficheJeu()
            if ev.type==pygame.MOUSEBUTTONDOWN:
                if self.fini:
                    continue
                (x,y)=self.getCase(ev.pos)
                if getPhase(self.labyrinthe)==1:
                    res=executerActionPhase1(self.labyrinthe,x,y)
                    if res==0:
                        self.messageInfo="La carte a été tournée"
                        self.imgInfo=[]
                    elif res==1:
                        if (getCoordonneesJoueurCourant(self.labyrinthe) == None):
                            prendrePion(self.labyrinthe["carteAmovible"], getJoueurCourant(self.labyrinthe))
                            
                            if (x == 'N'):
                                mettrePionL(self.labyrinthe, 6, y, getJoueurCourant(self.labyrinthe))
                            elif (x == 'S'):
                                mettrePionL(self.labyrinthe, 0, y, getJoueurCourant(self.labyrinthe))
                            elif (x == 'E'):
                                mettrePionL(self.labyrinthe, y, 0, getJoueurCourant(self.labyrinthe))
                            elif (x == 'O'):
                                mettrePionL(self.labyrinthe, y, 6, getJoueurCourant(self.labyrinthe))
								
                            self.messageInfo="La carte a bien été insérée"
                            self.imgInfo=[]
                    elif res==2:
                        self.messageInfo="Ce coup est interdit car l'opposé du précédent"
                        self.imgInfo=[]
                    elif res==3:
                        self.messageInfo="Vous devez insérer la carte avant de vous déplacer"
                        self.imgInfo=[]
                    else:
                        self.messageInfo="Veuillez cliquer sur la carte à jouer ou sur une flèche"
                        self.imgInfo=[]
                else: # on est dans la phase 2
                    if x in ['N','E','S','O','T'] or x==-1 or y==-1:
                        self.messageInfo="Veuillez choisir une case du labyrinthe"
                        self.imgInfo=[]
                    else:
                        chemin=accessibleDistJoueurCourant(self.labyrinthe,x,y)
                        jc=getJoueurCourant(self.labyrinthe)
                        if chemin==None:
                            self.messageInfo="Cette case n'est pas accessible au joueur @img@"
                            self.imgInfo=[self.surfacePion(jc)]            
                        else: # on a un chemin donc le déplacement est possible
                            self.animationChemin(chemin,jc)
                            t=getTresorCourant(self.labyrinthe)
                            res2=finirTour(self.labyrinthe)
                            if res2==2:
                                self.messageInfo="Le joueur @img@ a gagné"
                                self.imgInfo=[self.surfacePion(jc)]
                                self.fini=True
                            elif res2==1:
                                self.messageInfo="Le joueur @img@ vient de trouver le trésor @img@"
                                self.imgInfo=[self.surfacePion(jc),self.surfaceTresor(t)]

                self.afficheJeu()
                
            pygame.display.flip()
        pygame.quit()

#------------------------------
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
g=LabyrintheGraphique(l)
#démarrage de la partie
g.demarrer()