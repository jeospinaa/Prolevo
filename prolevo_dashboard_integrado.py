#!/usr/bin/env python3
"""
Dashboard interactivo – Propuesta de riesgo compartido PROLEVO® v3.0
Basado 100% en la tabla real de consumo de levotiroxina (cohorte 1 millón de usuarios)
y en las tres propuestas de valor para SURA y SANITAS.

Autor: Jorge Ospina (contenido) / Asistente IA (armado del código)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILO
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PROLEVO® – Modelo de riesgo compartido",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Dashboard PROLEVO®")

st.markdown("""
<style>
/* Cabecera principal */
.main-title {
    font-size: 2.3rem;
    font-weight: 700;
    text-align: center;
    color: #0F4C81;
    margin-bottom: 0.3rem;
}
.main-subtitle {
    font-size: 1.0rem;
    text-align: center;
    color: #555;
    margin-bottom: 1.5rem;
}

/* Cajitas de propuesta */
.proposal-box {
    background: #F3F7FB;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 10px;
    border-left: 4px solid #0F4C81;
}

/* Métricas más compactas */
[data-testid="stMetricValue"] {
    font-size: 1.3rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">PROLEVO® – Levotiroxina líquida en cápsulas blandas</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Modelo clínico–económico y propuestas de riesgo compartido para EPS colombianas</div>', unsafe_allow_html=True)
st.markdown("---")

# -----------------------------------------------------------------------------
# DATOS REALES – COHORTE ESTÁNDAR 1.000.000 USUARIOS
# (los mismos del script de verificación v2.0)
# -----------------------------------------------------------------------------
datos_reales = [
    {"Descripcion": "LEVOTIROXINA SÓDICA 200MCG (TABLETA) - EUTIROX", "RotacionMes": 423, "PrecioUnitario": 1175, "Tipo": "Eutirox"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 137 MCG (TABLETA) - EUTIROX", "RotacionMes": 453, "PrecioUnitario": 753, "Tipo": "Eutirox"},
    {"Descripcion": "LEVOTIROXINA 62 MCG (TABLETA)", "RotacionMes": 641, "PrecioUnitario": 298, "Tipo": "Genérico"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 175 MCG (TABLETA) - EUTIROX", "RotacionMes": 720, "PrecioUnitario": 1075, "Tipo": "Eutirox"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 112 MCG (TABLETA) - EUTIROX", "RotacionMes": 1254, "PrecioUnitario": 646, "Tipo": "Eutirox"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 137 MCG (TABLETA)", "RotacionMes": 1377, "PrecioUnitario": 753, "Tipo": "Eutirox"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 175 MCG (TABLETA)", "RotacionMes": 1544, "PrecioUnitario": 1075, "Tipo": "Eutirox"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 25 MCG (TABLETA) - EUTIROX", "RotacionMes": 1628, "PrecioUnitario": 571, "Tipo": "Eutirox"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 88 MCG (TABLETA) - EUTIROX", "RotacionMes": 2109, "PrecioUnitario": 620, "Tipo": "Eutirox"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 150 MCG - EUTIROX (TABLETA)", "RotacionMes": 2794, "PrecioUnitario": 353, "Tipo": "Eutirox"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 125 MCG - EUTIROX (TABLETA)", "RotacionMes": 2979, "PrecioUnitario": 475, "Tipo": "Eutirox"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 112 MCG (TABLETA)", "RotacionMes": 3442, "PrecioUnitario": 320, "Tipo": "Genérico"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 88 MCG (TABLETA)", "RotacionMes": 7400, "PrecioUnitario": 288, "Tipo": "Genérico"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 50 MCG (TABLETA) - EUTIROX", "RotacionMes": 8168, "PrecioUnitario": 131, "Tipo": "Eutirox"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 150 MCG (TABLETA)", "RotacionMes": 8547, "PrecioUnitario": 94, "Tipo": "Genérico"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 100 MCG EUTIROX (TABLETA)", "RotacionMes": 8598, "PrecioUnitario": 128, "Tipo": "Eutirox"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 75 MCG - EUTIROX (TABLETA)", "RotacionMes": 9503, "PrecioUnitario": 258, "Tipo": "Eutirox"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 125 MCG (TABLETA)", "RotacionMes": 11964, "PrecioUnitario": 83, "Tipo": "Genérico"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 25 MCG (TABLETA)", "RotacionMes": 16697, "PrecioUnitario": 58, "Tipo": "Genérico"},
    {"Descripcion": "LEVOTIROXINA SÓDICA 75 MCG (TABLETA)", "RotacionMes": 65631, "PrecioUnitario": 64, "Tipo": "Genérico"},
]

df_base = pd.DataFrame(datos_reales)

# Totales cohorte 1M
unidades_total_mes = df_base["RotacionMes"].sum()
unidades_eut_mes = df_base[df_base["Tipo"] == "Eutirox"]["RotacionMes"].sum()
unidades_gen_mes = df_base[df_base["Tipo"] == "Genérico"]["RotacionMes"].sum()

costo_mensual_eut = (df_base[df_base["Tipo"] == "Eutirox"]["RotacionMes"] *
                     df_base[df_base["Tipo"] == "Eutirox"]["PrecioUnitario"]).sum()
costo_mensual_gen = (df_base[df_base["Tipo"] == "Genérico"]["RotacionMes"] *
                     df_base[df_base["Tipo"] == "Genérico"]["PrecioUnitario"]).sum()
costo_mensual_total = costo_mensual_eut + costo_mensual_gen

pacientes_total_1M = unidades_total_mes / 30.0
pacientes_eut_1M = unidades_eut_mes / 30.0

precio_prom_eut = costo_mensual_eut / unidades_eut_mes
precio_prom_gen = costo_mensual_gen / unidades_gen_mes

# Poblaciones EPS
eps_info = {
    "Cohorte estándar 1.000.000": 1_000_000,
    "SURA EPS": 5_447_647,
    "SANITAS EPS": 5_942_826,
    "SURA + SANITAS": 5_447_647 + 5_942_826,
}

# -----------------------------------------------------------------------------
# SIDEBAR – PARÁMETROS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Parámetros de simulación")

    eps_sel = st.selectbox("Seleccione EPS / cohorte:", list(eps_info.keys()), index=1)
    usuarios_eps = eps_info[eps_sel]
    factor = usuarios_eps / 1_000_000

    st.markdown("—")
    st.subheader("👥 Selección de pacientes")

    pct_candidatos = st.slider(
        "% de pacientes en Eutirox clínicamente candidatos a Prolevo®",
        10.0, 60.0, 35.0, 1.0
    )
    pct_migrados = st.slider(
        "% de candidatos que efectivamente migran",
        10.0, 100.0, 50.0, 5.0
    )

    st.caption("Escenarios de referencia sobre pacientes en Eutirox:\n"
               "• Conservador 38,8%  • Moderado 46,3%  • Agresivo 52,8%")

    st.markdown("—")
    st.subheader("💊 Precio y eficacia clínica")

    precio_rel_prolevo = st.slider(
        "Precio Prolevo® vs precio promedio Eutirox",
        0.50, 1.00, 1.00, 0.05,
        help="1.00 = mismo precio por tableta; 0.50 = 50% más barato"
    )
    reduccion_dosis = st.slider(
        "Reducción de dosis con Prolevo® (%)",
        10.0, 25.0, 20.0, 1.0
    )
    reduccion_ajustes = st.slider(
        "Reducción de ajustes de dosis (%)",
        20.0, 60.0, 45.0, 1.0
    )

    st.markdown("—")
    st.subheader("📈 Control de TSH")

    control_base = st.slider(
        "% de pacientes con TSH controlada con tableta",
        40, 90, 70, 1
    )
    control_prolevo = st.slider(
        "% de pacientes con TSH controlada con Prolevo®",
        60, 98, 88, 1
    )

    st.markdown("—")
    st.subheader("💰 Costos clínicos y monitoreo")

    costo_no_controlado = st.number_input(
        "Costo anual por paciente con TSH no controlada (COP)",
        min_value=0.0, value=150_000.0, step=50_000.0,
        help="Incluye consultas adicionales, laboratorios y descompensaciones"
    )
    costo_monitoreo_paciente = st.number_input(
        "Costo de monitoreo del cambio (primer año, por paciente migrado)",
        min_value=0.0, value=93_000.0, step=10_000.0
    )

    st.markdown("—")
    st.subheader("🎯 Parámetros de riesgo compartido")

    meta_control = st.slider(
        "Meta mínima de TSH controlada en pacientes migrados (%)",
        70, 95, 85, 1
    )
    meta_qol = st.slider(
        "Meta de pacientes con mejora significativa en QoL (%)",
        40, 80, 60, 1
    )

# -----------------------------------------------------------------------------
# MOTOR DE CÁLCULO BASE
# -----------------------------------------------------------------------------
def calcular_escenario_base_y_migracion():
    """Calcula métricas base y escenario con Prolevo para la EPS seleccionada."""

    # Escalamiento por EPS
    pacientes_tot = pacientes_total_1M * factor
    pacientes_eut = pacientes_eut_1M * factor
    pacientes_gen = pacientes_tot - pacientes_eut

    costo_farm_base_anual = costo_mensual_total * factor * 12

    # Candidatos y migrados (sobre Eutirox)
    candidatos = pacientes_eut * (pct_candidatos / 100.0)
    migrados = candidatos * (pct_migrados / 100.0)

    # Unidades asociadas
    unidades_eut_eps = unidades_eut_mes * factor
    unidades_gen_eps = unidades_gen_mes * factor

    # Pacientes en Eutirox que NO migran
    pacientes_eut_no_mig = pacientes_eut - migrados

    # Unidades de Eutirox que se reemplazan
    unidades_por_paciente_eut = unidades_eut_eps / pacientes_eut if pacientes_eut > 0 else 0
    unidades_migradas = migrados * unidades_por_paciente_eut

    # Unidades Prolevo (considerando reducción de dosis)
    factor_dosis = 1.0 - (reduccion_dosis / 100.0)
    unidades_prolevo = unidades_migradas * factor_dosis

    # Unidades de Eutirox remanentes
    unidades_eut_rem = unidades_eut_eps - unidades_migradas

    # Precios promedio
    precio_prolevo = precio_prom_eut * precio_rel_prolevo

    # Costos farmacológicos – escenario "Prolevo sin riesgo"
    costo_eut_mes_esc = unidades_eut_rem * precio_prom_eut
    costo_gen_mes_esc = unidades_gen_eps * precio_prom_gen
    costo_prolevo_mes_esc = unidades_prolevo * precio_prolevo

    costo_farm_escenario_anual = (costo_eut_mes_esc + costo_gen_mes_esc + costo_prolevo_mes_esc) * 12

    # Control de TSH y costos clínicos
    # Base: todos con esquema actual
    controlados_base = pacientes_tot * (control_base / 100.0)
    no_controlados_base = pacientes_tot - controlados_base
    costo_clinico_base = no_controlados_base * costo_no_controlado

    # Escenario: migrados con eficacia de Prolevo, el resto igual que base
    control_migrados = migrados * (control_prolevo / 100.0)
    control_no_migrados = (pacientes_tot - migrados) * (control_base / 100.0)
    controlados_esc = control_migrados + control_no_migrados
    no_controlados_esc = pacientes_tot - controlados_esc
    costo_clinico_esc = no_controlados_esc * costo_no_controlado

    # Monitoreo
    costo_monitoreo_total = migrados * costo_monitoreo_paciente

    return {
        "pacientes_tot": pacientes_tot,
        "pacientes_eut": pacientes_eut,
        "pacientes_gen": pacientes_gen,
        "candidatos": candidatos,
        "migrados": migrados,
        "costo_farm_base_anual": costo_farm_base_anual,
        "costo_farm_escenario_anual": costo_farm_escenario_anual,
        "controlados_base": controlados_base,
        "controlados_esc": controlados_esc,
        "no_controlados_base": no_controlados_base,
        "no_controlados_esc": no_controlados_esc,
        "costo_clinico_base": costo_clinico_base,
        "costo_clinico_esc": costo_clinico_esc,
        "costo_monitoreo_total": costo_monitoreo_total,
        "precio_prolevo": precio_prolevo,
    }

esc = calcular_escenario_base_y_migracion()

# -----------------------------------------------------------------------------
# FUNCIONES AUXILIARES PARA LAS 3 PROPUESTAS
# -----------------------------------------------------------------------------
def descuento_por_volumen(pct_migracion_eut):
    """Descuento (%) por volumen sobre pacientes en Eutirox (Propuesta 2)."""
    if pct_migracion_eut < 10:
        return 0.0
    elif pct_migracion_eut < 20:
        return 5.0
    elif pct_migracion_eut < 30:
        return 10.0
    else:
        return 15.0

def aplicar_propuesta_1(escenario):
    """
    Propuesta 1 – Garantía de control bioquímico.
    Procaps paga TSH de todos los migrados y reembolsa Prolevo de los que no cumplen la meta.
    """
    migrados = escenario["migrados"]
    if migrados <= 0:
        return {"costo_total": escenario["costo_farm_base_anual"] + escenario["costo_clinico_base"],
                "reintegro": 0.0,
                "detalle": "Sin pacientes migrados."}

    # TSH de cambio la paga Procaps → se descuenta del costo clínico del pagador
    costo_clinico_pagador = escenario["costo_clinico_esc"]
    ahorro_lab = escenario["costo_monitoreo_total"]  # labs incluidos en monitoreo

    # Pacientes migrados que NO alcanzan meta de control
    frac_no_meta = max(0.0, (meta_control - control_prolevo) / meta_control) if control_prolevo < meta_control else 0.0
    reintegro = frac_no_meta * (escenario["costo_farm_escenario_anual"] - escenario["costo_farm_base_anual"])

    costo_total_pagador = escenario["costo_farm_escenario_anual"] + costo_clinico_pagador \
                          + escenario["costo_monitoreo_total"] - ahorro_lab - reintegro

    return {
        "costo_total": costo_total_pagador,
        "reintegro": max(reintegro, 0.0),
        "ahorro_lab": ahorro_lab
    }

def aplicar_propuesta_2(escenario):
    """
    Propuesta 2 – Descuentos progresivos por volumen + performance.
    Descuento sobre Prolevo según % de migración en pacientes Eutirox
    + 5% adicional si se cumple meta de control de TSH.
    """
    if escenario["pacientes_eut"] <= 0:
        return {"costo_total": escenario["costo_farm_base_anual"] + escenario["costo_clinico_base"],
                "descuento_total": 0.0}

    pct_migracion_eut = 100.0 * escenario["migrados"] / escenario["pacientes_eut"]
    desc_vol = descuento_por_volumen(pct_migracion_eut)
    desc_perf = 5.0 if control_prolevo >= meta_control else 0.0
    descuento_total = min(20.0, desc_vol + desc_perf)

    # Ajustar costo de Prolevo dentro del costo farmacológico del escenario
    costo_farm = escenario["costo_farm_escenario_anual"]
    costo_farm_desc = costo_farm * (1 - descuento_total / 100.0)

    costo_total = costo_farm_desc + escenario["costo_clinico_esc"] + escenario["costo_monitoreo_total"]

    return {
        "costo_total": costo_total,
        "descuento_total": descuento_total,
        "pct_migracion_eut": pct_migracion_eut
    }

def aplicar_propuesta_3(escenario):
    """
    Propuesta 3 – Modelo híbrido QoL.
    Precio Prolevo = Eutirox + 3%, con posibilidad de -2% en año 2 si se cumplen metas de QoL
    + ahorro compartido en consultas.
    Aquí se muestra solo el año 1.
    """
    premium = 0.03  # +3% sobre precio de referencia (ya incluido en slider si se desea)
    # Ajustamos solo la parte de Prolevo: aproximación usando costo farmacológico escenario
    costo_farm = escenario["costo_farm_escenario_anual"] * (1 + premium)

    # Supongamos que mejor control reduce 20% las consultas por mal control
    # y que la mitad de ese ahorro se comparte con la EPS como descuento efectivo.
    ahorro_consultas_teorico = (escenario["no_controlados_base"] - escenario["no_controlados_esc"]) * 2 * 45_000
    ahorro_compartido = 0.5 * max(0.0, ahorro_consultas_teorico)

    # Bonificación de -2% en precio para año 2 queda como mensaje; aquí usamos solo año 1.
    costo_total = costo_farm + escenario["costo_clinico_esc"] + escenario["costo_monitoreo_total"] - ahorro_compartido

    return {
        "costo_total": costo_total,
        "ahorro_compartido": ahorro_compartido
    }

# Costos totales base (sin Prolevo)
costo_total_base = esc["costo_farm_base_anual"] + esc["costo_clinico_base"]

# Aplicar propuestas
res_p1 = aplicar_propuesta_1(esc)
res_p2 = aplicar_propuesta_2(esc)
res_p3 = aplicar_propuesta_3(esc)

# -----------------------------------------------------------------------------
# LAYOUT PRINCIPAL – TABS
# -----------------------------------------------------------------------------
tab_resumen, tab_p1, tab_p2, tab_p3, tab_datos = st.tabs([
    "📈 Resumen ejecutivo",
    "🧪 Propuesta 1 – Garantía TSH",
    "📊 Propuesta 2 – Descuentos progresivos",
    "🎯 Propuesta 3 – Modelo híbrido QoL",
    "📂 Datos y supuestos"
])

# ------------------------------ TAB RESUMEN ----------------------------------
with tab_resumen:
    st.subheader("📈 Resumen ejecutivo del escenario seleccionado")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Afiliados EPS", f"{usuarios_eps:,.0f}")
    with col2:
        st.metric("Pacientes tratados con levotiroxina",
                  f"{esc['pacientes_tot']:,.0f}")
    with col3:
        st.metric("Pacientes migrados a PROLEVO®", f"{esc['migrados']:,.0f}",
                  delta=f"{pct_migrados:.0f}% de candidatos")
    with col4:
        ahorro_p1 = costo_total_base - res_p1["costo_total"]
        st.metric("Ahorro estimado – Propuesta 1",
                  f"${ahorro_p1:,.0f}",
                  delta=f"{ahorro_p1 / costo_total_base * 100:0.1f}% vs base")

    st.markdown("—")
    st.markdown("### Distribución de pacientes y control de TSH")

    c1, c2 = st.columns(2)
    with c1:
        labels = ["Eutirox (no migran)", "Prolevo® (migrados)", "Genéricos"]
        values = [
            esc["pacientes_eut"] - esc["migrados"],
            esc["migrados"],
            esc["pacientes_gen"]
        ]
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
        fig_pie.update_layout(height=360)
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            name="Base (solo tabletas)",
            x=["Pacientes controlados", "No controlados"],
            y=[esc["controlados_base"], esc["no_controlados_base"]],
        ))
        fig_bar.add_trace(go.Bar(
            name="Con PROLEVO®",
            x=["Pacientes controlados", "No controlados"],
            y=[esc["controlados_esc"], esc["no_controlados_esc"]],
        ))
        fig_bar.update_layout(
            barmode="group",
            height=360,
            yaxis_title="Número de pacientes"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("—")
    st.markdown("### Comparación de costo total anual por modelo")

    df_costo = pd.DataFrame({
        "Escenario": [
            "Base (sin PROLEVO®)",
            "Propuesta 1 – Garantía TSH",
            "Propuesta 2 – Descuentos progresivos",
            "Propuesta 3 – Modelo híbrido QoL",
        ],
        "Costo total anual (COP)": [
            costo_total_base,
            res_p1["costo_total"],
            res_p2["costo_total"],
            res_p3["costo_total"],
        ]
    })

    fig_cost = px.bar(
        df_costo,
        x="Escenario",
        y="Costo total anual (COP)",
        text="Costo total anual (COP)"
    )
    fig_cost.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_cost.update_layout(height=420, xaxis_tickangle=-10)
    st.plotly_chart(fig_cost, use_container_width=True)

    st.markdown("""
    <div class="proposal-box">
    <b>Cómo leer este gráfico:</b><br>
    • La columna gris muestra el costo actual de la EPS con el mix real de Eutirox + genéricos.<br>
    • Cada color corresponde a una propuesta de riesgo compartido distinta, incluyendo costo de monitorización.<br>
    • La brecha entre cada barra y el escenario base corresponde al ahorro o sobrecosto neto esperado.
    </div>
    """, unsafe_allow_html=True)

# ------------------------------ TAB P1 ---------------------------------------
with tab_p1:
    st.subheader("🧪 Propuesta 1 – Modelo de riesgo compartido con garantía de control bioquímico")

    st.markdown("""
    <div class="proposal-box">
    <ul>
      <li>Procaps garantiza que al menos <b>{}%</b> de los pacientes migrados alcancen TSH en rango objetivo.</li>
      <li>Procaps asume el <b>100% del costo de TSH</b> de monitoreo del cambio.</li>
      <li>Si no se cumple la meta de control, Procaps <b>reembolsa el costo de PROLEVO®</b> de los pacientes fuera de objetivo.</li>
    </ul>
    </div>
    """.format(meta_control), unsafe_allow_html=True)

    ahorro = costo_total_base - res_p1["costo_total"]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Costo total anual – BASE", f"${costo_total_base:,.0f}")
    with col2:
        st.metric("Costo total anual – Propuesta 1", f"${res_p1['costo_total']:,.0f}",
                  delta=f"${ahorro:,.0f}")
    with col3:
        st.metric("Reintegros potenciales Procaps",
                  f"${res_p1['reintegro']:,.0f}",
                  help="Monto aproximado de reembolso si no se cumple la meta de TSH")

    st.markdown("—")
    st.write("**Desglose de costos incluidos en la Propuesta 1:**")

    df_p1 = pd.DataFrame({
        "Concepto": [
            "Fármacos (Eutirox + genéricos + PROLEVO®)",
            "Costos clínicos (pacientes no controlados)",
            "Monitoreo del cambio (TSH + consultas)",
            "Reintegros Procaps (negativo para la EPS)"
        ],
        "Costo (COP)": [
            esc["costo_farm_escenario_anual"],
            esc["costo_clinico_esc"],
            esc["costo_monitoreo_total"],
            -res_p1["reintegro"],
        ]
    })

    fig_p1 = px.bar(df_p1, x="Concepto", y="Costo (COP)", text="Costo (COP)")
    fig_p1.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_p1.update_layout(height=400, xaxis_tickangle=-15)
    st.plotly_chart(fig_p1, use_container_width=True)

# ------------------------------ TAB P2 ---------------------------------------
with tab_p2:
    st.subheader("📊 Propuesta 2 – Descuentos progresivos por volumen y performance")

    st.markdown("""
    <div class="proposal-box">
    <ul>
      <li>Precio de lista de PROLEVO® en <b>paridad con Eutirox</b> (o el factor que definas en el panel lateral).</li>
      <li>Descuento automático según volumen de migración sobre pacientes en Eutirox:</li>
      <ul>
        <li>10–20% de migración: <b>–5%</b> sobre el precio de PROLEVO®</li>
        <li>20–30%: <b>–10%</b></li>
        <li>&gt;30%: <b>–15%</b></li>
      </ul>
      <li>Bonificación adicional de <b>–5%</b> si el control de TSH en la cohorte migrada es ≥ meta establecida.</li>
      <li>Descuento total máximo: <b>–20%</b> (15% volumen + 5% performance).</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    ahorro = costo_total_base - res_p2["costo_total"]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("% migración sobre Eutirox",
                  f"{res_p2['pct_migracion_eut']:0.1f}%")
    with col2:
        st.metric("Descuento total aplicado a PROLEVO®",
                  f"{res_p2['descuento_total']:0.1f}%")
    with col3:
        st.metric("Ahorro neto anual – Propuesta 2",
                  f"${ahorro:,.0f}",
                  delta=f"{ahorro / costo_total_base * 100:0.1f}% vs base")

    st.markdown("—")
    df_p2 = pd.DataFrame({
        "Escenario": ["Base (sin PROLEVO®)", "Propuesta 2"],
        "Costo total anual (COP)": [costo_total_base, res_p2["costo_total"]]
    })
    fig_p2 = px.bar(df_p2, x="Escenario", y="Costo total anual (COP)",
                    text="Costo total anual (COP)")
    fig_p2.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_p2.update_layout(height=380)
    st.plotly_chart(fig_p2, use_container_width=True)

# ------------------------------ TAB P3 ---------------------------------------
with tab_p3:
    st.subheader("🎯 Propuesta 3 – Modelo híbrido con calidad de vida y ahorro compartido")

    st.markdown(f"""
    <div class="proposal-box">
    <ul>
      <li>Precio de PROLEVO® con una prima teórica de <b>+3%</b> sobre Eutirox.</li>
      <li>Meta de control de TSH: <b>{meta_control}%</b> de pacientes migrados.</li>
      <li>Meta de mejora en calidad de vida (Cuestionarios ThyPRO/SF-36): <b>{meta_qol}%</b> de pacientes con cambio clínicamente relevante.</li>
      <li>Si se cumplen ambas metas, se ofrece una <b>reducción de 2% en el precio</b> a partir del año 2.</li>
      <li>Reducción observada en consultas por hipotiroidismo mal controlado se comparte al 50% como descuento efectivo.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    ahorro = costo_total_base - res_p3["costo_total"]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ahorro compartido en consultas (año 1)",
                  f"${res_p3['ahorro_compartido']:,.0f}")
    with col2:
        st.metric("Ahorro neto anual – Propuesta 3",
                  f"${ahorro:,.0f}",
                  delta=f"{ahorro / costo_total_base * 100:0.1f}% vs base")
    with col3:
        st.metric("Pacientes con potencial medición de QoL",
                  f"{esc['migrados']:,.0f}",
                  help="Cohorte en la que se aplicarían los cuestionarios")

    st.markdown("—")
    df_p3 = pd.DataFrame({
        "Escenario": ["Base (sin PROLEVO®)", "Propuesta 3"],
        "Costo total anual (COP)": [costo_total_base, res_p3["costo_total"]]
    })
    fig_p3 = px.bar(df_p3, x="Escenario", y="Costo total anual (COP)",
                    text="Costo total anual (COP)")
    fig_p3.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_p3.update_layout(height=380)
    st.plotly_chart(fig_p3, use_container_width=True)

# ------------------------------ TAB DATOS ------------------------------------
with tab_datos:
    st.subheader("📂 Datos reales y supuestos de modelamiento")

    st.markdown("#### Tabla base de consumo mensual (cohorte 1.000.000 usuarios)")
    df_viz = df_base.copy()
    df_viz["CostoMes"] = df_viz["RotacionMes"] * df_viz["PrecioUnitario"]
    st.dataframe(df_viz, use_container_width=True)

    st.markdown("#### Resumen numérico para la cohorte seleccionada")

    resumen = pd.DataFrame({
        "Indicador": [
            "Afiliados EPS",
            "Pacientes tratados con levotiroxina (estimado por consumo)",
            "Pacientes en Eutirox",
            "Pacientes en genéricos",
            "Candidatos clínicos a PROLEVO®",
            "Pacientes migrados a PROLEVO®",
            "% migración sobre Eutirox",
        ],
        eps_sel: [
            f"{usuarios_eps:,.0f}",
            f"{esc['pacientes_tot']:,.0f}",
            f"{esc['pacientes_eut']:,.0f}",
            f"{esc['pacientes_gen']:,.0f}",
            f"{esc['candidatos']:,.0f}",
            f"{esc['migrados']:,.0f}",
            f"{100 * esc['migrados'] / esc['pacientes_eut'] if esc['pacientes_eut']>0 else 0:0.1f}%",
        ]
    })
    st.dataframe(resumen, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.caption("""
    Todas las cifras anteriores se calculan a partir de la tabla real de rotación mensual
    de levotiroxina en una población estándar de 1.000.000 de afiliados, escalada
    proporcionalmente al número de afiliados de la EPS seleccionada.
    """)

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
Dashboard interactivo de soporte para notas técnicas y negociación de acuerdos
 de riesgo compartido PROLEVO® vs Eutirox en SURA y SANITAS.
</div>
""", unsafe_allow_html=True)
