package Lab1;
import java.util.*;

public class Main {
    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);
        String str;
        HashMap<Character, HashMap<Character, Character>> fa = new HashMap<>();

        System.out.println("Print the derivation rules in column (e.g S -> aB). Enter 'stop' to finish. ");

        // reading the input until stop
        while(true) {
            str = scanner.nextLine();

            if (str.equals("stop"))
                break;

            // splitting the string into 2 parts
            String[] parts = str.split(" -> ");

            if(fa.containsKey(parts[0].charAt(0))) {
                if(parts[1].length() == 2) {
                    fa.get(parts[0].charAt(0)).put(parts[1].charAt(0), parts[1].charAt(1));
                } else {
                    fa.get(parts[0].charAt(0)).put(parts[1].charAt(0), '$');
                }

            } else {
                HashMap<Character, Character> sr = new HashMap<>();
                if(parts[1].length() == 2) {
                    sr.put(parts[1].charAt(0), parts[1].charAt(1));
                } else {
                    sr.put(parts[1].charAt(0), '$');
                }
                fa.put(parts[0].charAt(0), sr);
            }
        }

        System.out.println("Print the string to be verified: ");
        str = scanner.nextLine();
        char next = 'S';

        for(int i = 0; i < str.length(); i++) {
            if(fa.get(next).containsKey(str.charAt(i))) {
                next = fa.get(next).get(str.charAt(i));
            }

            if(i == str.length() - 1) {
                if(next == '$')
                {
                    System.out.println("The string '" + str + "' is accepted");
                }
                else
                    System.out.println("The string '" + str + "' is rejected");
            }
        }
    }
}