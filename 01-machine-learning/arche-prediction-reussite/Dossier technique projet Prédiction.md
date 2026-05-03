** une approche hybride utilisée dans ce projet:**

1. **Programmation procédurale** pour le notebook `Main.ipynb`
2. **Programmation orientée objet (POO)** pour l'application `Application.py`

###  Programmation Orientée Objet  dans Application.py

**Fonctions définies (approche objet implicite) :**

```python
@st.cache_data
def load_data(logs_file, notes_file):
    """Charge les données"""
    logs = pd.read_csv(logs_file)
    notes = pd.read_csv(notes_file)
    return logs, notes

def clean_data(logs, notes):
    """Nettoie les données"""
    # ...
    return logs, notes

def create_features(logs):
    """Crée les features"""
    # ...
    return features
```

**Principe :**
- Chaque fonction a **une responsabilité unique**
- Les fonctions sont **réutilisables**
- Le code est **modulaire**

###  Utilisation d'Objets Externes

**Classes utilisées de Scikit-learn :**

```python
# Objet LinearRegression
reg = LinearRegression()
reg.fit(X_train, y_train)      # Méthode
predictions = reg.predict(X)    # Méthode
coef = reg.coef_                # Attribut

# Objet RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
predictions = rf.predict(X)
importance = rf.feature_importances_
```

**Avantages de la POO :**
-  **Encapsulation** : Les détails complexes sont cachés
-  **Réutilisabilité** : Même interface pour tous les modèles
-  **Maintenance** : Facile à modifier et étendre

###  Session State de Streamlit

**Streamlit utilise un objet `session_state` pour stocker des données :**

```python
# Sauvegarder dans la session
st.session_state['logs'] = logs_clean
st.session_state['reg_model'] = reg

# Récupérer depuis la session
logs = st.session_state['logs']
model = st.session_state['reg_model']
```

**Pourquoi ?**  
Streamlit recharge la page à chaque interaction. Le `session_state` permet de **conserver les données entre les rechargements**.

--