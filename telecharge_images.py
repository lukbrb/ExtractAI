import time
import csv
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
} 

def download_image(url, artiste, numero_image):
    response = requests.get(url, stream=True, headers=headers)
    extension = '.jpg' if '.jpg' in url else '.png'
    filename = f"{artiste}_{numero_image}{extension}"
    if response.ok:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Image {filename} téléchargée avec succès")
    else:
        print(f"Erreur lors du téléchargement de l'image {url}")
        input("Va changer ton VPN")
        download_image(url, artiste, numero_image)


def read_csv(filename, sep=";"):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=sep)
        liens = list()
        descriptions = list()
        for row in reader:
            descriptions.append(row[0].split()[-1])
            liens.append(row[1])

    return descriptions, liens


descriptions, liens_images = read_csv('images_generales.csv')
print(len(liens_images))
for i, lien_image in enumerate(liens_images):
    description = descriptions[i]
    download_image(lien_image, description, i)
    if i % 50 == 0:
        print("💤", end='')
        time.sleep(0.5)
        print("💤", end='')
        time.sleep(0.5)
        print("💤", end='\n')