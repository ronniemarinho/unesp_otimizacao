from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import pandas as pd

# Dados
tempo = [0, 10, 20, 30, 40]
temperatura = [20.0, 20.2, 20.7, 21.4, 22.3]

# Criar figura maior
fig = plt.figure(figsize=(10, 5))
ax = fig.add_axes([0.08, 0.15, 0.55, 0.75])  # gráfico

# Configurações do gráfico
ax.set_xlim(0, 40)
ax.set_ylim(19.5, 23)
ax.set_xlabel("Tempo (min)")
ax.set_ylabel("Temperatura (°C)")
ax.set_title("Sistema Dinâmico")

line, = ax.plot([], [], linewidth=3)
point, = ax.plot([], [], marker='o', markersize=10)

# Criar tabela separada
ax_table = fig.add_axes([0.72, 0.2, 0.25, 0.6])
ax_table.axis('off')

df = pd.DataFrame({
    "Tempo": tempo,
    "Temperatura": temperatura
})

table = ax_table.table(
    cellText=df.values,
    colLabels=df.columns,
    loc='center',
    cellLoc='center'
)

table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 2)

# Inicialização
def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

# Atualização
def update(frame):
    x = tempo[:frame + 1]
    y = temperatura[:frame + 1]

    line.set_data(x, y)
    point.set_data([x[-1]], [y[-1]])

    return line, point

# Criar animação contínua
ani = FuncAnimation(
    fig,
    update,
    frames=len(tempo),
    init_func=init,
    interval=500,
    repeat=True,
    blit=True
)

# Salvar GIF corretamente
gif_path = "grafico_dinamico_loop.gif"

writer = PillowWriter(fps=2)
ani.save(gif_path, writer=writer)

plt.close(fig)

print("Arquivo criado:", gif_path)
