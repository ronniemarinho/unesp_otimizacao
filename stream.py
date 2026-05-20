# Sistema Dinâmico Inteligente para Irrigação com VPD e Grid Search


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# CONFIGURAÇÕES INICIAIS
# ============================================================

st.set_page_config(layout="wide")

sns.set_theme()

# ============================================================
# TÍTULO
# ============================================================

st.title("Sistema Dinâmico Inteligente para Irrigação 🌱")

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(
        "https://images.unsplash.com/photo-1500382017468-9049fed747ef",
        width=650
    )

# ============================================================
# INTRODUÇÃO
# ============================================================

st.markdown("""
## Modelagem Dinâmica Aplicada à Agricultura Inteligente

Esta aplicação utiliza conceitos de:

- Sistemas Dinâmicos
- Equações Diferenciais
- Modelagem Matemática
- Agricultura de Precisão
- Internet das Coisas (IoT)
- Ciência de Dados
- Otimização com Grid Search

para modelar dinamicamente o comportamento do:

# Déficit de Pressão de Vapor (VPD)

O VPD é uma variável extremamente importante na agricultura, pois indica:

- estresse hídrico;
- necessidade de irrigação;
- perda de água pela planta;
- risco ambiental;
- condições atmosféricas.

O sistema utiliza:

- temperatura;
- umidade relativa;
- modelagem dinâmica;
- otimização de parâmetros.

para prever condições ambientais em tempo real.

---

### 📚 Áreas Envolvidas

- 🌱 Engenharia de Biossistemas
- 🌎 Ciências Ambientais
- 📈 Modelagem Matemática
- 💻 Computação Científica
- 🤖 Agricultura 4.0
- 📡 Sensoriamento IoT

---
""")

st.markdown(
    "<h3 style='text-align: center;'>Desenvolvido por Prof. Dr. Ronnie Shida Marinho</h3>",
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Configurações")

cenario = st.sidebar.selectbox(
    "Escolha o cenário ambiental",
    [
        "Cenário 1 - Ambiente Úmido",
        "Cenário 2 - Ambiente Moderado",
        "Cenário 3 - Ambiente Crítico"
    ]
)

# ============================================================
# BASES DE DADOS
# ============================================================

if cenario == "Cenário 1 - Ambiente Úmido":

    tempo = np.array([0,1,2,3,4,5])

    T = np.array([24,25,25,26,26,27])

    U = np.array([85,84,82,81,80,79])

elif cenario == "Cenário 2 - Ambiente Moderado":

    tempo = np.array([0,1,2,3,4,5])

    T = np.array([28,29,30,31,32,33])

    U = np.array([72,70,68,65,63,60])

else:

    tempo = np.array([0,1,2,3,4,5])

    T = np.array([32,33,35,36,38,39])

    U = np.array([60,57,54,50,46,42])

# ============================================================
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

st.header("1. Carregamento dos Dados Ambientais")

col1, col2 = st.columns([1,2])

with col1:

    st.subheader("Código Python")

    st.code('''
import pandas as pd
import numpy as np

base = pd.DataFrame({
    "Tempo": tempo,
    "Temperatura": T,
    "Umidade": U
})
''', language='python')

with col2:

    st.subheader("Prévia da Base de Dados")

    st.dataframe(base, use_container_width=True)

# ============================================================
# 2. CÁLCULO DO VPD
# ============================================================

st.header("2. Cálculo do Déficit de Pressão de Vapor (VPD)")

col1, col2 = st.columns([1,2])

with col1:

    st.subheader("Modelo Matemático")

    st.latex(r"VPD = e_s\left(1-\frac{UR}{100}\right)")

    st.latex(r"e_s = 0.6108e^{\left(\frac{17.27T}{T+237.3}\right)}")

    st.markdown("""
O VPD representa:

- demanda atmosférica por água;
- perda hídrica das plantas;
- estresse ambiental;
- necessidade de irrigação.
""")

with col2:

    VPD_real = []

    for i in range(len(T)):

        es = (
            0.6108 *
            np.exp(
                (17.27*T[i]) /
                (T[i] + 237.3)
            )
        )

        ea = es * (U[i]/100)

        vpd = es - ea

        VPD_real.append(vpd)

    VPD_real = np.array(VPD_real)

    base_vpd = pd.DataFrame({
        "Tempo": tempo,
        "Temperatura": T,
        "Umidade": U,
        "VPD": np.round(VPD_real,3)
    })

    st.dataframe(base_vpd, use_container_width=True)

# ============================================================
# 3. SISTEMA DINÂMICO
# ============================================================

st.header("3. Sistema Dinâmico do VPD")

col1, col2 = st.columns([1,2])

with col1:

    st.subheader("Equação Diferencial")

    st.latex(r"\frac{dV}{dt}=kV")

    st.markdown("""
Hipótese do modelo:

- a taxa de crescimento do VPD
é proporcional ao próprio VPD.

Isso caracteriza um:

# Sistema Dinâmico

A solução da EDO é:
""")

    st.latex(r"V(t)=V_0e^{kt}")

with col2:

    st.info(
        "O sistema tenta aprender dinamicamente "
        "o comportamento temporal do VPD."
    )

# ============================================================
# 4. GRID SEARCH
# ============================================================

st.header("4. Otimização dos Parâmetros com Grid Search")

col1, col2 = st.columns([1,2])

with col1:

    st.code('''
melhor_rmse = 999999

for k in valores_k:

    VPD_prev = []

    for t in tempo:

        V = V0*np.exp(k*t)

        VPD_prev.append(V)

    rmse = np.sqrt(
        np.mean(
            (VPD_real - VPD_prev)**2
        )
    )
''', language='python')

with col2:

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

col1, col2 = st.columns([1,2])

with col1:

    st.code('''
plt.plot(
    tempo,
    VPD_real,
    'o-',
    label='VPD Real'
)

plt.plot(
    tempo,
    melhor_prev,
    's--',
    label='VPD Previsto'
)
''', language='python')

with col2:

    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(
        tempo,
        VPD_real,
        'o-',
        linewidth=3,
        label='VPD Real'
    )

    ax.plot(
        tempo,
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

with col1:

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

with col2:

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

analise = []

for i in range(len(melhor_prev)):

    valor = melhor_prev[i]

    if valor < 0.8:

        estado = "Muito Úmido"

        decisao = "Irrigação desnecessária"

    elif valor < 1.2:

        estado = "Ideal"

        decisao = "Ambiente estável"

    elif valor < 1.6:

        estado = "Atenção"

        decisao = "Monitorar ambiente"

    elif valor < 2.0:

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

col1, col2 = st.columns([1,2])

with col1:

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

with col2:

    st.dataframe(
        analise_df,
        use_container_width=True
    )

# ============================================================
# 8. VISUALIZAÇÃO DAS ZONAS
# ============================================================

st.header("8. Visualização das Zonas de Irrigação")

fig2, ax2 = plt.subplots(figsize=(11,5))

ax2.plot(
    tempo,
    melhor_prev,
    'o-',
    linewidth=3,
    label='VPD Previsto'
)

ax2.axhspan(0,0.8,alpha=0.08)
ax2.axhspan(0.8,1.2,alpha=0.08)
ax2.axhspan(1.2,1.6,alpha=0.08)
ax2.axhspan(1.6,2.0,alpha=0.08)
ax2.axhspan(2.0,5,alpha=0.08)

ax2.set_xlabel

