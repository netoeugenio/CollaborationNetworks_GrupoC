import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

public class LeitorDeGrafo {

    public static void main(String[] args) {

        if (args.length == 0) {
            StdOut.println("Por favor, informe o nome do arquivo.");
            StdOut.println("Uso no terminal: java LeitorDeGrafo CA-GrQc.txt");
            return;
        }

        String nomeArquivo = args[0];
        StdOut.println("Lendo o arquivo: " + nomeArquivo + "...\n");

        try {

            In in = new In(nomeArquivo);
            String[] linhas = in.readAllLines();

            ArrayList<int[]> arestas = new ArrayList<>();
            int maxId = 0;

            // ==========================
            // 1. Leitura das arestas
            // ==========================
            for (String linha : linhas) {

                linha = linha.trim();

                if (linha.isEmpty() || linha.startsWith("#"))
                    continue;

                String[] partes = linha.split("\\s+");

                if (partes.length >= 2) {

                    int v = Integer.parseInt(partes[0]);
                    int w = Integer.parseInt(partes[1]);

                    arestas.add(new int[]{v, w});

                    if (v > maxId) maxId = v;
                    if (w > maxId) maxId = w;
                }
            }

            // ==========================
            // 2. Criação do grafo
            // ==========================
        int V = maxId + 1;
Graph grafo = new Graph(V);

for (int[] aresta : arestas) {
    int v = aresta[0];
    int w = aresta[1];

    // adiciona apenas uma vez cada aresta não-direcionada
    if (v < w) {
        grafo.addEdge(v, w);
    }
}

            StdOut.println("✅ Leitura e construção do Grafo concluídas!\n");

            StdOut.println("ESTATISTICAS DO GRAFO:");
            StdOut.println("Tamanho do Array de Vertices: " + grafo.V());
            StdOut.println("Número de Arestas: " + grafo.E());

            // ==========================
            // 3. Cálculo dos graus
            // ==========================
            ArrayList<Integer> listaGraus = new ArrayList<>();

            int verticesReais = 0;
            int grauMaximo = 0;
            int verticeMaximo = 0;

            for (int v = 0; v < grafo.V(); v++) {

                int grauAtual = grafo.degree(v);

                if (grauAtual > 0) {
                    verticesReais++;
                    listaGraus.add(grauAtual);
                }

                if (grauAtual > grauMaximo) {
                    grauMaximo = grauAtual;
                    verticeMaximo = v;
                }
            }

            // ==========================
// 3.1 Grau médio e Densidade
// ==========================

double grauMedio = (2.0 * grafo.E()) / verticesReais;

double densidade = (2.0 * grafo.E()) / 
                   (verticesReais * (verticesReais - 1));

StdOut.println("\nMÉTRICAS INICIAIS:");
StdOut.printf("Grau médio: %.4f\n", grauMedio);
StdOut.printf("Densidade: %.6f\n", densidade);

            StdOut.println("Vertices REAIS: " + verticesReais);
            StdOut.println("\nAutor mais colaborativo: " + verticeMaximo);
            StdOut.println("Numero de coautorias: " + grauMaximo);

            // ==========================
            // 4. Distribuição de graus
            // ==========================
            int[] frequencia = new int[grauMaximo + 1];

            for (int grau : listaGraus) {
                frequencia[grau]++;
            }

            // ==========================
            // 5. Gerar arquivo TXT
            // ==========================
            PrintWriter writerTxt = new PrintWriter(new FileWriter("lista_graus.txt"));

            for (int grau : listaGraus) {
                writerTxt.println(grau);
            }

            writerTxt.close();

            // ==========================
            // 6. Gerar arquivo CSV
            // ==========================
            PrintWriter writerCsv = new PrintWriter(new FileWriter("distribuicao_graus.csv"));

            writerCsv.println("grau,quantidade");

            for (int i = 1; i < frequencia.length; i++) {
                if (frequencia[i] > 0) {
                    writerCsv.println(i + "," + frequencia[i]);
                }
            }

            writerCsv.close();

            StdOut.println("\n Arquivos gerados com sucesso:");
            StdOut.println(" - lista_graus.txt");
            StdOut.println(" - distribuicao_graus.csv");

        } catch (IOException e) {
            StdOut.println("Erro ao gerar arquivos.");
            e.printStackTrace();
        } catch (Exception e) {
            StdOut.println("Erro ao processar o arquivo.");
            e.printStackTrace();
        }
    }
}