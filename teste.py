import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# ESCOLHA DO CENÁRIO
# ============================================================

cenario = 3

# ============================================================
# BASES DE DADOS
# ============================================================

tempo = np.array([0,1,2,3,4,5])

# ------------------------------------------------------------
# CENÁRIO 1 - ÚMIDO
# ------------------------------------------------------------

if cenario == 1:

    T = np.array([24,25,25,26,26,27])

    U = np.array([85,84,82,81,80,79])

# ------------------------------------------------------------
# CENÁRIO 2 - MODERADO
# ------------------------------------------------------------

elif cenario == 2:

    T = np.array([28,29,30,31,32,33])

    U = np.array([72,70,68,65,63,60])

# ------------------------------------------------------------
# CENÁRIO 3 - CRÍTICO
# ------------------------------------------------------------

elif cenario == 3:

    T = np.array([32,33,35,36,38,39])

    U = np.array([60,57,54,50,46,42])

# ============================================================
# ETAPA 1 - CÁLCULO DO VPD REAL
# ============================================================

VPD_real = []

for i in range(len(T)):

    # pressão de vapor saturado

    es = (
        0.6108 *
        np.exp(
            (17.27*T[i]) /
            (T[i] + 237.3)
        )
    )

    # pressão real

    ea = es * (U[i]/100)

    # VPD

    vpd = es - ea

    VPD_real.append(vpd)

VPD_real = np.array(VPD_real)

# ============================================================
# ETAPA 2 - GRID SEARCH
# ============================================================
#
# Encontrar o melhor k
# minimizando RMSE
#

melhor_rmse = 999999

melhor_k = 0

melhor_prev = None

# intervalo de busca do k

valores_k = np.arange(
    -0.05,
    0.20,
    0.0005
)

# ------------------------------------------------------------
# TESTE DE TODOS OS k
# ------------------------------------------------------------

for k in valores_k:

    # VPD inicial

    V0 = VPD_real[0]

    # modelo previsto

    VPD_prev = []

    # solução da EDO:
    #
    # V(t)=V0*exp(k*t)
    #

    for t in tempo:

        V = V0 * np.exp(k*t)

        VPD_prev.append(V)

    VPD_prev = np.array(VPD_prev)

    # --------------------------------------------------------
    # RMSE
    # --------------------------------------------------------

    rmse = np.sqrt(
        np.mean(
            (VPD_real - VPD_prev)**2
        )
    )

    # --------------------------------------------------------
    # Melhor solução
    # --------------------------------------------------------

    if rmse < melhor_rmse:

        melhor_rmse = rmse

        melhor_k = k

        melhor_prev = VPD_prev

# ============================================================
# RESULTADOS
# ============================================================

print("\nMELHOR k ENCONTRADO:")
print(round(melhor_k,6))

print("\nMELHOR RMSE:")
print(round(melhor_rmse,6))

# ============================================================
# ETAPA 3 - TOMADA DE DECISÃO
# ============================================================

print("\nANÁLISE AMBIENTAL:\n")

for i in range(len(melhor_prev)):

    valor = melhor_prev[i]

    # --------------------------------------------------------
    # CLASSIFICAÇÃO DO VPD
    # --------------------------------------------------------

    if valor < 0.8:

        estado = "Muito Úmido"

        decisao = (
            "Irrigação desnecessária"
        )

    elif valor < 1.2:

        estado = "Ideal"

        decisao = (
            "Ambiente estável"
        )

    elif valor < 1.6:

        estado = "Atenção"

        decisao = (
            "Monitorar ambiente"
        )

    elif valor < 2.0:

        estado = "Moderado"

        decisao = (
            "Irrigação recomendada"
        )

    else:

        estado = "Crítico"

        decisao = (
            "Irrigação urgente"
        )

    print(
        f"Tempo {tempo[i]}h | "
        f"VPD={valor:.2f} | "
        f"{estado} | "
        f"{decisao}"
    )

# ============================================================
# ETAPA 4 - VISUALIZAÇÃO
# ============================================================

plt.figure(figsize=(11,5))

# ------------------------------------------------------------
# VPD REAL
# ------------------------------------------------------------

plt.plot(
    tempo,
    VPD_real,
    'o-',
    linewidth=3,
    label='VPD Real'
)

# ------------------------------------------------------------
# VPD PREVISTO
# ------------------------------------------------------------

plt.plot(
    tempo,
    melhor_prev,
    's--',
    linewidth=3,
    label='VPD Previsto'
)

# ------------------------------------------------------------
# ZONAS DE DECISÃO
# ------------------------------------------------------------

plt.axhspan(
    0,
    0.8,
    alpha=0.08
)

plt.axhspan(
    0.8,
    1.2,
    alpha=0.08
)

plt.axhspan(
    1.2,
    1.6,
    alpha=0.08
)

plt.axhspan(
    1.6,
    2.0,
    alpha=0.08
)

plt.axhspan(
    2.0,
    5,
    alpha=0.08
)

plt.xlabel("Tempo")

plt.ylabel("VPD")

plt.title(
    "Sistema Dinâmico Inteligente para Irrigação"
)

plt.legend()

plt.grid(True)

plt.show()