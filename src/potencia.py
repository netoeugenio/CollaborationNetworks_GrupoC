import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import zeta
from scipy.optimize import minimize_scalar

# =========================
# 1. Carregamento dos dados
# =========================
df = pd.read_csv("distribuicao_graus.csv")
graus = df['grau'].values
quantidades = df['quantidade'].values
total_nos = quantidades.sum()

# =========================
# 2. Função de ajuste da Lei de Potência com busca automática de xmin
# =========================
def executar_analise_mle_ks_automatico(graus, quantidades, min_n_cauda=15):
    """
    Ajusta a distribuição de graus a uma Lei de Potência.
    Busca automaticamente o melhor xmin que minimiza a diferença KS.
    """
    melhor_erro_ks = float('inf')
    melhor_alpha_mle = 0
    melhor_xmin_corte = 0
    n_cauda_final = 0

    # Testa todos os valores únicos de grau como candidatos a xmin
    candidatos_xmin = np.unique(graus)

    for xmin_teste in candidatos_xmin:
        # Seleciona apenas os nós com grau >= xmin_teste
        selecao = graus >= xmin_teste
        k_cauda, n_cauda = graus[selecao], quantidades[selecao]
        N = n_cauda.sum()
        if N < min_n_cauda:
            continue  # ignora caudas muito pequenas

        # =========================
        # Estima alpha via MLE
        # =========================
        def calculo_mle(a):
            return N * np.log(zeta(a, xmin_teste)) + a * np.sum(n_cauda * np.log(k_cauda))

        solucao = minimize_scalar(calculo_mle, bounds=(1.1, 10), method='bounded')
        alpha_mle = solucao.x

        # =========================
        # Calcula distância KS
        # =========================
        ordenar = np.argsort(k_cauda)
        k_f, n_f = k_cauda[ordenar], n_cauda[ordenar]
        observado_acumulado = np.cumsum(n_f[::-1])[::-1] / N
        teorico_modelo = zeta(alpha_mle, k_f) / zeta(alpha_mle, xmin_teste)
        distancia_ks = np.max(np.abs(observado_acumulado - teorico_modelo))

        # =========================
        # Atualiza melhor ajuste
        # =========================
        if distancia_ks < melhor_erro_ks:
            melhor_erro_ks = distancia_ks
            melhor_alpha_mle = alpha_mle
            melhor_xmin_corte = xmin_teste
            n_cauda_final = N

    return melhor_xmin_corte, melhor_alpha_mle, melhor_erro_ks, n_cauda_final

# =========================
# 3. Executa o ajuste automático
# =========================
xmin, alpha, erro_ks, n_cauda = executar_analise_mle_ks_automatico(graus, quantidades)

# =========================
# 4. Plotagem intuitiva
# =========================
plt.figure(figsize=(18,5))

# --- Linear ---
plt.subplot(1,3,1)
plt.plot(graus, quantidades/total_nos, 'o', color='green', alpha=0.6, label='Dados Observados')
plt.axvline(xmin, color='purple', linestyle='--', label=f'Ponto de corte xmin = {xmin}')
plt.title("Distribuição de frequência dos graus (Linear)")
plt.xlabel("Grau k")
plt.ylabel("Fração de nós com grau k")
plt.grid(True)
plt.legend()

# --- Log-Log ---
plt.subplot(1,3,2)
plt.loglog(graus, quantidades/total_nos, 'o', color='green', alpha=0.6, label='Dados Observados')
plt.axvline(xmin, color='purple', linestyle='--', label=f'Ponto de corte xmin = {xmin}')
plt.title("Distribuição de frequência dos graus (Log-Log)")
plt.xlabel("Grau k")
plt.ylabel("Fração de nós com grau k")
plt.grid(True, which="both", alpha=0.3)
plt.legend()

# --- Ajuste da Lei de Potência ---
plt.subplot(1,3,3)
k_reta = np.geomspace(xmin, graus.max(), 100)
ajuste_vertical = (n_cauda / total_nos) / zeta(alpha, xmin)
plt.loglog(k_reta, ajuste_vertical*(k_reta**-alpha), color='blue', linewidth=2, label=f'Modelo Lei de Potência (α={alpha:.2f})')
plt.loglog(graus, quantidades/total_nos, 'o', color='gray', alpha=0.4, label='Dados Observados')
plt.axvline(xmin, color='purple', linestyle='--', label=f'Ponto de corte xmin = {xmin}')
plt.title("Ajuste da Lei de Potência à fração de nós")
plt.xlabel("Grau k")
plt.ylabel("Fração de nós com grau k")
plt.grid(True, which="both", alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()

# =========================
# 5. Resultados
# =========================
print("===== Resultados do Ajuste Automático =====")
print(f"Ponto de corte xmin: {xmin}")
print(f"Expoente Alpha (α): {alpha:.4f}")
print(f"Erro KS: {erro_ks:.4f} (quanto menor, melhor)")
print(f"Nós na cauda (k >= xmin): {n_cauda}")