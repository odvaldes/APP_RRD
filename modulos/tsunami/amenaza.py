import streamlit as st
import geopandas as gpd
import zipfile, os, tempfile, uuid

import folium
from streamlit_folium import st_folium

def app():
    st.title("IRD Tsunami - Amenaza")
    st.write("Evaluación de amenaza por tsunami.")

    # --- ARCHIVOS ---
    uploaded_curves = st.file_uploader('🔴 Curvas de altura de tsunami (KML/KMZ)', type=['kml', 'kmz'])
    uploaded_project = st.file_uploader('🟦 Polígono del proyecto (KML/KMZ)', type=['kml', 'kmz'])

    def read_kml_or_kmz(uploaded_file):
        if uploaded_file.name.endswith('.kml'):
            return gpd.read_file(uploaded_file)
        elif uploaded_file.name.endswith('.kmz'):
            with tempfile.TemporaryDirectory() as tmpdirname:
                kmz_path = os.path.join(tmpdirname, 'temp.kmz')
                with open(kmz_path, 'wb') as f:
                    f.write(uploaded_file.read())
                with zipfile.ZipFile(kmz_path, 'r') as zip_ref:
                    zip_ref.extractall(tmpdirname)
                for root, _, files in os.walk(tmpdirname):
                    for name in files:
                        if name.endswith('.kml'):
                            return gpd.read_file(os.path.join(root, name))
        return None

    # --- LÓGICA DE AMENAZA ---
    mapeo_categorias = {
        'Profundidad de la inundación: 6 y más': 'Muy Alto',
        'Profundidad de la inundación: 4 - 6': 'Muy Alto',
        'Profundidad de la inundación: 2 - 4': 'Alto',
        'Profundidad de la inundación: 1 - 2': 'Medio',
        'Profundidad de la inundación: 0.3 - 1': 'Bajo',
        'Sin inundación': 'Nulo'
    }
    valores_amenaza = {'Muy Alto': 1, 'Alto': 0.8426, 'Medio': 0.5579, 'Bajo': 0.101, 'Nulo': 0}

    categoria_amenaza = 'Nulo'
    valor_amenaza = 0
    gdf_curves, gdf_project = None, None

    if uploaded_curves:
        gdf_curves = read_kml_or_kmz(uploaded_curves)
        if gdf_curves is not None:
            gdf_curves = gdf_curves.to_crs(epsg=4326)

    if uploaded_project:
        gdf_project = read_kml_or_kmz(uploaded_project)
        if gdf_project is not None:
            gdf_project = gdf_project.to_crs(epsg=4326)

            st.markdown("#### 🗺️ Mapa del Proyecto y Curvas de Inundación")
            m = folium.Map(
                location=[gdf_project.geometry.centroid.y.mean(), gdf_project.geometry.centroid.x.mean()],
                zoom_start=13
            )
            folium.GeoJson(gdf_project, style_function=lambda x: {'color': 'blue'}).add_to(m)

            if gdf_curves is not None:
                folium.GeoJson(gdf_curves, style_function=lambda x: {'color': 'red', 'weight': 1, 'fillOpacity': 0.1}).add_to(m)

            intersect = gdf_curves[gdf_curves.geometry.intersects(gdf_project.geometry.unary_union)] if gdf_curves is not None else None
            if intersect is not None and not intersect.empty:
                categorias = intersect['Name'].unique().tolist()
                categorias_convertidas = [mapeo_categorias.get(c, 'Nulo') for c in categorias]
                categoria_amenaza = max(categorias_convertidas, key=lambda x: valores_amenaza.get(x, 0))
                valor_amenaza = valores_amenaza[categoria_amenaza]
                folium.GeoJson(intersect, style_function=lambda x: {'color': 'green'}).add_to(m)
                st.success(f"✅ Amenaza asignada: **{categoria_amenaza}** (valor: {valor_amenaza})")
            else:
                st.warning("⚠️ El polígono no intersecta ninguna zona de amenaza. Amenaza = Nulo.")

            st_folium(m, width=650, height=450)

    # --- JUSTIFICACIÓN Y ENLACE ---
    col1, col2 = st.columns(2)
    with col1:
        justificacion = st.text_area("✍️ Justificación de la Amenaza (con fuente)", placeholder="Ej: Según carta CITSU de Valparaíso 2022...")
    with col2:
        st.markdown("""
        <p style='font-size:13px;'>Consulta las cartas <b>CITSU</b> oficiales:<br>
        <a href='https://www.shoa.cl/php/citsu.php' target='_blank'>https://www.shoa.cl/php/citsu.php</a></p>
        """, unsafe_allow_html=True)

    col_guardar, col_siguiente = st.columns(2)

    with col_guardar:
        if st.button("💾 Guardar Amenaza"):
            guardar_amenaza(categoria_amenaza, valor_amenaza, justificacion)

    with col_siguiente:
        if st.button("⏭️ Siguiente: Vulnerabilidad"):
            guardar_amenaza(categoria_amenaza, valor_amenaza, justificacion)
            st.session_state["tsunami"] = "Vulnerabilidad"
            st.experimental_rerun()


def guardar_amenaza(categoria, valor, justificacion):
    if 'usuario' not in st.session_state or not st.session_state.usuario:
        st.warning("⚠️ Debes iniciar sesión para guardar datos.")
        return

    if 'proyectos' not in st.session_state:
        st.session_state.proyectos = {}
    if st.session_state.usuario not in st.session_state.proyectos:
        st.session_state.proyectos[st.session_state.usuario] = []

    nombre_proyecto = st.session_state.get('nombre_proyecto', f"Proyecto_{uuid.uuid4().hex[:6]}")

    datos_amenaza = {
        'categoria_amenaza': categoria,
        'valor_amenaza': valor,
        'justificacion_amenaza': justificacion
    }

    proyecto = {
        'Nombre Proyecto': nombre_proyecto,
        'Amenaza': datos_amenaza
    }

    st.session_state.proyectos[st.session_state.usuario].append(proyecto)
    st.success("✅ Amenaza guardada correctamente.")
