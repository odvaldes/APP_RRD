import streamlit as st

# Inicialización
if 'usuario' not in st.session_state:
    st.session_state.usuario = None
if 'usuarios' not in st.session_state:
    st.session_state.usuarios = {}  # { 'usuario': 'contraseña' }
if 'proyectos' not in st.session_state:
    st.session_state.proyectos = {}  # { 'usuario': [lista de proyectos] }

# Selector: Login o Registro
modo = st.radio("Selecciona una opción", ["Iniciar sesión", "Registrarse"])

if modo == "Registrarse":
    st.subheader("📝 Crear nueva cuenta")
    nuevo_usuario = st.text_input("Nuevo usuario")
    nueva_clave = st.text_input("Crear contraseña", type="password")
    confirmar = st.text_input("Confirmar contraseña", type="password")

    if st.button("Crear cuenta"):
        if nuevo_usuario in st.session_state.usuarios:
            st.error("❌ El usuario ya existe.")
        elif nueva_clave != confirmar:
            st.error("❌ Las contraseñas no coinciden.")
        elif nuevo_usuario.strip() == "" or nueva_clave.strip() == "":
            st.error("❌ Usuario y contraseña no pueden estar vacíos.")
        else:
            st.session_state.usuarios[nuevo_usuario] = nueva_clave
            st.session_state.proyectos[nuevo_usuario] = []
            st.success("✅ Usuario creado correctamente. Ahora puedes iniciar sesión.")

elif modo == "Iniciar sesión":
    st.subheader("🔐 Ingresar")
    usuario = st.text_input("Usuario")
    clave = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if usuario in st.session_state.usuarios and st.session_state.usuarios[usuario] == clave:
            st.session_state.usuario = usuario
            st.success(f"Bienvenido, {usuario} 👋")
        else:
            st.error("❌ Usuario o contraseña incorrectos.")

# Detener la ejecución si no hay sesión activa
if not st.session_state.usuario:
    st.stop()
