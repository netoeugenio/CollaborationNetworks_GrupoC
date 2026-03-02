import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import powerlaw

df = pd.read_csv("distribuicao_graus.csv")


graus = df["grau"].values
quantidades = df["quantidade"].values


#Expandir dados:Agrupa graus com quantidados em um vetor

dados = np.repeat(graus, quantidades)


#  Ajustar distribuições
# O xmin é escolhido como o valor que minimiza a distância KS
# (diferença entre a distribuição empírica e o modelo)
# Para esse xmin, o alpha é estimado por máxima verossimilhança (MLE)
# ou seja o valor que torna os dados mais prováveis segundo o modelo.

fit = powerlaw.Fit(dados, discrete=True,)

alpha = fit.power_law.alpha
xmin = fit.power_law.xmin

# Aqui caluculamos o modelos de verssimilhaça do modelo 1 e do modelo 2
# Compara power-law e lognormal usando razão de verossimilhança para r e teste de Vuong para p
# R > 0 favorece power-law; R < 0 favorece lognormal
R, p = fit.distribution_compare('power_law', 'lognormal')


#  Plot PDF em escala log-log

plt.figure(figsize=(9,7))

# Pontos empíricos
fit.plot_pdf(marker='o', linestyle='none', markersize=6, color="#1f77b4", label='Empírico')

# Curvas ajustadas
fit.power_law.plot_pdf(color="#ff7f0e", linewidth=2, label='Power-law')
fit.lognormal.plot_pdf(color="#2ca02c", linewidth=2, label='Lognormal')

# Escala log-log
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Grau (k)", fontsize=12)
plt.ylabel("P(k)", fontsize=12)
plt.title("Distribuição de Graus (Power-law vs Lognormal)", fontsize=14)

# Adicionar resultados no gráfico
plt.text(0.05, 0.05,
        f"α = {alpha:.2f}\nXmin = {xmin:.0f}\nR = {R:.2f}\nP = {p:.3f}",
        transform=plt.gca().transAxes,
        fontsize=11,
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray', boxstyle='round,pad=0.5'))

plt.legend(frameon=False, fontsize=11)
plt.grid(True, which="both", ls="--", alpha=0.3)

plt.tight_layout()
plt.show()