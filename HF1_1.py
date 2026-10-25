import string
import pandas as pd
import os

text_file = ""   #szövegfájl elérési  útja

output_path = ""    #kimeneti file elérési útja



with (open (text_file, "r", encoding = "utf-8") as f):   #szöveget tartalmazó file megnyitása

    words = []

    for line in f:  #szövegfájl beolvasása soronként
        cleared_line = line.translate(str.maketrans('', '', string.punctuation))    #írásjelek eltávolítása a szövegből
        words.extend(cleared_line.split())  #írásjelmentes sorok szavakra bontása, elmentése

        selected_length_words = []

        for word in words:
            if len(word) > 4:   #4 betűnél hosszabb szavak kiválasztása
                selected_length_words.append(word)

    unique_words = []

    for i in range(len(selected_length_words)): #ismétlődő szavak kiszűrése
        repeated = False
        for j in range(len(selected_length_words)):
            if i != j and selected_length_words[i] == selected_length_words[j]:
                repeated = True

        if not repeated:
            unique_words.append(selected_length_words[i])

df = pd.DataFrame(unique_words, columns = ["Szavak"]) #kigyűjtött szavak elmentése excel file-ba
df.to_excel(os.path.join(output_path, "szoveg_output.xlsx"), index=False)
print(f"File elmentve: {output_path}")





