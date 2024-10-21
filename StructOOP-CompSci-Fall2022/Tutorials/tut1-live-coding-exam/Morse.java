package Code;

public class Morse {

    private static String word = "BARA"; //Word to translate to morse code
    
    private static char[] letters = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','R','S','T','U','W','Y','Z'};
    private static String[] code = { ".-","-...","-.-.","-..", ".","..-.","--.","....","..",".---","-.-",".-..","--","-.","---",".--.", "--.-"};

    /**Translates from the english alphabet to morse code */
    public String letterToMorse(String wordToConvert, char[] alphabetVariant, String[] morseCodeVariant){

        String wordInMorse = "";
        for(int i = 0; i < wordToConvert.length(); i++){
            for(int j = 0; j < alphabetVariant.length; j++){
                if(wordToConvert.charAt(i) == alphabetVariant[j]) {
                    wordInMorse += " " + morseCodeVariant[j];
                }
            }
        }
        return wordInMorse;
    }

    /**Displays letters with no dots */
    public String onlyDashes(char[] alphabetVariant, String[] morseCodeVariant){

        String lettersWithNoDash = "";
        for(int i = 0; i < morseCodeVariant.length; i++){
            if(morseCodeVariant[i].contains(".")){
            } else {
                lettersWithNoDash += alphabetVariant[i];
            }
        }
        return lettersWithNoDash;
    }

    //Getters and setters
    public static String getWord() {
        return word;
    }

    public static void setWord(String word) {
        Morse.word = word;
    }

    public static char[] getLetters() {
        return letters;
    }

    public static void setLetters(char[] letters) {
        Morse.letters = letters;
    }

    public static String[] getCode() {
        return code;
    }

    public static void setCode(String[] code) {
        Morse.code = code;
    }
}