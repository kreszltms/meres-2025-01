import java.io.*;
import java.util.*;

public class Kalapacsvetes {
    public static void main(String[] args) throws IOException {
        // A sportolók listája
        List<Sportolo> sportolok = new ArrayList<>();
        
        // Fájl beolvasása
        BufferedReader br = new BufferedReader(new FileReader("kalapacsvetes.txt"));
        String sor;
        br.readLine(); // Az első sor fejléc, ezt kihagyjuk
        
        while ((sor = br.readLine()) != null) {
            String[] adatok = sor.split(";");
            int helyezes = Integer.parseInt(adatok[0].trim());
            double eredmeny = Double.parseDouble(adatok[1].trim());
            String nev = adatok[2].trim();
            String orszagKod = adatok[3].trim();
            String helyszin = adatok[4].trim();
            String datum = adatok[5].trim();
            
            Sportolo sportolo = new Sportolo(helyezes, eredmeny, nev, orszagKod, helyszin, datum);
            sportolok.add(sportolo);
        }
        br.close();
        
        // 4. Feladat: A fájlban szereplő dobások száma
        System.out.println("4. Feladat:");
        System.out.println("A fájlban szereplő dobások száma: " + sportolok.size());

        // 5. Feladat: Magyar sportolók dobásainak átlageredménye
        System.out.println("5. Feladat:");
        double osszEredmeny = 0;
        int magyarDb = 0;

        for (Sportolo sportolo : sportolok) {
            if (sportolo.getOrszagKod().equals("HUN")) {
                osszEredmeny += sportolo.getEredmeny();
                magyarDb++;
            }
        }

        if (magyarDb > 0) {
            double atlag = osszEredmeny / magyarDb;
            System.out.println("A magyar sportolók dobásainak átlaga: " + String.format("%.2f", atlag));
        } else {
            System.out.println("Nincs magyar sportoló az adatokban.");
        }

        // 6. Feladat: Dobások száma egy adott évben
        System.out.println("6. Feladat:");
        Scanner scanner = new Scanner(System.in);
        System.out.print("Adjon meg egy évszámot: ");
        int ev = scanner.nextInt();

        boolean talalt = false;
        for (Sportolo sportolo : sportolok) {
            if (sportolo.getDatum().startsWith(String.valueOf(ev))) {
                if (!talalt) {
                    System.out.println("A " + ev + "-ban elért legjobb dobások:");
                    talalt = true;
                }
                System.out.println(sportolo.getNev() + " - " + sportolo.getEredmeny() + " m");
            }
        }

        if (!talalt) {
            System.out.println("A megadott évben nem került be egy dobás sem a legjobbak közé.");
        }

        // 7. Feladat: Statisztika: Országok és dobások száma
        System.out.println("7. Feladat:");
        Map<String, Integer> orszagokStat = new HashMap<>();

        for (Sportolo sportolo : sportolok) {
            orszagokStat.put(sportolo.getOrszagKod(), orszagokStat.getOrDefault(sportolo.getOrszagKod(), 0) + 1);
        }

        for (Map.Entry<String, Integer> entry : orszagokStat.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue() + " dobás");
        }

        // 8. Feladat: Magyar sportolók eredményeinek kiírása fájlba
        System.out.println("8. Feladat:");
        BufferedWriter bw = new BufferedWriter(new FileWriter("magyarok.txt"));

        for (Sportolo sportolo : sportolok) {
            if (sportolo.getOrszagKod().equals("HUN")) {
                bw.write(sportolo.getHelyezes() + ";" + sportolo.getEredmeny() + ";" + sportolo.getNev() + ";" + sportolo.getOrszagKod() + ";" + sportolo.getHelyszin() + ";" + sportolo.getDatum());
                bw.newLine();
            }
        }

        bw.close();
    }
}
