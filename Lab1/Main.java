package Lab1;
import java.util.*;
import java.util.Scanner;
import java.io.*;

public class Main {
    public static void main(String[] args) throws FileNotFoundException {

        Scanner scanner = new Scanner(System.in);
        String str;
        HashMap<Character, HashMap<Character, Character>> FA = new HashMap<>();

        // reading the input from a file
        String path = "C:/users/Nastea/LFPC/src/Lab1/var11.txt";
        File file = new File(path);
        Scanner scan = new Scanner(file);

        // reading the input until stop word
        while(true) {
            str = scan.nextLine();

            if (str.equals("stop"))
                break;

            // splitting the string into 2 parts
            String[] parts = str.split(" -> ");

            // check if the map contains a mapping for the specified key
            if(FA.containsKey(parts[0].charAt(0))) {
                if(parts[1].length() == 2) {
                    FA.get(parts[0].charAt(0)).put(parts[1].charAt(0), parts[1].charAt(1));
                } else {
                    FA.get(parts[0].charAt(0)).put(parts[1].charAt(0), '$');
                }
            } else {
                HashMap<Character, Character> sr = new HashMap<>();
                if(parts[1].length() == 2) {
                    sr.put(parts[1].charAt(0), parts[1].charAt(1));
                } else {
                    sr.put(parts[1].charAt(0), '$');
                }
                FA.put(parts[0].charAt(0), sr);
            }
        }

        System.out.println("\n Print the string to be verified: ");
        str = scanner.nextLine();
        char next = 'S';
        StringBuilder route = new StringBuilder(); // for showing the route
        route.append("S"); // start character

        for(int i = 0; i < str.length(); i++) {
            if(FA.get(next).containsKey(str.charAt(i))) {
                next = FA.get(next).get(str.charAt(i));
                if (next != '$')
                    route.append(" -> " + next);
            }

            if(i == str.length() - 1) {
                if(next == '$') {
                    System.out.println("The string '" + str + "' is accepted");
                    System.out.println("The route to obtain the string is: " + route.toString());
                }
                else System.out.println("The string '" + str + "' is rejected");
            }
        }
    }
}