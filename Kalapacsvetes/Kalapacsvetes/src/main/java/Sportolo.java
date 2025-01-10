public class Sportolo {
    private int helyezes;
    private double eredmeny;
    private String nev;
    private String orszagKod;
    private String helyszin;
    private String datum;

    public Sportolo(int helyezes, double eredmeny, String nev, String orszagKod, String helyszin, String datum) {
        this.helyezes = helyezes;
        this.eredmeny = eredmeny;
        this.nev = nev;
        this.orszagKod = orszagKod;
        this.helyszin = helyszin;
        this.datum = datum;
    }

    public int getHelyezes() {
        return helyezes;
    }

    public double getEredmeny() {
        return eredmeny;
    }

    public String getNev() {
        return nev;
    }

    public String getOrszagKod() {
        return orszagKod;
    }

    public String getHelyszin() {
        return helyszin;
    }

    public String getDatum() {
        return datum;
    }

    @Override
    public String toString() {
        return "Helyezés: " + helyezes + ", Eredmény: " + eredmeny + ", Név: " + nev + ", Ország: " + orszagKod + ", Helyszín: " + helyszin + ", Dátum: " + datum;
    }
}
