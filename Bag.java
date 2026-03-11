import java.util.Iterator;
import java.util.NoSuchElementException;

public class Bag<Item> implements Iterable<Item> {

    private Node<Item> first; // primeiro elemento da lista
    private int n;            // número de elementos na Bag

    // Classe auxiliar da lista encadeada
    private static class Node<Item> {
        private Item item;       // valor armazenado
        private Node<Item> next; // referência para o próximo nó
    }

    /**
     * Inicializa uma Bag vazia.
     */
    public Bag() {
        first = null;
        n = 0;
    }

    /**
     * Verifica se a Bag está vazia.
     */
    public boolean isEmpty() {
        return first == null;
    }

    /**
     * Retorna o número de elementos na Bag.
     */
    public int size() {
        return n;
    }

    /**
     * Adiciona um elemento na Bag.
     */
    public void add(Item item) {

        Node<Item> oldfirst = first;

        first = new Node<Item>();
        first.item = item;
        first.next = oldfirst;

        n++;
    }

    /**
     * Retorna um iterador para percorrer os elementos da Bag.
     */
    public Iterator<Item> iterator()  {
        return new LinkedIterator(first);
    }

    private class LinkedIterator implements Iterator<Item> {

        private Node<Item> current;

        public LinkedIterator(Node<Item> first) {
            current = first;
        }

        public boolean hasNext()  {
            return current != null;
        }

        public Item next() {

            if (!hasNext()) throw new NoSuchElementException();

            Item item = current.item;
            current = current.next;

            return item;
        }
    }
}