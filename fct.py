import pandas as pd
from itertools import combinations
from sklearn.preprocessing import StandardScaler
from mlxtend.preprocessing import TransactionEncoder



def apriori_Classique_frozenset(data, minsup, minconf):
    # Phase 1: Find frequent single items
    # on a creer un dictionnaire qui contient la frequence d'apprition de chauque itemset
    singletons = {} #dictionnaire 
    for transaction in data:
        for item in transaction:
            if item in singletons:
                singletons[item] += 1
            else:
                singletons[item] = 1
    
    nb_elements=0
    for transaction in data:
    # Ajouter le nombre d'éléments dans la transaction au compteur
         nb_elements += len(transaction)
     #le support 
    for key in singletons:
     singletons[key] = singletons[key] / nb_elements            

    # Filter infrequent singletons
    freq_items = {frozenset([item]):supp for item, supp in singletons.items() if supp >= minsup}
    #type dect_key
    itemsets = freq_items.keys()
    
    
    k = 2
    while itemsets:
        # Phase 2: Generate candidate itemsets of size k
        #on utilise les set pour eviter les repetition 
        candidates = set()
        for itemset1 in itemsets:
            for itemset2 in itemsets:
                if  len(itemset1.union(itemset2)) == k:
                    candidate = itemset1.union(itemset2)
                    if candidate not in candidates:
                        candidates.add(candidate)
        
        # Phase 3: Count supports of candidate itemsets
        #creer un dictionnaire qui contient les nvx candidate concatiner avec les values 0
        item_counts = {itemset: 0 for itemset in candidates}
      
        
        # chercher ou apparaissent ses candidates dans data et mettre a jour les values de items count 
        for transaction in data:
            print(transaction)
            for candidate in candidates:
                if candidate.issubset(set(transaction)):
                    item_counts[candidate] += 1


        #le support
        for key in item_counts:
            item_counts[key] = item_counts[key] / nb_elements          
       
        
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
                    #verifier quil sont frequent 
                    if antecedent in freq_items and consequent in freq_items:
                        conf = freq_items[itemset] / freq_items[antecedent]
                        if conf >= minconf:
                            rule = (antecedent, consequent, conf)
                            rules.append(rule)
    
    # Sort rules by decreasing confidence
    rules.sort(key=lambda x:x[2], reverse=True)
    print(freq_items)
    # Return frequent itemsets and association rules
    return rules, freq_items

def apriori_vfrag_Frozenset(data, minsup, minconf):
    # Phase 1 : Calculer les supports des singletons
    singletons = {}
    for transaction in data:
        for item in transaction:
            if item in singletons:
                singletons[item] += 1
            else:
                singletons[item] = 1
    nb_elements=0
    for transaction in data:
    # Ajouter le nombre d'éléments dans la transaction au compteur
         nb_elements += len(transaction)
     #le support 
    for key in singletons:
     singletons[key] = singletons[key] / nb_elements            

    
    # Filtrer les singletons qui ne respectent pas le seuil de support
    freq_items = {frozenset([item]):supp for item, supp in singletons.items() if supp >= minsup}
    itemsets = freq_items.keys()
    #print(freq_items)
    #print(itemsets)
   
    # Fragmentation verticale
    transactions = [set(transaction) for transaction in data]

    print('transaction')
    print(transactions)

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
            print(transaction)

            for candidate in candidates:
                if candidate.issubset(transaction):
                    item_counts[candidate] += 1
        
        nb_elementsT=0
        for transaction in transactions:
         # Ajouter le nombre d'éléments dans la transaction au compteur
            nb_elementsT += len(transaction)
        #le support
        for key in item_counts:
            item_counts[key] = item_counts[key] / nb_elementsT              

        

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
    print(freq_items)
    return rules , freq_items

def apriori_Close(data, minsup, minconf):
    # Phase 1: Find frequent single items
    singletons = {}
    for transaction in data:
        for item in transaction:
            if item in singletons:
                singletons[item] += 1
            else:
                singletons[item] = 1
    
    for key in singletons:
        singletons[key] = singletons[key] / len(data)

    # Filter infrequent singletons
    freq_items = {frozenset([item]):supp for item, supp in singletons.items() if supp >= minsup}
    closed_items = freq_items.copy()
    
    k = 2
    while freq_items:
        # Phase 2: Generate candidate itemsets of size k
        candidates = set()
        for itemset1 in freq_items.keys():
            for itemset2 in freq_items.keys():
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
        
        # Filter infrequent itemsets and update closed itemsets
        freq_items_temp = {itemset:supp for itemset, supp in item_counts.items() if supp >= minsup}
        closed_items.update(freq_items_temp)
        freq_items = {itemset:supp for itemset, supp in freq_items_temp.items() if not any([itemset.issubset(other) and freq_items_temp[itemset] == freq_items_temp[other] for other in freq_items if itemset != other])}
        
        k += 1
    
    # Generate association rules from closed itemsets
    rules = []
    for itemset in closed_items.keys():
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset.difference(antecedent)
                    if antecedent in closed_items and consequent in closed_items:
                        conf = closed_items[itemset] / closed_items[antecedent]
                        if conf >= minconf:
                            rule = (antecedent, consequent, conf)
                            rules.append(rule)
    
    # Sort rules by decreasing confidence
    rules.sort(key=lambda x:x[2], reverse=True)
    
    # Return closed itemsets and association rules
    return rules, closed_items

