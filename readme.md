# TubeToNotion


**TubeToNotion** est un outil Python qui enrichit automatiquement une base de données Notion contenant des liens YouTube. Il récupère la durée des vidéos et le nom de la chaîne, puis les insère dans les propriétés dédiées de chaque page.

---

## 🚀 Fonctionnalités

- Parcourt toutes les pages d'une base Notion
- Détecte les URL de vidéos YouTube
- Récupère :
  - La durée de la vidéo (format HH\:MM\:SS)
  - Le nom de la chaîne YouTube
  - La durée convertie en secondes (pour le tri dans Notion)
- Met à jour les propriétés `Durée`, `Durée (s)` et `Auteur`
- Ignore automatiquement les pages déjà complétées

---

## 🔧 Installation

1. **Cloner le projet**

```bash
git clone https://github.com/votre-utilisateur/TubeToNotion.git
cd TubeToNotion
```

2. **Installer les dépendances**

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configurer les variables d'environnement**
   Créez un fichier `.env` à la racine avec :

```env
NOTION_TOKEN=ntn_xxx...
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
YOUTUBE_API_KEY=AIzaSy...
```

---

## 🔄 Utilisation

### ✅ Mode manuel (via terminal)

```bash
python main.py
```

### 💡 Mode double-clic

Exécutez le fichier `tube_to_notion.bat` pour lancer automatiquement le script dans l'environnement virtuel.

---

## 📂 Structure du projet

```
TubeToNotion/
├── main.py                  # Script principal
├── tube_to_notion.bat      # Lancement en double-clic
├── requirements.txt        # Librairies Python
├── .gitignore              # Fichiers à ignorer dans Git
├── Guide.docx              # Documentation utilisateur
└── TubeToNotion_logo.png   # Logo du projet
```

---

## 📈 Exemple de champs Notion requis

- `Titre` : titre de la vidéo (propriété titre)
- `URL` : URL vers la vidéo YouTube
- `Durée` : texte (HH\:MM\:SS)
- `Durée (s)` : nombre entier (**utilisé pour trier par durée**)
- `Auteur` : texte (chaîne YouTube)

> ⚠️ Le tri dans Notion doit se faire sur le champ `Durée (s)` (type "nombre"), et non sur `Durée` qui est un champ texte. Le champ `Durée (s)` peut être masqué dans l'interface si besoin.

> ⚠️ Le script ignore les pages où `Durée` **et** `Auteur` sont déjà renseignés.

---

## 🚧 Dépendances

- `notion-client`
- `google-api-python-client`
- `python-dotenv`

---

## 🚫 Limitations

- Fonctionne uniquement avec les vidéos publiques YouTube
- N'analyse que les liens contenant `youtube.com/watch`

---

## 🌟 Créateur

Ce projet a été conçu pour automatiser et enrichir ma base Notion personnelle à partir de vidéos YouTube. Il reflète ma volonté de relier des outils du quotidien (comme Notion et YouTube) à des compétences techniques concrètes (API, automatisation, structuration de données).

> ✨ TubeToNotion est un clin d'œil direct à l'extension "Save to Notion", que j'utilise pour collecter les vidéos dans Notion.

---

Merci d'utiliser **TubeToNotion** 😊

