import random

############################################################
################# Definition des classes ###################
############################################################

################# Classe Pion ###################
# Contient la colonne et l'etage d'un pion x

class Pion:
  def __init__(self, colonne : int, etage : int):
    self.colonne = colonne
    self.etage = etage
  def __repr__(self) -> str:
    return "Pion('" + str(self.colonne)+", "+str(self.etage) + "')"

################ Classe Combi ####################
# Contient une des combi 1 et 2 de deux dés parmis 4 et si il faut les séparer ou pas lorsqu'on demande au joueur de choisir

class CombiDes:
  def __init__(self, separation : bool, combi1 : int, combi2 : int):
    self.separation = separation
    self.combi1 = combi1
    self.combi2 = combi2
  def __repr__(self) -> str:
    return "CombiDes('" + str(self.separation) + ", " + str(self.combi1) + ", " + str(self.combi2) + "')"

############## Classe joueur #####################
# Contient tout les paramètres des joueurs avec : ses dés lancés au tour X, ses 9 pions enregistrés et ses 3 grimpeurs

class Joueur:
  def __init__(self, des : int, pions : list, grimpeurs : list):
    self.des = des
    self.pions_restant = 0
    self.pions = pions
    self.grimpeurs_restant = 0
    self.grimpeurs = grimpeurs
    for i in range (len(grimpeurs)):
      if grimpeurs[i].colonne == 0:
        self.grimpeurs_restant += 1
    for i in range (len(pions)):
      if pions[i].colonne == 0:
        self.pions_restant += 1
  def __repr__(self) -> str:
    return "Joueur('" + str(self.des) + ", " + str(self.pions_restant) + ", " + "[" + ', '.join(str(elem) for elem in self.pions) + "]" + ", " + str(self.grimpeurs_restant) + ", " + "[" + ', '.join(str(elem) for elem in self.grimpeurs) + "]" + "')"
    
######################################
############ Fonctions ###############
######################################

def combine():
    print(addition())

########## On lance 4 dés ############

def lancer_des() -> list:
    des = []
    for i in range (4):
        des.append(random.randint(1, 6))
    return des

############ On créé les combinaison de dés ###############

#[[[dés[0],dés[1]],[dés[2],dés[3]]],[[dés[0],dés[2]],[dés[1],dés[3]]],[[dés[0],dés[3]],[dés[1],dés[2]]]]

def addition(dés) -> list:
    possibilités = [CombiDes(False,dés[0]+dés[1],dés[2]+dés[3]),CombiDes(False,dés[0]+dés[2],dés[1]+dés[3]),CombiDes(False,dés[0]+dés[3],dés[1]+dés[2])]
    print (possibilités) 
    return(possibilités)
    
############ On définie la priorité des joueurs ###############

def prio() -> int:
  prio = 0
  while prio == 0 : 
    un = random.randint(1,6)
    deux = random.randint(1,6)
    if un > deux :
      prio = 1
    elif un < deux :
      prio = 2
    elif un == deux :
      prio = 0
  #print (un,deux)
  if prio == 1:
    print("le joueur 1 joue en premier")
  if prio == 2:
    print("le joueur 2 joue en premier")
  return prio

############ Condition pour joueur.grimpeurs_restant == 1 #################

def Aucun_grimpeur_avance(poss,grimpeurs):
    #si aucun grimpeur placé ne peut avancer
    if (grimpeurs[0].colonne != poss.combi1 and grimpeurs[1].colonne != poss.combi2
        and grimpeurs[0].colonne != poss.combi2 and grimpeurs[1].colonne != poss.combi1):
        return True

def erreurs(pion, poss):
    err = [0,0]
    for j in range(len(pion)):
        #Si la possibilité 1/2 de la combi i testé correspond au grimpeur j, on ajoute une erreur
        if poss.combi1 != pion[j].colonne:
            err[0] += 1
        if poss.combi2 != pion[j].colonne:
            err[1] += 1
    return err

############ Test si peut placer ses pions ###########

def test_place_pion(possibilités,joueur,col):
    possibilités_finales = possibilités
    
    # Il reste deux/trois grimpeurs à placer et il peut utiliser les deux combinaisons de dés
    if 1 < joueur.grimpeurs_restant == len(joueur.grimpeurs):
        possibilités_finales = possibilités
        
    # Il reste un grimpeur
    if joueur.grimpeurs_restant == 1:
        #On considère que le dernier grimpeur est joueur.grimpeurs[2]
        grimpeurs = joueur.grimpeurs
        for t in range (len(possibilités_finales)):
            #On met la séparation en True
            if Aucun_grimpeur_avance(possibilités_finales[t],grimpeurs):
                if possibilités_finales[t].combi1 != possibilités_finales[t].combi2:
                    possibilités_finales[t].separation = True
                
    if joueur.grimpeurs_restant == 0:
        #On test pour chaque combinaison de possibilités
        for i in range(len(possibilités_finales)): #0 1 2
            err = erreurs(joueur.grimpeurs,possibilités_finales[i])
            #Si aucun grimpeur ne peut avancer avec la possibilité choisie, on la met à 0 (colonne inexistante)
            if err[0] == len(joueur.grimpeurs):
                possibilités_finales[i].combi1 = 0
            if err[1] == len(joueur.grimpeurs):
                possibilités_finales[i].combi2 = 0
    
    if joueur.pions_restant == len(joueur.grimpeurs) - joueur.grimpeurs_restant:
        pion_tempo = []
        for i in range (len(joueur.pions) - joueur.pions_restant):
            pion_tempo.append(joueur.pions[i])
        for i in range (len(joueur.grimpeurs) - joueur.grimpeurs_restant):
            pion_tempo.append(joueur.grimpeurs[i])
        for i in range(len(possibilités_finales)):
            err = erreurs(pion_tempo,possibilités_finales[i])
            #Si aucun grimpeur ne peut avancer avec la possibilité choisie, on la met à 0 (colonne inexistante)
            if err[0] == len(pion_tempo):
                possibilités_finales[i].combi1 = 0
            if err[1] == len(pion_tempo):
                possibilités_finales[i].combi2 = 0
    
    if joueur.pions_restant - (len(joueur.grimpeurs) - joueur.grimpeurs_restant) == 1:
        pion_tempo = []
        for i in range (len(joueur.pions) - joueur.pions_restant):
            pion_tempo.append(joueur.pions[i])
        for i in range (len(joueur.grimpeurs) - joueur.grimpeurs_restant):
            pion_tempo.append(joueur.grimpeurs[i])
        for i in range(len(possibilités_finales)):
            err = erreurs(pion_tempo,possibilités_finales[i])
            rep = True
            for k in range(1,len(pion_tempo)):
                for j in range(k,len(pion_tempo)):
                    if pion_tempo[k-1] == pion_tempo[j]:
                        rep = False
            #Si aucun grimpeur ne peut avancer avec la possibilité choisie, on la met à 0 (colonne inexistante)
            if err[1] == err[0] == len(pion_tempo) and possibilités_finales[i].combi1 != possibilités_finales[i].combi2 and rep:
                possibilités_finales[i].separation = True

    for i in range(len(possibilités_finales)):
        for k in range(len(joueur.pions)):
            for j in range(len(col)):
                if j+2 == possibilités_finales[i].combi1 == joueur.pions[k].colonne and joueur.pions[k].etage == col[j]:
                    possibilités_finales[i].combi1 = 0
                if j+2 == possibilités_finales[i].combi2 == joueur.pions[k].colonne and joueur.pions[k].etage == col[j]:
                    possibilités_finales[i].combi2 = 0

    return possibilités_finales
    
############ boucle de jeu ##############

def trois_lignes_complete(joueur,colonne):
  res = False
  for i in range(joueur.pions_restant):
    for j in range(len(colonne)):
      if j+2 == joueur.pions[i].colonne and colonne[j] == joueur.pions[i].etage:
        res = True
  return res

############ Choix d'une des possibilités #########

def choix_possibilité(possibilités):
    message = ""
    for i in range(len(possibilités)):
      if possibilités[i].separation == True:
        if possibilités[i].combi1 != 0:
          message += str(i + 1) + "a, "
        if possibilités[i].combi2 != 0:
          message += str(i + 1) + "b, "
      elif not(possibilités[i].combi1 == 0 and possibilités[i].combi2 == 0):
        message += str(i + 1) + ", "
    
    if message != "":
      choix = input(message)
    else:
      choix = ""
    col = []
    for i in range(len(possibilités)):
      if str(choix) == str(i + 1):
        if possibilités[i].combi1 != 0:
          col.append(possibilités[i].combi1)
        if possibilités[i].combi2 != 0:
          col.append(possibilités[i].combi2)
      if choix == str(i + 1) + "a":
        col.append(possibilités[i].combi1)
      if choix == str(i + 1) + "b":
        col.append(possibilités[i].combi2)

    return col
    #retourne une liste avec les possibilités choisit

############ continuer ou pas ##############

def continuer():
  return True


############ avancer les pions ###############

def avancer_pions(col,joueur):
  return joueur.grimpeurs
#Le jeu est basé sur le fait qu'on place 3 pions grimpeurs par tours (avec x nombres de tirages)
#Et sont enregistré lorsque le joueur finis son tour.
#Il faut donc vérifié si la col[i] à avancer est déjà enregistré ou pas, et faire avancer un grimpeurs en fonction de ça.

#On test si déjà il peut avancer

#1ère étape, tester si la colonne que l'on veut avancer est déjà enregistrer dans les pions.
"""
joueur.pions[i].colonne A utiliser dans un for pour tester toute les colonnes de tout les pions enregistré par rapport à col[i]
Si l'un correspond, enregistrer la valeur de son étage pour dire "Ouais, on reprend à là", et pk pas un False/True si un col correspond
"""

#On se retrouve avec étage = 5 (par exemple) et peut être correspond = True.
#Si aucune col ne correspondrait avec ce qu'on veut tester, on aurait étage = 0 et correspond = False

#2ème étape. On veut tester les grimpeurs. Et tant qu'on a pas fait avancé un grimpeurs, on continue, car on peut obligatoirement faire avancer un grimpeurs
#2a Si on trouve qu'un grimpeur à la meme colonne que la colonne qu'on veut faire avancer, on augmenter son étage de 1. Et on break la boucle
#2b Sinon si le grimpeur n'est pas placé (et aussi qu'un grimpeur n'a pas la meme colonne que l'on veut faire avancer dc), on met sa colonne à la colonne qu'on veut avancer, et ensuite on a deux choix possible
#Sois on a correspondance et donc on démarre depuis l'étage qu'on a trouvé (on avance donc à l'étage etage + 1)
#Sois on avait aucune correspondance de base, et son étage n'augment que de 1
#T'auras besoin de :
"""
une variable enregistrant la correspondance True/False
une variable enregistrant l'etage si correspondance
joueur.pions[i]/joueur.grimpeurs[i]/ avec un .etage/.colonne (car grimpeurs[i]/pions[i] de type Pion, donc avec un etage et une colonne)
Et c'est tout. Tu as ces deux étapes à faire. Juste à retourner les nouveaux grimpeurs
"""

############ On associe un joueur à ses dés, ses pions restants et ses grimpeurs placés ###############

def jeu():
  p = prio()
  joueur1 = Joueur([], [Pion(2,8),Pion(3,6),Pion(4,4),Pion(5,0),Pion(6,0),Pion(11,0),Pion(12,0),Pion(0,0),Pion(0,0)], [Pion(11,0),Pion(9,0),Pion(0,0)])
  joueur2 = Joueur([], [Pion(9,8),Pion(10,6),Pion(11,4),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0),Pion(0,0)], [Pion(0,0),Pion(0,0),Pion(0,0)])
  joueurs = [joueur1,joueur2]
  colonne= [2,4,6,8,10,12,10,8,6,4,2]

  win = trois_lignes_complete(joueurs[p-1],colonne)

  #while not win:
  
  #Définition des combinaisons de dés que le joueur peut jouer
  joueurs[p-1].des = test_place_pion(addition(lancer_des()),joueurs[p-1],colonne)
  print(joueurs[p-1].pions)
  print(joueurs[p-1].grimpeurs)
  print(p)
  print(joueurs[p-1].des)
    #Quel choix parmis ses combinaisons de dés veut-il faire
  col = choix_possibilité(joueurs[p-1].des)
  print(col)
  if col != []:
    loose = False
  else:
    loose = True
  
    #Avec ce choix, faire avancer le(s) grimpeur(s)
  #joueurs[p-1].grimpeurs = avancer_pions(col,joueurs[p-1])

    #Ce joueur a-t-il gagné ?
  win = trois_lignes_complete(joueurs[p-1],colonne)
  #Si on est au dernier joueur, on revient au premier, sinon on passe au suivant
  
  if p == len(joueurs):
      p = 1
  else:
      p += 1

jeu()