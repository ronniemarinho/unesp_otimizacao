# Sistema Dinâmico Inteligente para Irrigação com VPD e Grid Search

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_autorefresh import st_autorefresh
import firebase_admin
import plotly.express as px
from firebase_admin import credentials
from firebase_admin import db
# ============================================================
# CONFIGURAÇÕES INICIAIS
# ============================================================

st.set_page_config(layout="wide")

sns.set_theme()

# ============================================================
# TÍTULO
# ============================================================

st.title("Sistema Inteligente de Irrigação com Modelagem Dinâmica do Déficit de Pressão de Vapor")

# AUTO REFRESH A CADA 4 SEGUNDOS
##################################################
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(
        "fels_lagoa.svg",
        width=650
    )

st.markdown(
    "<h3 style='text-align: center;'>Desenvolvido por Prof. Dr. Ronnie Shida Marinho</h3>",
    unsafe_allow_html=True
)

# ============================================================
# INTRODUÇÃO
# ============================================================



st_autorefresh(interval=4000, key="dadosfirebase")

##################################################
# CONEXÃO FIREBASE
##################################################

# IMPORTANTE:
# Baixe a chave JSON do Firebase e coloque
# no mesmo diretório do projeto

if not firebase_admin._apps:

    cred = credentials.Certificate(
    dict(st.secrets["gcp_service_account"]))

    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://esp32-fe8e3-default-rtdb.firebaseio.com/'
    })

##################################################
# LER DADOS DO FIREBASE
##################################################

ref = db.reference("/historico")

dados = ref.get()

##################################################
# TRANSFORMAR EM DATAFRAME
##################################################

lista_dados = []

if dados:

    for chave, valor in dados.items():

        lista_dados.append({
            "Temperatura": valor.get("temperatura"),
            "Umidade": valor.get("umidade"),
            "DataHora": valor.get("data_hora")
        })

df = pd.DataFrame(lista_dados)

##################################################
# VERIFICA DADOS
##################################################

if df.empty:

    st.warning("Nenhum dado encontrado no Firebase.")

else:

    ##################################################
    # TRATAMENTO
    ##################################################

    df["DataHora"] = pd.to_datetime(
        df["DataHora"],
        format="%d/%m/%Y %H:%M:%S"
    )

    df = df.sort_values("DataHora")



    ##################################################
    # MÉTRICAS
    ##################################################

    temperatura_atual = df["Temperatura"].iloc[-1]
    umidade_atual = df["Umidade"].iloc[-1]

    temperatura_media = df["Temperatura"].mean()
    umidade_media = df["Umidade"].mean()

    ##################################################
    # CARDS
    ##################################################

    st.markdown("## 📊 Resumo Ambiental")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🌡️ Temperatura Atual",
            f"{temperatura_atual:.1f} °C"
        )

    with col2:
        st.metric(
            "💧 Umidade Atual",
            f"{umidade_atual:.1f} %"
        )

    with col3:
        st.metric(
            "📈 Temperatura Média",
            f"{temperatura_media:.1f} °C"
        )

    with col4:
        st.metric(
            "📉 Umidade Média",
            f"{umidade_media:.1f} %"
        )

    ##################################################
    # GRÁFICOS
    ##################################################

    col1, col2 = st.columns(2)

    ##################################################
    # GRÁFICO TEMPERATURA
    ##################################################

    fig_temp = px.line(
        df,
        x="DataHora",
        y="Temperatura",
        title="🌡️ Temperatura ao Longo do Tempo",
        markers=True,
        color_discrete_sequence=["red"]
    )

    col1.plotly_chart(fig_temp, use_container_width=True)

    ##################################################
    # GRÁFICO UMIDADE
    ##################################################

    fig_umidade = px.line(
        df,
        x="DataHora",
        y="Umidade",
        title="💧 Umidade ao Longo do Tempo",
        markers=True

    )

    col2.plotly_chart(fig_umidade, use_container_width=True)

    ##################################################
    # HISTOGRAMA TEMPERATURA
    ##################################################

    col3, col4 = st.columns(2)

    fig_hist_temp = px.histogram(
        df,
        x="Temperatura",
        nbins=20,
        title="Distribuição de Temperatura",
        color_discrete_sequence=["red"]
    )

    col3.plotly_chart(fig_hist_temp, use_container_width=True)

    ##################################################
    # HISTOGRAMA UMIDADE
    ##################################################

    fig_hist_umidade = px.histogram(
        df,
        x="Umidade",
        nbins=20,
        title="Distribuição de Umidade"
    )

    col4.plotly_chart(fig_hist_umidade, use_container_width=True)




# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.image("fels_lagoa.svg", use_container_width=True)



# ============================================================
# DADOS VINDOS DO FIREBASE
# ============================================================
tempo_real = df["DataHora"]

#tempo = np.arange(len(df))
tempo = np.arange(len(df))


T = df["Temperatura"].values

U = df["Umidade"].values

base = pd.DataFrame({
    "Tempo": tempo_real,
    "Temperatura": T,
    "Umidade": U
})# ============================================================
# DATAFRAME
# ============================================================

base = pd.DataFrame({
    "Tempo": tempo,
    "Temperatura": T,
    "Umidade": U
})

# ============================================================
# 1. CARREGAMENTO DOS DADOS
# ============================================================

st.header("1. Captação dos Dados Ambientais")

st.subheader("Prévia da Base de Dados")

st.dataframe(base, use_container_width=True)

# ============================================================
# 2. MODELO MATEMÁTICO
# ============================================================

st.header("2. Modelo Matemático")

st.subheader("Cálculo do Déficit de Pressão de Vapor (VPD)")

col1, col2 = st.columns([1, 2])



st.subheader("Equações Matemáticas")

st.latex(
    r"VPD = e_s\left(1-\frac{UR}{100}\right)"
)

st.latex(
    r"e_s = 0.6108e^{\left(\frac{17.27T}{T+237.3}\right)}"
)



VPD_real = []

for i in range(len(T)):

    es = (
            0.6108 *
            np.exp(
                (17.27 * T[i]) /
                (T[i] + 237.3)
            )
    )

    ea = es * (U[i] / 100)

    vpd = es - ea

    VPD_real.append(vpd)

VPD_real = np.array(VPD_real)

base_vpd = pd.DataFrame({
    "Tempo": tempo,
    "Temperatura": T,
    "Umidade": U,
    "VPD": np.round(VPD_real, 3)
})

st.subheader("Resultados do Modelo")

st.dataframe(
    base_vpd,
    use_container_width=True
)

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    tempo_real,
    VPD_real,
    'o-',
    linewidth=3,
    label='VPD'
)

ax.set_xlabel("Tempo")

ax.set_ylabel("VPD")

ax.set_title(
    "Evolução Temporal do VPD"
)

ax.grid(True)

ax.legend()

st.pyplot(fig)

# ============================================================
# 3. SISTEMA DINÂMICO
# ============================================================

st.header("3. Sistema Dinâmico do VPD")

col1, col2 = st.columns([1,2])

with col1:

    st.subheader("Equação Diferencial")

    st.latex(
        r"\frac{dV}{dt}=kV"
    )

    st.markdown("A solução da EDO é:")

    st.latex(
        r"V(t)=V_0e^{kt}"
    )

with col2:

    st.markdown("""
    Hipótese do modelo:

    - a taxa de crescimento do VPD
    é proporcional ao próprio VPD.

    Isso caracteriza um:

    ## Sistema Dinâmico
    """)

    st.info(
        "O sistema tenta aprender dinamicamente "
        "o comportamento temporal do VPD."
    )

# ============================================================
# 4. GRID SEARCH
# ============================================================

st.header("4. Otimização dos Parâmetros com Grid Search")

col1, col2 = st.columns([1,2])



melhor_rmse = 999999

melhor_k = 0

melhor_prev = None

valores_k = np.arange(-0.05,0.20,0.0005)

for k in valores_k:

    V0 = VPD_real[0]

    VPD_prev = []

    for t in tempo:

        V = V0*np.exp(k*t)

        VPD_prev.append(V)

    VPD_prev = np.array(VPD_prev)

    rmse = np.sqrt(
        np.mean(
            (VPD_real - VPD_prev)**2
        )
    )

    if rmse < melhor_rmse:

        melhor_rmse = rmse

        melhor_k = k

        melhor_prev = VPD_prev

# ============================================================
# SIDEBAR INTELIGENTE
# ============================================================

st.sidebar.header("🤖 Painel Inteligente")

# último VPD previsto

vpd_atual = melhor_prev[-1]

# ------------------------------------------------------------
# DECISÃO AUTOMÁTICA
# ------------------------------------------------------------

if vpd_atual < 0.8:

    estado = "Muito Úmido"
    decisao = "Irrigação desnecessária"

elif vpd_atual < 1.2:

    estado = "Ideal"
    decisao = "Ambiente estável"

elif vpd_atual < 1.6:

    estado = "Atenção"
    decisao = "Monitorar ambiente"

elif vpd_atual < 2.0:

    estado = "Moderado"
    decisao = "Irrigação recomendada"

else:

    estado = "Crítico"
    decisao = "Irrigação urgente"

# ------------------------------------------------------------
# STATUS
# ------------------------------------------------------------

st.sidebar.subheader("🌱 Estado Atual")

if estado == "Muito Úmido":

    st.sidebar.success(estado)

elif estado == "Ideal":

    st.sidebar.success(estado)

elif estado == "Atenção":

    st.sidebar.warning(estado)

elif estado == "Moderado":

    st.sidebar.warning(estado)

else:

    st.sidebar.error(estado)

# ------------------------------------------------------------
# DECISÃO
# ------------------------------------------------------------

st.sidebar.subheader("🧠 Decisão Inteligente")

st.sidebar.info(decisao)

# ------------------------------------------------------------
# VELOCÍMETRO VPD
# ------------------------------------------------------------

import plotly.graph_objects as go

fig_gauge = go.Figure(go.Indicator(

    mode="gauge+number",

    value=float(vpd_atual),

    title={'text': "VPD Atual"},

    gauge={

        'axis': {'range': [0, 3]},

        'steps': [

            {'range': [0, 0.8], 'color': "blue"},

            {'range': [0.8, 1.2], 'color': "green"},

            {'range': [1.2, 1.6], 'color': "yellow"},

            {'range': [1.6, 2.0], 'color': "orange"},

            {'range': [2.0, 3], 'color': "red"}

        ]
    }
))

st.sidebar.plotly_chart(
    fig_gauge,
    use_container_width=True
)

st.markdown("Minimizar a Função Objetivo")

st.latex(
    r"\min \left( \frac{1}{n}\sum_{i=1}^{n}(y_i-\hat y_i)^2 \right)"
)

st.success("✅ Otimização concluída com sucesso!")

st.metric(
    "Melhor k encontrado",
    round(melhor_k,6)
)

st.metric(
    "Melhor RMSE",
    round(melhor_rmse,6)
)

# ============================================================
# 5. COMPARAÇÃO REAL X PREVISTO
# ============================================================

st.header("5. Comparação entre Dados Reais e Modelo Previsto")

fig, ax = plt.subplots(figsize=(10,5))

ax.plot(
    tempo_real,
    VPD_real,
    'o-',
    linewidth=3,
    label='VPD Real'
)

ax.plot(
    tempo_real,
    melhor_prev,
    's--',
    linewidth=3,
    label='VPD Previsto'
)

ax.set_xlabel("Tempo")

ax.set_ylabel("VPD")

ax.set_title(
    "Sistema Dinâmico Inteligente para Irrigação"
)

ax.legend()

ax.grid(True)

st.pyplot(fig)

# ============================================================
# 6. ERRO DO MODELO
# ============================================================

st.header("6. Análise do Erro do Modelo")

col1, col2 = st.columns([1,2])



st.markdown("""
### RMSE

O RMSE mede:

- distância entre:
- valor real;
- valor previsto.

Quanto menor o RMSE:

✅ melhor o modelo.
""")

st.latex(
    r"RMSE=\sqrt{\frac{1}{n}\sum(y_i-\hat y_i)^2}"
)



erro = VPD_real - melhor_prev

erro_df = pd.DataFrame({
    "Tempo": tempo,
    "Erro": np.round(erro,4)
})

st.dataframe(
    erro_df,
    use_container_width=True
)

# ============================================================
# 7. TOMADA DE DECISÃO
# ============================================================

st.header("7. Sistema Inteligente de Tomada de Decisão")


st.markdown("""
### Estados Ambientais

| VPD | Situação |
|---|---|
| < 0.8 | Muito úmido |
| 0.8–1.2 | Ideal |
| 1.2–1.6 | Atenção |
| 1.6–2.0 | Moderado |
| > 2.0 | Crítico |
""")

analise = []

for i in range(len(melhor_prev)):

    valor = melhor_prev[i]

    if valor < 0.6:

        estado = "Muito Úmido"
        decisao = "Irrigação desnecessária"

    elif valor < 0.7:

        estado = "Ideal"
        decisao = "Ambiente estável"

    elif valor < 0.8:

        estado = "Atenção"
        decisao = "Monitorar ambiente"

    elif valor < 0.9:

        estado = "Moderado"
        decisao = "Irrigação recomendada"

    else:

        estado = "Crítico"
        decisao = "Irrigação urgente"

    analise.append([
        tempo[i],
        round(valor,2),
        estado,
        decisao
    ])

analise_df = pd.DataFrame(
    analise,
    columns=[
        "Tempo",
        "VPD Previsto",
        "Estado",
        "Decisão"
    ]
)

st.subheader("Resultado da Análise Inteligente")

st.dataframe(
    analise_df,
    use_container_width=True
)

# ============================================================
# 8. VISUALIZAÇÃO DAS ZONAS
# ============================================================

st.header("8. Visualização das Zonas de Irrigação")

col1, col2 = st.columns([1,2])



st.markdown("""
### Interpretação das Zonas

| Faixa de VPD | Estado Ambiental |
|---|---|
| < 0.8 | Muito Úmido |
| 0.8 – 1.2 | Ideal |
| 1.2 – 1.6 | Atenção |
| 1.6 – 2.0 | Moderado |
| > 2.0 | Crítico |
""")

fig2, ax2 = plt.subplots(figsize=(11,5))

ax2.plot(
    tempo_real,
    melhor_prev,
    'o-',
    linewidth=3,
    label='VPD Previsto'
)

ax2.axhspan(
    0,
    0.8,
    color='blue',
    alpha=0.12,
    label='Muito Úmido'
)

ax2.axhspan(
    0.8,
    1.2,
    color='green',
    alpha=0.12,
    label='Ideal'
)

ax2.axhspan(
    1.2,
    1.6,
    color='yellow',
    alpha=0.15,
    label='Atenção'
)

ax2.axhspan(
    1.6,
    2.0,
    color='orange',
    alpha=0.15,
    label='Moderado'
)

ax2.axhspan(
    2.0,
    5,
    color='red',
    alpha=0.15,
    label='Crítico'
)

ax2.set_xlabel("Tempo")

ax2.set_ylabel("VPD")

ax2.set_title(
    "Zonas Inteligentes de Irrigação"
)

ax2.grid(True)

handles, labels = ax2.get_legend_handles_labels()

by_label = dict(zip(labels, handles))

ax2.legend(
    by_label.values(),
    by_label.keys(),
    loc='upper left'
)

st.pyplot(fig2)

