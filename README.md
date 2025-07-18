# 🌍 IRD Dashboard - Evaluación del Índice de Riesgo de Desastres

Aplicación desarrollada en **Streamlit** para evaluar el Índice de Riesgo de Desastres (IRD) considerando amenazas naturales como tsunami, remoción en masa, incendios forestales y erupciones volcánicas. La app permite:

- Visualización de mapas interactivos con `Folium`
- Carga de archivos geoespaciales `.kml` y `.kmz`
- Geocodificación de direcciones
- Cálculo del IRD según amenaza × vulnerabilidad × (1 - resiliencia)
- Gráficos tipo velocímetro y radar con `Plotly`
- Recomendaciones automáticas según intersección con zonas de amenaza

---

## 📦 Requisitos

Python ≥ 3.10 (se recomienda evitar 3.13 por problemas de compatibilidad)

Instalar dependencias:

```bash
pip install -r requirements.txt
