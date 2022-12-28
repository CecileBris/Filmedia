# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 21:31:21 2020

@author: seren
"""

import pandas as pd

path = input('Chemin des fichiers csv: ')

#importation des csv sous forme de dataframe
df_movies = pd.read_csv(path + 'IMDb_movies.csv', sep=",", dtype=str)
df_names = pd.read_csv(path + 'IMDb_names.csv', sep=",", dtype=str)
df_ratings = pd.read_csv(path + 'IMDb_ratings.csv', sep=",", dtype=str)
df_title = pd.read_csv(path + 'IMDb_title_principals.csv', sep=",", dtype=str)


#creation d'une liste à partir de la colonne titre des films

T = df_movies['title']
T = list(T)

#fonction qui permet de fusionner la liste des titres avec différentes colonnes pour en faire des dictionnaires 
def fusion(a):
    d = df_movies[a]
    d = list(d)
    fus = zip(T,d)
    fus = dict(fus)
    return fus

#Execution de la fonction avec différentes colonnes
y = fusion('year')
g = fusion('genre')
du = fusion('duration')
c = fusion('country')
l = fusion('language')
d = fusion('director')
de = fusion('description')
a = fusion('actors')

#création d'une liste avec les identifiants des films, ainsi qu'un dictionnaire associant le titre des films a son identifiant 
T_id = df_movies['imdb_title_id']
T_id = list(T_id)
t_idT = zip(T, T_id)
t_idT = dict(t_idT)

#création d'une liste des identifiants du dataframe df_ratings
id_ratings = df_ratings['imdb_title_id']
id_ratings = list(id_ratings)

#fonction qui permet de fusionner la liste des identifiants associée à certaines informations en un dictionnaire 
def fusio(a):
    d = df_ratings[a]
    d = list(d)
    fus = zip(id_ratings,d)
    fus = dict(fus)
    return fus

#execution de la fonction pour différentes colonnes
meanvote = fusio('mean_vote')
allgenders_18 = fusio('allgenders_18age_avg_vote')
allgenders_30 = fusio('allgenders_30age_avg_vote')
allgenders_45 = fusio('allgenders_45age_avg_vote')
males_allages = fusio('males_allages_avg_vote')
females_allages = fusio('females_allages_avg_vote')
    
    
#Fusionne les 4 dataframe en un seul :
    
data = pd.merge(pd.merge(pd.merge(df_movies, df_ratings, on='imdb_title_id'), df_title, on='imdb_title_id'), df_names, on='imdb_name_id')

#modifie le type de la colonne title en string, pour que cela marche avec les inputs :
    
data = data.astype({'title': str})

#changement de l'index du dataframe data : 
    
data_title = data.set_index('title') #remplace les index par la colonne title 
data_name = data.set_index('name') #remplace les index par la colonne name 

#création de la fonction pour afficher les informations d'un film. Marche en appelant les clés des différents dictionnaires, ce qui permet d'afficher sa valeur, cad l'information qu'on souhaite 
def information(film):
    
    """ cette procédure doit prendre en argument le titre d'un film et elle retourne ces informations:
    sa date de sortie, sa langue originale, son directeur ainsi que la liste des acteurs principaux.
    Sa durée et son genre, ainsi que son synopsis. Enfin, elle permet de savoir la note moyenne obtenue 
    ainsi que la note attribuée par certaines catégories de votant
    
    """
    ID = t_idT[film] #donne identifiant associé au film

    paragraph = ('This movie was released in ' +  str(y[film])+ '.' 
                 + ' and its original language is ' + str(l[film]) + 'Its director is  ' 
                 + str(d[film]) + ' and the list of its main actors is: ' + str(a[film]) +'.' 
                 + 'It lasts '  + str(du[film])  + ' minutes.' + 'Here is his synopsis : ' 
                 + str(de[film]) + '.' + 'Viewers gave it an average rating of ' 
                 + str(meanvote[ID]) + '.' + str(film) + ' received a rating of ' 
                 + str(allgenders_18[ID]) + ' from 18 years old viewers, ' + str(allgenders_30[ID]) 
                 + ' by those aged 30, and finally ' + str(allgenders_45[ID]) + ' by those aged 45.'
                 + 'Men gave it an average rating of ' + str(males_allages[ID]) + ' and women of '
                 + str(females_allages[ID]) + '.')
    
    return paragraph


def common_actors(A,B):
    """ 
    Cette procédure doit prendre en argument deux titres de films, et elle retourne 
    le ou les acteurs communs à ces deux films
    
    """ 
    
    A = str(A)
    B = str(B)
    NA = data[data['title']==A] #dataframe associé au film A 
    TA = NA['name'] #extrait de la colonne name du dataframe 
    TA = list(TA) #création d'une liste 
    NB = data[data['title']==B] #meme procédure pour le film B 
    TB = NB['name']
    TB = list(TB)
    T = set(TA).intersection(TB) #création d'une liste avec les elements communs aux deux listes précédentes 
    T = ",".join(T) 
    result = str(A) + ' and ' + str(B) + ' have ' + str(T) + ' as common actor(s).'
    if len(str(T))==0 : 
        result = str(A) + ' and ' + str(B) + ' have no common actor(s).'
    return result 


def info_actors(Name):
    
    """
    
    Cette procédure doit prendre en argument le nom dun acteur, et elle retourne sa biographie, 
    la liste de ses films et ses co-acteurs ainsi que leur note
    
    """
    
    bio = data_name.loc[Name, 'bio'] #Appel la valeur de la colonne bio et de la ligne name 
    bio = list(bio) #converti en liste 
    bio = list(set(bio)) #supprime les doublons
    
    result1 = 'Here is the biography of ' + str(Name) + ' : ' + str(bio) + '.'
    
    liste_film = data_name.loc[Name,'title'] #appel valeur de la colonne title des lignes name
    liste_film = list(liste_film)
   
    result2 = ' He/She played in the following movies : ' + str(liste_film) + '.'
    
    for x in liste_film: #création d'une boucle pour parcourir chaque film associé à l'acteur 
        A = data_title.loc[x,'name']
        A = list(A)
        A = ",".join(A)
        
        result3 = 'In ' + str(x) + ' he played with ' + str(A) + '.'
        
    for y in liste_film: #création de la meme boucle 
        B = data_title.loc[y,'mean_vote']
        B = list(B)
        B = B[0]
        #B = list(set(B))
        C = data_title.loc[y,'votes_10']
        C = list(C)
        C = C[0]
        #C = list(set(C))
        D = data_title.loc[y,'votes_1']
        D = list(D)
        D = D[0]
        #D = list(set(D))
        result4 = (str(y) + ' receives an average vote of ' + str(B) + '\n' + str(C) 
                   + ' people give it a note of 10 and ' + str(D) + ' a note of 1.') 
    
    return "Bigraphie :  {}  Films : {}  Co-acteurs : {}  Note : {}".format(result1,result2,result3,result4)

      
#Convertit les colonnes genre et year en type string
df_movies = df_movies.astype({'genre':str, 'year' : str})

def top_movie(A,B):
    
    """ cette procédure doit prendre en argument un genre de film et une année, et elle 
    retourne les 3 films les mieux notés appartenant à ce genre et cette année
    """
   
    A = str(A)
    B = str(B)
    genre = df_movies[df_movies['genre']==A ]
    year = genre[genre['year']== B]
    year = year.sort_values('avg_vote', ascending=False)
    T = year['title']
    T = list(T)
    T = T[0:3]
    T = ", ".join(T)
    top = 'The top rated ' + str(A) + ' movies of ' + str(B) + ' are : ' + str(T) + '.'
    
    return top


def common_movie(A,B):
    
    """ Cette procédure doit prendre en argument deux acteurs, et elle 
    retourne les films communs à ces deux acteurs 
    """
    NA = data[data['name']==A] #dataframe associé à l'acteur A
    FA = NA['title'] #titre des films dans lesquels a joué l'acteur A. 
    FA = list(FA)
    NB = data[data['name']==B] #meme procédure pour l'acteur B 
    FB = NB['title']
    FB = list(FB)
    I = set(FA).intersection(FB) #titre en commun entre les deux listes de films
    if len(I)!=0:
        I = ",".join(I) 
        common = str(A) + ' and ' + str(B) + ' played thogether in ' + str(I) + '.'
    else:
        common = str(A) + ' and ' + str(B) + ' never played together'
    
    return common 

def single_or_not(A):
    
    """cette procédure doit prendre en argument un acteur, et elle retourne son nbre d'enfants, 
    s'il est marié ou non, et s'il a divorcé plus de deux fois 
    """
    N = data[data['name']==A]
    C = N['children'] #nombre d'enfants de l'acteur 
    C = list(C)
    C = int(C[0]) #Conversion en int pour pouvoir faire la condition
    if C != 0:
        ph = str(A) + ' has ' + str(C) + ' children(s)'
    else:
        ph = str(A) + ' has no children'
        
    S = N['spouses'] #nombre d'époux/épouses durant sa vie 
    S = list(S)
    S = int(S[0])
    D = N['divorces'] #nombre de divorces 
    D = list(D)
    D = int(D[0])
    if S != D: 
        ph2 = 'and is married.'
    else:
        ph2 = 'and is not married.'
    ph3 = ''
    if D >= 2:
        ph3 = 'He/She has more than twice divorce.'
    
    return ph +'\n'+ ph2 + '\n' + ph3