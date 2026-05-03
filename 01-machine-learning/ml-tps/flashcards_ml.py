from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Pas d'en-tête sur la première page de titre
        if self.page_no() > 1:
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128)
            self.cell(0, 10, 'Flashcards Machine Learning - Synthèse Complète', 0, 0, 'R')
            self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 16)
        self.set_fill_color(65, 105, 225)  # Royal Blue
        self.set_text_color(255, 255, 255) # White
        self.cell(0, 12, title, 1, 1, 'L', True)
        self.set_text_color(0, 0, 0) # Reset text color to black
        self.ln(5)

    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(220, 220, 220) # Light Grey
        self.cell(0, 8, title, 0, 1, 'L', True)
        self.ln(2)

    def sub_section_title(self, title):
        self.set_font('Arial', 'B', 11)
        self.set_text_color(65, 105, 225) # Royal Blue text
        self.cell(0, 8, title, 0, 1, 'L')
        self.set_text_color(0, 0, 0) # Reset text color

    def body_text(self, text, is_bold=False):
        self.set_font('Arial', 'B' if is_bold else '', 11)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def bullet_point(self, title, text):
        self.set_font('Arial', 'B', 11)
        # Astuce pour mettre le titre en gras et le reste en normal sur la même ligne/paragraphe
        self.write(6, '. ' + title + ' : ')
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, text)
        self.ln(2)

    # Fonction personnalisée pour créer un tableau simple
    def create_table(self, headers, data, col_widths):
        self.set_font('Arial', 'B', 10)
        self.set_fill_color(200, 220, 255) # Light Blue header header
        
        # Headers
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 10, header, 1, 0, 'C', True)
        self.ln()
        
        # Data
        self.set_font('Arial', '', 9)
        self.set_fill_color(255, 255, 255) # White rows
        
        line_height = 6

        for row in data:
            # Calculate max height for the row based on cell content
            max_lines = 1
            for i, cell_data in enumerate(row):
                 # Use MultiCell to calculate height without drawing
                pdf_dummy = FPDF()
                pdf_dummy.add_page()
                pdf_dummy.set_font('Arial', '', 9)
                lines = pdf_dummy.multi_cell(col_widths[i], line_height, str(cell_data), split_only=True)
                max_lines = max(max_lines, len(lines))
            
            row_height = max_lines * line_height

            # Draw cells
            x_start = self.get_x()
            y_start = self.get_y()
            
            for i, cell_data in enumerate(row):
                self.set_xy(x_start, y_start)
                self.multi_cell(col_widths[i], line_height, str(cell_data), border=1, align='L')
                x_start += col_widths[i]
                
            self.set_xy(self.l_margin, y_start + row_height) # Move to next row start

# --- Création du PDF ---
pdf = PDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=15)

# --- PAGE DE TITRE ---
pdf.add_page()
pdf.ln(60)
pdf.set_font('Arial', 'B', 30)
pdf.set_text_color(65, 105, 225)
pdf.cell(0, 20, 'FLASHCARDS', 0, 1, 'C')
pdf.set_font('Arial', 'B', 24)
pdf.set_text_color(50, 50, 50)
pdf.cell(0, 20, 'MACHINE LEARNING', 0, 1, 'C')
pdf.ln(20)
pdf.set_font('Arial', '', 14)
pdf.cell(0, 10, "L'Essentiel & Les Modèles (Descriptions Complètes)", 0, 1, 'C')


# --- PAGE 2 : FLASHCARD 1 - L'ESSENTIEL (Partie 1) ---
pdf.add_page()
pdf.chapter_title("FLASHCARD 1 : L'ESSENTIEL DU ML")

pdf.section_title("1. DÉFINITION CLÉ")
pdf.body_text("C'est quoi ? Sous-domaine de l'Intelligence Artificielle (IA).")
pdf.body_text("Le principe : Au lieu de programmer des règles fixes (si X, alors Y), on donne des données à un algorithme pour qu'il apprenne lui-même les règles.")
pdf.set_font('Arial', 'I', 11)
pdf.multi_cell(0, 6, '"Apprendre des données sans être explicitement programmé."')
pdf.ln(5)

pdf.section_title("2. LES 3 PILIERS D'APPRENTISSAGE")
pdf.body_text("Si vous ne devez retenir qu'une chose, c'est ce tableau comparatif :")
pdf.ln(2)

# Données du tableau
table_headers = ['Type', 'Supervisé', 'Non Supervisé', 'Par Renforcement']
table_data = [
    ['Données', 
     'Étiquetées (Questions + Réponses). Ex: Photos avec label "chat".', 
     'Non Étiquetées (Données brutes). Ex: Historique d\'achats.', 
     'Environnement & Récompenses (Pas de données fixes, action en temps réel).'],
    ['But', 
     'Prédire ou Classer. Apprendre la relation entrée/sortie.', 
     'Découvrir la structure. Trouver des motifs cachés.', 
     'Maximiser la récompense. Apprendre par essai-erreur.'],
    ['Exemples', 
     'Détection de spam, Prédiction météo, Reconnaissance faciale.', 
     'Segmentation client, Systèmes de recommandation.', 
     'Robots, IA de jeux (Échecs, Go), Conduite autonome.'],
     ['Algos Clés', 
     'Régression Linéaire, Random Forest.', 
     'K-Means, ACP (PCA).', 
     'Q-Learning.']
]
col_widths = [25, 55, 55, 55]
pdf.create_table(table_headers, table_data, col_widths)

# --- PAGE 3 : FLASHCARD 1 - L'ESSENTIEL (Partie 2) ---
pdf.add_page()

pdf.section_title("3. LE FLUX DE TRAVAIL (WORKFLOW STANDARD)")
pdf.body_text("1. Données (Collecte, Nettoyage, Préparation) -> TÂCHE CRITIQUE (80% du temps)")
pdf.body_text(" ")
pdf.body_text("2. Entraînement (L'algorithme 'étudie' les données)")
pdf.body_text(" ")
pdf.body_text("3. Évaluation (Test sur des données jamais vues)")
pdf.body_text(" ")
pdf.body_text("4. Déploiement (Mise en production)")
pdf.ln(5)

pdf.section_title("4. CONCEPTS ET PIÈGES À CONNAÎTRE")
pdf.bullet_point("Deep Learning", "Sous-ensemble du ML utilisant des Réseaux de Neurones complexes pour des tâches difficiles (image, son, texte).")
pdf.bullet_point("Surapprentissage (Overfitting)", "L'ennemi n°1. Le modèle apprend 'par coeur' les données d'entraînement et ne sait pas généraliser. Solution : Plus de données, simplifier le modèle.")
pdf.bullet_point("Biais (Bias)", "Si les données d'entraînement ne sont pas représentatives, le modèle prendra des décisions injustes ou fausses.")


# --- PAGE 4 : FLASHCARD 2 - LES MODÈLES (Partie 1) ---
# MISE À JOUR ICI AVEC LES DESCRIPTIONS COMPLÈTES
pdf.add_page()
pdf.chapter_title("FLASHCARD 2 : LES PRINCIPAUX MODÈLES")
pdf.body_text("Les 'outils' concrets choisis en fonction du problème à résoudre.")
pdf.ln(5)

pdf.section_title("1. APPRENTISSAGE SUPERVISÉ (Données étiquetées)")
pdf.body_text("Objectif : Prédire une valeur ou une catégorie.", True)
pdf.ln(2)

pdf.sub_section_title("A. RÉGRESSION (Prédire un nombre continu)")
pdf.body_text("Ex: Prédire le prix d'une maison, la température de demain.")
# Descriptions mises à jour
pdf.bullet_point("Régression Linéaire", "Le plus simple. Cherche la ligne droite qui colle le mieux aux données. Idéal pour voir des tendances simples.")
pdf.bullet_point("Arbres de Décision (Decision Trees)", "Pose une série de questions binaires (oui/non) pour arriver à une prédiction. Facile à interpréter.")
pdf.bullet_point("Forêts Aléatoires (Random Forest)", "Combine des centaines d'arbres de décision pour une prédiction plus robuste et précise (évite le surapprentissage des arbres seuls).")
pdf.ln(3)

pdf.sub_section_title("B. CLASSIFICATION (Prédire une catégorie)")
pdf.body_text("Ex: Email spam ou non, image de chat ou chien, tumeur bénigne ou maligne.")
# Descriptions mises à jour
pdf.bullet_point("Régression Logistique", "Malgré son nom, c'est pour classer (souvent en binaire : 0 ou 1). Estime la probabilité d'appartenir à une classe.")
pdf.bullet_point("SVM (Support Vector Machines)", "Très efficace pour trouver la meilleure frontière de séparation entre deux classes, même complexe.")
pdf.bullet_point("K-Plus Proches Voisins (K-NN)", "'Dis-moi qui sont tes voisins, je te dirai qui tu es'. Classe un nouveau point en fonction de la majorité de ses K voisins les plus proches.")
pdf.bullet_point("Random Forest & Gradient Boosting (ex: XGBoost)", "Très populaires et puissants pour les compétitions de ML sur données tabulaires.")


# --- PAGE 5 : FLASHCARD 2 - LES MODÈLES (Partie 2) ---
# MISE À JOUR ICI AVEC LES DESCRIPTIONS COMPLÈTES
pdf.add_page()

pdf.section_title("2. APPRENTISSAGE NON SUPERVISÉ (Données non étiquetées)")
pdf.body_text("Objectif : Trouver des structures cachées sans réponses préétablies.", True)
pdf.ln(2)

pdf.sub_section_title("A. CLUSTERING (Regroupement)")
pdf.body_text("Ex: Segmenter des clients en groupes similaires pour le marketing.")
# Description mise à jour
pdf.bullet_point("K-Means", "L'algorithme le plus célèbre. On lui dit combien de groupes (K) on veut, et il tente de rassembler les données autour de K centres distincts.")
pdf.ln(3)

pdf.sub_section_title("B. RÉDUCTION DE DIMENSION (Simplification)")
pdf.body_text("Ex: Visualiser des données complexes en 2D/3D, compresser des données.")
# Description mise à jour
pdf.bullet_point("ACP (Analyse en Composantes Principales / PCA)", "Résume l'information en transformant un grand nombre de variables en un petit nombre de nouvelles variables 'principales' qui capturent le maximum de variance.")
pdf.ln(5)

pdf.section_title("3. DEEP LEARNING (Réseaux de Neurones)")
pdf.body_text("Souvent supervisé, pour des données complexes (images, texte, son). Utilise des couches successives de neurones pour extraire des caractéristiques abstraites.", True)
pdf.ln(2)

# Descriptions mises à jour
pdf.bullet_point("MLP (Multilayer Perceptron)", "Le réseau de neurones classique et polyvalent, fait de couches entièrement connectées. Bon pour les données tabulaires complexes.")
pdf.bullet_point("CNN (Réseaux Convolutifs)", "Les rois de la vision par ordinateur (images, vidéos). Ils utilisent des filtres pour détecter des motifs visuels (bords, textures, formes).")
pdf.bullet_point("RNN & LSTM / Transformers", "Spécialisés pour les données séquentielles (texte, traduction, séries temporelles, son). Les Transformers sont l'état de l'art actuel pour le traitement du langage naturel (NLP).")


# --- FIN ET SAUVEGARDE ---
# Nom du fichier modifié pour refléter le contenu complet
name = "Flashcards_ML_Descriptions_Completes.pdf"
pdf.output(name)
print(f"PDF généré avec succès : {name}")