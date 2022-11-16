# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 21:43:08 2020

@author: seren
"""
#Importation du module contenant les fonctions 
from script_partie_2 import *

from tkinter import *
import tkinter as Tk

#pathlogo = input("Donnez le chemin de la photo movietime.png : ")

#Création d'une class

class SearchEngine() :

    """ Cette section permet de réaliser l'interface graphique du moteur 
    de recherche Filmedia sur Tkinter.
    """  
# Création du widget principal ("maître") :

    #Initialisation des attributs de la class
    def __init__(self):
        """ Initialisation de la fenêtre """
        
        self.fen1 = Tk.Tk()
        
        self.fen1.geometry("4600x2600")
        self.fen1.config(background="black")
        self.fen1.resizable(width=True, height=True)
        
        self.beau_ty()
        
        self.fen1.mainloop()

    # Création du frame :

    def beau_ty(self):
        """ Construction du frame et des widgets"""
        
        self.Screen = Frame(self.fen1, borderwidth=0, relief=FLAT, bg="black")
        self.Screen.pack(side=TOP)
        
        # Création des widgets "esclaves" dans le Frame:
            
        # Création d'un caneva comportant textes et logo :
            
        can1 = Canvas(self.Screen,bg='black',height=160,width=300,highlightthickness=0)

        txt1 = can1.create_text(65, 70, text="F.l", font=('Stencil','26', 'bold'), fill="blue violet")
        txt2 = can1.create_text(66, 70, text="i", font=('Stencil','26'), fill="RoyalBlue2")
        txt3 = can1.create_text(105, 70, text="m", font=('Stencil','26', 'bold'), fill="indian red")
        txt4 = can1.create_text(140, 70, text="ed", font=('Stencil','26'), fill="goldenrod1")
        txt5 = can1.create_text(165, 70, text="i", font=('Stencil','26'), fill="RoyalBlue2")
        txt6 = can1.create_text(180, 70, text="a", font=('Stencil','26'), fill="pale green")

        
        #self.logo = PhotoImage( file= pathlogo)
        #image = can1.create_image(220, 20, anchor=NW, image=self.logo)
        
        # Création d'un canva pour récupérer les résultats :
        
        self.can2 = Canvas(self.Screen,bg='black', height=450,width=900,
                      highlightthickness=0.6,highlightbackground ='indian red')
        
        #Placement des canvas avec grid:
        can1.grid(row=0,column=0,padx=200,sticky=N)
        self.can2.grid(row=4,column=0,padx=100,sticky=SE,pady=35)

        #Création de la liste permettant à l'utilisateur de donner quel type d'information il souhaite:
        
            
        self.liste = Listbox(self.Screen,bg='blue violet', highlightthickness=0,
                        width=35, height=3, selectforeground='black',
                        selectbackground ='pale green',font=('Calibri','13'))
        self.liste.insert(1, "  Info about a movie")
        self.liste.insert(2, "  Common actors between two movies")
        self.liste.insert(3, "  An actor's biography")
        self.liste.insert(4, "  A top 3")
        self.liste.insert(5, "  Common films between two actors")
        self.liste.insert(6, "  Is this actor/actress single ?")
        self.liste.grid(row=1,column=0,sticky=SW,padx=180)
        
        #Creation d'un Scrollbar permettant de faire défiler la liste:
        yDefilB = Scrollbar(self.Screen,orient='vertical',command=self.liste.yview)
        yDefilB.grid(row=1, column=0, sticky='nsw',padx=165)
        self.liste['yscrollcommand']=yDefilB.set
        
        # Création des barres de recherche :
        self.search_var1 = StringVar()
        self.search_var2 = StringVar()

        self.entry1 = Entry(self.Screen, textvariable=self.search_var1, width=55)
        self.entry2 = Entry(self.Screen, textvariable=self.search_var2, width=55)

        self.entry1.grid(row=1,column=0,sticky=NE,padx=200)
        self.entry2.grid(row=1,column=0,sticky=SE,padx=200)

        self.entry1.insert(5,'Hey little cinephile ! Type and find your happyness...')
        self.entry2.insert(5,'Hey little cinephile ! Type and find your happyness...')
        
        # Création du bouton de recherche associé avec la fonction search :
        bsearch1 = Tk.Button(self.Screen, text ='Search', bg='RoyalBlue2', relief=RAISED, 
                             font=('Calibri','11'),width=6, 
                             command=self.search).grid(row=1,column=0,sticky=E,padx=120)
       
        # Ajout d'un bouton quitter associé à la fonction exitengine :
        bexit = Button(self.Screen,text='EXIT',bg='goldenrod1',font=('Calibri','12','bold'),
                       width=4, height=1, relief=GROOVE, 
                       command=self.exitengine).grid(row=6,column=0,padx=300,pady=10)
      
    #définition de la fonction search
    def search(self):
        
        """ Cette instruction permet de récupérer la chaîne de caractère entrée 
        dans la barre de recherche, l'entry dédiée et de retourner les résultats 
        dans le deuxième Canva       
        """
        #Initialisation de la valeur function_name : récupération de ce que l'utilisateur sélectionne dans la liste:
        function_name = self.liste.get(self.liste.curselection())
        #initialisation de search_result qui prendra comme valeur le résultat
        search_result = ""
        #Initialisation des valeurs search_text1 et 2, argument des fonctions: récupération de ce que l'utilisateur rentre dans les barres de recherche:
        search_text1 = self.search_var1.get()
        search_text2 = self.search_var2.get()
        

        #Création de la boucle if - elif, qui appelle les fonctions du module partie 2 selon la valeur que prend function_name
        if function_name.strip()=="Info about a movie":
            self.can2.delete("all")
            search_result = information(search_text1)     
        elif function_name.strip()=="Common actors between two movies":
            self.can2.delete("all")
            search_result = common_actors(search_text1,search_text2)
        elif function_name.strip()=="An actor's biography":
            self.can2.delete("all")
            search_result = info_actors(search_text1)
        elif function_name.strip()=="A top 3":
            self.can2.delete("all")
            search_result = top_movie(search_text1,search_text2)
        elif function_name.strip()=="Common films between two actors":
            self.can2.delete("all")
            search_result = common_movie(search_text1,search_text2)
        elif function_name.strip()=="Is this actor/actress single ?":    
            self.can2.delete("all")
            search_result = single_or_not(search_text1)

       
        #Création d'un texte dans le canva 2 : on y affiche les résultats 
        txtresult = self.can2.create_text(420,100 ,text=search_result, font=('Calibri','11'), 
                                          fill = 'white', width=800)
        
             
    #définition de la fonction permettant de quitter la fenêtre            
    def exitengine(self):
        self.fen1.destroy()
        

SearchEngine()