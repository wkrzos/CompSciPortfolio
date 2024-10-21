import subprocess
import sys
import os
import json
import platform

def main(directory_path):
    results = []
    total_files = 0
    total_characters = 0
    total_words = 0
    total_lines = 0
    char_frequency = {}
    word_frequency = {}

    for file in os.listdir(directory_path):
        if file.endswith(".txt"):
            total_files += 1
            path = os.path.join(directory_path, file)

            # Determine the correct executable based on the operating system
            executable_name = ".\\file_analyser\\text_analyser.exe" if platform.system() == "Windows" else "./file_analyser/text_analyser"
            process = subprocess.Popen([executable_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

            output, _ = process.communicate(input=path.encode())
            result = json.loads(output)
            results.append(result)

            total_characters += result["totalCharacters"]
            total_words += result["totalWords"]
            total_lines += result["totalLines"]

            char_frequency[result["mostFrequentChar"]] = char_frequency.get(result["mostFrequentChar"], 0) + 1
            word_frequency[result["mostFrequentWord"]] = word_frequency.get(result["mostFrequentWord"], 0) + 1

    most_frequent_char = max(char_frequency, key=char_frequency.get)
    most_frequent_word = max(word_frequency, key=word_frequency.get)

    summary = {
        "totalFiles": total_files,
        "totalCharacters": total_characters,
        "totalWords": total_words,
        "totalLines": total_lines,
        "mostFrequentChar": most_frequent_char,
        "mostFrequentWord": most_frequent_word,
    }

    print(json.dumps(summary, indent=4))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)
    main(sys.argv[1])
