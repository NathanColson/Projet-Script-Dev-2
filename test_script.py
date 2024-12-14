import unittest
import os
import csv
from script import GestionCSV  # Import de ta classe


class TestGestionCSV(unittest.TestCase):

    def setUp(self):
        """
        Configure les prérequis avant chaque test.
        """
        self.gestion_csv = GestionCSV()

    def tearDown(self):
        """
        Nettoie les fichiers/dossiers après chaque test.
        """
        for directory in [self.gestion_csv.LISTE_CSV_DIR, self.gestion_csv.RECAP_CSV_DIR]:
            if os.path.exists(directory):
                for file in os.listdir(directory):
                    os.remove(os.path.join(directory, file))
                os.rmdir(directory)

    def test_create_csv(self):
        """
        Teste la création d'un fichier CSV.
        """
        file_name = "test_produits.csv"
        self.gestion_csv.create_csv(file_name)
        file_path = self.gestion_csv.get_file_path(file_name, is_recap=False)

        # Vérifie que le fichier est créé
        self.assertTrue(os.path.exists(file_path))

        # Vérifie le contenu du fichier (colonnes)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
            self.assertEqual(headers, ['nom du produit', 'quantité', 'prix unitaire', 'catégorie'])


    def test_add_product(self):
        """
        Teste l'ajout d'un produit dans un fichier CSV existant.
        """
        file_name = "test_produits.csv"
        self.gestion_csv.create_csv(file_name)
        product_info = ["Banane", "10", "1.5", "Fruits"]

        # Ajout d'un produit
        self.gestion_csv.add_product(file_name, product_info, is_recap=False)

        # Vérifie que le produit est bien ajouté
        file_path = self.gestion_csv.get_file_path(file_name, is_recap=False)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Passe les en-têtes
            row = next(reader)
            self.assertEqual(row, product_info)


    def test_delete_product(self):
        """
        Teste la suppression d'un produit dans un fichier CSV.
        """
        file_name = "test_produits.csv"
        self.gestion_csv.create_csv(file_name)
        product_info = ["Banane", "10", "1.5", "Fruits"]
        self.gestion_csv.add_product(file_name, product_info, is_recap=False)

        # Suppression du produit
        self.gestion_csv.delete_product(file_name, "Banane", is_recap=False)

        # Vérifie que le produit est supprimé
        file_path = self.gestion_csv.get_file_path(file_name, is_recap=False)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Passe les en-têtes
            rows = list(reader)
            self.assertEqual(len(rows), 0)


    def test_merge_csv(self):
        """
        Teste la fusion de plusieurs fichiers CSV.
        """
        file1 = "produits1.csv"
        file2 = "produits2.csv"
        output_file = "recapitulatif.csv"

        # Création des fichiers source
        self.gestion_csv.create_csv(file1)
        self.gestion_csv.create_csv(file2)
        self.gestion_csv.add_product(file1, ["Banane", "10", "1.5", "Fruits"], is_recap=False)
        self.gestion_csv.add_product(file2, ["Carotte", "5", "0.8", "Légumes"], is_recap=False)

        # Fusion des fichiers
        self.gestion_csv.merge_csv([file1, file2], output_file)

        # Vérifie le contenu du fichier récapitulatif
        file_path = self.gestion_csv.get_file_path(output_file, is_recap=True)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Vérifie les en-têtes et les données
        self.assertEqual(rows[0], ['nom du produit', 'quantité', 'prix unitaire', 'catégorie'])
        self.assertEqual(rows[1], ["Banane", "10", "1.5", "Fruits"])
        self.assertEqual(rows[2], ["Carotte", "5", "0.8", "Légumes"])


    def test_search_product(self):
        """
        Teste la recherche d'un produit dans un fichier CSV.
        """
        file_name = "test_produits.csv"
        self.gestion_csv.create_csv(file_name)
        self.gestion_csv.add_product(file_name, ["Banane", "10", "1.5", "Fruits"], is_recap=False)

        # Redirige la sortie standard pour capturer les résultats
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Recherche un produit
        self.gestion_csv.search_product(file_name, product_name="Banane", is_recap=False)

        # Vérifie que le produit est trouvé
        sys.stdout = sys.__stdout__  # Restaure la sortie standard
        self.assertIn("Banane", captured_output.getvalue())

