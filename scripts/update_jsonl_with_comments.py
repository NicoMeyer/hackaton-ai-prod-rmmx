import requests
import os
import json
import pdb

# Variables necesarias para la autenticación y el acceso
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PR_NUMBER = os.getenv("PR_NUMBER")
REPO_NAME = 'NicoMeyer/hackaton-ai-prod-rmmx'

# Archivo JSONL donde se guardarán los comentarios
JSONL_FILE = "comments.jsonl"

# API URL para obtener los comentarios del PR
API_URL = f"https://api.github.com/repos/{REPO_NAME}/pulls/{PR_NUMBER}/comments"

# Obtener los comentarios del PR desde la API de GitHub
def get_pr_comments():
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(API_URL, headers=headers)
    
    if response.status_code == 200:
        print(response.json())
        
        return response.json()
    else:
        print(f"Error al obtener los comentarios: {response.status_code}")
        return []

# Verificar las reacciones de un comentario
def analyze_comment_reactions(comment):
    positive_reactions = comment["reactions"]["+1"]
    negative_reactions = comment["reactions"]["-1"]

    if positive_reactions > 0 and negative_reactions == 0:
        return "Comentario válido"
    elif negative_reactions > 0 and positive_reactions == 0:
        return "Comentario inválido"
    return None  # Si tiene reacciones mixtas o no tiene reacciones

# Procesar y actualizar el archivo JSONL
def update_jsonl_file(comments):
    with open(JSONL_FILE, "a", encoding="utf-8") as f:
        for comment in comments:
            # Obtener el contenido de diff_hunk y body, y las reacciones
            diff_hunk = comment.get("diff_hunk")
            body = comment.get("body")
            analysis_result = analyze_comment_reactions(comment)
            
            # Solo agregar comentarios con reacciones válidas o inválidas
            if analysis_result and diff_hunk and body:
                entry = {
                    "prompt": diff_hunk,  # Usar diff_hunk como prompt
                    "completion": f"{analysis_result}: {body}"  # Usar body como parte de completion
                }
                # Escribir el JSON con ensure_ascii=False para que no escape caracteres especiales
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# Obtener y procesar los comentarios del PR
comments = get_pr_comments()
if comments:
    update_jsonl_file(comments)
else:
    print("No hay comentarios para procesar.")