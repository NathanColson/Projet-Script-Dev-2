import csv
import os
import argparse

# Définit les dossiers
LISTE_CSV_DIR = "liste_csv"
RECAP_CSV_DIR = "recap_csv"

def ensure_directories():
    """Crée les dossiers nécessaires s'ils n'existent pas."""
    os.makedirs(LISTE_CSV_DIR, exist_ok=True)
    os.makedirs(RECAP_CSV_DIR, exist_ok=True)

def create_csv(file_name):
    """Crée un fichier CSV dans le dossier liste_csv avec des colonnes prédéfinies."""
    ensure_directories()
    file_path = os.path.join(LISTE_CSV_DIR, file_name)

    if os.path.exists(file_path):
        print(f"Le fichier '{file_path}' existe déjà.")
        return

    headers = ['nom du produit', 'quantité', 'prix unitaire', 'catégorie']
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

    print(f"Fichier '{file_path}' créé avec les colonnes : {', '.join(headers)}.")

def add_product(file_name, product_info):
    """Ajoute une ligne au fichier CSV existant dans le dossier liste_csv."""
    ensure_directories()
    file_path = os.path.join(LISTE_CSV_DIR, file_name)

    if not os.path.exists(file_path):
        print(f"Le fichier '{file_path}' n'existe pas. Veuillez le créer d'abord.")
        return

    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(product_info)

    print(f"Produit ajouté au fichier '{file_path}'.")

def delete_product(file_name, product_name):
    """Supprime une ligne d'un fichier CSV dans le dossier liste_csv en fonction du nom du produit."""
    ensure_directories()
    file_path = os.path.join(LISTE_CSV_DIR, file_name)

    if not os.path.exists(file_path):
        print(f"Le fichier '{file_path}' n'existe pas.")
        return

    temp_file = file_path + '.tmp'
    with open(file_path, mode='r', encoding='utf-8') as infile, open(temp_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)
        writer.writerow(headers)

        line_deleted = False
        for row in reader:
            if row[0] != product_name:
                writer.writerow(row)
            else:
                line_deleted = True

    os.replace(temp_file, file_path)

    if line_deleted:
        print(f"Produit '{product_name}' supprimé du fichier '{file_path}'.")
    else:
        print(f"Produit '{product_name}' non trouvé dans le fichier '{file_path}'.")

def merge_csv(input_files, output_file):
    """Fusionne plusieurs fichiers CSV depuis liste_csv et sauvegarde le fichier récapitulatif dans recap_csv."""
    ensure_directories()
    input_paths = [os.path.join(LISTE_CSV_DIR, file) for file in input_files]
    output_path = os.path.join(RECAP_CSV_DIR, output_file)

    header_written = False

    with open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = None

        for file_path in input_paths:
            if not os.path.exists(file_path):
                print(f"Erreur : Le fichier '{file_path}' n'existe pas.")
                continue

            with open(file_path, mode='r', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                header = next(reader)

                if not header_written:
                    writer = csv.writer(outfile)
                    writer.writerow(header)
                    header_written = True

                for row in reader:
                    writer.writerow(row)

    print(f"Fichier récapitulatif créé : {output_path}")

def search_product_in_recap(recap_file, product_name):
    """Recherche un produit dans un fichier récapitulatif et affiche ses informations."""
    ensure_directories()
    file_path = os.path.join(RECAP_CSV_DIR, recap_file)

    if not os.path.exists(file_path):
        print(f"Le fichier '{file_path}' n'existe pas.")
        return

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)

        for row in reader:
            if row[0] == product_name:
                print(f"Produit trouvé :")
                for header, value in zip(headers, row):
                    print(f"{header}: {value}")
                return

    print(f"Produit '{product_name}' non trouvé dans le fichier '{file_path}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gérer les fichiers CSV (création, ajout, suppression, fusion, recherche).")
    parser.add_argument("action", choices=['create', 'add', 'delete', 'merge', 'search'],
                        help="Action à réaliser : 'create', 'add', 'delete', 'merge', 'search'.")
    parser.add_argument("file_name", help="Nom du fichier CSV pour 'create', 'add', 'delete' ou 'search'.")
    parser.add_argument("--product_info", nargs=4, metavar=('NOM', 'QUANTITÉ', 'PRIX', 'CATÉGORIE'),
                        help="Informations du produit à ajouter : nom, quantité, prix unitaire, catégorie.")
    parser.add_argument("--product_name", help="Nom du produit à supprimer ou rechercher.")
    parser.add_argument("--input_files", nargs='+', help="Liste des fichiers CSV à fusionner (pour 'merge').")
    parser.add_argument("--output_file", help="Nom du fichier récapitulatif (pour 'merge').")

    args = parser.parse_args()

    if args.action == 'create':
        create_csv(args.file_name)
    elif args.action == 'add':
        if args.product_info:
            add_product(args.file_name, args.product_info)
        else:
            print("Veuillez fournir les informations du produit avec l'option '--product_info'.")
    elif args.action == 'delete':
        if args.product_name:
            delete_product(args.file_name, args.product_name)
        else:
            print("Veuillez fournir le nom du produit à supprimer avec l'option '--product_name'.")
    elif args.action == 'merge':
        if args.input_files and args.output_file:
            merge_csv(args.input_files, args.output_file)
        else:
            print("Veuillez fournir les fichiers d'entrée avec '--input_files' et le fichier de sortie avec '--output_file'.")
    elif args.action == 'search':
        if args.product_name:
            search_product_in_recap(args.file_name, args.product_name)
        else:
            print("Veuillez fournir le nom du produit à rechercher avec l'option '--product_name'.")
