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

    def test_create_csv_file_already_exists(self):
        """
        Teste la création d'un fichier déjà existant.
        """
        file_name = "test_produits.csv"
        self.gestion_csv.create_csv(file_name)

        # Vérifie que le fichier existe
        file_path = self.gestion_csv.get_file_path(file_name, is_recap=False)
        self.assertTrue(os.path.exists(file_path))

        # Tente de recréer le même fichier
        self.gestion_csv.create_csv(file_name)

        # Vérifie que le fichier n'a pas été modifié
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
            self.assertEqual(headers, ['nom du produit', 'quantité', 'prix unitaire', 'catégorie'])
            rows = list(reader)
            self.assertEqual(len(rows), 0)  # Aucun produit ajouté lors de la recréation

    def test_create_csv_with_invalid_name(self):
        """
        Teste la création d'un fichier avec un nom invalide.
        """
        file_name = "test/produits.csv"  # Contient un slash non autorisé dans les noms de fichiers
        with self.assertRaises(OSError):
            self.gestion_csv.create_csv(file_name)


    def test_create_csv_special_characters(self):
        """
        Teste la création d'un fichier CSV avec des caractères spéciaux dans le nom.
        """
        file_name = "produits_@#$%.csv"
        self.gestion_csv.create_csv(file_name)

        # Vérifie que le fichier est créé
        file_path = self.gestion_csv.get_file_path(file_name, is_recap=False)
        self.assertTrue(os.path.exists(file_path))

        # Vérifie le contenu des colonnes
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
            self.assertEqual(headers, ['nom du produit', 'quantité', 'prix unitaire', 'catégorie'])

    def test_create_csv_large_number_of_files(self):
        """
        Teste la création d'un grand nombre de fichiers CSV.
        """
        for i in range(100):
            file_name = f"test_produits_{i}.csv"
            self.gestion_csv.create_csv(file_name)

            # Vérifie que chaque fichier est créé
            file_path = self.gestion_csv.get_file_path(file_name, is_recap=False)
            self.assertTrue(os.path.exists(file_path))

        # Vérifie que tous les fichiers sont dans le répertoire LISTE_CSV_DIR
        files_in_dir = os.listdir(self.gestion_csv.LISTE_CSV_DIR)
        self.assertEqual(len(files_in_dir), 100)  # 100 fichiers créés


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



    def test_add_product_invalid_file(self):
        """
        Teste l'ajout d'un produit dans un fichier inexistant.
        """
        file_name = "fichier_inexistant.csv"

        # Ajout d'un produit dans un fichier inexistant
        product_info = ["Banane", "10", "1.5", "Fruits"]
        self.gestion_csv.add_product(file_name, product_info, is_recap=False)

        # Vérifie qu'un message d'erreur est affiché (redirection sortie standard)
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Réexécution pour capturer le message
        self.gestion_csv.add_product(file_name, product_info, is_recap=False)

        # Vérifie que le message d'erreur est présent
        sys.stdout = sys.__stdout__  # Restaure la sortie standard
        self.assertIn("Le fichier", captured_output.getvalue())
        self.assertIn("n'existe pas", captured_output.getvalue())

    def test_add_product_duplicate(self):
        """
        Teste l'ajout de deux produits identiques dans un fichier CSV.
        """
        file_name = "test_produits.csv"
        self.gestion_csv.create_csv(file_name)

        # Ajout d'un produit
        product_info = ["Banane", "10", "1.5", "Fruits"]
        self.gestion_csv.add_product(file_name, product_info, is_recap=False)

        # Ajout du même produit une deuxième fois
        self.gestion_csv.add_product(file_name, product_info, is_recap=False)

        # Vérifie que les deux produits identiques sont présents
        file_path = self.gestion_csv.get_file_path(file_name, is_recap=False)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Passe les en-têtes
            rows = list(reader)
            self.assertEqual(len(rows), 2)  # Deux entrées présentes
            self.assertEqual(rows[0], product_info)
            self.assertEqual(rows[1], product_info)

    def test_add_product_special_characters(self):
        """
        Teste l'ajout d'un produit avec des caractères spéciaux dans les données.
        """
        file_name = "test_produits.csv"
        self.gestion_csv.create_csv(file_name)

        # Ajout d'un produit avec des caractères spéciaux
        product_info = ["Pomme & Co.", "5", "3.0", "Fruits \"Bio\""]
        self.gestion_csv.add_product(file_name, product_info, is_recap=False)

        # Vérifie que les données sont correctement ajoutées
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

    def test_delete_product_not_found(self):
        """
        Teste la suppression d'un produit qui n'existe pas.
        """
        file_name = "test_produits.csv"
        self.gestion_csv.create_csv(file_name)
        self.gestion_csv.add_product(file_name, ["Banane", "10", "1.5", "Fruits"], is_recap=False)

        # Suppression d'un produit inexistant
        self.gestion_csv.delete_product(file_name, "Orange", is_recap=False)

        # Vérifie que le fichier reste inchangé
        file_path = self.gestion_csv.get_file_path(file_name, is_recap=False)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Passe les en-têtes
            rows = list(reader)
            self.assertEqual(len(rows), 1)  # Il reste 1 produit
            self.assertEqual(rows[0][0], "Banane")


    def test_delete_product_empty_file(self):
        """
        Teste la suppression dans un fichier vide.
        """
        file_name = "test_produits.csv"
        self.gestion_csv.create_csv(file_name)

        # Suppression d'un produit dans un fichier vide
        self.gestion_csv.delete_product(file_name, "Banane", is_recap=False)

        # Vérifie que le fichier reste vide
        file_path = self.gestion_csv.get_file_path(file_name, is_recap=False)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Passe les en-têtes
            rows = list(reader)
            self.assertEqual(len(rows), 0)  # Aucun produit

    def test_delete_product_multiple_occurrences(self):
        """
        Teste la suppression d'un produit avec plusieurs occurrences dans le fichier CSV.
        """
        file_name = "test_produits.csv"
        self.gestion_csv.create_csv(file_name)

        # Ajout de plusieurs occurrences du même produit
        self.gestion_csv.add_product(file_name, ["Banane", "10", "1.5", "Fruits"], is_recap=False)
        self.gestion_csv.add_product(file_name, ["Pomme", "5", "2.0", "Fruits"], is_recap=False)
        self.gestion_csv.add_product(file_name, ["Banane", "20", "1.7", "Fruits"], is_recap=False)

        # Suppression d'une occurrence de "Banane"
        self.gestion_csv.delete_product(file_name, "Banane", is_recap=False)

        # Vérifie que toutes les occurrences ont été supprimées
        file_path = self.gestion_csv.get_file_path(file_name, is_recap=False)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Passe les en-têtes
            rows = list(reader)

        self.assertEqual(len(rows), 1)  # Seule la ligne avec "Pomme" doit rester
        self.assertEqual(rows[0], ["Pomme", "5", "2.0", "Fruits"])

    def test_delete_product_empty_file(self):
        """
        Teste la suppression dans un fichier vide.
        """
        file_name = "test_produits.csv"
        self.gestion_csv.create_csv(file_name)

        # Tentative de suppression d'un produit dans un fichier vide
        self.gestion_csv.delete_product(file_name, "Banane", is_recap=False)

        # Vérifie que le fichier reste vide
        file_path = self.gestion_csv.get_file_path(file_name, is_recap=False)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Passe les en-têtes
            rows = list(reader)

        self.assertEqual(len(rows), 0)  # Aucun produit

    def test_delete_product_case_insensitive(self):
        """
        Teste la suppression d'un produit avec une casse différente.
        """
        file_name = "test_produits.csv"
        self.gestion_csv.create_csv(file_name)

        # Ajout d'un produit
        self.gestion_csv.add_product(file_name, ["Banane", "10", "1.5", "Fruits"], is_recap=False)

        # Suppression avec une casse différente
        self.gestion_csv.delete_product(file_name, "banane", is_recap=False)

        # Vérifie que le produit n'est pas supprimé à cause de la casse
        file_path = self.gestion_csv.get_file_path(file_name, is_recap=False)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Passe les en-têtes
            rows = list(reader)

        self.assertEqual(len(rows), 1)  # La ligne doit toujours exister
        self.assertEqual(rows[0], ["Banane", "10", "1.5", "Fruits"])

    def test_delete_product_not_found(self):
        """
        Teste la suppression d'un produit qui n'existe pas.
        """
        file_name = "test_produits.csv"
        self.gestion_csv.create_csv(file_name)

        # Ajout d'un produit
        self.gestion_csv.add_product(file_name, ["Pomme", "5", "2.0", "Fruits"], is_recap=False)

        # Suppression d'un produit inexistant
        self.gestion_csv.delete_product(file_name, "Banane", is_recap=False)

        # Vérifie que le fichier reste inchangé
        file_path = self.gestion_csv.get_file_path(file_name, is_recap=False)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Passe les en-têtes
            rows = list(reader)

        self.assertEqual(len(rows), 1)  # Le produit existant reste
        self.assertEqual(rows[0], ["Pomme", "5", "2.0", "Fruits"])

    def test_delete_product_special_characters(self):
        """
        Teste la suppression d'un produit avec des caractères spéciaux dans le nom.
        """
        file_name = "test_produits.csv"
        self.gestion_csv.create_csv(file_name)

        # Ajout d'un produit avec des caractères spéciaux
        self.gestion_csv.add_product(file_name, ["Pomme & Co.", "5", "3.0", "Fruits"], is_recap=False)

        # Suppression du produit
        self.gestion_csv.delete_product(file_name, "Pomme & Co.", is_recap=False)

        # Vérifie que le produit est supprimé
        file_path = self.gestion_csv.get_file_path(file_name, is_recap=False)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Passe les en-têtes
            rows = list(reader)

        self.assertEqual(len(rows), 0)  # Aucun produit après suppression


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

    def test_merge_csv_with_empty_file(self):
        """
        Teste la fusion de fichiers CSV, dont l'un est vide.
        """
        file1 = "produits1.csv"
        file2 = "produits2.csv"
        output_file = "recapitulatif.csv"

        # Création des fichiers source
        self.gestion_csv.create_csv(file1)
        self.gestion_csv.create_csv(file2)
        self.gestion_csv.add_product(file1, ["Banane", "10", "1.5", "Fruits"], is_recap=False)

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
        self.assertEqual(len(rows), 2)  # 1 ligne de données + 1 ligne d'en-têtes


    def test_merge_csv_with_empty_files(self):
        """
        Teste la fusion de fichiers CSV où l'un ou plusieurs des fichiers source sont vides.
        """
        file1 = "produits1.csv"
        file2 = "produits2.csv"
        output_file = "recapitulatif.csv"

        # Création des fichiers source
        self.gestion_csv.create_csv(file1)
        self.gestion_csv.create_csv(file2)
        self.gestion_csv.add_product(file1, ["Banane", "10", "1.5", "Fruits"], is_recap=False)

        # Fusion des fichiers
        self.gestion_csv.merge_csv([file1, file2], output_file)

        # Vérifie le contenu du fichier récapitulatif
        file_path = self.gestion_csv.get_file_path(output_file, is_recap=True)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Vérifie que seules les lignes non vides sont ajoutées
        self.assertEqual(rows[0], ['nom du produit', 'quantité', 'prix unitaire', 'catégorie'])  # En-têtes
        self.assertEqual(rows[1], ["Banane", "10", "1.5", "Fruits"])  # Ligne valide
        self.assertEqual(len(rows), 2)  # 1 ligne de données + 1 en-tête

    def test_merge_csv_with_nonexistent_files(self):
        """
        Teste la fusion de fichiers CSV où un ou plusieurs fichiers n'existent pas.
        """
        file1 = "produits1.csv"
        nonexistent_file = "inexistant.csv"
        output_file = "recapitulatif.csv"

        # Création d'un fichier source valide
        self.gestion_csv.create_csv(file1)
        self.gestion_csv.add_product(file1, ["Pomme", "20", "2.0", "Fruits"], is_recap=False)

        # Fusion avec un fichier inexistant
        self.gestion_csv.merge_csv([file1, nonexistent_file], output_file)

        # Vérifie que seul le contenu du fichier existant est ajouté
        file_path = self.gestion_csv.get_file_path(output_file, is_recap=True)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Vérifie les en-têtes et les données
        self.assertEqual(rows[0], ['nom du produit', 'quantité', 'prix unitaire', 'catégorie'])  # En-têtes
        self.assertEqual(rows[1], ["Pomme", "20", "2.0", "Fruits"])  # Ligne valide
        self.assertEqual(len(rows), 2)  # 1 ligne de données + 1 en-tête


    def test_merge_csv_large_files(self):
        """
        Teste la fusion de fichiers contenant un grand nombre de lignes.
        """
        file1 = "produits1.csv"
        file2 = "produits2.csv"
        output_file = "recapitulatif.csv"

        # Création de deux fichiers avec de nombreuses lignes
        self.gestion_csv.create_csv(file1)
        self.gestion_csv.create_csv(file2)
        for i in range(1000):
            self.gestion_csv.add_product(file1, [f"Produit1_{i}", str(i), str(i * 1.5), "Catégorie1"], is_recap=False)
            self.gestion_csv.add_product(file2, [f"Produit2_{i}", str(i), str(i * 2.0), "Catégorie2"], is_recap=False)

        # Fusion des fichiers
        self.gestion_csv.merge_csv([file1, file2], output_file)

        # Vérifie le contenu du fichier récapitulatif
        file_path = self.gestion_csv.get_file_path(output_file, is_recap=True)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Vérifie le nombre total de lignes fusionnées
        self.assertEqual(len(rows), 2001)  # 2000 lignes de données + 1 en-tête



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


    def test_search_product_no_match(self):
        """
        Teste la recherche d'un produit qui n'existe pas.
        """
        file_name = "test_produits.csv"
        self.gestion_csv.create_csv(file_name)
        self.gestion_csv.add_product(file_name, ["Banane", "10", "1.5", "Fruits"], is_recap=False)

        # Redirige la sortie standard pour capturer les résultats
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Recherche un produit qui n'existe pas
        self.gestion_csv.search_product(file_name, product_name="Orange", is_recap=False)

        # Vérifie que le produit n'est pas trouvé
        sys.stdout = sys.__stdout__  # Restaure la sortie standard
        output = captured_output.getvalue()
        self.assertIn("Aucun produit trouvé", output)

