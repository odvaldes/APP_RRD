# menu_ird.py
import sys
print(sys.executable)

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
                🌍 Dashboard Evaluación Índice de Riesgo de Desastres (IRD)
            </h2>
        </div>
    """, unsafe_allow_html=True)
with col_logo:
    st.image("images/logo.png", width=100)


# --- VELOCÍMETROS DE RIESGO ---
st.subheader("📊 Índice de Riesgo de Desastres por Amenaza")

riesgos = {
    "Tsunami": 3.1,
    "Remoción en Masa": 2.4,
    "Incendios Forestales": 1.9,
    "Erupciones Volcánicas": 2.8
}

cols = st.columns(len(riesgos))
for idx, (riesgo, valor) in enumerate(riesgos.items()):
    with cols[idx]:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=valor,
            title={'text': riesgo},
            gauge={
                'axis': {'range': [0, 5]},
                'bar': {'color': "red"},
                'steps': [
                    {'range': [0, 1], 'color': "#DFF0D8"},
                    {'range': [1, 2], 'color': "#FCF8E3"},
                    {'range': [2, 3], 'color': "#FBEED5"},
                    {'range': [3, 4], 'color': "#F2DEDE"},
                    {'range': [4, 5], 'color': "#EBA3A3"}
                ],
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

# --- RADARES DE VULNERABILIDAD Y RESILIENCIA ---
st.subheader("🕸️ Análisis de Vulnerabilidad y Resiliencia")

radar_cols = st.columns(2)

with radar_cols[0]:
    categorias_vuln = ['Física', 'Funcional', 'Social']
    valores_vuln = [0.7, 0.6, 0.8]
    fig_vuln = go.Figure()
    fig_vuln.add_trace(go.Scatterpolar(
        r=valores_vuln + [valores_vuln[0]],
        theta=categorias_vuln + [categorias_vuln[0]],
        fill='toself',
        name='Vulnerabilidad'
    ))
    fig_vuln.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        title="Vulnerabilidad"
    )
    st.plotly_chart(fig_vuln, use_container_width=True)

with radar_cols[1]:
    categorias_res = ['Física', 'Funcional', 'Local']
    valores_res = [0.5, 0.6, 0.7]
    fig_res = go.Figure()
    fig_res.add_trace(go.Scatterpolar(
        r=valores_res + [valores_res[0]],
        theta=categorias_res + [categorias_res[0]],
        fill='toself',
        name='Resiliencia'
    ))
    fig_res.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        title="Resiliencia"
    )
    st.plotly_chart(fig_res, use_container_width=True)
