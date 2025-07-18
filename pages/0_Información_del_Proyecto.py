# Página: Información del Proyecto
import streamlit as st
# --- Banner con Título a la izquierda y Logo a la derecha ---
col_1, col_2 = st.columns([8, 1])
with col_1:
    st.markdown(
        """
        <div style='background-color:#003DA5; padding: 10px; border-radius: 5px;'>
            <h2 style='color:white; text-align:center;'>📁 Información del Proyecto</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_2:
    st.image("images/logo.png", width=120)  # Ajusta el ancho si quieres que sea más grande o pequeño




col1, col2 = st.columns([5, 1])

with col1:
    nombre_proyecto = st.text_input("1.1 Nombre del proyecto", max_chars=100)
with col2:
    codigo_bip = st.text_input("1.2 Código BIP", max_chars=20)
    
    
region= st.text_input("1.3 Región", max_chars=100)
comuna= st.text_input("1.4 Comuna", max_chars=100) 
sector= st.text_input("1.5 sector", max_chars=100)

descripcion_proyecto = st.text_area("1.6 Descripción del proyecto", max_chars=3000)

Alternativa_solucion = st.text_area("1.7 Descripción alternativa de solución", max_chars=3000)

import uuid

if st.button("💾 Guardar Información del Proyecto"):

    # Verifica que el usuario esté autenticado
    if 'usuario' not in st.session_state or not st.session_state.usuario:
        st.warning("⚠️ Debes iniciar sesión para guardar datos.")
        st.stop()

    usuario = st.session_state.usuario

    # Inicializa el contenedor si no existe
    if 'proyectos' not in st.session_state:
        st.session_state.proyectos = {}
    if usuario not in st.session_state.proyectos:
        st.session_state.proyectos[usuario] = []

    # Si no hay un proyecto actual en construcción, crear uno
    if 'proyecto_actual' not in st.session_state:
        nuevo_id = str(uuid.uuid4())[:8]
        st.session_state.proyecto_actual = {
            'ID': nuevo_id
        }

    # Agregar información del proyecto al objeto actual
    st.session_state.proyecto_actual.update({
        'Nombre Proyecto': nombre_proyecto,
        'Código BIP': codigo_bip,
        'Región': region,
        'Comuna': comuna,
        'Sector': sector,
        'Descripción Proyecto': descripcion_proyecto,
        'Alternativa de Solución': Alternativa_solucion
    })

    st.success("✅ Información del proyecto guardada correctamente.")
    
    import json
from utils.github_api import guardar_en_github

# Solo si ya existe proyecto_actual
if 'proyecto_actual' in st.session_state:
    proyecto_json = json.dumps(st.session_state.proyecto_actual, indent=2)
    nombre_archivo = f"{usuario}_proyecto_{st.session_state.proyecto_actual['ID']}.json"
    repo = "NOMBRE_DEL_REPO"
    usuario_github = "TU_USUARIO"
    token_github = st.secrets["github_token"]  # o directamente "ghp_xxx..." si no usas secrets

    exito = guardar_en_github(nombre_archivo, proyecto_json, repo, token_github, usuario_github)
    if exito:
        st.success("✅ Proyecto guardado también en GitHub")
    else:
        st.warning("⚠️ No se pudo guardar en GitHub")

