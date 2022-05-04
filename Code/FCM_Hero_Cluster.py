import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

import warnings
warnings.filterwarnings('ignore')

# membaca Data
players = pd.read_csv('DataSet/players.csv')
players.columns
playersClustering = players[['hero_id', 'gold',
       'gold_per_min', 'xp_per_min', 'kills', 'deaths',
       'assists', 'hero_damage',
       'hero_healing', 'tower_damage', 'level', 'leaver_status']]

heroes = pd.read_csv('DataSet/hero_names.csv')
hero_lookup = dict(zip(heroes['hero_id'],heroes['localized_name']))
hero_lookup[0] = 'unknown'
playersClustering['hero'] = playersClustering['hero_id'].apply(lambda _id : hero_lookup[_id])

playersClustering.head(20)

heroes_stat = playersClustering.groupby(['hero']).mean()
heroes_stat.drop('unknown', inplace=True)
#print(heroes_stat)

heroes_clustering = heroes_stat[['gold_per_min','kills','deaths','assists','hero_damage','hero_healing','tower_damage']]

number_cluster = 6

from fcmeans import FCM
fcm = FCM(n_clusters=number_cluster)
fcm.fit(heroes_clustering.values)

fcm_centers = fcm.centers
fcm_labels = fcm.predict(heroes_clustering.values)
heroes_clustering['Fuzzy_Cluster'] = fcm_labels

print(heroes_clustering)
print(fcm_centers)

# generate groupby stats
FCmeans_stats = heroes_clustering.groupby(['Fuzzy_Cluster']).mean()
FCmeans_stats['count'] = heroes_clustering.groupby(['Fuzzy_Cluster'])['kills'].count()

# normalize
FCmeans_statmeans = FCmeans_stats.mean(axis=0)
FCmeans_range = FCmeans_stats.max(axis=0) - FCmeans_stats.min(axis=0)
kmeans_statnorm = (FCmeans_stats - FCmeans_statmeans) / FCmeans_range
kmeans_statnorm = kmeans_statnorm

# make plot
fig, (axis1, axis2) = plt.subplots(2,1,figsize=(14,14))
FCmeans_stats['count'].plot.bar(ax=axis1)
kmeans_statnorm.iloc[:,:7].plot.bar(ax=axis2).legend(loc='lower left')
plt.show()

