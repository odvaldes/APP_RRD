import streamlit as st

def app():
    st.title("IRD Tsunami - Resiliencia")
    st.write("Formulario para evaluar resiliencia física, funcional y local.")

    st.markdown("""
    <p style='font-size:20px; font-weight:bold; text-align:left;'>Selecciona la escala correspondiente para cada subfactor de Resiliencia física, funcional y local.</p>
    """, unsafe_allow_html=True)

    # Variables
    resiliencia_fisica_pesos = []
    resiliencia_fisica_valores = []
    resiliencia_funcional_pesos = []
    resiliencia_funcional_valores = []
    resiliencia_local_pesos = []
    resiliencia_local_valores = []

    col1, col2, col3 = st.columns(3)

    # Resiliencia Física
    with col1:
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#004080;'>a) CAPACIDAD FÍSICA</p>", unsafe_allow_html=True)
        subfactores_fisica_res = [
            ('Infraestructura protección proyecto', 0.1007, {'Seleccionar escala': 0, 'Tiene': 1, 'No tiene': 0, 'Sin Información': 0}),
            ('Obras protección externas', 0.1571, {'Seleccionar escala': 0, 'Tiene': 1, 'No tiene': 0, 'Sin Información': 0})
        ]
        for nombre, peso, opciones in subfactores_fisica_res:
            seleccion = st.selectbox(f"{nombre}", list(opciones.keys()), key=f'res_fis_{nombre}')
            resiliencia_fisica_pesos.append(peso)
            resiliencia_fisica_valores.append(opciones[seleccion])

    # Resiliencia Funcional
    with col2:
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#004080;'>b) RESILIENCIA FUNCIONAL</p>", unsafe_allow_html=True)
        subfactores_funcional_res = [
            ('Plan de continuidad operacional', 0.0438, {'Seleccionar escala': 0, 'Tiene': 1, 'No tiene': 0, 'Sin Información': 0}),
            ('Autonomía servicios básicos', 0.2280, {'Seleccionar escala': 0, 'Alta': 1, 'Moderada': 0.7223, 'Baja': 0.347, 'Nulo': 0, 'Sin Información': 0}),
            ('Conectividad servicio', 0.1089, {'Seleccionar escala': 0, 'Alto': 1, 'Medio': 0.333, 'Bajo': 0, 'Sin Información': 0}),
            ('Redundancia sistema', 0.2570, {'Seleccionar escala': 0, 'Alto': 1, 'Medio': 0.6705, 'Bajo': 0.3199, 'Nulo': 0, 'Sin Información': 0})
        ]
        for nombre, peso, opciones in subfactores_funcional_res:
            seleccion = st.selectbox(f"{nombre}", list(opciones.keys()), key=f'res_fun_{nombre}')
            resiliencia_funcional_pesos.append(peso)
            resiliencia_funcional_valores.append(opciones[seleccion])

    # Resiliencia Local
    with col3:
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#004080;'>c) RESILIENCIA LOCAL</p>", unsafe_allow_html=True)
        subfactores_local_res = [
            ('Plan de gestión riesgo local', 0.1045, {'Seleccionar escala': 0, 'Alto': 1, 'Medio': 0.1319, 'Bajo': 0, 'Sin Información': 0})
        ]
        for nombre, peso, opciones in subfactores_local_res:
            seleccion = st.selectbox(f"{nombre}", list(opciones.keys()), key=f'res_loc_{nombre}')
            resiliencia_local_pesos.append(peso)
            resiliencia_local_valores.append(opciones[seleccion])

    # Cálculo
    resiliencia_fisica = sum(p * v for p, v in zip(resiliencia_fisica_pesos, resiliencia_fisica_valores))
    resiliencia_funcional = sum(p * v for p, v in zip(resiliencia_funcional_pesos, resiliencia_funcional_valores))
    resiliencia_local = sum(p * v for p, v in zip(resiliencia_local_pesos, resiliencia_local_valores))
    resiliencia = resiliencia_fisica + resiliencia_funcional + resiliencia_local

    # Justificación
    justificacion_res = st.text_area("Justificación Resiliencia")

    # Botones
    colg1, colg2 = st.columns([1, 1])
    with colg1:
        if st.button("💾 Guardar Resiliencia"):
            st.session_state['resiliencia_data'] = {
                'resiliencia': resiliencia,
                'resiliencia_fisica': resiliencia_fisica,
                'resiliencia_funcional': resiliencia_funcional,
                'resiliencia_local': resiliencia_local,
                'justificacion_res': justificacion_res
            }
            st.success("✅ Resiliencia guardada correctamente")

    with colg2:
        if st.button("⏭️ Finalizar evaluación IRD"):
            st.success("Resiliencia registrada. Puedes revisar resultados finales.")
            # Si tienes una pestaña de resultados finales, podrías redirigir ahí:
            # st.session_state["resultados"] = True
            # st.experimental_rerun()
