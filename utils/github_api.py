import requests
import base64

def guardar_en_github(nombre_archivo, contenido, repo, token, usuario):
    url = f"https://api.github.com/repos/{usuario}/{repo}/contents/{nombre_archivo}"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Obtener SHA si el archivo ya existe
    response_get = requests.get(url, headers=headers)
    sha = response_get.json().get("sha") if response_get.status_code == 200 else None

    # Codificar el contenido en base64
    contenido_b64 = base64.b64encode(contenido.encode("utf-8")).decode("utf-8")

    data = {
        "message": f"Subida automática de {nombre_archivo}",
        "content": contenido_b64,
        "branch": "main"
    }
    if sha:
        data["sha"] = sha

    response = requests.put(url, headers=headers, json=data)
    return response.status_code in [200, 201]
