# Estaciones Policiales más Cercanas 🚓

Servicio en la nube que recibe una coordenada (latitud/longitud) y muestra
las **3 estaciones policiales más cercanas** en Honduras, calculando la
distancia real con la fórmula de Haversine.

## Cómo funciona

1. El usuario presiona el ícono de ubicación 📍 y autoriza el permiso de
   geolocalización del navegador — la app detecta su latitud/longitud
   automáticamente (no requiere escribir coordenadas).
2. En cuanto detecta la ubicación, calcula la distancia entre esa
   coordenada y cada estación policial registrada.
3. Muestra las 3 estaciones más cercanas en tarjetas con medalla (🥇🥈🥉) y
   distancia en km, junto con un mapa con la ubicación del usuario y las
   estaciones encontradas.

> **Nota:** la geolocalización del navegador solo funciona sobre HTTPS (como
> Streamlit Community Cloud) o en localhost, y requiere que el usuario
> conceda el permiso cuando el navegador lo solicite, y que el GPS/servicio
> de ubicación del dispositivo esté activo.

## Diseño de la interfaz

La app usa un tema oscuro personalizado (`.streamlit/config.toml`) con un
color de acento verde-turquesa, tarjetas con jerarquía visual por rango
(oro/plata/bronce), y una barra lateral con estadísticas rápidas de la base
de datos — siguiendo principios de UX como jerarquía visual, contraste y
feedback inmediato al usuario.

## Estaciones registradas

La base incluye **37 estaciones reales** distribuidas en los **18
departamentos** de Honduras (Atlántida, Choluteca, Colón, Comayagua, Copán,
Cortés, El Paraíso, Francisco Morazán, Gracias a Dios, Intibucá, Islas de la
Bahía, La Paz, Lempira, Ocotepeque, Olancho, Santa Bárbara, Valle y Yoro),
con varias estaciones adicionales alrededor de Santa Bárbara y Comayagua
para mayor precisión en esas zonas. La lista completa está dentro de `app.py` (variable
`ESTACIONES`) y también se puede ver dentro de la propia aplicación en el
desplegable "Ver todas las estaciones registradas".

## Instalación y ejecución local

```bash
pip install -r requirements.txt
streamlit run app.py
```

El tema visual se aplica automáticamente desde `.streamlit/config.toml` —
asegúrate de subir esa carpeta oculta también al repositorio de GitHub.

## Despliegue en Streamlit Community Cloud

1. Sube `app.py`, `requirements.txt` y este `README.md` a un repositorio
   público de GitHub.
2. Entra a https://share.streamlit.io y conecta tu cuenta de GitHub.
3. Crea una nueva app apuntando a tu repositorio y al archivo `app.py`.
4. Despliega — no requiere ninguna clave ni configuración adicional.

## Tecnologías utilizadas

- Python
- Streamlit
- Pandas
- Fórmula de Haversine (cálculo de distancia geográfica)
