# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 15:42:47 2025

@author: ovaldes
"""

import streamlit as st
import geopandas as gpd
from shapely.geometry import Point
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import folium
from streamlit_folium import st_folium
import zipfile, tempfile, os


# --- TÍTULO Y DESCRIPCIÓN ---

with st.form("form_rrd"):
    st.markdown("### 📋 Cuestionario RRD")
    preguntas = {
            "1.1": "¿Historial de eventos extremos (inundaciones, derrumbes, etc)?",
            "1.2a": "¿Sedimentación en quebradas o ríos?",
            "1.2b": "¿Interferencia con planicie de inundación?",
            "1.2c": "¿Ha sido afectada por tsunami?",
            "1.2d": "¿Cerca de pendientes altas?",
            "1.2e": "¿Cambio en flujos de agua?",
            "1.2f": "¿Erosión cercana?",
            "1.2g": "¿Problemas de drenaje cercanos?",
            "1.3a": "¿Vegetación expuesta a incendios?",
            "1.4a": "¿En zona de peligro volcánico?",
            "1.4b": "¿Volcán activo cercano?",
            "1.5a": "¿Amenazas futuras por cambio climático?"
        }
    respuestas = {
            clave: st.radio(texto, ["Sí", "No"], key=clave)
            for clave, texto in preguntas.items()
        }
    justificación= st.text_input("Justificación", max_chars=10000)
    enviar = st.form_submit_button("💾 Guardar respuestas")
    if enviar:
            if any(resp == "Sí" for resp in respuestas.values()):
                aplicar_ird = True
            st.session_state["aplicar_ird_tsunami"] = aplicar_ird
            st.success("✅ Cuestionario guardado.")
