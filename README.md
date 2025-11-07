# Prolevo® Dashboard Integrado

Dashboard interactivo en Streamlit que modela una propuesta de riesgo compartido para EPS colombianas basada en la introducción de Prolevo®.

## Requisitos

- Python 3.12 (o compatible)
- Dependencias del archivo `requirements.txt`

## Instalación local

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run prolevo_dashboard_integrado.py
```

## Estructura del repositorio

- `prolevo_dashboard_integrado.py`: código principal del dashboard.
- `requirements.txt`: dependencias para ejecutar el proyecto en Streamlit Community Cloud.
- `.gitignore`: excluye el entorno virtual y artefactos temporales.

## Despliegue en Streamlit

1. Sube el repositorio a GitHub (ver instrucciones en la sección inferior).
2. Ingresa a [Streamlit Community Cloud](https://share.streamlit.io/), conecta tu cuenta de GitHub y selecciona este repositorio.
3. Usa `prolevo_dashboard_integrado.py` como archivo principal y `requirements.txt` como archivo de dependencias.

## Publicación en GitHub

```bash
git init
git add .
git commit -m "Inicializa dashboard Prolevo"
git branch -M main
git remote add origin https://github.com/<usuario>/<repositorio>.git
git push -u origin main
```

> Reemplaza `<usuario>` y `<repositorio>` con tu información. Streamlit necesita que el repositorio sea público para cuentas gratuitas.

