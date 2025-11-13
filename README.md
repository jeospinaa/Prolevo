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

## Despliegue en Streamlit Community Cloud (Gratuito)

El proyecto ya está configurado para desplegarse fácilmente en Streamlit Community Cloud. Sigue estos pasos:

### 1. Sube los cambios a GitHub

```bash
git add .
git commit -m "Prepara despliegue en Streamlit Cloud"
git push origin main
```

### 2. Despliega en Streamlit Cloud

1. Ve a [https://share.streamlit.io/](https://share.streamlit.io/)
2. Inicia sesión con tu cuenta de GitHub
3. Haz clic en "New app"
4. Selecciona tu repositorio: `jeospinaa/Prolevo`
5. En "Main file path", usa: `streamlit_app.py`
6. En "Python version", selecciona: `3.12` (o la versión compatible)
7. Haz clic en "Deploy!"

### 3. Configuración automática

El proyecto incluye:
- `streamlit_app.py`: archivo principal para el despliegue
- `.streamlit/config.toml`: configuración del tema y servidor
- `requirements.txt`: dependencias necesarias

> **Nota**: El repositorio debe ser público para usar el plan gratuito de Streamlit Cloud.

### Acceso a tu app

Una vez desplegada, tu app estará disponible en una URL como:
`https://prolevo.streamlit.app` o `https://share.streamlit.io/jeospinaa/prolevo/main`



