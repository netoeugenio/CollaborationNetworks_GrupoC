import pandas as pd
import matplotlib.pyplot as plt

# Ler o CSV
df = pd.read_csv("distribuicao_graus.csv")

# Gráfico
plt.figure()
plt.bar(df["grau"], df["quantidade"])
plt.xlabel("Grau")
plt.ylabel("Quantidade de Vértices")
plt.title("Distribuição de Graus")
plt.show()