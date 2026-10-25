import cv2
import os

img_1 = cv2.imread("")  #bemeneti file-ok elérési útja
img_2 = cv2.imread("")

output_path = ""    #kimeneti file elérési útja

width_1 = img_1.shape[1]
height_1 = img_1.shape[0]
width_2 = img_2.shape[1]
height_2 = img_2.shape[0]

if width_1 == width_2 and height_1 == height_2: #azonos felbontás ellenőrzése
    print(f"Same resolutions: {width_1} x {height_1}, {width_2} x {height_2}")
else:
    print(f"Different resolutions: {width_1} x {height_1}, {width_2} x {height_2}")

img_1_percentage = int(input("Image 1. % (0-100): ")) / 100 #morfolási arány bekérése terminálról
img_2_percentage = 1 - img_1_percentage

morphed_img = cv2.addWeighted(img_1, img_1_percentage, img_2, img_2_percentage, 0)  #megfelelő arányú morfolás

cv2.imwrite(os.path.join(output_path,"morfolt_kep.jpg"), morphed_img)   #morfolt kép elmentése
print(f"File saved to: {output_path}")