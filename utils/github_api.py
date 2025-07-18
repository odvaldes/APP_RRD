# utils/github_api.py
import requests
import base64

def guardar_en_github(nombre_archivo, contenido, repo, token, usuario):
    url = f"https://api.github.com/repos/{usuario}/{repo}/contents/{nombre_archivo}"
    headers = {"Authorization": f"token {token}"}

    contenido_bytes = base64.b64encode(contenido.encode()).decode("utf-8")

    data = {
        "message": f"Guardar {nombre_archivo}",
        "content": contenido_bytes
    }

    response = requests.put(url, json=data, headers=headers)
    return response.status_code in [201, 200]  # 200 si se reemplaza un archivo existente
