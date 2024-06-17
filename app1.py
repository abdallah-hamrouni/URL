from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Paramètres de connexion à la base de données
parametres_connexion = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'pfe'
}
@app.route('/api/chercher-url', methods=['GET'])
def chercher_url():
    # Récupérer l'URL local depuis les paramètres de la requête
    url = request.args.get('url')

    # Établir la connexion à la base de données
    connexion = mysql.connector.connect(**parametres_connexion)
    curseur = connexion.cursor()

    # Exécuter la requête SQL pour récupérer le chemin associé à l'URL local
    requete_sql = "SELECT path FROM pfe_test WHERE path= %s"
    curseur.execute(requete_sql, (url,))
    resultat = curseur.fetchone()

    # Fermer la connexion à la base de données
    connexion.close()

    # Vérifier si un résultat a été trouvé
    if resultat:
        return jsonify({"path": resultat[0]})
    else:
        return jsonify({"message": "L'URL local n'existe pas dans la base de données"}), 404
if __name__ == '__main__':
    app.run(debug=True)
