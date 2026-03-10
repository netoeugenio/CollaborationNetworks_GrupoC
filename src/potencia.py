import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import zeta
from scipy.optimize import minimize_scalar

# =========================
# 1. Carregar dados
# =========================
df = pd.read_csv("distribuicao_graus.csv")
graus = df['grau'].values
quantidades = df['quantidade'].values
total_nos = quantidades.sum()

# =========================
# 2. Função para encontrar o melhor xmin e α
# =========================
def buscar_xmin_alpha(graus, quantidades, min_n_cauda=15):
    # Variáveis para guardar o melhor resultado
    melhor_xmin = None
    melhor_alpha = None
    menor_erro_ks = float('inf')
    nos_cauda_final = 0

    # Testar todos os valores únicos de grau como candidatos a xmin
    candidatos = np.unique(graus)

    for xmin in candidatos:
        # Seleciona apenas os nós com grau >= xmin
        indices_cauda = graus >= xmin
        graus_cauda = graus[indices_cauda]
        contagem_cauda = quantidades[indices_cauda]
        N = contagem_cauda.sum()
        
        # Pular caudas muito pequenas
        if N < min_n_cauda:
            continue
        
        # Função de verossimilhança para α
        def verossimilhanca(alpha):
            return N * np.log(zeta(alpha, xmin)) + alpha * np.sum(contagem_cauda * np.log(graus_cauda))
        
        # Encontrar α que minimiza a função de verossimilhança
        resultado = minimize_scalar(verossimilhanca, bounds=(1.1, 10), method='bounded')
        alpha = resultado.x
        
        # Comparar modelo com dados usando distância KS
        ordem = np.argsort(graus_cauda)
        graus_ord = graus_cauda[ordem]
        cont_ord = contagem_cauda[ordem]
        observado = np.cumsum(cont_ord[::-1])[::-1] / N
        esperado = zeta(alpha, graus_ord) / zeta(alpha, xmin)
        distancia_ks = np.max(np.abs(observado - esperado))
        
        # Atualizar melhor ajuste
        if distancia_ks < menor_erro_ks:
            menor_erro_ks = distancia_ks
            melhor_xmin = xmin
            melhor_alpha = alpha
            nos_cauda_final = N

    return melhor_xmin, melhor_alpha, menor_erro_ks, nos_cauda_final

# =========================
# 3. Executar ajuste
# =========================
xmin, alpha, erro_ks, n_cauda = buscar_xmin_alpha(graus, quantidades)

# =========================
# 4. Plotagem dos resultados
# =========================
plt.figure(figsize=(18, 5))

# --- Gráfico Linear ---
plt.subplot(1,3,1)
plt.plot(graus, quantidades / total_nos, 'o', color='green', alpha=0.6)
plt.axvline(xmin, color='purple', linestyle='--', label=f'x_min = {xmin}')
plt.title("Distribuição Linear")
plt.xlabel("Grau k")
plt.ylabel("Fração de nós")
plt.grid(True)
plt.legend()

# --- Gráfico Log-Log ---
plt.subplot(1,3,2)
plt.loglog(graus, quantidades / total_nos, 'o', color='green', alpha=0.6)
plt.axvline(xmin, color='purple', linestyle='--')
plt.title("Distribuição Log-Log")
plt.xlabel("Grau k")
plt.ylabel("Fração de nós")
plt.grid(True, which="both", alpha=0.3)

# --- Ajuste da Lei de Potência ---
plt.subplot(1,3,3)
k_reta = np.geomspace(xmin, graus.max(), 100)
ajuste = (n_cauda / total_nos) / zeta(alpha, xmin)
plt.loglog(k_reta, ajuste * (k_reta ** -alpha), color='blue', linewidth=2, label=f'Ajuste MLE α={alpha:.2f}')
plt.loglog(graus, quantidades / total_nos, 'o', color='gray', alpha=0.4)
plt.axvline(xmin, color='purple', linestyle='--')
plt.title("Ajuste da Lei de Potência")
plt.xlabel("Grau k")
plt.ylabel("Fração de nós")
plt.grid(True, which="both", alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()

# =========================
# 5. Resultados
# =========================
print(f"Ponto de corte xmin: {xmin}")
print(f"Expoente Alpha (α): {alpha:.4f}")
print(f"Erro KS: {erro_ks:.4f}")
print(f"Nós na cauda: {n_cauda}")