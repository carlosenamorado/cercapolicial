import streamlit as st
import pandas as pd
from math import radians, sin, cos, sqrt, atan2
from streamlit_geolocation import streamlit_geolocation

# ==========================================================
# CONFIGURACIÓN
# ==========================================================
st.set_page_config(
    page_title="Estaciones Policiales más Cercanas - Honduras",
    page_icon="🚓",
    layout="centered"
)

# ==========================================================
# LISTA DE ESTACIONES POLICIALES (Honduras)
# Datos reales tomados de Google Maps
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
    R = 6371.0  # radio de la Tierra en km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# ==========================================================
# INTERFAZ
# ==========================================================
st.title("🚓 Estaciones Policiales más Cercanas")
st.markdown(
    "Servicio en la nube que ubica las **3 estaciones policiales más cercanas** "
    "a una coordenada dada, en cualquier punto de Honduras."
)

with st.expander("📍 Ver todas las estaciones registradas"):
    st.dataframe(
        pd.DataFrame(ESTACIONES)[["nombre", "ciudad", "lat", "lon"]],
        hide_index=True,
        use_container_width=True
    )

st.subheader("Ingresa tu ubicación")

st.markdown("**Opción 1 — Detectar automáticamente** (te pedirá permiso del navegador)")

col_geo, col_info = st.columns([1, 4])
with col_geo:
    ubicacion = streamlit_geolocation()

if "lat_input" not in st.session_state:
    st.session_state.lat_input = 15.5044
if "lon_input" not in st.session_state:
    st.session_state.lon_input = -88.0250

if ubicacion and ubicacion.get("latitude") is not None:
    nueva_coord = (ubicacion["latitude"], ubicacion["longitude"])
    if st.session_state.get("ultima_deteccion") != nueva_coord:
        st.session_state.lat_input = nueva_coord[0]
        st.session_state.lon_input = nueva_coord[1]
        st.session_state.ultima_deteccion = nueva_coord
        st.session_state.geo_ok = True

if st.session_state.get("geo_ok"):
    with col_info:
        st.success(
            f"📍 Ubicación detectada: {st.session_state.lat_input:.6f}, "
            f"{st.session_state.lon_input:.6f}"
        )
else:
    with col_info:
        st.caption("Presiona el ícono de ubicación y acepta el permiso del navegador.")

st.markdown("**Opción 2 — Ingresar manualmente** (o ajustar la ubicación detectada)")
col1, col2 = st.columns(2)
with col1:
    lat_usuario = st.number_input(
        "Latitud", min_value=-90.0, max_value=90.0,
        format="%.6f", key="lat_input"
    )
with col2:
    lon_usuario = st.number_input(
        "Longitud", min_value=-180.0, max_value=180.0,
        format="%.6f", key="lon_input"
    )

buscar = st.button("🔍 Buscar", type="primary", use_container_width=True)

if buscar:
    resultados = []
    for est in ESTACIONES:
        d = distancia_km(lat_usuario, lon_usuario, est["lat"], est["lon"])
        resultados.append({**est, "distancia_km": d})

    resultados.sort(key=lambda x: x["distancia_km"])
    top3 = resultados[:3]

    st.subheader("🏆 3 estaciones más cercanas")
    for i, est in enumerate(top3, start=1):
        st.markdown(
            f"**{i}. {est['nombre']}** — {est['ciudad']}  \n"
            f"📏 {est['distancia_km']:.2f} km de distancia"
        )

    st.subheader("🗺️ Mapa")
    mapa_df = pd.DataFrame(
        [{"lat": lat_usuario, "lon": lon_usuario, "tipo": "Tu ubicación"}] +
        [{"lat": e["lat"], "lon": e["lon"], "tipo": e["nombre"]} for e in top3]
    )
    st.map(mapa_df[["lat", "lon"]], size=40)

else:
    st.info("⬅️ Ingresa tu latitud y longitud, y presiona **Buscar**.")

st.divider()
st.caption("Proyecto académico — Servicio en la Nube · Estaciones Policiales de Honduras")
