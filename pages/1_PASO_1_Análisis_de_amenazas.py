import streamlit as st
import geopandas as gpd
from shapely.geometry import Point
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import folium
from streamlit_folium import st_folium
import zipfile, tempfile, os

st.set_page_config(page_title="Verificador RRD", layout="wide")

# --- FUNCIÓN PARA LEER KML O KMZ ---
def leer_kml_kmz(ruta_archivo):
    if ruta_archivo.endswith('.kml'):
        return gpd.read_file(ruta_archivo)
    elif ruta_archivo.endswith('.kmz'):
        with tempfile.TemporaryDirectory() as tmpdirname:
            with zipfile.ZipFile(ruta_archivo, 'r') as zip_ref:
                zip_ref.extractall(tmpdirname)
                for nombre_archivo in zip_ref.namelist():
                    if nombre_archivo.endswith(".kml"):
                        kml_path = os.path.join(tmpdirname, nombre_archivo)
                        return gpd.read_file(kml_path)
        st.error("❌ No se encontró archivo KML dentro del KMZ.")
        return None
    else:
        st.error("❌ El archivo debe ser .kml o .kmz")
        return None

# --- TÍTULO Y DESCRIPCIÓN ---
st.title("🌍 PASO 1: Cruce de capas de amenazas")
st.markdown("Haz clic en el mapa o escribe una dirección para verificar si se intersecta con zonas de amenaza (Cota 30 m).")
col1, col2= st.columns(2)
with col1: 
    
    direccion = st.text_input("📍 Dirección (opcional):")
    lat, lon = None, None

    if direccion:
        try:
            geolocator = Nominatim(user_agent="ird_app")
            location = geolocator.geocode(direccion, timeout=10)
            if location:
                lat, lon = location.latitude, location.longitude
                st.session_state["lat"] = lat
                st.session_state["lon"] = lon
                st.success(f"📌 Coordenadas de dirección: {lat:.5f}, {lon:.5f}")
                
        except GeocoderTimedOut:
                    st.warning("⚠️ El servicio de geocodificación demoró demasiado.")

# MAPA DE SELECCIÓN
    map_center = [st.session_state.get("lat", -33.45), st.session_state.get("lon", -70.65)]
    m = folium.Map(location=map_center, zoom_start=12)
    m.add_child(folium.LatLngPopup())
    st_map = st_folium(m, width=700, height=450)

    if st_map and st_map.get("last_clicked"):
        lat = st_map["last_clicked"]["lat"]
        lon = st_map["last_clicked"]["lng"]
        st.session_state["lat"] = lat
        st.session_state["lon"] = lon
        st.success(f"🖱️ Coordenadas seleccionadas: {lat:.5f}, {lon:.5f}")

# BOTÓN VERIFICAR INTERSECCIÓN
    if "lat" in st.session_state and "lon" in st.session_state:
        lat = st.session_state["lat"]
        lon = st.session_state["lon"]

        if st.button("🔍 Verificar intersección con Cota 30"):
            punto = Point(lon, lat)
            punto_gdf = gpd.GeoDataFrame(geometry=[punto], crs="EPSG:4326")
            buffer = punto_gdf.to_crs(epsg=32719).buffer(50).to_crs(epsg=4326)

            ruta_cota30 = "data/Área_de_Evacuació_LayerToKML.kmz"
            gdf_cota30 = leer_kml_kmz(ruta_cota30)

            if gdf_cota30 is not None:
                intersecta = gdf_cota30[gdf_cota30.geometry.intersects(buffer.iloc[0])]
                st.session_state["buffer"] = buffer
                st.session_state["gdf_cota30"] = gdf_cota30
                st.session_state["intersecta"] = not intersecta.empty

# SI YA SE EJECUTÓ LA VERIFICACIÓN, MOSTRAR MAPA
with col2: 
    if "buffer" in st.session_state and "gdf_cota30" in st.session_state:
        st.markdown("### 📌 Análisis espacial")
        m2 = folium.Map(location=[st.session_state["lat"], st.session_state["lon"]], zoom_start=15)
        folium.Marker([st.session_state["lat"], st.session_state["lon"]], tooltip="Ubicación").add_to(m2)
        folium.GeoJson(st.session_state["buffer"].geometry[0], style_function=lambda x: {
            "fillColor": "blue", "color": "blue", "fillOpacity": 0.1, "weight": 2
            }).add_to(m2)
        folium.GeoJson(st.session_state["gdf_cota30"].geometry, style_function=lambda x: {
            "fillColor": "red", "color": "red", "weight": 1
            }).add_to(m2)
        st_folium(m2, width=700, height=400)

        aplicar_ird = st.session_state["intersecta"]

        if aplicar_ird:
            st.warning("⚠️ La ubicación **SE CRUZA** con zona de amenaza. Debe aplicar la Metodología complementaria para la evaluación del riesgo de desastres y calcular el Índice de Riesgo de DEsastres (RRD).")
        else:
                st.success("✅ La ubicación **NO** se cruza con zona de amenaza (Cota 30 m).")



