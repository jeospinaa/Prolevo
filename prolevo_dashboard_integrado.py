#!/usr/bin/env python3
"""
Dashboard Interactivo - Propuesta de Riesgo Compartido PROLEVO® (versión integrada)
Motor basado en consumo real por 1 millón de afiliados + narrativa de propuestas.

Autor: (Tú)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from io import BytesIO

# --------------------------------------------------------------------
# Configuración de página y estilo
# --------------------------------------------------------------------
st.set_page_config(
    page_title="Prolevo® - Propuesta de Valor Integrada",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
    }
    .proposal-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------
# 1. Datos base de mercado (1 millón de afiliados)
#    Usamos precios en COP como enteros
# --------------------------------------------------------------------
def cargar_datos_rotacion():
    data = [
        {"Descripcion": "LEVOTIROXINA SÓDICA 200 MCG (TABLETA) - EUTIROX", "RotacionMes": 423,   "PrecioProm": 1175, "Compania": "Merck S.A."},
        {"Descripcion": "LEVOTIROXINA SÓDICA 137 MCG (TABLETA) - EUTIROX", "RotacionMes": 453,   "PrecioProm": 753,  "Compania": "Merck S.A."},
        {"Descripcion": "LEVOTIROXINA 62 MCG (TABLETA)",                    "RotacionMes": 641,   "PrecioProm": 298,  "Compania": "Genérico"},
        {"Descripcion": "LEVOTIROXINA SÓDICA 175 MCG (TABLETA) - EUTIROX", "RotacionMes": 720,   "PrecioProm": 1075, "Compania": "Merck S.A."},
        {"Descripcion": "LEVOTIROXINA SÓDICA 112 MCG (TABLETA) - EUTIROX", "RotacionMes": 1254,  "PrecioProm": 646,  "Compania": "Merck S.A."},
        {"Descripcion": "LEVOTIROXINA SÓDICA 137 MCG (TABLETA)",           "RotacionMes": 1377,  "PrecioProm": 753,  "Compania": "Merck S.A."},
        {"Descripcion": "LEVOTIROXINA SÓDICA 175 MCG (TABLETA)",           "RotacionMes": 1544,  "PrecioProm": 1075, "Compania": "Merck S.A."},
        {"Descripcion": "LEVOTIROXINA SÓDICA 25 MCG (TABLETA) - EUTIROX",  "RotacionMes": 1628,  "PrecioProm": 571,  "Compania": "Merck S.A."},
        {"Descripcion": "LEVOTIROXINA SÓDICA 88 MCG (TABLETA) - EUTIROX",  "RotacionMes": 2109,  "PrecioProm": 620,  "Compania": "Merck S.A."},
        {"Descripcion": "LEVOTIROXINA SÓDICA 150 MCG - EUTIROX (TABLETA)", "RotacionMes": 2794,  "PrecioProm": 353,  "Compania": "Merck S.A."},
        {"Descripcion": "LEVOTIROXINA SÓDICA 125 MCG - EUTIROX (TABLETA)", "RotacionMes": 2979,  "PrecioProm": 475,  "Compania": "Merck S.A."},
        {"Descripcion": "LEVOTIROXINA SÓDICA 112 MCG (TABLETA)",           "RotacionMes": 3442,  "PrecioProm": 320,  "Compania": "Genérico"},
        {"Descripcion": "LEVOTIROXINA SÓDICA 88 MCG (TABLETA)",            "RotacionMes": 7400,  "PrecioProm": 288,  "Compania": "Genérico"},
        {"Descripcion": "LEVOTIROXINA SÓDICA 50 MCG (TABLETA) - EUTIROX",  "RotacionMes": 8168,  "PrecioProm": 131,  "Compania": "Merck S.A."},
        {"Descripcion": "LEVOTIROXINA SÓDICA 150 MCG (TABLETA)",           "RotacionMes": 8547,  "PrecioProm": 94,   "Compania": "Genérico"},
        {"Descripcion": "LEVOTIROXINA SÓDICA 100 MCG EUTIROX (TABLETA)",   "RotacionMes": 8598,  "PrecioProm": 128,  "Compania": "Merck S.A."},
        {"Descripcion": "LEVOTIROXINA SÓDICA 75 MCG - EUTIROX (TABLETA)",  "RotacionMes": 9503,  "PrecioProm": 258,  "Compania": "Merck S.A."},
        {"Descripcion": "LEVOTIROXINA SÓDICA 125 MCG (TABLETA)",           "RotacionMes": 11964, "PrecioProm": 83,   "Compania": "Genérico"},
        {"Descripcion": "LEVOTIROXINA SÓDICA 25 MCG (TABLETA)",            "RotacionMes": 16697, "PrecioProm": 58,   "Compania": "Genérico"},
        {"Descripcion": "LEVOTIROXINA SÓDICA 75 MCG (TABLETA)",            "RotacionMes": 65631, "PrecioProm": 64,   "Compania": "Genérico"},
    ]
    df = pd.DataFrame(data)
    df["Tipo"] = np.where(df["Compania"].str.contains("Merck", case=False),
                          "Eutirox (innovador)", "Genérico")
    df["Dosis_mcg"] = df["Descripcion"].str.extract(r"(?i)(\d+)\s*mcg", expand=False).astype(int)
    return df

df_base = cargar_datos_rotacion()

# --------------------------------------------------------------------
# 2. Datos de EPS y parámetros de simulación (sidebar)
# --------------------------------------------------------------------
eps_data = {
    "Población estándar 1.000.000": {"usuarios": 1_000_000},
    "SURA EPS": {"usuarios": 5_409_527},
    "SANITAS EPS": {"usuarios": 5_775_816},
    "SURA + SANITAS": {"usuarios": 5_409_527 + 5_775_816},
}

st.markdown('<p class="main-header">💊 PROLEVO® - Dashboard Integrado de Propuesta de Valor</p>',
            unsafe_allow_html=True)
st.markdown("### Levotiroxina sódica en cápsulas de gelatina blanda – modelo clínico–económico para EPS")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Parámetros de simulación")

    eps_sel = st.selectbox("Seleccione EPS o cohorte:", list(eps_data.keys()), index=1)
    usuarios_eps = eps_data[eps_sel]["usuarios"]

    st.markdown("---")
    st.subheader("📊 Parámetros clínicos")

    # Prevalencia solo para visualización de población; la carga real viene del consumo
    prevalencia_hipo = st.slider(
        "Prevalencia estimada de hipotiroidismo (%)",
        min_value=3.0, max_value=8.0, value=5.0, step=0.5
    ) / 100

    # Control de TSH
    tsh_control_base = st.slider(
        "Pacientes con TSH controlada en la situación actual (%)",
        min_value=40, max_value=90, value=70, step=1
    )
    tsh_control_prolevo = st.slider(
        "TSH controlada en los pacientes migrados a Prolevo® (%)",
        min_value=60, max_value=98, value=88, step=1
    )

    st.markdown("---")
    st.subheader("💊 Migración a Prolevo®")

    pct_candidatos_eutirox = st.slider(
        "Pacientes en Eutirox candidatos clínicamente a Prolevo® (%)",
        min_value=10, max_value=70, value=40, step=5
    )
    pct_migracion_candidatos = st.slider(
        "De los candidatos, ¿qué porcentaje migra a Prolevo®?",
        min_value=10, max_value=100, value=50, step=5
    )

    st.markdown("---")
    st.subheader("💰 Parámetros económicos")

    precio_rel_prolevo = st.number_input(
        "Multiplicador de precio de Prolevo® vs Eutirox (1.10 = 10% más caro)",
        min_value=0.5, max_value=2.0, value=1.10, step=0.05
    )

    costo_no_controlado = st.number_input(
        "Costo adicional anual por paciente con TSH no controlada (COP)",
        min_value=0.0, value=150_000.0, step=50_000.0
    )

    st.markdown("---")
    st.subheader("🤝 Riesgo compartido")

    meta_control = st.slider(
        "Meta de pacientes con TSH controlada para evitar descuento (%)",
        min_value=70, max_value=95, value=85, step=1
    )
    descuento_prolevo = st.number_input(
        "Descuento sobre Prolevo® si no se cumple la meta (%)",
        min_value=0.0, max_value=50.0, value=15.0, step=1.0
    )

# --------------------------------------------------------------------
# 3. Motor de cálculo: escala por EPS y simula cambio a Prolevo
# --------------------------------------------------------------------
factor_poblacion = usuarios_eps / 1_000_000

df = df_base.copy()
df["RotacionMes_EPS"] = df["RotacionMes"] * factor_poblacion
df["CostoMes_EPS"] = df["RotacionMes_EPS"] * df["PrecioProm"]

# Consumo y pacientes tratados por datos reales
consumo_mensual_total = df["RotacionMes_EPS"].sum()
pacientes_tratados_aprox = consumo_mensual_total / 30.0  # dosis diaria

costo_anual_farmacos_base = df["CostoMes_EPS"].sum() * 12

# Prevalencia teórica, solo para comparación
pacientes_hipo_prevalencia = usuarios_eps * prevalencia_hipo

# Separar Eutirox y genéricos
df_eutirox = df[df["Tipo"] == "Eutirox (innovador)"].copy()
df_generico = df[df["Tipo"] == "Genérico"].copy()

unidades_eutirox_mes = df_eutirox["RotacionMes_EPS"].sum()
unidades_generico_mes = df_generico["RotacionMes_EPS"].sum()

precio_prom_eutirox = (df_eutirox["RotacionMes_EPS"] * df_eutirox["PrecioProm"]).sum() / unidades_eutirox_mes
precio_prom_generico = (df_generico["RotacionMes_EPS"] * df_generico["PrecioProm"]).sum() / unidades_generico_mes

precio_prom_prolevo = precio_prom_eutirox * precio_rel_prolevo

# Candidatos y migrados (sobre Eutirox)
unidades_candidatas = unidades_eutirox_mes * (pct_candidatos_eutirox / 100)
unidades_migradas = unidades_candidatas * (pct_migracion_candidatos / 100)

pacientes_migrados = unidades_migradas / 30.0
pacientes_no_migrados = pacientes_tratados_aprox - pacientes_migrados

# Costos de fármacos en escenario con Prolevo
unidades_eutirox_remanente = unidades_eutirox_mes - unidades_migradas

costo_eutirox_mes_escenario = unidades_eutirox_remanente * precio_prom_eutirox
costo_generico_mes_escenario = unidades_generico_mes * precio_prom_generico
costo_prolevo_mes_escenario = unidades_migradas * precio_prom_prolevo

costo_anual_farmacos_escenario = (costo_eutirox_mes_escenario +
                                  costo_generico_mes_escenario +
                                  costo_prolevo_mes_escenario) * 12

# Control de TSH y costos clínicos
pacientes_controlados_base = pacientes_tratados_aprox * (tsh_control_base / 100)
pacientes_no_controlados_base = pacientes_tratados_aprox - pacientes_controlados_base

control_no_migrados = pacientes_no_migrados * (tsh_control_base / 100)
control_migrados = pacientes_migrados * (tsh_control_prolevo / 100)

pacientes_controlados_escenario = control_no_migrados + control_migrados
pacientes_no_controlados_escenario = pacientes_tratados_aprox - pacientes_controlados_escenario
porc_control_escenario = 100 * pacientes_controlados_escenario / pacientes_tratados_aprox

costo_clinico_base = pacientes_no_controlados_base * costo_no_controlado
costo_clinico_escenario = pacientes_no_controlados_escenario * costo_no_controlado

# Riesgo compartido
if porc_control_escenario < meta_control:
    costo_prolevo_mes_desc = costo_prolevo_mes_escenario * (1 - descuento_prolevo / 100)
    costo_anual_farmacos_escenario_ajustado = (costo_eutirox_mes_escenario +
                                               costo_generico_mes_escenario +
                                               costo_prolevo_mes_desc) * 12
else:
    costo_anual_farmacos_escenario_ajustado = costo_anual_farmacos_escenario

costo_total_base = costo_anual_farmacos_base + costo_clinico_base
costo_total_escenario = costo_anual_farmacos_escenario_ajustado + costo_clinico_escenario
ahorro_neto_ajustado = costo_total_base - costo_total_escenario

# --------------------------------------------------------------------
# 4. Tabs
# --------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Resumen ejecutivo",
    "👥 Población y selección clínica",
    "💰 Análisis económico y riesgo compartido",
    "🎯 Proyección a 3 años"
])

# --------------------------------------------------------------------
# TAB 1 – Resumen ejecutivo
# --------------------------------------------------------------------
with tab1:
    st.header("📈 Resumen ejecutivo")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Usuarios EPS", f"{usuarios_eps:,.0f}")
    with c2:
        st.metric("Pacientes tratados con levotiroxina (estimados por consumo)",
                  f"{pacientes_tratados_aprox:,.0f}",
                  delta=f"Prevalencia ~{100*pacientes_tratados_aprox/usuarios_eps:0.1f}%")
    with c3:
        st.metric("Pacientes migrados a Prolevo® (estimados)", f"{pacientes_migrados:,.0f}",
                  delta=f"{pct_migracion_candidatos}% de candidatos")
    with c4:
        st.metric("Ahorro neto anual ajustado",
                  f"${ahorro_neto_ajustado:,.0f}",
                  delta=f"{(ahorro_neto_ajustado/costo_total_base)*100:0.1f}% vs base")

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Distribución de población (visión macro)")

        usuarios_sin_hipo = max(usuarios_eps - pacientes_hipo_prevalencia, 0)
        pacientes_hipo_no_trat = max(pacientes_hipo_prevalencia - pacientes_tratados_aprox, 0)
        pacientes_trat_no_migr = max(pacientes_tratados_aprox - pacientes_migrados, 0)

        fig_pob = go.Figure(data=[go.Pie(
            labels=[
                "Usuarios sin hipotiroidismo",
                "Hipotiroidismo sin tratamiento (estimado)",
                "Tratados sin Prolevo®",
                "Tratados en Prolevo®"
            ],
            values=[
                usuarios_sin_hipo,
                pacientes_hipo_no_trat,
                pacientes_trat_no_migr,
                pacientes_migrados
            ],
            hole=0.4
        )])
        fig_pob.update_layout(height=400)
        st.plotly_chart(fig_pob, use_container_width=True)

    with col_b:
        st.subheader("Costos totales anuales")

        fig_cost = go.Figure()
        fig_cost.add_trace(go.Bar(
            name="Escenario base",
            x=["Base"],
            y=[costo_total_base],
            marker_color="#e63946"
        ))
        fig_cost.add_trace(go.Bar(
            name="Con Prolevo® + riesgo compartido",
            x=["Con Prolevo"],
            y=[costo_total_escenario],
            marker_color="#2a9d8f"
        ))
        fig_cost.update_layout(
            barmode="group",
            yaxis_title="Costo anual total (COP)",
            height=400
        )
        st.plotly_chart(fig_cost, use_container_width=True)

    st.markdown("---")
    st.subheader("✅ Beneficios clave de Prolevo® (para notas médicas y argumentación clínica)")

    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown("""
        <div class="proposal-box">
        <h4>🎯 Mejora en control de TSH</h4>
        <ul>
            <li>Mayor proporción de pacientes en rango objetivo</li>
            <li>Menos necesidad de ajustes de dosis</li>
            <li>Particularmente útil con inhibidores de bomba de protones y malabsorción</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    with b2:
        st.markdown("""
        <div class="proposal-box">
        <h4>💊 Adherencia y comodidad</h4>
        <ul>
            <li>No exige ayuno estricto</li>
            <li>Menor interferencia con alimentos y café</li>
            <li>Menos interferencia con calcio, hierro y otros suplementos</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    with b3:
        st.markdown("""
        <div class="proposal-box">
        <h4>💰 Impacto económico</h4>
        <ul>
            <li>Reducción de consultas y laboratorios por descontrol</li>
            <li>Menos cambios de formulación de levotiroxina</li>
            <li>Modelo de riesgo compartido auditable</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------------------------
# TAB 2 – Población y selección clínica
# --------------------------------------------------------------------
with tab2:
    st.header("👥 Población objetivo y criterios de selección para Prolevo®")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        #### Grupo A – TSH descontrolada
        - TSH repetidamente fuera de rango a pesar de buena adherencia.
        - Dosis elevadas de levotiroxina en tableta (> 2.2 microgramos/kg/día).
        - Pacientes donde cambiar de formulación evita seguir subiendo dosis.
        """)

        st.markdown("""
        #### Grupo B – Malabsorción digestiva
        - Uso crónico de inhibidores de bomba de protones.
        - Gastritis atrófica o infección por Helicobacter pylori.
        - Enfermedad celíaca o intestinal inflamatoria.
        - Cirugía bariátrica o resecciones digestivas.
        """)

    with c2:
        st.markdown("""
        #### Grupo C – Interacciones medicamentosas
        - Tratamiento crónico con calcio, hierro o multivitamínicos con minerales.
        - Uso de resinas para lípidos o fósforo.
        - Pacientes polimedicados donde se desea simplificar el régimen.
        """)

        st.markdown("""
        #### Grupos especiales
        - Pacientes con intolerancia a excipientes de tabletas (por ejemplo lactosa).
        - Personas que requieren flexibilidad de horario por su rutina diaria.
        - Situaciones donde el control estricto de TSH es crítico (gestantes, cardiopatía).
        """)

    st.markdown("---")
    st.subheader("📊 Estimación numérica de candidatos (sobre pacientes en Eutirox)")

    pacientes_eutirox = unidades_eutirox_mes / 30.0

    # Supuestos de proporción de cada grupo, puedes afinarlos
    grupo_a = int(pacientes_eutirox * 0.125)   # 12.5 %
    grupo_b = int(pacientes_eutirox * 0.175)   # 17.5 %
    grupo_c = int(pacientes_eutirox * 0.30)    # 30 %
    solapamiento = int(pacientes_eutirox * 0.10)  # 10 % de solapamiento entre grupos

    fig_water = go.Figure(go.Waterfall(
        name="Candidatos",
        orientation="v",
        measure=["relative", "relative", "relative", "relative"],
        x=["TSH descontrolada", "Malabsorción", "Interacciones", "Solapamiento (-)"],
        text=[f"{grupo_a:,}", f"{grupo_b:,}", f"{grupo_c:,}", f"-{solapamiento:,}"],
        y=[grupo_a, grupo_b, grupo_c, -solapamiento],
        connector={"line": {"color": "rgb(63,63,63)"}}
    ))
    fig_water.update_layout(
        yaxis_title="Número de pacientes",
        height=450,
        title="Estimación escalonada de candidatos clínicos"
    )
    st.plotly_chart(fig_water, use_container_width=True)

    total_candidatos_estimados = pacientes_eutirox * (pct_candidatos_eutirox / 100)

    df_resumen = pd.DataFrame({
        "Indicador": [
            "Usuarios EPS",
            "Pacientes con hipotiroidismo (prevalencia aplicada)",
            "Pacientes tratados con levotiroxina (por consumo)",
            "Pacientes en Eutirox (por consumo)",
            "Candidatos clínicos estimados a Prolevo®",
            "Pacientes que migran a Prolevo®"
        ],
        eps_sel: [
            f"{usuarios_eps:,.0f}",
            f"{pacientes_hipo_prevalencia:,.0f}",
            f"{pacientes_tratados_aprox:,.0f}",
            f"{pacientes_eutirox:,.0f}",
            f"{total_candidatos_estimados:,.0f}",
            f"{pacientes_migrados:,.0f}"
        ]
    })
    st.dataframe(df_resumen, use_container_width=True, hide_index=True)

# --------------------------------------------------------------------
# TAB 3 – Análisis económico y riesgo compartido
# --------------------------------------------------------------------
with tab3:
    st.header("💰 Análisis económico y modelo de riesgo compartido")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Costo anual de fármacos – base", f"${costo_anual_farmacos_base:,.0f}")
    with c2:
        st.metric("Costo anual de fármacos – escenario ajustado",
                  f"${costo_anual_farmacos_escenario_ajustado:,.0f}")
    with c3:
        st.metric("Costo por descontrol de TSH – base",
                  f"${costo_clinico_base:,.0f}",
                  delta=f"Escenario: ${costo_clinico_escenario:,.0f}")

    st.markdown("---")

    # Desglose de costos
    df_costos = pd.DataFrame({
        "Concepto": [
            "Fármacos – base",
            "Fármacos – escenario (ajustado por riesgo compartido)",
            "Costos clínicos – base (no controlados)",
            "Costos clínicos – escenario (no controlados)"
        ],
        "Costo anual (COP)": [
            costo_anual_farmacos_base,
            costo_anual_farmacos_escenario_ajustado,
            costo_clinico_base,
            costo_clinico_escenario
        ]
    })

    fig_stack = px.bar(
        df_costos,
        x="Concepto",
        y="Costo anual (COP)",
        title="Desglose de costos anuales"
    )
    st.plotly_chart(fig_stack, use_container_width=True)

    st.markdown("---")
    st.subheader("🎲 Análisis de sensibilidad: penetración de Prolevo® vs ahorro")

    escenarios_pen = np.arange(0.10, 0.41, 0.05)
    ahorros_esc = []

    for pen in escenarios_pen:
        unidades_mig = unidades_eutirox_mes * (pct_candidatos_eutirox / 100) * pen
        pacs_mig = unidades_mig / 30.0

        # Simple: solo cambiamos número de migrados, el resto igual
        control_mig = pacs_mig * (tsh_control_prolevo / 100)
        pacs_no_mig = pacientes_tratados_aprox - pacs_mig
        control_no_mig = pacs_no_mig * (tsh_control_base / 100)

        control_total = control_mig + control_no_mig
        no_control = pacientes_tratados_aprox - control_total
        costo_clinico = no_control * costo_no_controlado

        unidades_eut_rem = unidades_eutirox_mes - unidades_mig
        costo_farm = ((unidades_eut_rem * precio_prom_eutirox) +
                      (unidades_generico_mes * precio_prom_generico) +
                      (unidades_mig * precio_prom_prolevo)) * 12

        porc_control = 100 * control_total / pacientes_tratados_aprox
        if porc_control < meta_control:
            costo_farm -= unidades_mig * precio_prom_prolevo * 12 * (descuento_prolevo / 100)

        costo_total = costo_farm + costo_clinico
        ahorros_esc.append(costo_total_base - costo_total)

    fig_sens = go.Figure()
    fig_sens.add_trace(go.Scatter(
        x=escenarios_pen * 100,
        y=ahorros_esc,
        mode="lines+markers",
        name="Ahorro anual",
        line=dict(color="#2a9d8f", width=3)
    ))
    fig_sens.add_trace(go.Scatter(
        x=[pct_migracion_candidatos],
        y=[ahorro_neto_ajustado],
        mode="markers",
        name="Escenario actual",
        marker=dict(size=12, color="#e63946", symbol="star")
    ))
    fig_sens.update_layout(
        xaxis_title="Penetración entre candidatos (%)",
        yaxis_title="Ahorro anual (COP)",
        height=400
    )
    st.plotly_chart(fig_sens, use_container_width=True)

    st.markdown("---")
    st.subheader("📤 Exportar resumen a Excel (para soporte de notas técnicas y médicas)")

    # Detalle por presentación
    df_detalle = df[[
        "Descripcion", "Dosis_mcg", "Tipo", "Compania",
        "RotacionMes_EPS", "PrecioProm", "CostoMes_EPS"
    ]].copy()
    df_detalle["RotacionMes_EPS"] = df_detalle["RotacionMes_EPS"].round(0)

    resumen = pd.DataFrame({
        "EPS / cohorte": [eps_sel],
        "Población afiliada": [usuarios_eps],
        "Pacientes tratados estimados": [pacientes_tratados_aprox],
        "Pacientes migrados a Prolevo": [pacientes_migrados],
        "% TSH controlada – base": [tsh_control_base],
        "% TSH controlada – escenario": [porc_control_escenario],
        "Costo total anual – base (COP)": [costo_total_base],
        "Costo total anual – escenario (COP)": [costo_total_escenario],
        "Ahorro neto ajustado (COP/año)": [ahorro_neto_ajustado],
    })

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_detalle.to_excel(writer, index=False, sheet_name="Detalle_presentaciones")
        resumen.to_excel(writer, index=False, sheet_name="Resumen_EPS")
    output.seek(0)

    st.download_button(
        "📥 Descargar Excel con resumen",
        data=output,
        file_name=f"Prolevo_riesgo_compartido_{eps_sel.replace(' ', '_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --------------------------------------------------------------------
# TAB 4 – Proyección a 3 años (simple)
# --------------------------------------------------------------------
with tab4:
    st.header("🎯 Proyección a 3 años")

    st.markdown("Se asume que la penetración entre candidatos crece de forma escalonada en 3 años.")

    pen_a1 = (pct_migracion_candidatos / 100) * 0.5
    pen_a2 = (pct_migracion_candidatos / 100) * 0.8
    pen_a3 = (pct_migracion_candidatos / 100) * 1.0

    años = ["Año 1", "Año 2", "Año 3"]
    penetraciones = [pen_a1, pen_a2, pen_a3]

    pacientes_por_año = [pacientes_eutirox * (pct_candidatos_eutirox / 100) * p for p in penetraciones]

    costos_eut = []
    costos_prol = []
    ahorros = []

    for pacs_mig in pacientes_por_año:
        unidades_mig = pacs_mig * 30.0
        unidades_eut_rem = unidades_eutirox_mes - unidades_mig

        costo_eut_ano = unidades_eutirox_mes * precio_prom_eutirox * 12
        costo_prol_ano = ((unidades_eut_rem * precio_prom_eutirox) +
                          (unidades_generico_mes * precio_prom_generico) +
                          (unidades_mig * precio_prom_prolevo)) * 12

        costos_eut.append(costo_eut_ano)
        costos_prol.append(costo_prol_ano)
        ahorros.append(costo_eut_ano - costo_prol_ano)

    ahorro_acum = np.cumsum(ahorros)

    c1, c2 = st.columns(2)
    with c1:
        fig_pac = go.Figure(go.Scatter(
            x=años,
            y=pacientes_por_año,
            mode="lines+markers+text",
            text=[f"{int(p):,}" for p in pacientes_por_año],
            textposition="top center"
        ))
        fig_pac.update_layout(
            yaxis_title="Pacientes en Prolevo®",
            height=400
        )
        st.plotly_chart(fig_pac, use_container_width=True)

    with c2:
        fig_ah = go.Figure(go.Bar(
            x=años,
            y=ahorros,
            text=[f"${a:,.0f}" for a in ahorros],
            textposition="auto"
        ))
        fig_ah.update_layout(
            yaxis_title="Ahorro anual (solo fármacos, COP)",
            height=400
        )
        st.plotly_chart(fig_ah, use_container_width=True)

    st.markdown("---")
    st.subheader("📊 Ahorro acumulado a 3 años")

    fig_acum = go.Figure(go.Scatter(
        x=años,
        y=ahorro_acum,
        mode="lines+markers+text",
        text=[f"${a:,.0f}" for a in ahorro_acum],
        textposition="top center",
        fill="tozeroy"
    ))
    fig_acum.update_layout(
        yaxis_title="Ahorro acumulado (COP)",
        height=400
    )
    st.plotly_chart(fig_acum, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Pacientes en Prolevo® al año 3", f"{int(pacientes_por_año[-1]):,}")
    with c2:
        st.metric("Ahorro acumulado 3 años", f"${ahorro_acum[-1]:,.0f}")
    with c3:
        ahorro_per_capita = ahorro_acum[-1] / (pacientes_por_año[-1] + 1e-6)
        st.metric("Ahorro medio por paciente (año 3)", f"${ahorro_per_capita:,.0f}")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>Dashboard Interactivo – Propuesta Prolevo® con modelo de riesgo compartido</strong></p>
    <p>Los resultados pueden anexarse como soporte a notas médicas y farmacoterapéuticas
    para justificar el cambio de formulación en pacientes seleccionados.</p>
</div>
""", unsafe_allow_html=True)
