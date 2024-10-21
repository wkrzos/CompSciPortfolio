import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;

class HuffmanNode implements Comparable<HuffmanNode> {
    char character;
    int frequency;
    HuffmanNode left;
    HuffmanNode right;

    public HuffmanNode(char character, int frequency) {
        this.character = character;
        this.frequency = frequency;
    }

    @Override
    public int compareTo(HuffmanNode otherNode) {
        return this.frequency - otherNode.frequency;
    }
}

public class HuffmanCoding {
    private Map<Character, String> characterToCode = new HashMap<>();
    private Map<String, Character> codeToCharacter = new HashMap<>();

    public void buildCodeTable(HuffmanNode root, String code) {
        if (root == null) {
            return;
        }

        if (root.left == null && root.right == null) {
            characterToCode.put(root.character, code);
            codeToCharacter.put(code, root.character);
        }

        buildCodeTable(root.left, code + "0");
        buildCodeTable(root.right, code + "1");
    }

    public String encodeText(String text) {
        StringBuilder encodedText = new StringBuilder();
        for (int i = 0; i < text.length(); i++) {
            char character = text.charAt(i);
            encodedText.append(characterToCode.get(character));
        }
        return encodedText.toString();
    }

    public String decodeText(String encodedText) {
        StringBuilder decodedText = new StringBuilder();
        StringBuilder currentCode = new StringBuilder();

        for (int i = 0; i < encodedText.length(); i++) {
            currentCode.append(encodedText.charAt(i));
            if (codeToCharacter.containsKey(currentCode.toString())) {
                char character = codeToCharacter.get(currentCode.toString());
                decodedText.append(character);
                currentCode.setLength(0);
            }
        }

        return decodedText.toString();
    }

    public void displayTree(HuffmanNode node, String indent) {
        if (node != null) {
            System.out.println(indent + "Character: " + node.character + ", Frequency: " + node.frequency);
            displayTree(node.left, indent + "  |");
            displayTree(node.right, indent + "  |");
        }
    }

    public void displayCodeTable() {
        System.out.println("Coding Table:");
        for (Map.Entry<Character, String> entry : characterToCode.entrySet()) {
            System.out.println("Character: " + entry.getKey() + ", Code: " + entry.getValue());
        }
    }

    public static void main(String[] args) {
        char[] characters = {'a', 'b', 'c', 'd', 'e'};
        int[] frequencies = {5, 9, 12, 13, 16};

        PriorityQueue<HuffmanNode> queue = new PriorityQueue<>();
        for (int i = 0; i < characters.length; i++) {
            HuffmanNode node = new HuffmanNode(characters[i], frequencies[i]);
            queue.offer(node);
        }

        while (queue.size() > 1) {
            HuffmanNode leftChild = queue.poll();
            HuffmanNode rightChild = queue.poll();

            HuffmanNode parentNode = new HuffmanNode('\0', leftChild.frequency + rightChild.frequency);
            parentNode.left = leftChild;
            parentNode.right = rightChild;

            queue.offer(parentNode);
        }

        HuffmanNode root = queue.poll();

        HuffmanCoding huffmanCoding = new HuffmanCoding();
        huffmanCoding.buildCodeTable(root, "");

        String text = "abacabad";
        String encodedText = huffmanCoding.encodeText(text);
        String decodedText = huffmanCoding.decodeText(encodedText);

        System.out.println("Original text: " + text);
        System.out.println("Encoded text: " + encodedText);
        System.out.println("Decoded text: " + decodedText);

        System.out.println("Huffman Tree:");
        huffmanCoding.displayTree(root, "");

        huffmanCoding.displayCodeTable();
    }
}
