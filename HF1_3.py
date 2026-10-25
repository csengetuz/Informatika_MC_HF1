
import random
import csv
import os

output_path = ""    #kimeneti fájl elérési útja

n_participants = int(input("Number of participants: "))   #kísérleti alanyok számának bekérése terminálról

ID =[]
Age = []
Gender = []
Sys = []
Dys = []
Pul = []
Temp = []
RT = []
K = []

for i in range (n_participants):    #adatok generálása megfelelő tartományokon belül
    ID.append(i)
    Age.append(random.randint(18, 70))
    Gender.append(random.choice(["F", "M"]))
    Sys.append(random.randint(120, 129))    #https://www.webbeteg.hu/cikkek/magasvernyomas/272/szisztoles-es-diasztoles-ertek
    Dys.append(random.randint(80, 84))
    Pul.append(random.randint(50, 120)) #https://www.webbeteg.hu/cikkek/magasvernyomas/5457/mit-mutat-meg-a-pulzus
    Temp.append(f"{random.randint(360, 370) / 10:.1f}") #https://www.webbeteg.hu/cikkek/egeszseges/25387/mi-a-testhomerseklet-normal-tartomanya
    RT.append(f"{random.randint(0, 50) / 10:.2f}")
    K.append(f"{random.randint(0, 1000) / 10:.2f}")

with open(os.path.join(output_path, "tesztadatok.csv"), "w", newline="") as file:   #adatok elmentése .csv file-ba
    writer = csv.writer(file)

    writer.writerow(["ID",  #fejléc
                     "Age", 
                     "Gender", 
                     "Sys (Hgmm)", 
                     "Dys (Hgmm)",
                     "Pul", 
                     "Temp (°C)", 
                     "RT (s)", 
                     "K"])

    writer.writerows(zip(ID, Age, Gender, Sys, Dys, Pul, Temp, RT, K))

    print(f"File saved to: {output_path}")