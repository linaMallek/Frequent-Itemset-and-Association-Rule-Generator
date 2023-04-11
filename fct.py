import pandas as pd
from itertools import combinations
from sklearn.preprocessing import StandardScaler
from mlxtend.preprocessing import TransactionEncoder


def apriori_Classique_frozenset(data, minsup, minconf):
    # Phase 1: Find frequent single items
    singletons = {}
    for transaction in data:
        for item in transaction:
            if item in singletons:
                singletons[item] += 1
            else:
                singletons[item] = 1
    
    # Filter infrequent singletons
    freq_items = {frozenset([item]):supp for item, supp in singletons.items() if supp >= minsup}
    itemsets = freq_items.keys()
    
    k = 2
    while itemsets:
        # Phase 2: Generate candidate itemsets of size k
        candidates = set()
        for itemset1 in itemsets:
            for itemset2 in itemsets:
                if len(itemset1.union(itemset2)) == k:
                    candidate = itemset1.union(itemset2)
                    if candidate not in candidates:
                        candidates.add(candidate)
        
        # Phase 3: Count supports of candidate itemsets
        item_counts = {itemset: 0 for itemset in candidates}

        for transaction in data:
            for candidate in candidates:
                if candidate.issubset(set(transaction)):
                    item_counts[candidate] += 1
        
        # Filter infrequent itemsets
        freq_items_temp = {itemset:supp for itemset, supp in item_counts.items() if supp >= minsup}
        itemsets = freq_items_temp.keys()
        
        # Add frequent itemsets to the list of frequent itemsets
        freq_items.update(freq_items_temp)
        
        k += 1
    
    # Generate association rules from frequent itemsets
    rules = []
    for itemset in freq_items.keys():
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset.difference(antecedent)
                    if antecedent in freq_items and consequent in freq_items:
                        conf = freq_items[itemset] / freq_items[antecedent]
                        if conf >= minconf:
                            rule = (antecedent, consequent, conf)
                            rules.append(rule)
    
    # Sort rules by decreasing confidence
    rules.sort(key=lambda x:x[2], reverse=True)
    
    # Return frequent itemsets and association rules
    return rules, freq_items

def apriori_classic_tuple(data, minsup, minconf):
    # Phase 1 : Calculer les supports des singletons
    singletons = {}
    for transaction in data:
        for item in transaction:
            if item in singletons:
                singletons[item] += 1
            else:
                singletons[item] = 1
    
    # Filtrer les singletons qui ne respectent pas le seuil de support
    freq_items = {tuple([item]):supp for item, supp in singletons.items() if supp >= minsup}
    itemsets = list(freq_items.keys())
    
    # Génération des candidats
    k = 2
    while itemsets:
        # Phase 2 : Joindre les itemsets fréquents pour générer les candidats
        candidates = []
        for i in range(len(itemsets)):
            for j in range(i+1, len(itemsets)):
                itemset1 = itemsets[i]
                itemset2 = itemsets[j]
                candidate = sorted(list(set(itemset1) | set(itemset2)))
                if candidate not in candidates:
                    candidates.append(candidate)
        
        # Phase 3 : Compter les supports des candidats
        item_counts = {tuple(candidate): 0 for candidate in candidates}
        for transaction in data:
            for candidate in candidates:
                if set(candidate).issubset(set(transaction)):
                    item_counts[tuple(candidate)] += 1
        
        # Filtrer les candidats qui ne respectent pas le seuil de support
        freq_items_temp = {itemset:supp for itemset, supp in item_counts.items() if supp >= minsup}
        itemsets = list(freq_items_temp.keys())
        
        # Ajouter les itemsets fréquents trouvés à la liste des itemsets fréquents
        freq_items.update(freq_items_temp)
    
    # Générer les règles d'association à partir des itemsets fréquents
    rules = []
    for itemset in freq_items.keys():
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = tuple(sorted(list(antecedent)))
                    consequent = tuple(sorted(list(set(itemset).difference(set(antecedent)))))
                    if antecedent in freq_items and consequent in freq_items:
                        conf = freq_items[itemset] / freq_items[antecedent]
                        if conf >= minconf:
                            rule = (antecedent, consequent, conf)
                            rules.append(rule)
    
    # Trier les règles par confiance décroissante
    rules.sort(key=lambda x:x[2], reverse=True)
    
    # Retourner les itemsets fréquents et les règles d'association
    return rules, freq_items


def apriori_vfrag_tuple(data, minsup, minconf):
    # Phase 1 : Calculer les supports des singletons
    singletons = {}
    for transaction in data:
        for item in transaction:
            if item in singletons:
                singletons[item] += 1
            else:
                singletons[item] = 1
    
    # Filtrer les singletons qui ne respectent pas le seuil de support
    freq_items = {tuple([item]):supp for item, supp in singletons.items() if supp >= minsup}
    itemsets = freq_items.keys()
    
    # Fragmentation verticale
    transactions = [set(transaction) for transaction in data]
    while itemsets:
        # Phase 2 : Joindre les itemsets fréquents pour générer les candidats
        candidates = set()
        for itemset1 in itemsets:
            for itemset2 in itemsets:
                if itemset1 != itemset2:
                    candidate = itemset1+itemset2
                    if len(candidate) == len(itemset1) + 1:
                        candidates.add(candidate)
        
        # Phase 3 : Compter les supports des candidats
        item_counts = {itemset: 0 for itemset in candidates}
        for transaction in transactions:
            for candidate in candidates:
                if  set(candidate).issubset(set(transaction)):
                    item_counts[candidate] += 1
        
        # Filtrer les candidats qui ne respectent pas le seuil de support
        freq_items_temp = {itemset:supp for itemset, supp in item_counts.items() if supp >= minsup}
        itemsets = freq_items_temp.keys()
        
        # Ajouter les itemsets fréquents trouvés à la liste des itemsets fréquents
        freq_items.update(freq_items_temp)
    
    # Générer les règles d'association à partir des itemsets fréquents
    rules = []
    for itemset in freq_items.keys():
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = (antecedent)
                    consequent = tuple(set(itemset).difference(set(antecedent)))
                    if antecedent in freq_items and consequent in freq_items:
                        conf = freq_items[itemset] / freq_items[antecedent]
                        if conf >= minconf:
                            rule = (antecedent, consequent, conf)
                            rules.append(rule)
    
    # Trier les règles par confiance décroissante
    rules.sort(key=lambda x:x[2], reverse=True)
    
    # Retourner les itemsets fréquents et les règles d'association
    return  rules,freq_items


def apriori_vfrag_Frozenset(data, minsup, minconf):
    # Phase 1 : Calculer les supports des singletons
    singletons = {}
    for transaction in data:
        for item in transaction:
            if item in singletons:
                singletons[item] += 1
            else:
                singletons[item] = 1
    
    # Filtrer les singletons qui ne respectent pas le seuil de support
    freq_items = {frozenset([item]):supp for item, supp in singletons.items() if supp >= minsup}
    itemsets = freq_items.keys()
    
    # Fragmentation verticale
    transactions = [set(transaction) for transaction in data]
    while itemsets:
        # Phase 2 : Joindre les itemsets fréquents pour générer les candidats
        candidates = set()
        for itemset1 in itemsets:
            for itemset2 in itemsets:
                if itemset1 != itemset2:
                    candidate = itemset1.union(itemset2)
                    if len(candidate) == len(itemset1) + 1:
                        candidates.add(candidate)
        
        # Phase 3 : Compter les supports des candidats
        item_counts = {itemset: 0 for itemset in candidates}

        for transaction in transactions:
            for candidate in candidates:
                if candidate.issubset(transaction):
                    item_counts[candidate] += 1
        
        # Filtrer les candidats qui ne respectent pas le seuil de support
        freq_items_temp = {itemset:supp for itemset, supp in item_counts.items() if supp >= minsup}
        itemsets = freq_items_temp.keys()
        
        # Ajouter les itemsets fréquents trouvés à la liste des itemsets fréquents
        freq_items.update(freq_items_temp)
    
    # Générer les règles d'association à partir des itemsets fréquents
    rules = []
    for itemset in freq_items.keys():
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset.difference(antecedent)
                    if antecedent in freq_items and consequent in freq_items:
                        conf = freq_items[itemset] / freq_items[antecedent]
                        if conf >= minconf:
                            rule = (antecedent, consequent, conf)
                            rules.append(rule)
    
    # Trier les règles par confiance décroissante
    rules.sort(key=lambda x:x[2], reverse=True)
    
    # Retourner les itemsets fréquents et les règles d'association
    return  rules , freq_items