import pandas as pd
import matplotlib.pyplot as plt
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

# Chargement des données
data = [['A', 'B', 'C'], ['B', 'C'], ['A', 'B', 'D'], ['A', 'C'], ['A', 'D']]
te = TransactionEncoder()
te_ary = te.fit(data).transform(data)
df = pd.DataFrame(te_ary, columns=te.columns_)

# Utilisation de l'algorithme Apriori pour trouver les ensembles d'articles fréquents
frequent_itemsets = apriori(df, min_support=0.5, use_colnames=True)

# Création d'un graphique de barres pour visualiser les articles les plus fréquents
frequent_itemsets.plot(kind='bar', x='itemsets', y='support')
plt.show()
