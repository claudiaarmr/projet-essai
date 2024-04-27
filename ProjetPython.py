
# Analyse de Performance des Contrats Perpétuels vs Marché Spot pour Ethereum

## Contexte
#Dans le cadre de lévaluation des investissements en crypto-monnaies, il est crucial de comprendre les différentes options de trading disponibles. Ce projet se concentre sur la comparaison entre les contrats perpétuels et les achats directs sur le marché spot pour lEthereum (ETH). Les contrats perpétuels, une forme populaire de dérivés sur les plateformes de crypto-monnaies, nont pas de date dexpiration et ajustent continuellement leur valeur à travers des taux de financement pour imiter le marché spot.

## Objectif
#Lobjectif de ce projet est de calculer et de comparer la performance financière dune position longue sur un contrat perpétuel avec celle dun achat direct sur le marché spot. Nous utilisons des données historiques pour estimer les coûts et les rendements, en tenant compte des taux de financement et des fluctuations des prix pendant lannée 2023.


import requests
import pandas as pd
  
#Choix de la période
from datetime import datetime

date_debut = datetime(2023, 1, 1)
date_fin = datetime(2023, 12, 31)

    # Conversion en millisecondes
timestamp_debut = int(date_debut.timestamp() * 1000)
timestamp_fin = int(date_fin.timestamp() * 1000)

#Choix de la cryptomonnaie

Crypto = "ETHUSDT" #nous avons choisi la crypto ethereum

#Collecte de données
url_contrat = f"https://api.binance.com/api/v1/klines?symbol=ETHUSDT&interval=1d&startTime={timestamp_debut}&endTime={timestamp_fin}"
url_spot = f"https://api.binance.com/api/v3/klines?symbol=ETHUSDT&interval=1d&startTime={timestamp_debut}&endTime={timestamp_fin}"
url_Tx_Fi = f"https://fapi.binance.com/fapi/v1/fundingRate?symbol=ETHUSDT&interval=1d&startTime={timestamp_debut}&endTime={timestamp_fin}"

response_contrat = requests.get(url_contrat)
response_spot = requests.get(url_spot)
response_Tx_Fi = requests.get(url_Tx_Fi)

data_contrat = response_contrat.json()
data_spot = response_spot.json()
data_Tx_Fi = response_Tx_Fi.json()

#Nom des colonnes pour le DataFrame
colonnes = ['Date ouverture','Ouverture','Plus haut','Plus bas','Fermeture','Volume','Date fermeture','Volume Trades','Nombre Trades','Taker buy base asset volume','Taker buy quote asset volume','Valeur à ignorer']
colonnes2 = ['fundingTime', 'fundingRate']  

#Conversion en DataFrame
df_contrat = pd.DataFrame(data_contrat, columns = colonnes)
df_spot = pd.DataFrame(data_spot, columns = colonnes)
df_Tx_Fi = pd.DataFrame(data_Tx_Fi, columns = colonnes2)


#Reconversion des dates en dates lisibles
df_contrat['Date ouverture'] = pd.to_datetime(df_contrat['Date ouverture'], unit='ms')
df_contrat['Date fermeture'] = pd.to_datetime(df_contrat['Date fermeture'], unit='ms')

df_spot['Date ouverture'] = pd.to_datetime(df_spot['Date ouverture'], unit='ms')
df_spot['Date fermeture'] = pd.to_datetime(df_spot['Date fermeture'], unit='ms')
df_Tx_Fi['fundingTime'] = pd.to_datetime(df_Tx_Fi['fundingTime'], unit='ms')

df_Tx_Fi.rename(columns={'fundingTime': 'Dates', 'fundingRate': 'Taux de financement'}, inplace=True)


#Fonction pour calculer la quantité d'Ethereum achetée
def calc_quantite_achetee(investissement_usd, prix_ouverture, marge=0.25):
    """
    Calcule la quantité d'ETH achetée en fonction de l'investissement initial, du prix d'ouverture et de la marge.
    """
    quantite_achetee = (investissement_usd / prix_ouverture) / marge
    return quantite_achetee

#Fonction pour calculer la performance du contrat perpétuel
def calc_perf_contrat(prix_ouverture, prix_fermeture, taux_financement_moyen, jours_investis, quantite_eth, investissement_usd):
    """
    Calcule la performance financière d'un investissement dans un contrat perpétuel.
    """
    perf = ((prix_fermeture - prix_ouverture) * quantite_eth) - (taux_financement_moyen * investissement_usd * jours_investis)
    return perf

#Fonction pour calculer la performance sur le marché spot
def calc_perf_spot(prix_ouverture, prix_fermeture, quantite_eth):
    """
    Calcule la performance financière d'un investissement sur le marché spot.
    """
    performance = (prix_fermeture - prix_ouverture) * quantite_eth
    return performance

#Calcul du taux de financement moyen
def calculer_Tx_Fi_moyen(taux_financement):
    """
    Calcule le taux de financement moyen à partir des données historiques.
    """
    taux_financement_float = df_Tx_Fi['Taux de financement'] = pd.to_numeric(df_Tx_Fi['Taux de financement'], errors='coerce')
    taux_financement_moyen = taux_financement_float.mean()
    return taux_financement_moyen


#Déclaration des variables préliminaires
investissement_initial_usd = float(input('Entrez le montant de votre investissement initial en USD: '))
jours_investis = (date_fin - date_debut).days
prix_ouverture_spot = float(df_spot.iloc[0]['Ouverture'])
prix_fermeture_contrat = float(df_contrat.iloc[-1]['Fermeture'])
prix_fermeture_spot = float(df_spot.iloc[-1]['Fermeture'])
taux_financement_moyen = calculer_Tx_Fi_moyen(df_Tx_Fi['Taux de financement'])
quantite_eth_achetee = calc_quantite_achetee(investissement_initial_usd, prix_ouverture_spot)

#Calcul des performances
perf_contrat = calc_perf_contrat(prix_ouverture_spot, prix_fermeture_contrat, taux_financement_moyen, jours_investis, quantite_eth_achetee, investissement_initial_usd)
perf_spot = calc_perf_spot(prix_ouverture_spot, prix_fermeture_spot, quantite_eth_achetee)

#Affichage
print("Performance du contrat perpétuel :", perf_contrat, "USD")
print("Performance sur le marché spot :", perf_spot,"USD")

## Conclusion

### Résultats
#Après une année complète de suivi, le script a calculé la performance des investissements en contrats perpétuels et sur le marché spot pour lEthereum. Les résultats montrent des différences significatives de rendement, influencées par les fluctuations du marché et les taux de financement appliqués aux contrats perpétuels.

### Implications
#Ces analyses permettent aux investisseurs de mieux comprendre le comportement des différents instruments financiers dans le domaine des crypto-monnaies. Selon les conditions de marché prévalentes, le choix entre les contrats perpétuels et lachat direct peut avoir un impact substantiel sur le rendement de linvestissement.

### Étapes futures
#Pour des analyses futures, il serait bénéfique délargir cette étude à dautres crypto-monnaies et dintégrer des modèles prédictifs pour mieux anticiper les mouvements de marché et les ajustements des taux de financement.

#Nous encourageons les utilisateurs à explorer différentes configurations de simulation et à ajuster les paramètres selon leurs besoins spécifiques pour maximiser leur compréhension et leur efficacité dans le trading de crypto-monnaies.

