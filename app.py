import streamlit as st
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

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
    {
        "nombre": "Estación de Policía Barrio El Manchén",
        "ciudad": "Tegucigalpa, Francisco Morazán",
        "lat": 14.1079146,
        "lon": -87.1906047,
    },
    {
        "nombre": "Posta Policial (Centro)",
        "ciudad": "San Pedro Sula, Cortés",
        "lat": 15.4764390,
        "lon": -88.0209728,
    },
    {
        "nombre": "Policía Nacional Santa Bárbara UMEP 16",
        "ciudad": "Santa Bárbara",
        "lat": 14.9064858,
        "lon": -88.2520188,
    },
    {
        "nombre": "Posta Policial Bonitillo",
        "ciudad": "La Ceiba, Atlántida",
        "lat": 15.7590270,
        "lon": -86.8688754,
    },
    {
        "nombre": "Posta Policial (Centro)",
        "ciudad": "Choluteca",
        "lat": 13.3142075,
        "lon": -87.1472005,
    },
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

col1, col2 = st.columns(2)
with col1:
    lat_usuario = st.number_input(
        "Latitud", min_value=-90.0, max_value=90.0,
        value=15.5044, format="%.6f"
    )
with col2:
    lon_usuario = st.number_input(
        "Longitud", min_value=-180.0, max_value=180.0,
        value=-88.0250, format="%.6f"
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
