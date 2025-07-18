import streamlit as st
import pandas as pd
import uuid
from utils.github_api import guardar_en_github

# --- Constants for subfactors (move outside the function to avoid redefinition) ---
SUBFACTORES_FISICA = [
    ('Material estructura principal', 0.174534907, {'Seleccionar escala': 0, 'Alto': 1, 'Moderado': 0.53, 'Bajo': 0.22, 'Sin Información': 1}),
    ('Estado actual', 0.104720944, {'Seleccionar escala': 0, 'Malo': 1, 'Bueno': 0, 'Obra Nueva': 0, 'Sin Información': 1}),
    ('Plan de mantenimiento', 0.032206441, {'Seleccionar escala': 0, 'No': 1, 'Si': 0, 'Sin Información': 1})
]
SUBFACTORES_FUNCIONAL = [
    ('Criticidad del servicio', 0.24964993, {'Seleccionar escala': 0, 'Alto': 1, 'Medio': 0.7157, 'Bajo': 0.3461, 'No crítico': 0.1344}),
    ('Incidencia del servicio en la economía local', 0.083216643, {'Seleccionar escala': 0, 'Alto': 1, 'Medio': 0.2154, 'Baja': 0.116, 'Sin Incidencia': 0, 'Sin Información': 1})
]
SUBFACTORES_SOCIAL = [
    ('Grupos etarios vulnerables', 0.052710542, {'Seleccionar escala': 0, 'Personas dependientes': 1, 'Niño o adolescentes': 0.6711, 'Adultos': 0, 'Sin Información': 1}),
    ('Dependencia física población', 0.037507502, {'Seleccionar escala': 0, 'Atiende': 1, 'No atiende': 0, 'Sin Información': 1}),
    ('Población afectada', 0.133626725, {'Seleccionar escala': 0, 'Muy alto': 1, 'Alto': 0.6968, 'Medio': 0.3742, 'Bajo': 0.1987, 'Muy bajo': 0.0869, 'Sin Información': 1}),
    ('Pobreza por ingresos', 0.065913183, {'Seleccionar escala': 0, 'Alto': 1, 'Moderado': 0.6357, 'Bajo': 0.1005, 'Nulo': 0, 'Sin Información': 1}),
    ('Pobreza multidimensional', 0.065913183, {'Seleccionar escala': 0, 'Alto': 1, 'Moderado': 0.6357, 'Bajo': 0.1005, 'Nulo': 0, 'Sin Información': 1})
]

def app():
    st.title("IRD Tsunami - Vulnerabilidad")
    st.write("Formulario para evaluar vulnerabilidad física, funcional y social.")

    st.markdown("""
    <p style='font-size:20px;'>Selecciona la escala correspondiente para cada subfactor:</p>
    <p style='font-size:12px;'>📥 <a href='https://sni.gob.cl/storage/docs/Manual_de_escalas_IRD_amenaza_por_Tsunami_-sep2022.pdf' target='_blank'>
    Manual de Escalas IRD - Tsunami</a></p>
    """, unsafe_allow_html=True)

    # Use session state to store form responses and only recompute on change.
    if "vul_form" not in st.session_state:
        st.session_state.vul_form = {}

    def render_selectboxes(subfactores, prefix):
        valores = []
        pesos = []
        registros = []
        for nombre, peso, opciones in subfactores:
            key = f"{prefix}_{nombre}"
            default = list(opciones.keys())[0]
            seleccion = st.selectbox(nombre, list(opciones.keys()), key=key)
            st.session_state.vul_form[key] = seleccion
            valores.append(opciones[seleccion])
            pesos.append(peso)
            registros.append({'Subfactor': nombre, 'Escala': seleccion, 'Peso': peso, 'Valor': opciones[seleccion]})
        return valores, pesos, registros

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("##### a) Vulnerabilidad Física")
        valores_fis, pesos_fis, registros_fis = render_selectboxes(SUBFACTORES_FISICA, 'fis')
    with col2:
        st.markdown("##### b) Vulnerabilidad Funcional")
        valores_fun, pesos_fun, registros_fun = render_selectboxes(SUBFACTORES_FUNCIONAL, 'fun')
    with col3:
        st.markdown("##### c) Vulnerabilidad Social")
        valores_soc, pesos_soc, registros_soc = render_selectboxes(SUBFACTORES_SOCIAL, 'soc')

    # --- Calculation (lightweight, no need to cache) ---
    vulnerabilidad_pesos = pesos_fis + pesos_fun + pesos_soc
    vulnerabilidad_valores = valores_fis + valores_fun + valores_soc
    registros = registros_fis + registros_fun + registros_soc
    valor_total_vul = sum([p * v for p, v in zip(vulnerabilidad_pesos, vulnerabilidad_valores)])

    # --- Only create DataFrame if something changed (lightweight in this case) ---
    df_vulnerabilidad = pd.DataFrame(registros)

    st.markdown("#### Resultado de Vulnerabilidad")
    st.dataframe(df_vulnerabilidad, use_container_width=True)
    st.metric("Vulnerabilidad total", f"{valor_total_vul:.4f}")

    justificacion_vul = st.text_area("✍️ Justificación de la evaluación de vulnerabilidad")

    col_guardar, col_siguiente = st.columns(2)

    def guardar_en_sesion(valor_total_vul, df_vulnerabilidad, justificacion_vul):
        # Guardar en sesión interna
        st.session_state['vulnerabilidad_data'] = {
            'vulnerabilidad': valor_total_vul,
            'vuln_df': df_vulnerabilidad.to_dict(orient="records"),
            'justificacion_vul': justificacion_vul
        }
        # Guardar también en proyecto actual si existe
        if 'usuario' not in st.session_state or not st.session_state.usuario:
            st.warning("⚠️ Debes iniciar sesión para guardar datos.")
            return

        if 'proyectos' not in st.session_state:
            st.session_state.proyectos = {}
        if st.session_state.usuario not in st.session_state.proyectos:
            st.session_state.proyectos[st.session_state.usuario] = []

        nombre_proyecto = st.session_state.get('nombre_proyecto', f"Proyecto_{uuid.uuid4().hex[:8]}")
        proyecto = {
            'Nombre Proyecto': nombre_proyecto,
            'Vulnerabilidad': {
                'valor': valor_total_vul,
                'detalle': df_vulnerabilidad.to_dict(orient="records"),
                'justificacion': justificacion_vul
            }
        }

        st.session_state.proyectos[st.session_state.usuario].append(proyecto)
        st.success("✅ Vulnerabilidad guardada correctamente.")

    with col_guardar:
        if st.button("💾 Guardar Vulnerabilidad"):
            guardar_en_sesion(valor_total_vul, df_vulnerabilidad, justificacion_vul)

    with col_siguiente:
        if st.button("⏭️ Siguiente: Resiliencia"):
            guardar_en_sesion(valor_total_vul, df_vulnerabilidad, justificacion_vul)
            st.session_state["tsunami"] = "Resiliencia"
            st.experimental_rerun()

    st.session_state.proyectos[st.session_state.usuario].append(proyecto)
    st.success("✅ Vulnerabilidad guardada correctamente.")
