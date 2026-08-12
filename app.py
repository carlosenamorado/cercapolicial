import streamlit as st
import pandas as pd
from math import radians, sin, cos, sqrt, atan2
from streamlit_js_eval import get_geolocation

# ==========================================================
# CONFIGURACIÓN
# ==========================================================
st.set_page_config(
    page_title="Estaciones Policiales Cercanas · Honduras",
    page_icon="🚓",
    layout="wide"
)

# ==========================================================
# ESTILOS PERSONALIZADOS
# ==========================================================
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}

    .block-container {
        padding-top: 2.2rem;
        max-width: 1100px;
    }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
    }
    .hero-subtitle {
        color: #9AA4AF;
        font-size: 1.05rem;
        margin-bottom: 1.8rem;
        max-width: 640px;
    }

    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-top: 1.6rem;
        margin-bottom: 0.6rem;
    }

    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #2FD9A8, #1FB88A);
        color: #06231A;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.4rem;
        font-size: 1.05rem;
        box-shadow: 0 4px 14px rgba(47, 217, 168, 0.25);
        transition: transform 0.15s ease;
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(47, 217, 168, 0.35);
    }

    .station-card {
        background: #171B24;
        border: 1px solid #262C38;
        border-radius: 16px;
        padding: 1.1rem 1.2rem;
        height: 100%;
    }
    .station-card.rank-1 { border-left: 5px solid #FFD54A; }
    .station-card.rank-2 { border-left: 5px solid #C7CDD6; }
    .station-card.rank-3 { border-left: 5px solid #E0A15C; }

    .medal { font-size: 1.6rem; margin-bottom: 0.3rem; }
    .station-name { font-size: 1.05rem; font-weight: 700; margin-bottom: 0.25rem; }
    .station-city { color: #9AA4AF; font-size: 0.9rem; margin-bottom: 0.6rem; }
    .station-distance {
        display: inline-block;
        background: rgba(47, 217, 168, 0.12);
        color: #2FD9A8;
        font-weight: 700;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        font-size: 0.9rem;
    }

    .sidebar-badge {
        background: #171B24;
        border: 1px solid #262C38;
        border-radius: 12px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.7rem;
    }
    .sidebar-badge b { color: #2FD9A8; }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# LISTA DE ESTACIONES POLICIALES (Honduras)
# Datos reales tomados de Google Maps — 18 departamentos
# ==========================================================
ESTACIONES = [
    # --- Francisco Morazán ---
    {"nombre": "Estación de Policía Barrio El Manchén", "ciudad": "Tegucigalpa, Francisco Morazán", "lat": 14.1079146, "lon": -87.1906047},
    # --- Cortés ---
    {"nombre": "Posta Policial (Centro)", "ciudad": "San Pedro Sula, Cortés", "lat": 15.4764390, "lon": -88.0209728},
    {"nombre": "Posta de Policía Camagüey", "ciudad": "Puerto Cortés, Cortés", "lat": 15.8623767, "lon": -87.9248849},
    {"nombre": "UMEP No.12 Villanueva", "ciudad": "Villanueva, Cortés", "lat": 15.3176240, "lon": -87.9937251},
    # --- Santa Bárbara ---
    {"nombre": "Policía Nacional Santa Bárbara UMEP 16", "ciudad": "Santa Bárbara (centro)", "lat": 14.9064858, "lon": -88.2520188},
    {"nombre": "Jefatura de Estación Policial Quimistán", "ciudad": "Quimistán, Santa Bárbara", "lat": 15.3485251, "lon": -88.4014455},
    {"nombre": "Policía Nacional Ilama", "ciudad": "Ilama, Santa Bárbara", "lat": 15.0667539, "lon": -88.2254452},
    {"nombre": "Posta Policial San José de Colinas", "ciudad": "San José de Colinas, Santa Bárbara", "lat": 15.0419594, "lon": -88.3025929},
    {"nombre": "Policía Nacional San Nicolás", "ciudad": "San Nicolás, Santa Bárbara", "lat": 14.9372426, "lon": -88.3265871},
    {"nombre": "Posta Policial Naranjito", "ciudad": "Naranjito, Santa Bárbara", "lat": 14.9527575, "lon": -88.6847895},
    {"nombre": "Posta Policial La Ceibita", "ciudad": "La Ceibita, Santa Bárbara", "lat": 15.3134678, "lon": -88.2536760},
    # --- Comayagua ---
    {"nombre": "Jefatura de Policía Comayagua", "ciudad": "Comayagua (centro)", "lat": 14.4608823, "lon": -87.6664399},
    {"nombre": "Posta Policial Central DPI Siguatepeque", "ciudad": "Siguatepeque, Comayagua", "lat": 14.5936503, "lon": -87.8408823},
    {"nombre": "Policía Nacional Taulabé", "ciudad": "Taulabé, Comayagua", "lat": 14.6947156, "lon": -87.9683289},
    {"nombre": "Policía Nacional San Jerónimo", "ciudad": "San Jerónimo, Comayagua", "lat": 14.6289902, "lon": -87.6070414},
    {"nombre": "Policía Nacional Minas de Oro", "ciudad": "Minas de Oro, Comayagua", "lat": 14.7944187, "lon": -87.3477207},
    {"nombre": "Posta Policial Esquías", "ciudad": "Esquías, Comayagua", "lat": 14.7379106, "lon": -87.3659125},
    # --- Yoro ---
    {"nombre": "UMEP No.11 El Progreso", "ciudad": "El Progreso, Yoro", "lat": 15.3946163, "lon": -87.8082829},
    {"nombre": "UDEP No.18 Yoro", "ciudad": "Yoro (centro)", "lat": 15.1365201, "lon": -87.1254273},
    # --- Atlántida ---
    {"nombre": "Posta Policial Bonitillo", "ciudad": "La Ceiba, Atlántida", "lat": 15.7590270, "lon": -86.8688754},
    {"nombre": "Policía Nacional Tela", "ciudad": "Tela, Atlántida", "lat": 15.7667875, "lon": -87.4671371},
    # --- Choluteca ---
    {"nombre": "Posta Policial (Centro)", "ciudad": "Choluteca", "lat": 13.3142075, "lon": -87.1472005},
    # --- Valle ---
    {"nombre": "Posta Policial Jícaro Galán", "ciudad": "Nacaome, Valle", "lat": 13.5310141, "lon": -87.4381769},
    {"nombre": "Policía Nacional San Lorenzo", "ciudad": "San Lorenzo, Valle", "lat": 13.4259048, "lon": -87.4448790},
    # --- El Paraíso ---
    {"nombre": "Posta Policial Danlí", "ciudad": "Danlí, El Paraíso", "lat": 14.0392762, "lon": -86.5717099},
    {"nombre": "Policía Nacional Yuscarán", "ciudad": "Yuscarán, El Paraíso", "lat": 13.9434194, "lon": -86.8523122},
    # --- Olancho ---
    {"nombre": "Posta Policial Telica", "ciudad": "Juticalpa, Olancho", "lat": 14.7231030, "lon": -86.1379545},
    {"nombre": "Policía Nacional Catacamas", "ciudad": "Catacamas, Olancho", "lat": 14.8463755, "lon": -85.8881307},
    # --- Intibucá ---
    {"nombre": "Posta Policía Nacional La Esperanza", "ciudad": "La Esperanza, Intibucá", "lat": 14.3086516, "lon": -88.1776360},
    # --- Lempira ---
    {"nombre": "Posta Policial Villami", "ciudad": "Gracias, Lempira", "lat": 14.6214230, "lon": -88.5894447},
    # --- Ocotepeque ---
    {"nombre": "Policía Nacional Ocotepeque", "ciudad": "Ocotepeque", "lat": 14.4347080, "lon": -89.1861526},
    # --- Colón ---
    {"nombre": "Posta Policial Ilanga", "ciudad": "Trujillo, Colón", "lat": 15.7031074, "lon": -86.0850760},
    # --- Islas de la Bahía ---
    {"nombre": "Posta Policial French Harbour", "ciudad": "Roatán, Islas de la Bahía", "lat": 16.3526201, "lon": -86.4578959},
    # --- Copán ---
    {"nombre": "UDEP No.04 Copán", "ciudad": "Santa Rosa de Copán, Copán", "lat": 14.7799972, "lon": -88.7774414},
    # --- Gracias a Dios ---
    {"nombre": "Estación de Policía Puerto Lempira", "ciudad": "Puerto Lempira, Gracias a Dios", "lat": 15.2611144, "lon": -83.7781985},
    # --- La Paz ---
    {"nombre": "Policía Nacional Marcala", "ciudad": "Marcala, La Paz", "lat": 14.1562309, "lon": -88.0376970},
    {"nombre": "Policía Nacional La Paz", "ciudad": "La Paz (centro)", "lat": 14.3242835, "lon": -87.6815425},
]

# ==========================================================
# CÁLCULO DE DISTANCIA (fórmula de Haversine)
# ==========================================================
def distancia_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

DEPARTAMENTOS = sorted({e["ciudad"].split(",")[-1].strip() for e in ESTACIONES})

# ==========================================================
# SIDEBAR
# ==========================================================
with st.sidebar:
    st.markdown("### ℹ️ Información")
    st.markdown(
        f'<div class="sidebar-badge">✅ <b>{len(ESTACIONES)}</b> estaciones cargadas</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sidebar-badge">📡 Datos: ubicaciones reales verificadas</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="sidebar-badge">🗺️ Cobertura: {len(DEPARTAMENTOS)} departamentos de Honduras</div>',
        unsafe_allow_html=True
    )
    with st.expander("Ver estaciones registradas"):
        st.dataframe(
            pd.DataFrame(ESTACIONES)[["nombre", "ciudad"]],
            hide_index=True,
            use_container_width=True
        )
    st.markdown("---")
    st.caption("Proyecto académico · Servicio en la Nube")
    st.caption("Streamlit Community Cloud")

# ==========================================================
# ENCABEZADO
# ==========================================================
st.markdown('<div class="hero-title">🚓 Estaciones Policiales Cercanas</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Detecta tu ubicación con un clic y encuentra al instante '
    'las 3 estaciones policiales más cercanas en cualquier punto de Honduras.</div>',
    unsafe_allow_html=True
)

# ==========================================================
# GEOLOCALIZACIÓN
# ==========================================================
st.markdown('<div class="section-title">📡 Obtener ubicación</div>', unsafe_allow_html=True)

if "geo_intentos" not in st.session_state:
    st.session_state.geo_intentos = 0

col_btn, col_msg = st.columns([1, 3], vertical_alignment="center")
mensaje = col_msg.empty()

with col_btn:
    if st.button("📍  Usar mi ubicación", type="primary", use_container_width=True):
        st.session_state.geo_intentos += 1
        st.session_state.buscando_ubicacion = True

if not st.session_state.get("buscando_ubicacion"):
    mensaje.caption("Presiona el botón y acepta el permiso de ubicación de tu navegador.")

if st.session_state.get("buscando_ubicacion"):
    mensaje.info("🔄 Obteniendo tu ubicación… si tu navegador pide permiso, acéptalo.")
    resultado = get_geolocation(component_key=f"geo_{st.session_state.geo_intentos}")

    if resultado is not None:
        if "coords" in resultado:
            lat_usuario = resultado["coords"]["latitude"]
            lon_usuario = resultado["coords"]["longitude"]
            st.session_state.ultima_deteccion = (lat_usuario, lon_usuario)
        elif "error" in resultado:
            st.session_state.geo_error = resultado["error"]["message"]
            st.session_state.pop("ultima_deteccion", None)

if st.session_state.get("ultima_deteccion"):
    lat_usuario, lon_usuario = st.session_state.ultima_deteccion
    mensaje.success(f"📍 Ubicación detectada: {lat_usuario:.5f}, {lon_usuario:.5f}")

    # ---------- RESULTADOS ----------
    resultados = sorted(
        ESTACIONES,
        key=lambda e: distancia_km(lat_usuario, lon_usuario, e["lat"], e["lon"])
    )
    top3 = resultados[:3]

    st.markdown('<div class="section-title">🏆 Estaciones más cercanas</div>', unsafe_allow_html=True)
    medallas = ["🥇", "🥈", "🥉"]
    ranks = ["rank-1", "rank-2", "rank-3"]
    cols = st.columns(3)
    for col, medalla, rank, est in zip(cols, medallas, ranks, top3):
        d = distancia_km(lat_usuario, lon_usuario, est["lat"], est["lon"])
        with col:
            st.markdown(f"""
            <div class="station-card {rank}">
                <div class="medal">{medalla}</div>
                <div class="station-name">{est['nombre']}</div>
                <div class="station-city">📍 {est['ciudad']}</div>
                <div class="station-distance">📏 {d:.2f} km</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">🗺️ Mapa</div>', unsafe_allow_html=True)
    mapa_df = pd.DataFrame(
        [{"lat": lat_usuario, "lon": lon_usuario, "color": "#FF5C5C", "size": 220}] +
        [{"lat": e["lat"], "lon": e["lon"], "color": "#2FD9A8", "size": 140} for e in top3]
    )
    st.map(mapa_df, latitude="lat", longitude="lon", color="color", size="size")

elif st.session_state.get("geo_error"):
    mensaje.error(
        f"⚠️ No se pudo obtener tu ubicación ({st.session_state.geo_error}). "
        "Revisa que hayas dado permiso de ubicación a este sitio en tu navegador "
        "y que el GPS/servicio de ubicación de tu dispositivo esté activo, luego "
        "presiona el botón de nuevo."
    )
    st.info("⬅️ Presiona el botón de ubicación para intentarlo de nuevo.")

else:
    st.info("⬅️ Presiona el botón de ubicación para ver las estaciones más cercanas a ti.")

st.divider()
st.caption("Proyecto académico — Servicio en la Nube · Estaciones Policiales de Honduras")
