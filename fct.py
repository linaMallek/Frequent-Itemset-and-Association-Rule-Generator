import pandas as pd
from itertools import combinations
from sklearn.preprocessing import StandardScaler
from mlxtend.preprocessing import TransactionEncoder

#--------------------------------------------------------------Apriori classique -------------------------------------------------------------------

def apriori_Classique_frozenset(data, minsup, minconf,lift_choix):
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
                        lift = freq_items[itemset] / (freq_items[antecedent] * freq_items[consequent])
                        match lift_choix :
                          case "1": 
                             if conf >= minconf and lift>1 :
                               rule = (antecedent, consequent, conf,lift)
                               rules.append(rule)
                          case "2": 
                             if conf >= minconf and lift<1 :
                               rule = (antecedent, consequent, conf,lift) 
                               rules.append(rule)
                          case "3": 
                             if conf >= minconf  :
                               rule = (antecedent, consequent, conf,lift) 
                               rules.append(rule) 
                               
    # Sort rules by decreasing confidence
    rules.sort(key=lambda x:x[2], reverse=True)
    print(freq_items)
    # Return frequent itemsets and association rules
    return rules, freq_items


#----------------------------------------------------------------Apriori ameliorer-------------------------------------------------------------------
def apriori_vfrag_Frozenset(data, minsup, minconf,lift_choix):
    

    #Enlever les doublons 
    transactions = [set(transaction) for transaction in data]
    # Phase 1 : Calculer les supports des singletons
    singletons = {}
    for transaction in transactions:
        for item in transaction:
            if item in singletons:
                singletons[item] += 1
            else:
                singletons[item] = 1
                
    nb_elements=0
    for transaction in transactions:
    # Ajouter le nombre d'éléments dans la transaction au compteur
         nb_elements += len(transaction)
    
    #le support 
    print(nb_elements)
    for key in singletons:
     singletons[key] = singletons[key] / nb_elements            

    
    # Filtrer les singletons qui ne respectent pas le seuil de support
    freq_items = {frozenset([item]):supp for item, supp in singletons.items() if supp >= minsup}
    itemsets = freq_items.keys()
    #print(freq_items)
    #print(itemsets)
   
    # Fragmentation verticale
   
    # Obtenir les fréquences des items dans l'ordre croissant
    freq_sorted = sorted(freq_items.items(), key=lambda x: x[1], reverse=True)

    # Créer un dictionnaire pour accéder rapidement à la fréquence de chaque item
    freq_dict = dict(freq_sorted)

    # Ordonner chaque transaction selon la fréquence de ses éléments

    data_Frag = [[item for item in sorted(transaction, key=lambda x: freq_dict.get(frozenset([x]), 0), reverse=True)] for transaction in transactions]

    
    nb_elementsT=0

    for transaction in data_Frag:
         # Ajouter le nombre d'éléments dans la transaction au compteur
            nb_elementsT += len(transaction)

    print(nb_elementsT)        
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
        for transaction in data_Frag:
            for candidate in candidates:
                if candidate.issubset(transaction):
                    item_counts[candidate] += 1
        
       
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
                        lift = freq_items[itemset] / (freq_items[antecedent] * freq_items[consequent])
                        
                        match lift_choix :
                          case "1": 
                             if conf >= minconf and lift>1 :
                               rule = (antecedent, consequent, conf,lift)
                               rules.append(rule)
                          case "2": 
                             if conf >= minconf and lift<1 :
                               rule = (antecedent, consequent, conf,lift) 
                               rules.append(rule)
                          case "3": 
                             if conf >= minconf  :
                               rule = (antecedent, consequent, conf,lift) 
                               rules.append(rule)   
                               
                        
                       
    
    # Trier les règles par confiance décroissante
    rules.sort(key=lambda x:x[2], reverse=True)
    
    # Retourner les itemsets fréquents et les règles d'association
    print(freq_items)
    return rules , freq_items


#-----------------------------------------------------------Algorithme Close---------------------------------------------------------------------------

def apriori_Close(data, minsup,lift_choix ):
    # Phase 1: Find frequent single items and support
    singletons = {}
    for transaction in data:
        for item in transaction:
            if item in singletons:
                singletons[item] += 1
            else:
                singletons[item] = 1

    nb_elements = sum(len(transaction) for transaction in data)

    for key in singletons:
       singletons[key] = singletons[key] / nb_elements  
    # Filter infrequent singletons and calculate support
    freq_items = {frozenset([item]): supp for item, supp in singletons.items() if supp >= minsup}
    closed_items = freq_items.copy() #initialiser avec les items frequent
    maximal_items = {}
    # Phase 2: Generate candidate itemsets of size k
    k = 2
    while freq_items:
        # Generate candidate itemsets of size k
        candidates = set()
        for itemset1 in freq_items.keys():
            for itemset2 in freq_items.keys():
                if len(itemset1.union(itemset2)) == k:
                    candidate = itemset1.union(itemset2)
                    if candidate not in candidates:
                        candidates.add(candidate)

        # Count supports of candidate itemsets
        item_counts = {itemset: 0 for itemset in candidates}
        for transaction in data:
            for candidate in candidates:
                if candidate.issubset(set(transaction)):
                    item_counts[candidate] += 1

        
        #le support
        for key in item_counts:
            item_counts[key] = item_counts[key] / nb_elements                

        # Filter infrequent itemsets and calculate support
        freq_items = {itemset: supp for itemset, supp in item_counts.items() if supp >= minsup}
        #vérifier si l'itemset est fermé et maximal
        for itemset in freq_items:
            is_closed = True
            is_maximal = True
            for itemset2, supp2 in closed_items.items():
                if itemset.issubset(itemset2) and freq_items[itemset] == supp2:
                    is_closed = False
                    if itemset != itemset2:
                        is_maximal = False
            if is_closed:
                closed_items[itemset] = freq_items[itemset]
            if is_maximal:
                maximal_items[itemset] = freq_items[itemset]

        k += 1
    
    # Generate association rules from frequent itemsets
    rules = []
    for itemset in closed_items.keys():
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset.difference(antecedent)
                    #vérifier si l'antécédent est fermé
                    if antecedent in closed_items:
                        lift = closed_items[itemset] / (closed_items[antecedent] * closed_items[consequent])
                        conf = 1
                        match lift_choix :
                          case "1": 
                             if  lift>1 :
                               rule = (antecedent, consequent, conf,lift)
                               rules.append(rule)
                          case "2": 
                             if  lift<1 :
                               rule = (antecedent, consequent, conf,lift) 
                               rules.append(rule)
                          case "3": 
                             if conf == 1 :
                               rule = (antecedent, consequent, conf,lift) 
                               rules.append(rule)  
                              
    
                     
                        
    # Sort rules by decreasing confidence
    #rules.sort(key=lambda x:x[2], reverse=True)
    #print(rules)
    # Return frequent itemsets and association rules
    return  rules,closed_items