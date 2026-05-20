# ============================================================
# SISTEMA DINÂMICO INTELIGENTE DE IRRIGAÇÃO
# BASEADO EM EVAPOTRANSPIRAÇÃO (ET0)
# ============================================================

# Projeto:
# - Open-Meteo API
# - Penman-Monteith
# - Sistema Dinâmico
# - Otimização Matemática
# - Streamlit
#
# Objetivo:
# Minimizar desperdício hídrico
# mantendo ET0 próxima da ideal
#
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import requests
import math

from scipy.optimize import minimize

import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# CONFIG STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Sistema Inteligente de Irrigação",
    layout="wide"
)

# ============================================================
# TÍTULO
# ============================================================

st.title("🌱 Sistema Dinâmico Inteligente de Irrigação")

st.markdown("""
### Modelagem Matemática e Otimização da Evapotranspiração

O sistema:

- coleta dados meteorológicos;
- calcula evapotranspiração;
- modela perda hídrica;
- otimiza irrigação;
- reduz desperdício de água.
""")

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Configurações")

cidade = st.sidebar.text_input(
    "Cidade",
    value="Tupã"
)

ET_ideal = st.sidebar.slider(
    "ET0 Ideal",
    1.0,
    10.0,
    5.0,
    0.1
)

# ============================================================
# GEOLOCALIZAÇÃO
# ============================================================

geo_url = (
    f"https://geocoding-api.open-meteo.com/v1/search?"
    f"name={cidade}&count=1&language=pt&format=json"
)

geo_data = requests.get(geo_url).json()

latitude = geo_data["results"][0]["latitude"]
longitude = geo_data["results"][0]["longitude"]

# ============================================================
# API METEOROLÓGICA
# ============================================================

weather_url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={latitude}"
    f"&longitude={longitude}"
    f"&current="
    f"temperature_2m,"
    f"relative_humidity_2m,"
    f"wind_speed_10m,"
    f"shortwave_radiation,"
    f"surface_pressure"
)

weather_data = requests.get(weather_url).json()

current = weather_data["current"]

# ============================================================
# VARIÁVEIS
# ============================================================

T = current["temperature_2m"]

UR = current["relative_humidity_2m"]

u = current["wind_speed_10m"]

Rs = current["shortwave_radiation"]

P_atm = current["surface_pressure"]

# ============================================================
# RADIAÇÃO LÍQUIDA
# ============================================================

Rn = 0.77 * Rs

# ============================================================
# FUNÇÕES
# ============================================================

def calcular_vpd(T, UR):

    es = (
        0.6108 *
        math.exp((17.27 * T) / (T + 237.3))
    )

    ea = es * (UR / 100)

    return es - ea


def calcular_et0(T, UR, u2, Rn, P_atm):

    es = (
        0.6108 *
        math.exp((17.27 * T) / (T + 237.3))
    )

    ea = es * (UR / 100)

    delta = (
        4098 * es /
        ((T + 237.3) ** 2)
    )

    P_kPa = P_atm / 10

    gamma = 0.000665 * P_kPa

    ET0 = (

        (
            0.408 * delta * Rn
        )

        +

        (
            gamma *
            (900 / (T + 273)) *
            u2 *
            (es - ea)
        )

    ) / (

        delta +

        gamma * (1 + 0.34 * u2)

    )

    return max(ET0, 0)

# ============================================================
# ET0 REAL
# ============================================================

ET0_real = calcular_et0(
    T,
    UR,
    u,
    Rn,
    P_atm
)

# ============================================================
# VPD
# ============================================================

VPD_real = calcular_vpd(T, UR)

# ============================================================
# MODELO DINÂMICO
# ============================================================

# água perdida no sistema

perda_hidrica = ET0_real

# ============================================================
# FUNÇÃO OBJETIVO
# ============================================================

def funcao_objetivo(x):

    """
    x[0] = irrigação
    """

    irrigacao = x[0]

    # objetivo:
    # irrigação ideal ≈ ET ideal

    erro = (
        irrigacao - ET_ideal
    ) ** 2

    return erro

# ============================================================
# OTIMIZAÇÃO
# ============================================================

resultado = minimize(
    funcao_objetivo,
    x0=[ET0_real],
    bounds=[(0, 15)]
)

# ============================================================
# IRRIGAÇÃO ÓTIMA
# ============================================================

irrigacao_otima = resultado.x[0]

erro_otimo = resultado.fun

# ============================================================
# EFICIÊNCIA HÍDRICA
# ============================================================

eficiencia = (
    1 -
    abs(ET0_real - ET_ideal) / ET_ideal
) * 100

eficiencia = max(
    0,
    min(100, eficiencia)
)

# ============================================================
# CARDS
# ============================================================

st.header("📡 Dados Ambientais")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "🌡️ Temperatura",
    f"{T:.2f} °C"
)

c2.metric(
    "💧 Umidade",
    f"{UR:.2f} %"
)

c3.metric(
    "🌬️ Vento",
    f"{u:.2f} m/s"
)

c4.metric(
    "☀️ Radiação",
    f"{Rs:.2f}"
)

c5.metric(
    "🌱 ET0",
    f"{ET0_real:.2f}"
)

# ============================================================
# SISTEMA DINÂMICO
# ============================================================

st.header("📈 Sistema Dinâmico")

k1, k2, k3 = st.columns(3)

k1.metric(
    "💦 Perda Hídrica",
    f"{perda_hidrica:.2f}"
)

k2.metric(
    "🚿 Irrigação Ótima",
    f"{irrigacao_otima:.2f}"
)

k3.metric(
    "⚡ Eficiência",
    f"{eficiencia:.2f}%"
)

# ============================================================
# TOMADA DE DECISÃO
# ============================================================

st.header("🧠 Tomada de Decisão")

if ET0_real < 2:

    st.success("Baixa evapotranspiração")

    st.info("Pouca irrigação necessária")

elif ET0_real < 5:

    st.warning("Evapotranspiração moderada")

    st.info("Irrigação recomendada")

else:

    st.error("Alta evapotranspiração")

    st.warning("Irrigação urgente")

# ============================================================
# MODELO MATEMÁTICO
# ============================================================

st.header("📚 Modelagem Matemática")

st.latex(
    r"ET_0=\frac{0.408\Delta(R_n-G)+\gamma\frac{900}{T+273}u(e_s-e_a)}{\Delta+\gamma(1+0.34u)}"
)

st.markdown("""
A evapotranspiração representa:
- perda hídrica do sistema;
- demanda evaporativa da atmosfera.
""")

st.latex(
    r"\frac{dU}{dt}=I-ET"
)

st.markdown("""
Onde:

- U = água disponível;
- I = irrigação;
- ET = evapotranspiração.
""")

# ============================================================
# FUNÇÃO OBJETIVO
# ============================================================

st.header("🎯 Otimização Matemática")

st.latex(
    r"J=(I-ET_{ideal})^2"
)

st.latex(
    r"\min J"
)

st.markdown("""
O sistema tenta:

- minimizar o erro entre:
  - irrigação aplicada;
  - evapotranspiração ideal.

Isso reduz:
- desperdício hídrico;
- estresse vegetal.
""")

# ============================================================
# COMPARAÇÃO
# ============================================================

st.header("📊 Comparação")

comparacao = pd.DataFrame({

    "Variável": [
        "ET0 Real",
        "ET0 Ideal",
        "Irrigação Ótima"
    ],

    "Valor": [
        ET0_real,
        ET_ideal,
        irrigacao_otima
    ]
})

st.dataframe(
    comparacao,
    use_container_width=True
)

# ============================================================
# GRÁFICO
# ============================================================

fig = px.bar(
    comparacao,
    x="Variável",
    y="Valor",
    text_auto=True,
    title="Sistema Inteligente de Irrigação"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# VPD
# ============================================================

st.header("🌾 Estado Agroambiental")

st.metric(
    "VPD",
    f"{VPD_real:.2f} kPa"
)

if VPD_real < 0.8:

    st.info("Ambiente muito úmido")

elif VPD_real < 1.2:

    st.success("Ambiente ideal")

elif VPD_real < 1.6:

    st.warning("Ambiente em atenção")

else:

    st.error("Risco de estresse hídrico")

# ============================================================
# CONCLUSÃO
# ============================================================

st.header("✅ Conclusão")

st.markdown(f"""
O sistema identificou:

- ET0 atual = {ET0_real:.2f}
- ET0 ideal = {ET_ideal:.2f}
- Irrigação ótima = {irrigacao_otima:.2f}

O modelo realiza:
- modelagem matemática;
- sistema dinâmico;
- otimização ambiental;
- tomada de decisão inteligente.
""")