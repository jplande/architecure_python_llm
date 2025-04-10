import shutil
from git_connector import clone_repository, list_files

class AgentOrchestrator:
    def __init__(self):
        self.agents = []
        
    def register_agent(self, agent):
        self.agents.append(agent)
        
    def start_analysis(self, repo_url):
        """
        Démarre l'analyse d'un dépôt git
        """
        results = {}
        
        # Cloner le dépôt
        repo_path = clone_repository(repo_url)
        
        if not repo_path:
            return {"error": "Failed to clone repository"}
        
        try:
            # Exécuter chaque agent
            for agent in self.agents:
                agent_results = agent.analyze(repo_path)
                results[agent.name] = agent_results
                
            return results
        finally:
            # Nettoyage: Supprimer le dépôt cloné
            shutil.rmtree(repo_path, ignore_errors=True)