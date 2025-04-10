# Git Repository Analyzer

Un outil en ligne de commande pour cloner des dépôts Git et les analyser afin de détecter des mauvaises pratiques de codage et générer des statistiques. L'outil prépare également des prompts formatés pour l'analyse par des modèles de langage (LLM).

## Prérequis

- Python 3.6 ou supérieur
- Git installé sur votre système

## Installation

1. Clonez ou téléchargez les fichiers de ce projet dans un dossier
2. Installez les dépendances nécessaires :

```bash
pip install GitPython
```

## Structure des fichiers

- `git_connector.py` - Module pour cloner et lister les fichiers des dépôts Git
- `bad_practice_agent.py` - Agent pour détecter les mauvaises pratiques dans le code
- `orchestrator.py` - Orchestrateur pour gérer l'exécution des agents
- `git_analyzer_cli.py` - Interface en ligne de commande

## Utilisation

### Utilisation basique

Pour lancer l'application en mode interactif :

```bash
python git_analyzer_cli.py
```

L'application vous demandera l'URL du dépôt à cloner et vous guidera à travers les options disponibles.

### Utilisation avec arguments

Vous pouvez également spécifier des arguments directement :

```bash
python git_analyzer_cli.py --url https://github.com/user/repo.git --branch main --analyze
```

Options disponibles :
- `--url` : URL du dépôt Git à cloner
- `--branch` : Branche à cloner (par défaut: main)
- `--analyze` : Exécuter automatiquement les agents d'analyse
- `--stats-only` : Afficher uniquement les statistiques du dépôt
- `--save-prompt` : Générer et sauvegarder automatiquement un prompt pour LLM

### Exemples d'utilisation

1. Utilisation interactive (recommandée pour débuter) :
```bash
python git_analyzer_cli.py
```

Exemple de session interactive :
```
=== Analyseur de dépôt Git avec agents IA ===
Entrez l'URL du dépôt Git à cloner: https://github.com/user/repo.git
Entrez le nom de la branche (laissez vide pour 'main'): 
Clonage du dépôt https://github.com/user/repo.git, branche main...
Dépôt cloné avec succès dans: /tmp/tmp1234abcd

Statistiques du dépôt:
- Nombre total de fichiers: 42
- Fichiers Python: 15
- Fichiers JavaScript: 8
- Fichiers HTML: 3
- Extensions de fichiers:
  .py: 15
  .js: 8
  .html: 3
  .md: 2
  .json: 3
  .gitignore: 1

Lancer l'analyse avec les agents IA? (o/n): o

Lancement de l'analyse avec les agents...
Agent de détection de mauvaises pratiques enregistré
Exécution de l'agent: bad_practices

Résultats de l'analyse:
[Agent: bad_practices]
{
  "too_long_functions_count": 3,
  "unused_imports_count": 5,
  "hardcoded_credentials_count": 1,
  "details": {
    // ... détails des problèmes trouvés ...
  }
}

Sauvegarder les résultats? (j: JSON, p: Prompt LLM, b: Les deux, n: Non): b
Résultats JSON sauvegardés dans: analysis_repo_20250410_123456.json
Prompt LLM sauvegardé dans: prompt_repo_20250410_123456.txt
Vous pouvez envoyer ce prompt à un modèle de langage comme GPT-4 ou Claude pour obtenir une analyse approfondie.

Le dépôt est disponible à l'emplacement temporaire:
/tmp/tmp1234abcd

Attention: Ce répertoire sera supprimé automatiquement si vous utilisez l'orchestrateur directement.
```

2. Cloner un dépôt et obtenir des statistiques avec l'URL en argument :
```bash
python git_analyzer_cli.py --url https://github.com/user/repo.git
```

3. Cloner un dépôt, analyser le code et générer un prompt LLM :
```bash
python git_analyzer_cli.py --url https://github.com/user/repo.git --analyze --save-prompt
```

## Fonctionnalités

### Clonage de dépôts Git
- Clone le dépôt dans un répertoire temporaire
- Permet de spécifier la branche à cloner

### Analyse du code
- Détecte les fonctions trop longues (> 30 lignes)
- Identifie les imports potentiellement inutilisés
- Repère les informations d'identification codées en dur

### Statistiques du dépôt
- Nombre total de fichiers
- Nombre de fichiers par type (Python, JavaScript, HTML, etc.)
- Distribution des extensions de fichiers

### Génération de prompts LLM
L'outil génère des prompts formatés pour les modèles de langage large (LLM) qui incluent :
- Les statistiques du dépôt
- Les résultats de l'analyse des mauvaises pratiques
- Des questions pertinentes pour l'analyse du code

## Extension avec un modèle de langage (LLM)

Actuellement, l'application ne se connecte pas directement à un LLM, mais prépare un prompt structuré que vous pouvez soumettre manuellement à un service comme OpenAI GPT, Anthropic Claude, etc.

Pour une intégration future avec une LLM, vous pourriez :
1. Ajouter un nouveau fichier `llm_connector.py` pour gérer les connexions API
2. Étendre le CLI pour envoyer automatiquement le prompt généré à une LLM
3. Afficher et/ou sauvegarder la réponse dans un format facile à lire

## Notes importantes

- Les répertoires clonés sont temporaires et peuvent être supprimés automatiquement
- Pour les dépôts volumineux, le clonage peut prendre un certain temps
- Les analyses actuelles sont basiques et peuvent être étendues avec d'autres agents

## Débogage

Si vous rencontrez des erreurs :
1. Vérifiez que Git est installé et accessible depuis la ligne de commande
2. Assurez-vous que l'URL du dépôt Git est correcte et accessible
3. Vérifiez que tous les fichiers du projet sont dans le même dossier
4. Confirmez que GitPython est correctement installé
