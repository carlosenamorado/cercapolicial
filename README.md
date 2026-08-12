# Estaciones Policiales más Cercanas 🚓

Servicio en la nube que recibe una coordenada (latitud/longitud) y muestra
las **3 estaciones policiales más cercanas** en Honduras, calculando la
distancia real con la fórmula de Haversine.

## Cómo funciona

1. El usuario ingresa su latitud y longitud.
2. Al presionar **Buscar**, la app calcula la distancia entre esa coordenada
   y cada estación policial registrada.
3. Muestra las 3 estaciones más cercanas ordenadas por distancia, y las
   ubica en un mapa junto con la ubicación ingresada.

## Estaciones registradas

| Estación | Ciudad |
|---|---|
| Estación de Policía Barrio El Manchén | Tegucigalpa |
| Posta Policial (Centro) | San Pedro Sula |
| Policía Nacional Santa Bárbara UMEP 16 | Santa Bárbara |
| Posta Policial Bonitillo | La Ceiba |
| Posta Policial (Centro) | Choluteca |

## Instalación y ejecución local

```bash
pip install -r requirements.txt
streamlit run app.py
```

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
