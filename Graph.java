import java.util.NoSuchElementException;
import java.util.Stack;

public class Graph {
    private static final String NEWLINE = System.getProperty("line.separator");
    private final int V;
    private int E;

    // lista de adjacência para cada vértice armazenamos seus vizinhos
    private Bag<Integer>[] adj;

    // construtor que cria um grafo vazio com V vértices
    public Graph(int V) {

        // verifica se o número de vértices é válido
        if (V < 0) throw new IllegalArgumentException("Número de vértices deve ser não negativo");

        this.V = V;
        this.E = 0;

        // cria o array de listas de adjacência
        adj = (Bag<Integer>[]) new Bag[V];

        // inicializa uma Bag para cada vértice
        for (int v = 0; v < V; v++) {
            adj[v] = new Bag<Integer>();
        }
    }

    // construtor que cria o grafo a partir de um arquivo de entrada
    public Graph(In in) {

        if (in == null) throw new IllegalArgumentException("argumento nulo");

        try {

            
            this.V = in.readInt();

            if (V < 0) throw new IllegalArgumentException("número de vértices deve ser não negativo");

            adj = (Bag<Integer>[]) new Bag[V];

            // cria lista de adjacência para cada vértice
            for (int v = 0; v < V; v++) {
                adj[v] = new Bag<Integer>();
            }
            int E = in.readInt();
            if (E < 0) throw new IllegalArgumentException("número de arestas deve ser não negativo");

        
            for (int i = 0; i < E; i++) {

                int v = in.readInt();
                int w = in.readInt();

                validateVertex(v);
                validateVertex(w);

                // adiciona a aresta ao grafo
                addEdge(v, w);
            }

        } catch (NoSuchElementException e) {

            throw new IllegalArgumentException("formato de entrada inválido", e);
        }
    }

    // construtor que cria uma cópia de outro grafo
    public Graph(Graph graph) {

        this.V = graph.V();
        this.E = graph.E();

        if (V < 0) throw new IllegalArgumentException("Número de vértices deve ser não negativo");

        // cria novas listas de adjacência
        adj = (Bag<Integer>[]) new Bag[V];

        for (int v = 0; v < V; v++) {
            adj[v] = new Bag<Integer>();
        }

        // copia as conexões do grafo original
        for (int v = 0; v < graph.V(); v++) {

            // usamos uma pilha para manter a mesma ordem
            Stack<Integer> reverse = new Stack<Integer>();

            for (int w : graph.adj[v]) {
                reverse.push(w);
            }

            for (int w : reverse) {
                adj[v].add(w);
            }
        }
    }

    // retorna o número de vértices
    public int V() {
        return V;
    }

    // retorna o número de arestas
    public int E() {
        return E;
    }

    // verifica se o vértice está dentro do intervalo válido
    private void validateVertex(int v) {

        if (v < 0 || v >= V)

            throw new IllegalArgumentException("vértice " + v + " não está entre 0 e " + (V-1));
    }

    // adiciona uma aresta entre dois vértices
    public void addEdge(int v, int w) {

        validateVertex(v);
        validateVertex(w);

        E++;

        // adiciona w na lista de v
        adj[v].add(w);

        // adiciona v na lista de w (grafo não direcionado)
        adj[w].add(v);
    }

    // retorna os vértices adjacentes de um vértice v
    public Iterable<Integer> adj(int v) {

        validateVertex(v);

        return adj[v];
    }

    // retorna o grau de um vértice
    public int degree(int v) {

        validateVertex(v);

        return adj[v].size();
    }

    // imprime o grafo em forma de lista de adjacência
    public String toString() {

        StringBuilder s = new StringBuilder();

        s.append(V + " vertices, " + E + " arestas " + NEWLINE);

        for (int v = 0; v < V; v++) {

            s.append(v + ": ");

            for (int w : adj[v]) {
                s.append(w + " ");
            }

            s.append(NEWLINE);
        }

        return s.toString();
    }

    // gera uma representação do grafo no formato DOT (GraphViz)
    public String toDot() {

        StringBuilder s = new StringBuilder();

        s.append("graph {" + NEWLINE);

        s.append("node[shape=circle, style=filled, fixedsize=true, width=0.3, fontsize=\"10pt\"]" + NEWLINE);

        int selfLoops = 0;

        for (int v = 0; v < V; v++) {

            for (int w : adj[v]) {

                if (v < w) {

                    s.append(v + " -- " + w + NEWLINE);

                } else if (v == w) {

                    if (selfLoops % 2 == 0) {
                        s.append(v + " -- " + w + NEWLINE);
                    }

                    selfLoops++;
                }
            }
        }

        s.append("}" + NEWLINE);

        return s.toString();
    }

    // método principal para executar o programa
    public static void main(String[] args) {

        In in = new In(args[0]);

        Graph graph = new Graph(in);

        StdOut.println(graph);
    }
}