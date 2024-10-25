import argparse
import openai
import os
import requests
import json
import random
import traceback
from github import Github, PullRequest

github_client: Github
parameters: dict

def prompt_ia():
    prompt = """
    Tienes que realizar el code review de un Pull Request para una webapp. Tu enfoque debe ser analizar los cambios en los archivos proporcionados. A continuación te detallo el proceso:
    Archivos a revisar: Recibirás dos archivos. Uno con los cambios realizados y otro sin cambios. Concéntrate únicamente en las diferencias (diff) entre ambos.
    Entrega de feedback: Debes partir agregando tus propuestas como sugerencias de codigo a cambiar sin pasar punto por punto de los criterios. Es prioritario que tus respuestas deben ser breves, concisas y enfocarse en los puntos de mejora con código. las secciones de código que me sugieras puedes decirlo de la siguiente forma:

        - file_path: <nombre_del_archivo>
        - line: <número_de_línea>
        - review_title: <título breve>
        - review_content: <sugerencia de mejora sin explicación extensa>
        - suggested_code_changes: <fragmento de código optimizado o mejora sugerida>
    además mostrarme el ejemplo en una sección de código
    Claridad: El código debe ser fácil de leer. Asegúrate de que las variables y funciones tengan nombres autodescriptivos y evita malas prácticas. Los métodos deben seguir el principio de responsabilidad única. La estructura de control de recursos debe ser sencilla, evitando problemas como deadlocks.
    Correctitud: El código debe hacer lo que se espera. No sirve de nada si es rápido pero no cumple con su propósito.
    Eficiencia: Una vez que el código sea claro y correcto, revisa si es eficiente. Evita algoritmos con complejidad excesiva como O(n^3) y ejecución de queries con n+1.
    Flexibilidad: Revisa si el código es desacoplado y flexible. Puede ser útil para futuros cambios.
    Seguridad: Finalmente, asegúrate de que el código no tenga vulnerabilidades, como SQL Injection o uso de variables de ambiente.
    Guía de estilo: Al revisar el código, sigue los principios SOLID y guíate por las guidelines de Shopify. Contamos con herramientas automáticas como RuboCop para validar el código, pero tu análisis debe ser manual y detallado. Puedes consultar las guidelines de estilo aquí: https://ruby-style-guide.shopify.dev/
    Responde en el formato json usando las claves file_path, line, review_title, review_content y suggested_code_changes.
    Ejemplo:
    ```json
    {
    "file_path": "app/models/user.rb",
    "line": 42,
    "review_title": "Uso de variable no autodescriptiva",
    "review_content": "Renombra la variable para mayor claridad.",
    "suggested_code_changes": "user_name = params[:name]"
    }
    ```
    """ 

    return prompt

def code_review(parameters: dict):
    repo = github_client.get_repo(os.getenv('GITHUB_REPOSITORY'))   
    pull_request = repo.get_pull(parameters["pr_id"])

    commits = pull_request.get_commits()

    for commit in commits:
        files = commit.files

        for file in files:
            filename = file.filename
            content = repo.get_contents(filename, ref=commit.sha).decoded_content

            try:
                json_response = openai.ChatCompletion.create(
                    model=parameters['model'],
                    messages=[
                        {
                            "role" : "user",
                            "content" : (f"{parameters['prompt']}:\n```{content}```")
                        }
                    ],
                    response_format={ "type": "json_object" },
                    temperature=parameters['temperature']
                )

                # Extrayendo respuestas estructuradas en cada cambio
                for review in json_response["choices"]:
                    body = review["message"]["content"]
                    body = json.loads(body)

                    commented_body = f"### {body['review_title']}\n{body['review_content']}\n"

                    suggested_code = body['suggested_code_changes']
                    if suggested_code != "":
                        commented_body += f"```{body['suggested_code_changes']}```"

                    pull_request.create_review_comment(
                        body = commented_body,
                        commit = commit,
                        path = filename,
                        line = body['line']
                    )

            except Exception as ex:
                message = f"🚨 Fail code review process for file **{filename}**.\n\n`{str(ex)}`\n{traceback.format_exc()}"
                pull_request.create_issue_comment(message)

def make_prompt() -> str:
    review_prompt = prompt_ia()

    return review_prompt

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--openai-api-key', help='Your OpenAI API Key')
    parser.add_argument('--github-token', help='Your Github Token')
    parser.add_argument('--github-pr-id', help='Your Github PR ID')
    parser.add_argument('--dev-lang', help='Development language used for this request')
    parser.add_argument('--openai-engine', default="gpt-3.5-turbo", help='GPT-3.5 model to use. Options: text-davinci-003, text-davinci-002, text-babbage-001, text-curie-001, text-ada-001')
    parser.add_argument('--openai-temperature', default=0.0, help='Sampling temperature to use. Higher values means the model will take more risks. Recommended: 0.5')
    parser.add_argument('--openai-max-tokens', default=4096, help='The maximum number of tokens to generate in the completion.')
    
    args = parser.parse_args()

    openai.api_key = args.openai_api_key
    github_client = Github(args.github_token)

    review_parameters = {
        "pr_id" : int(args.github_pr_id),
        "prompt" : make_prompt(),
        "temperature" : float(args.openai_temperature),
        "max_tokens" : int(args.openai_max_tokens),
        "model" : args.openai_engine
    }

    code_review(parameters=review_parameters)