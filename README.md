# Runstat-groupe
Objectif du code
Ce script télécharge automatiquement les résultats du Marathon de Paris pour plusieurs années (2021-2025) depuis le site timeto.com et les sauvegarde dans des fichiers CSV exploitables.

📋 Fonctionnement étape par étape

1. La fonction principale : scrap_Runstat
Elle prend 2 paramètres :
•	num_json : un identifiant unique pour chaque édition du marathon
•	year : l'année du marathon

2. Téléchargement des données
URL = f"https://results.timeto.com/storage/results/races/{num_json}/{num_json}.json"
•	Construit une URL spécifique pour chaque course
•	Utilise des "headers" pour se faire passer pour un navigateur web (sinon le site pourrait bloquer)
•	Télécharge les données au format JSON

3. Sauvegarde brute
with open(f"paris_{year}_raw.json", "w") as f:
    json.dump(data, f, ...)
•	Crée un fichier de backup avec les données originales
•	Exemple : paris_2024_raw.json

4. Transformation en tableau
def json_to_df(obj):
    cols = [h.get("field_name") or h.get("csv_header") or "col" for h in obj["header"]]
    return pd.DataFrame(obj["data"], columns=cols)
•	Extrait les noms de colonnes depuis la structure JSON
•	Convertit les données en DataFrame pandas (tableau structuré)

5. Sélection des colonnes importantes
Le script cherche ces colonnes spécifiques :
•	Dossard : numéro du coureur
•	Nom, Prénom : identité
•	Sexe, Catégorie : classification
•	Nationalité : pays
•	Temps, Temps officiel : performances

6. Export final
df.to_csv(f"paris_marathon_{year}_fullv2.csv", ...)
•	Sauvegarde tout dans un fichier CSV
•	Exemple : paris_marathon_2024_fullv2.csv

7. Boucle sur plusieurs années
json_links = {
    "year": [2021, 2022, 2023, 2024, 2025],
    "num_json": [478, 412, 370, 318, 658]
}
•	Associe chaque année à son numéro JSON
•	Lance le scraping pour les 5 éditions automatiquement

🔑 Points clés
✅ Automatisation : Une seule exécution télécharge 5 années de données
✅ Double sauvegarde : JSON brut + CSV nettoyé
✅ Robustesse : Gestion des erreurs avec raise_for_status()
✅ Traçabilité : Affichage du nombre de lignes et aperçu des données
📊 Résultat final
Pour chaque année, vous obtenez :
•	1 fichier JSON brut (backup)
•	1 fichier CSV avec tous les coureurs et leurs résultats

Ce qui nous fait 5 fichiers que l'on va pouvoir fusionner en un seul grâce à ce second code :

📋 Fonctionnement étape par étape

Étape 1 : Recherche des fichiers
files = glob.glob("/home/.../paris_marathon_20*.csv")
Cherche tous les fichiers qui correspondent au motif
Le * signifie "n'importe quels caractères"
Trouve : paris_marathon_2021.csv, paris_marathon_2022.csv, etc.

Étape 2 : Boucle sur chaque fichier
for f in files:
    df = pd.read_csv(f, encoding="utf-8-sig")
Pour chaque fichier trouvé, le charge en mémoire
Crée un DataFrame pandas (tableau)

Étape 3 : Extraction de l'année
year_match = re.search(r"(20\d{2})", Path(f).stem)
year = year_match.group(1) if year_match else None
Utilise une expression régulière pour trouver l'année
20\d{2} signifie : "20 suivi de 2 chiffres" (2021, 2022, etc.)
Exemple : dans paris_marathon_2024.csv → extrait 2024

Étape 4 : Ajout de la colonne Année
if "Année" not in df.columns:
    df["Année"] = year
Si la colonne "Année" n'existe pas déjà
Crée cette colonne et la remplit avec l'année extraite
Permet de savoir de quelle année vient chaque ligne après fusion

Étape 5 : Fusion
merged = pd.concat(dfs, ignore_index=True)
Empile tous les DataFrames les uns sous les autres
ignore_index=True : réinitialise les numéros de lignes (0, 1, 2, 3...)
Crée un seul grand tableau avec tous les coureurs de toutes les années

Étape 6 : Tri par année
merged = merged.sort_values(by=["Année"], ascending=True)
Trie les lignes par année croissante (2021 → 2025)
Rend le fichier final plus organisé

Étape 7 : Export final
merged.to_csv("marathon_all_years.csv", index=False, encoding="utf-8-sig")
Sauvegarde le tableau fusionné dans un nouveau fichier CSV
index=False : n'inclut pas les numéros de lignes
encoding="utf-8-sig" : gère correctement les accents