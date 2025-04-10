import re
from git_connector import list_files

class BadPracticeAgent:
    def __init__(self):
        self.name = "bad_practices"
        
    def analyze(self, repo_path):
        """
        Détecte les mauvaises pratiques basiques dans le code
        """
        python_files = list_files(repo_path, extension=".py")
        
        bad_practices = {
            "too_long_functions": [],
            "unused_imports": [],
            "hardcoded_credentials": [],
        }
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    lines = content.split('\n')
                    
                    # Détecter les imports potentiellement non utilisés
                    imports = re.findall(r"import\s+(\w+)", content)
                    for imp in imports:
                        if imp not in content.replace(f"import {imp}", ""):
                            rel_path = file_path.replace(repo_path, "").lstrip("/\\")
                            bad_practices["unused_imports"].append(f"{rel_path}: {imp}")
                    
                    # Détecter des mots de passe codés en dur (simpliste)
                    if re.search(r"password\s*=\s*['\"]", content, re.IGNORECASE) or re.search(r"api_key\s*=\s*['\"]", content, re.IGNORECASE):
                        rel_path = file_path.replace(repo_path, "").lstrip("/\\")
                        bad_practices["hardcoded_credentials"].append(rel_path)
                    
                    # Détecter les fonctions trop longues
                    current_func = None
                    func_start_line = 0
                    func_lines = 0
                    
                    for i, line in enumerate(lines):
                        if re.match(r"^\s*def\s+(\w+)\s*\(", line):
                            if current_func and func_lines > 30:  # Seuil arbitraire de 30 lignes
                                rel_path = file_path.replace(repo_path, "").lstrip("/\\")
                                bad_practices["too_long_functions"].append(f"{rel_path}: {current_func} ({func_lines} lines)")
                            
                            current_func = re.match(r"^\s*def\s+(\w+)\s*\(", line).group(1)
                            func_start_line = i
                            func_lines = 0
                        
                        if current_func:
                            func_lines += 1
                    
                    # Vérifier la dernière fonction du fichier
                    if current_func and func_lines > 30:
                        rel_path = file_path.replace(repo_path, "").lstrip("/\\")
                        bad_practices["too_long_functions"].append(f"{rel_path}: {current_func} ({func_lines} lines)")
                        
            except Exception as e:
                print(f"Error analyzing bad practices in {file_path}: {e}")
        
        # Compter les occurrences
        summary = {
            "too_long_functions_count": len(bad_practices["too_long_functions"]),
            "unused_imports_count": len(bad_practices["unused_imports"]),
            "hardcoded_credentials_count": len(bad_practices["hardcoded_credentials"]),
            "details": bad_practices
        }
        
        return summary