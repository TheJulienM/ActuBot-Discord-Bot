# **Chat bot Discord réalisé en Python des actualités françaises et actualités météo**
# **par MARFELLA Julien et NIGON Corentin**

Ce bot permet au moyen de l'API **NewsApi** (https://newsapi.org/docs/client-libraries/python) d'obtenir les dernières actualités grâce à la commande
```/flashactu <nom_journal>``` et les actualités sur le mois grâce à la commande ```/actu <nom_journal>```

L'utilisateur peut également obtenir la météo quotidienne ou hebdomadaire d'une ville au moyen de l'API de **OpenWeatherMap** (https://openweathermap.org/api) en utilisant les
commandes ```/meteo Paris``` ou ```/meteo semaine Paris```

(La communication avec le bot Discord se faisant donc par le chat d'un serveur Discord où le bot y a été préalablement ajouté.)
