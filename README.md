# 📡 CheckMobi HLR Lookup Tool

Petit outil en Python qui utilise l'API [CheckMobi](https://checkmobi.com) pour faire des HLR Lookup et vérifier si un numéro est actif et quel opérateur il utilise.  
Pratique pour nettoyer une base de données et éviter d’envoyer des sms/appels vers des numéros morts.

---

## 🔎 C'est quoi un HLR Lookup ?

HLR (Home Location Register) c’est une requête envoyée direct au réseau mobile.  
Ça permet de savoir :
- si le numéro est **connecté/actif**
- si le numéro est **inactif ou éteint**
- l’**opérateur actuel** (même si y a eu portabilité MNP)
- le type de numéro (mobile, fixe, voip...)

Exemple de statuts :
- `connected` → numéro joignable
- `absent` → tel éteint / pas de réseau
- `invalid` → numéro pas valide
- `no-teleservice-provisioned` → SIM data only, pas de sms/call

---

## ⚙️ Installation

1. Cloner le projet :

```bash
git clone https://github.com/JulienDDD/checkmobi-hlr-lookup.git
cd checkmobi-hlr-lookup

python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
```


🔑 Configuration

Créer un fichier config.json :
```
{
  "api_key": "TA_CLE_API_CHECKMOBI"
}
```

⚠️ Ne partage pas ce fichier, il contient ta clé secrète.

📋 Utilisation

Mettre les numéros dans numbers.txt (un par ligne, format +33…).

```
+33612345678
+34657643870
```

Lancer le script :
```bash
python hlr_checker.py
```

Résultats :

Affichage en temps réel dans la console (stats + tableau)

Fichiers générés dans results/YYYY-MM-DD/OPERATEUR.txt
