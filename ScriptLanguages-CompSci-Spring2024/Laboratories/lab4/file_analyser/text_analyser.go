package main

import (
    "bufio"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "os"
    "strings"
)

func main() {
    reader := bufio.NewReader(os.Stdin)
    fmt.Print("Enter file path: ")
    path, _ := reader.ReadString('\n')
    path = strings.TrimSpace(path)

    content, err := ioutil.ReadFile(path)
    if err != nil {
        fmt.Println(err)
        return
    }

    text := string(content)
    words := strings.Fields(text)
    lines := strings.Split(text, "\n")

    charCount := len(text)
    wordCount := len(words)
    lineCount := len(lines)

    charFrequency := make(map[rune]int)
    wordFrequency := make(map[string]int)

    for _, char := range text {
        charFrequency[char]++
    }

    for _, word := range words {
        wordFrequency[strings.ToLower(word)]++
    }

    mostFrequentChar := ' '
    maxCharFreq := 0
    for char, freq := range charFrequency {
        if freq > maxCharFreq {
            maxCharFreq = freq
            mostFrequentChar = char
        }
    }

    mostFrequentWord := ""
    maxWordFreq := 0
    for word, freq := range wordFrequency {
        if freq > maxWordFreq {
            maxWordFreq = freq
            mostFrequentWord = word
        }
    }

    result := map[string]interface{}{
        "filePath":          path,
        "totalCharacters":   charCount,
        "totalWords":        wordCount,
        "totalLines":        lineCount,
        "mostFrequentChar":  string(mostFrequentChar),
        "mostFrequentWord":  mostFrequentWord,
    }

    resultJSON, err := json.Marshal(result)
    if err != nil {
        fmt.Println(err)
        return
    }

    fmt.Println(string(resultJSON))
}
