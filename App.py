# Import des bibliothèques nécessaires
import pandas as pd
from itertools import combinations
from fct import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from reportlab.pdfgen import canvas
import io
from flask import send_file


#from sklearn.preprocessing import StandardScaler
#from mlxtend.preprocessing import TransactionEncoder
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def upload_file():
   return render_template('upload.html')

@app.route('/hello')
def hello():
   return render_template('hello.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
   
      if request.method == 'POST':
        f = request.files['file']
        min_sup =float( request.form['min_sup'])
        min_conf = float(request.form['min_conf'] )
        type_algorithme= request.form['type_algorithme']
        filename = f.filename    
        f.save(f.filename)
   

      # Chargement des données
      df = pd.read_csv(filename)
     # Vérification de l'existence de la colonne "Date"
  

# Nettoyage des données
      df.dropna(inplace=True) # suppression des valeurs manquantes
      df.drop_duplicates(inplace=True) # suppression des doublons


      
      array = df.values


# Exemple d'utilisation de la fonction Apriori avec un ensemble de données fictif
      data = [['a', 'b', 'c', 'd'], ['a', 'c', 'd'], ['b', 'c'], ['a', 'b', 'd'], ['a', 'c', 'd']]
      #min_sup = -0.3
      #min_conf = 0.6
      match type_algorithme:
        case '1':
            rules , frequent_itemsets =apriori_Classique_frozenset(array, min_sup, min_conf)

            print(type(rules))
        case '2':
            rules , frequent_itemsets = apriori_vfrag_Frozenset(array, min_sup, min_conf)
            
            rules= list(rules)
            print(type(rules))
       



# Affichage des règles d'association générées
      freq_items_dict = {tuple(sorted(list(k))): v for k, v in frequent_itemsets.items()}
      # Convert float keys to string keys
      itemsets_frequens = {str(k): v for k, v in freq_items_dict.items()}
# Sort itemsets based on frequency values
      sorted_itemsets = itemsets_frequens.items()

    # Convert float keys to string keys
   

      # Extract itemsets and frequencies as separate lists
      labels = [', '.join(list(itemset)) for itemset, freq in sorted_itemsets]
      frequencies = [freq for itemset, freq in sorted_itemsets]

            # Create bar plot
      fig, ax = plt.subplots()
      ax.bar(labels, frequencies)

      # Add labels, title, and legend
      ax.set_xlabel('Itemsets')
      ax.set_ylabel('Frequency')
      ax.set_title('Frequent Itemsets')
      ax.legend(['Support'])

      # Save plot to PNG image file
      fig.savefig('static/plot.png')
      
      # Save plot to PNG image file
      plot_buf = io.BytesIO()
      fig.savefig(plot_buf, format='png')
      plot_buf.seek(0)


# Écrire les frozensets dans le fichier avec un saut de ligne
   
      with open("frozensets.txt", "w") as f:
        f.write('Les itemset frequent  :' + '\n')
        for freq in freq_items_dict :
             f.write(str(freq) + '\n')

        f.write('The rules :' + '\n')
        for rule in rules:
             f.write(str(rule) + '\n')

# Générer le PDF
      c = canvas.Canvas("static/frozensets.pdf")
      y = 750  # Position verticale de départ

# Lire les frozensets à partir du fichier et les ajouter au PDF
      with open("frozensets.txt", "r") as f:
       for line in f:
              c.drawString(50, y, line.strip())
              y -= 20  # Saut de ligne
      c.save()



            # Return the HTML template with links to the plot.png and frozensets.pdf files
      return render_template('result.html', plot_path='/plot.png', pdf_path='/frozensets.pdf')



# Serve the plot.png file
@app.route('/plot.png')
def plot_png():
    return send_file(io.BytesIO(open('plot.png', 'rb').read()), mimetype='image/png')

# Serve the frozensets.pdf file
@app.route('/frozensets.pdf')
def frozensets_pdf():
    return send_file('frozensets.pdf', mimetype='application/pdf')

if __name__ == '__main__':
   app.run(debug = True)

