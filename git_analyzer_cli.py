#!/usr/bin/env python
"""
CLI pour cloner et analyser un dépôt Git à l'aide d'agents d'IA.
"""
import sys
import os
import argparse
import json
from datetime import datetime

# Imports directs pour tous les fichiers dans le même dossier
from git_connector import clone_repository, list_files
from bad_practice_agent import BadPracticeAgent
from orchestrator import AgentOrchestrator

# Vérification que GitPython est installé
try:
    import git
except ImportError:
    print("Le package GitPython n'est pas installé.")
    print("Installez-le avec: pip install GitPython")
    sys.exit(1)

def clone_repo(repo_url, branch="main"):
    """Cloner un dépôt et retourner son chemin"""
    print(f"Clonage du dépôt {repo_url}, branche {branch}...")
    return clone_repository(repo_url, branch=branch)

def get_repo_stats(repo_path):
    """Obtenir des statistiques basiques sur le dépôt"""
    all_files = list_files(repo_path)
    py_files = list_files(repo_path, extension=".py")
    js_files = list_files(repo_path, extension=".js")
    html_files = list_files(repo_path, extension=".html")
    json_files = list_files(repo_path, extension=".json")
    
    return {
        "total_files": len(all_files),
        "python_files": len(py_files),
        "javascript_files": len(js_files),
        "html_files": len(html_files),
        "json_files": len(json_files),
        "file_extensions": get_file_extensions(all_files)
    }

def get_file_extensions(file_list):
    """Compter les occurrences de chaque extension de fichier"""
    extensions = {}
    for file in file_list:
        ext = os.path.splitext(file)[1]
        if ext:
            if ext in extensions:
                extensions[ext] += 1
            else:
                extensions[ext] = 1
    return extensions

def run_agents_analysis(repo_path):
    """Exécuter les agents d'analyse sur le dépôt"""
    orchestrator = AgentOrchestrator()
    
    # Enregistrer les agents disponibles
    try:
        bad_practice_agent = BadPracticeAgent()
        orchestrator.register_agent(bad_practice_agent)
        print("Agent de détection de mauvaises pratiques enregistré")
        
        # Ici, vous pourriez enregistrer d'autres agents d'analyse
        # orchestrator.register_agent(pattern_detection_agent)
        # orchestrator.register_agent(metrics_agent)
        
        # Lancer l'analyse sans cloner à nouveau (nous avons déjà le chemin du dépôt)
        results = {}
        for agent in orchestrator.agents:
            print(f"Exécution de l'agent: {agent.name}")
            results[agent.name] = agent.analyze(repo_path)
        
        return results
    
    except Exception as e:
        print(f"Erreur lors de l'analyse par agents: {e}")
        return {"error": str(e)}

def save_results(repo_url, repo_path, stats, agent_results=None):
    """Sauvegarder les résultats dans un fichier JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    filename = f"analysis_{repo_name}_{timestamp}.json"
    
    results = {
        "repository": {
            "url": repo_url,
            "path": repo_path,
            "analysis_date": datetime.now().isoformat()
        },
        "statistics": stats
    }
    
    if agent_results:
        results["agent_analysis"] = agent_results
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"Résultats sauvegardés dans {filename}")
    return filename

def create_llm_prompt(stats, agent_results=None):
    """Crée un prompt formaté pour un LLM"""
    prompt = "Analyse de dépôt Git\n\n"
    
    # Ajouter les statistiques
    prompt += "Statistiques du dépôt:\n"
    prompt += f"- Nombre total de fichiers: {stats['total_files']}\n"
    prompt += f"- Fichiers Python: {stats['python_files']}\n"
    prompt += f"- Fichiers JavaScript: {stats['javascript_files']}\n"
    prompt += f"- Fichiers HTML: {stats['html_files']}\n"
    prompt += "- Extensions de fichiers:\n"
    
    for ext, count in stats['file_extensions'].items():
        prompt += f"  {ext}: {count}\n"
    
    # Ajouter les résultats d'analyse
    if agent_results and "bad_practices" in agent_results:
        bad_practices = agent_results["bad_practices"]
        prompt += "\nDétection de mauvaises pratiques:\n"
        prompt += f"- Fonctions trop longues: {bad_practices['too_long_functions_count']}\n"
        prompt += f"- Imports inutilisés: {bad_practices['unused_imports_count']}\n"
        prompt += f"- Informations d'identification codées en dur: {bad_practices['hardcoded_credentials_count']}\n"
        
        # Ajouter des détails spécifiques
        if bad_practices['details']['too_long_functions']:
            prompt += "\nFonctions trop longues:\n"
            for func in bad_practices['details']['too_long_functions'][:5]:  # Limiter à 5 exemples
                prompt += f"- {func}\n"
                
        if bad_practices['details']['hardcoded_credentials']:
            prompt += "\nFichiers avec informations d'identification codées en dur:\n"
            for file in bad_practices['details']['hardcoded_credentials'][:5]:
                prompt += f"- {file}\n"
    
    # Ajouter des questions pour le LLM
    prompt += "\nEn tant qu'expert en développement logiciel, analyse ce dépôt et réponds aux questions suivantes:\n"
    prompt += "1. Quels problèmes potentiels peux-tu identifier dans ce code?\n"
    prompt += "2. Quelles améliorations recommanderais-tu pour ce projet?\n"
    prompt += "3. Y a-t-il des patterns ou anti-patterns de conception évidents?\n"
    prompt += "4. Quelle est la qualité globale du code de ce projet?\n"
    
    return prompt

def main():
    # Configurer le parser d'arguments
    parser = argparse.ArgumentParser(description='Analyseur de dépôt Git avec agents IA')
    parser.add_argument('--url', type=str, help='URL du dépôt Git à cloner')
    parser.add_argument('--branch', type=str, default='main', help='Branche à cloner (défaut: main)')
    parser.add_argument('--analyze', action='store_true', help='Exécuter les agents d\'analyse')
    parser.add_argument('--stats-only', action='store_true', help='Afficher uniquement les statistiques')
    parser.add_argument('--save-prompt', action='store_true', help='Générer un prompt pour LLM')
    args = parser.parse_args()
    
    print("=== Analyseur de dépôt Git avec agents IA ===")
    
    # Obtenir l'URL du dépôt
    repo_url = args.url
    if not repo_url:
        repo_url = input("Entrez l'URL du dépôt Git à cloner: ")
    
    if not repo_url:
        print("Erreur: URL non fournie.")
        return
    
    # Obtenir la branche
    branch = args.branch
    if not args.url:  # Si l'URL n'était pas fournie en argument, demander aussi la branche
        branch_input = input(f"Entrez le nom de la branche (laissez vide pour '{branch}'): ")
        if branch_input:
            branch = branch_input
    
    # Cloner le dépôt
    repo_path = clone_repo(repo_url, branch)
    
    if not repo_path:
        print("Échec du clonage du dépôt.")
        return
    
    print(f"Dépôt cloné avec succès dans: {repo_path}")
    
    # Obtenir les statistiques
    stats = get_repo_stats(repo_path)
    print("\nStatistiques du dépôt:")
    print(f"- Nombre total de fichiers: {stats['total_files']}")
    print(f"- Fichiers Python: {stats['python_files']}")
    print(f"- Fichiers JavaScript: {stats['javascript_files']}")
    print(f"- Fichiers HTML: {stats['html_files']}")
    print("- Extensions de fichiers:")
    for ext, count in stats['file_extensions'].items():
        print(f"  {ext}: {count}")
    
    # Lancer l'analyse si demandé
    agent_results = None
    if args.analyze or (not args.stats_only and 
                      input("\nLancer l'analyse avec les agents IA? (o/n): ").lower() == 'o'):
        print("\nLancement de l'analyse avec les agents...")
        agent_results = run_agents_analysis(repo_path)
        
        if agent_results and "error" not in agent_results:
            print("\nRésultats de l'analyse:")
            for agent_name, results in agent_results.items():
                print(f"\n[Agent: {agent_name}]")
                print(json.dumps(results, indent=2))
    
    # Sauvegarder les résultats
    save_option = args.save_prompt or input("\nSauvegarder les résultats? (j: JSON, p: Prompt LLM, b: Les deux, n: Non): ").lower()
    
    if save_option in ['j', 'b'] or save_option == 'o':
        result_file = save_results(repo_url, repo_path, stats, agent_results)
        print(f"Résultats JSON sauvegardés dans: {result_file}")
    
    if save_option in ['p', 'b']:
        prompt = create_llm_prompt(stats, agent_results)
        prompt_file = f"prompt_{repo_url.split('/')[-1].replace('.git', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
            
        print(f"Prompt LLM sauvegardé dans: {prompt_file}")
        print("Vous pouvez envoyer ce prompt à un modèle de langage comme GPT-4 ou Claude pour obtenir une analyse approfondie.")
    
    print("\nLe dépôt est disponible à l'emplacement temporaire:")
    print(repo_path)
    print("\nAttention: Ce répertoire sera supprimé automatiquement si vous utilisez l'orchestrateur directement.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOpération annulée par l'utilisateur.")
    except Exception as e:
        print(f"\nErreur inattendue: {e}")