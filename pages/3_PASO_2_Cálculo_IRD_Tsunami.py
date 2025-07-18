# Página: Información del Proyecto

import streamlit as st
import importlib
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Menú IRD", layout="wide")

# --- ESTILO GLOBAL ---
st.markdown("""
    <style>
    html, body, .stApp {
        font-size: 0.92rem !important;
    }
    h1, h2, h3, h4, p, li, label, .markdown-text-container {
        color: #0b1e34;
        font-family: 'Segoe UI', Calibri, sans-serif;
    }
    .stDownloadButton > button, .stButton > button {
        background-color: #1f6f8b;
        color: white;
        border-radius: 0.5rem;
        padding: 0.6rem 1.1rem;
        border: none;
        font-weight: 500;
    }
    .stDownloadButton > button:hover, .stButton > button:hover {
        background-color: #278ea5;
    }
    </style>
""", unsafe_allow_html=True)

# --- BANNER PRINCIPAL ---
col_title, col_logo = st.columns([8, 1])
with col_title:
    st.markdown("""
        <div style='background-color:#003DA5; padding: 12px; border-radius: 6px;'>
            <h2 style='color:white; text-align:left; margin: 0;'>
                🌍 Evaluación Índice de Riesgo de Desastres (IRD) por Tsunami
            </h2>
        </div>
    """, unsafe_allow_html=True)
with col_logo:
    st.image("images/logo.png", width=100)

# --- MENÚ DE SUBMÓDULOS ---
st.sidebar.title("Evaluación de Riesgo de Desastres")

modulo = None
with st.sidebar.expander("IRD tsunami"):
    opcion = st.radio("Selecciona una opción", ["Amenaza", "Vulnerabilidad", "Resiliencia"], 
                      key="tsunami", index=["Amenaza", "Vulnerabilidad", "Resiliencia"].index(
                          st.session_state.get("tsunami", "Amenaza")
                      ))
    modulo = f"modulos.tsunami.{opcion.lower()}"
    
    
# --- CARGAR MÓDULO SELECCIONADO ---
if modulo:
    try:
        mod = importlib.import_module(modulo)
        mod.app()
    except Exception as e:
        st.error(f"❌ No se pudo cargar el módulo '{modulo}': {e}")
