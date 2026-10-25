
import pandas as pd
import os

input_files = [ #bemeneti file-ok elérési útvonalai
    "",
    "",
    ""
]

output_path = ""    #kimeneti file elérési útvonala

All_results = []

for input_file in input_files:  #adott kísérleti alany eredményeinek vizsgálata

    df = pd.read_csv(   #megfelelő oszlopok beolvasása
        input_file,
        usecols=[
            "participant",
            "dotNumber",
            "key_resp_2.keys",
            "key_resp_2.corr",
            "key_resp_2.rt"
        ]
    )

    dots = [4, 5, 6, 7]

    RT_sum = {}
    RT_n = {}
    Corr_sum = {}
    RT = {}
    Corr = {}

    for dot in dots:
        RT_sum[dot] = 0
        RT_n[dot] = 0
        Corr_sum[dot] = 0

    All_corr = []
    All_RT = []

    for i, row in df.iterrows():
        if row[["dotNumber", 
                "key_resp_2.keys", 
                "key_resp_2.corr", 
                "key_resp_2.rt", 
                "participant"]].notna().all():

            participant = row["participant"]
            dot_number = row["dotNumber"]
            corr = row["key_resp_2.corr"]
            reaction_time = row["key_resp_2.rt"]

            for dot in dots:
                if dot == dot_number:
                    RT_sum[dot] += reaction_time
                    RT_n[dot] += 1
                    Corr_sum[dot] += corr

    for dot in dots:
        if RT_n[dot] > 0:
            RT[dot] = RT_sum[dot] / RT_n[dot]   #átlagos reakcióidők kiszámítása különböző számú pontok esetén
        else:
            RT[dot] = 0

        Corr[dot] = Corr_sum[dot] / 6   #találati pontosság arányának kiszámítása különböző számú pontok esetén

        All_RT.append(RT[dot])
        All_corr.append(Corr[dot])

    result = {"ID": participant}

    for i, dot in enumerate(dots):
        result[f"Corr_{dot}"] = All_corr[i]
    for i, dot in enumerate(dots):
        result[f"RT_{dot}"] = All_RT[i]

    All_results.append(result)  #adott kísérleti alany esetén kiszámított eredmények tárolása

results_df = pd.DataFrame(All_results)  #összes kísérleti alany esetén kiszámított eredményel elmentése .csv file-ba

output_file = os.path.join(output_path, "subitizing_eredmenyek.csv")
results_df.to_csv(output_file, index=False)

print(f"Results saved to: {output_file}")