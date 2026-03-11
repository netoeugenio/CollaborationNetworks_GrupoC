# Análise de Collaboration Networks com Grafos

**Integrantes do grupo**

* José Eugênio — 2320466
* Mateus Rocha Lessa — 2410456
* Carlos Huan Celestino de Brito — 2320478
* Lucas de Vasconcelos Barreira Carvalho — 2410424

---

Este projeto foi desenvolvido para a disciplina de **Grafos**.
Nosso grupo ficou responsável pelo **Grupo C**, que trabalha com **Collaboration Networks** da base de dados da **SNAP (Stanford Network Analysis Project)**.

A proposta do trabalho é **construir um grafo a partir de dados reais de colaboração científica** e analisar como os autores se conectam entre si.

---

## O que representa o grafo

Nesse tipo de rede:

* **Vértices** representam **autores**
* **Arestas** representam **colaborações entre autores**

Ou seja, quando dois autores publicam um artigo juntos, criamos uma **aresta conectando esses dois vértices** no grafo.

---

## Estrutura do projeto

Para construir o grafo utilizamos uma implementação baseada no **ALGS4** em java.

As principais partes do projeto são:

**Bag**

Estrutura usada para armazenar os **vizinhos de cada vértice**.

**Graph**

Representa o grafo utilizando **lista de adjacência**, guardando:

* número de vértices
* número de arestas
* conexões entre os vértices

**LeitorDeGrafo**

Classe responsável por:

* ler o dataset
* construir o grafo
* calcular o grau dos vértices
* gerar um **arquivo CSV com a distribuição de graus**

---

## Dataset utilizado

O dataset utilizado foi:

```
CA-GrQc.txt
```

Ele representa uma **rede de colaboração científica**.

Cada linha do arquivo representa uma colaboração entre dois autores.

Exemplo:

```
3466 937
3466 5233
5233 8573
```

Cada par de números indica **uma aresta no grafo**.

---

# Como rodar o projeto

## 1️⃣ Entrar na pasta do código

Primeiro entre na pasta onde estão os arquivos Java:

```bash
cd src
```

---

## 2️⃣ Compilar os arquivos Java

Compile todos os arquivos `.java`:

```bash
javac *.java
```

---

## 3️⃣ Ler o dataset da SNAP

Agora execute o leitor do grafo passando o dataset como argumento:

```bash
java LeitorDeGrafo CA-GrQc.txt
```

Esse programa irá:

* ler os dados da SNAP
* construir o grafo
* calcular o grau dos vértices
* gerar um **arquivo CSV com a distribuição de graus**

Esse arquivo será usado na etapa de geração dos gráficos.

---

# Gerando os gráficos (Python)

⚠️ Os gráficos **só podem ser gerados depois que o programa em Java for executado**, pois eles dependem do **CSV gerado com a distribuição de graus**.

---

## Histograma da distribuição de graus

Execute:

```bash
python grafico.py
```

Esse script gera um **histograma da distribuição de graus da rede**.

---

## Análise da Lei de Potência

Execute:

```bash
python potencia.py
```

Esse script gera:

* gráfico **linear**
* gráfico **log-log**
* **ajuste da lei de potência**
* Com isso conseguimos verificar se segue uma lei de potência*

---

## Tecnologias utilizadas

* **Java** → construção do grafo
* **Python** → geração dos gráficos
* **Dataset SNAP** → dados de colaboração científica
