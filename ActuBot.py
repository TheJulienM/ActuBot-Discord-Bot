# Chat bot des actualités françaises et actualités météo par MARFELLA Julien et NIGON Corentin

import discord
import asyncio
import requests

# Pour flash actu :
url='https://newsapi.org/v2/top-headlines?country=fr&category=entertainment&apiKey=2ce5084949cc460a82d8aab094b7b2ff'
json_data = requests.get(url).json()
liste_flash = json_data['articles']
max_article = len(liste_flash)

# Pour actu :
from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='2ce5084949cc460a82d8aab094b7b2ff')

# Pour la météo quotidienne:
api_address_q='http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='
lang = "&lang=fr" # Permet à la description de la météo d'être en français
ville_ask = ""
url_meteo_q = api_address_q + ville_ask + lang # Créer l'url avec la ville saisie comme : http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q=Paris&lang=fr

# Pour la météo 5 prochains jours :
api_address_s='http://api.openweathermap.org/data/2.5/forecast?appid=0c42f7f6b53b244c78a418f4f181282a&q='
liste_jours = []

# Discord
mention='{0.author.mention}'
client = discord.Client()
bad_word = False; # Pour éviter que le bot réponde bêtement si on l'insulte

import unicodedata
def sans_accent(mot) : # Fonction permettant du supprimer les accents (é devient e)
    mot_2 = unicodedata.normalize('NFD', mot).encode('ASCII', 'ignore')
    mot_liste = list(str(mot_2))
    for i in range(1,3) :
        del mot_liste[0]
    del mot_liste[-1]
    mot_final = "".join(mot_liste)
    
    return(mot_final)

@client.event
async def on_ready() :
    print("Connecté en tant que:", client.user.name)
    print("ID du bot", client.user.id)

@client.event
async def on_message(message):
    nom_bot = client.user.name
    insultes = ["connard","encule","con","couillon","fdp","pute","salaud","batard","merde","foutre"] # Liste non exhaustive d'insultes
                                                                                                    # Pour éviter que le bot réponde bêtement si on l'insulte
    
    salutations = ["bonjour","salut","coucou","salutations","yo","hello","bonsoir"] # Liste non exhaustive de message de salutataions
    
    if message.author == client.user: 
        return

    else :
        userID = message.author
        message1 = message.content
        message_min = sans_accent(message1)
        message_min = message_min.lower()
        phrase = message_min.split(" ")
       
        print("message de l'utilisateur :",phrase)
              
        max = len(phrase)
        # Pas de gros mots ^^
        for i in range(0,max):
            if phrase[i] in insultes[:] :
                bad_word = True
                print("gros mot détecté")
            else :
                bad_word = False
                #print("safe")
                             
    if bad_word == False : # Si aucune injures n'a été détecté (évidemment c'est tout à fain contournable malgré tout)
    
        for mot in range(0,len(phrase)) :
            if phrase[mot] in salutations :
                bjr = phrase[mot]
                liste_msg = [bjr.capitalize()," ",' {0.author.mention} ! :grinning:' ]
                chaine_msg = "".join(liste_msg)
                msg = chaine_msg.format(message)
                await client.send_message(message.channel, msg)
        
                        
        if "flashactu" in phrase :
            #print(message_min)                         
            journal_ask = ""
            taille_actu_liste = 0
            flash_actu_liste = message_min.split(" ")
            taille_flash_actu_liste = len(flash_actu_liste)
            journal_ask = flash_actu_liste[-1]
            #print("journal_ask :",journal_ask)
            
            if taille_flash_actu_liste > 10 :                
                msg = "Demander un seul journal à la fois via son site web s'il vous plaît :sweat_smile: Exemple : Les flashactu de 20minutes.fr "
                await client.send_message(message.channel,msg)
            
            elif taille_flash_actu_liste == 1 or taille_flash_actu_liste == 2 :
                msg = "Préciser le site du journal via son site web s'il vous plaît :sweat_smile: Exemple : Les flashactu de 20minutes.fr ou Les flashactu de Allocine.fr"
                await client.send_message(message.channel,msg)
            
            
            elif journal_ask == "tous" :
                for i in range(0,taille_flash_actu_liste) :
                    article = liste_flash[i]
                    description = ""
                    titre = ""
                    url = ""
                    image = ""
                    source = article.get('source')
                    journaux = source.get('name')
                    description = article.get('description')
                    titre = article.get('title')
                    url = article.get('url')
                    liste_msg = ["**Article de : **",journaux,"\n",titre,"\n",description,"\n",url,"\n"]
                    chaine_msg = "".join(liste_msg)
                    msg = chaine_msg.format(message)
                    await client.send_message(message.channel, msg)
            
            
            else :          
                info = 0
                for i in range(0,max_article) :
                    article = liste_flash[i]
                    description = ""
                    titre = ""
                    url = ""
                    image = ""
                    source = article.get('source')
                    journaux = source.get('name')
                
                    if journaux == journal_ask :
                        #print("source :", journaux)
                        description = article.get('description')
                        titre = article.get('title')
                        url = article.get('url')
                        image = article.get('urlToImage')
                        #print(titre + "\n" + description + "\n" + url + "\n" + image + "\n")
                        liste_msg = ["**Article de : **",journaux,"\n",titre,"\n",description,"\n",url]
                        chaine_msg = "".join(liste_msg)
                        msg = chaine_msg.format(message)
                        await client.send_message(message.channel, msg)
                        info = info + 1
                
                if info == 0 :
                    msg = 'Désolé je n\'ai pas trouvé votre journal dans les actus récentes... '.format(message)
                    await client.send_message(message.channel, msg)

        elif "actu" in phrase :
            
            journal_ask = ""
            taille_actu_liste = 0
            actu_liste = message_min.split(" ")
            taille_actu_liste = len(actu_liste)
            journal_ask = actu_liste[-1]
            #print("journal demandé : ",journal_ask)
            print(taille_actu_liste)
            
            import datetime # Permet de récupérer la date actuelle afin de sortir tous les articles de la journée
            date = datetime.datetime.now()
            annee = date.year
            mois = date.month
            jour = date.day
     
            liste_date = [str(annee),"-",str(0),str(mois),"-",str(0),str(jour)]
            date = "".join(liste_date)
            #print(date)
            
            if "liste" in phrase :
                chaine_msg = "Le Monde, L'Equipe, Libération et Les Echos vous sont proposés"
                msg = chaine_msg.format(message)
                await client.send_message(message.channel,msg)
                 
            elif taille_actu_liste > 10 :                
                liste_msg = ["Petit soucis dans votre demande :sweat_smile: Saississer un seul journal ^^ \n Exemple : Les actu de Le Monde " + "\n" + "Note : Faîtes actu liste pour voir la liste des journaux"]
                chaine_msg = "".join(liste_msg)
                msg = chaine_msg.format(message)
                await client.send_message(message.channel,msg)
            
            elif taille_actu_liste == 1 :
                msg = "Préciser le nom du journal s'il vous plaît :sweat_smile: Exemple : Les actu de L'Equipe"
                await client.send_message(message.channel,msg)
                
            else :
                #print(journal_ask)
                journal_ask = journal_ask.lower()
                if journal_ask == "monde" :
                    journal_ask = "le-monde"
                    
                elif journal_ask == "l'equipe" or journal_ask == "equipe":
                    journal_ask = "lequipe"
                    
                elif journal_ask == "echos" :
                    journal_ask = "les-echos"
                    
                elif journal_ask == "liberation" :
                    journal_ask == "liberation"
                    
                else :
                    msg = "Désolé mais le journal demandé n'est pas proposé, faites actu liste pour voir tous les journaux proposés"
                    await client.send_message(message.channel,msg)
                                    
                all_articles = newsapi.get_everything(
                                      sources=journal_ask,
                                      from_param= date,
                                      to= date,
                                      language='fr',
                                      )

                sources = newsapi.get_sources()
                liste_articles = all_articles.get('articles')    
                max = len(liste_articles)
                    
                for i in range(0,max) :
                    recup = liste_articles[i]
                    source = recup.get('source')
                    name = source.get('name')
                    titre = recup.get('title') 
                    description = recup.get('description')    
                    url = recup.get('url')
                    liste_msg = [titre,"\n",description,"\n",url]
                    chaine_msg = "".join(liste_msg)
                    msg = chaine_msg.format(message)
                    await client.send_message(message.channel, msg)
                    
        elif "meteo" in phrase :
            ville_ask = ""
            taille_meteo_liste = 0
            meteo_liste = message_min.split(" ")
            taille_meteo_liste = len(meteo_liste)
            ville_ask = meteo_liste[-1]
            ville_ask = ville_ask.capitalize()
            #print(ville_ask)
            
            if "semaine" not in phrase :
                                        
                if taille_meteo_liste == 1 :
                    msg = "Veuillez préciser une localisation s'il vous plaît :sweat_smile: \n Par exemple essayer :  \n La météo à Paris pour la météo actuelle \n La météo en semaine à Paris  pour la météo des 5 prochains jours "
                    await client.send_message(message.channel, msg.format(message))
                
                elif taille_meteo_liste > 10 :
                    msg = "Oulaah ! Une seule ville à la fois s'il vous plaît ! :dizzy_face: "
                    await client.send_message(message.channel, msg.format(message))
                                
                else :
                    url_meteo_q = api_address_q + ville_ask + lang
                    json_data = requests.get(url_meteo_q).json()
                    test_ville_ask = len(json_data)
                    
                    if test_ville_ask != 2 :
                        weather = json_data['weather'][0]['description']
                        temp = json_data['main']
                        temp = temp.get("temp")
                        temp = temp - 273.15
                        temp = round(temp,1)
                
                        liste_msg = ["Actuellement à " + ville_ask + " vous pouvez vous attendre au temps suivant : " + weather + " avec une température de " + str(temp) + "°C"]
                        chaine_msg = "".join(liste_msg)
                        msg = chaine_msg.format(message)
                        await client.send_message(message.channel, msg.format(message))
                        
                    else :
                        msg = "Désolé mais je crois bien que la ville : " + ville_ask + " n'existe pas... Vérifiez sur un globe :earth_africa: ou alors votre orthographe :wink: "
                        await client.send_message(message.channel, msg.format(message))
                            
            else :
                url_meteo_s = api_address_s + ville_ask + lang
                print(url_meteo_s)
                json_data = requests.get(url_meteo_s).json()
                test_ville_ask = len(json_data)
                
                if test_ville_ask != 2 :
                   
                    liste_msg = ["Météo à " + ville_ask + " pour les 5 prochains jours :" + "\n"]
                    chaine_msg = "".join(liste_msg)
                    msg = chaine_msg.format(message)
                    await client.send_message(message.channel, msg.format(message))
                    for i in range(0,30) :
                    
                        temps = json_data['list'][i]['weather']
                        test = temps[0]
    
                        description = test.get('description')
                        date = json_data['list'][i]['dt_txt']
                        temp = json_data['list'][i]['main']
                        temp = temp.get("temp")
                        temp = temp - 273.15
                        temp = round(temp,1)
    
                        date_liste = list(date)
                        
                        # Pour afficher la date au format dd/mm/yyyy et non yyyy/mm/dd
                        date_liste2 = [date_liste[8],date_liste[9],"/",date_liste[5],date_liste[6],"/",date_liste[0],date_liste[1],date_liste[2],date_liste[3]] 
                        date = "".join(date_liste2)
                        
                        # L'url retourne plusieurs fois la même date car à différents moments de la journée. On a choisit de n'afficher que la première apparition d'une journée.
                        if date not in liste_jours[:] :
                            liste_jours.append(date)
                            #print(date)
                            liste_msg = ["Le " + date + " vous pouvez vous attendre au temps suivant : " + description + " avec une température de " + str(temp) + " °C \n"]
                            chaine_msg = "".join(liste_msg)
                            msg = chaine_msg.format(message)
                            await client.send_message(message.channel, msg.format(message))
                            #print("liste jours pdt affichage :", liste_jours)
                            print(len(liste_jours))
                        elif len(liste_jours) == 5 :
                            for i in range(0,5) :
                                print(i)
                                del liste_jours[-1]
                                #print(liste_jours)
                                
                        
                    print("liste jours final :", liste_jours)
                        
                else :
                    msg = "Désolé mais je crois bien que la ville : " + ville_ask + " n'existe pas... Vérifiez sur un globe :earth_africa: ou alors votre orthographe :wink: "
                    await client.send_message(message.channel, msg.format(message))
    
    elif bad_word == True : # Si une injure a été détecté renvoie le gif suivant
        msg = "https://tenor.com/view/captain-america-language-gif-7292992"
        await client.send_message(message.channel,msg)
        
                   
client.run("INSERT DISCORD BOT TOKEN HERE")




