# Página: Resiliencia
import streamlit as st



col_1, col_2 = st.columns([8, 1])
with col_1:
    st.markdown(
        """
        <div style='background-color:#003DA5; padding: 10px; border-radius: 5px;'>
            <h2 style='color:white; text-align:center;'> Alternativas de proyecto ingresadas </h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_2:
    st.image("images/logo.png", width=120)  # Ajusta el ancho si quieres que sea más grande o pequeño

st.write("Base de datos de proyectos y alternativas de soluciòn ingresadas")

usuario_actual = st.session_state.usuario
proyectos_usuario = st.session_state.usuarios.get(usuario_actual, [])

if st.button("📥 Exportar proyectos de este usuario"):
    if not proyectos_usuario:
        st.warning("No hay proyectos guardados para este usuario.")
    else:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            for p in proyectos_usuario:
                prefix = f"ID_{p['ID']}_"
                # Hoja proyecto, IRD, subfactores, recomendaciones...
                # (como en el código anterior)

        output.seek(0)
        st.download_button("📥 Descargar Excel", data=output, file_name=f"proyectos_{usuario_actual}.xlsx")
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
