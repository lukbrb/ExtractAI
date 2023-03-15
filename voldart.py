import sys
import time
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
} 

class VolDeArt:
    def __init__(self, url, filename, max_pages=100, override_results=True) -> None:
        self.url = url 
        self.max_pages = max_pages
        self.filename = filename
        self.soup = self._fetch_html()
        if override_results:
            print("[*] Suppression des résultats précédents...")
            self._clear_file()

    def _fetch_html(self):
        print(f"[+] Requête pour le lien {self.url}...")
        response = requests.get(self.url, headers=headers)
        if response.ok:
            soup = BeautifulSoup(response.content, 'lxml')
            return soup
        else:
            print("[!] Erreur d'accès :", response.status_code)
            sys.exit(1)

    def _get_next_link(self):
        link_tags = self.soup.find_all('link')
        for link_tag in link_tags:
            if link_tag.get('rel') == ['next']:
                next_link = link_tag.get('href')

                return next_link
        print("[*] Pas de lien vers la prochaine page.")
    
    def _clear_file(self):
        try:
            file_cleaner = open(self.filename, "w")
            file_cleaner.close()
        except FileNotFoundError:
            pass
    
    def _save_links(self, lien_images):
        with open(self.filename, "a") as file_writer:
            for description, lien in lien_images.items():
                file_writer.write(f"{description};{lien}\n")
        
    def get_profile_images(self):
        liens = self.soup.find_all('a')
        liens_images = set()
        for lien in liens:
            if lien.get('data-icon'):
                liens_images.add(lien['data-icon'].strip().split("?")[0])
        print(f"[+] {len(liens_images)} images trouvées.")
        # self._save_links(liens_images)
    
    def get_images_links(self):
        liens_images = dict()
        images = self.soup.find_all('img')
        for image in images:
            lien = image.get("src")
            if 'images-wixmp' in lien:
                i = 0
                while image.name != 'a' and i <= 2:  # Remonte recursivement l'arbre HTML pour trouver le label de l'image 
                    image = image.parent
                    i += 1

                description = image.get('aria-label')
                if description: description = description.replace(', visual art', '')  # Enlève visual art, et condition pour éviter le None
                liens_images[description] = lien
        print(f"[+] {len(liens_images)} images trouvées.")
        self._save_links(liens_images)
    
    def next_page(self):
        next_link = self._get_next_link()
        if next_link:
            self.url = next_link
            self.soup = self._fetch_html()
        else:
            sys.exit(0)

    def get_all_data(self):
        compteur = 1
        while compteur <= self.max_pages:
            self.get_images_links()
            # time.sleep(2)
            self.next_page()
            compteur += 1


def download_image(url, artiste, numero_image):
    response = requests.get(url, stream=True, headers=headers)
    extension = '.jpg' if '.jpg' in url else '.png'
    filename = f"{artiste}_{numero_image}_{extension}"
    if response.ok:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Image {filename} téléchargée avec succès")
    else:
        print(f"Erreur lors du téléchargement de l'image {url}")


if __name__ == "__main__":
    nom_artiste = "yuumei"
    # site_url = "https://www.deviantart.com/topic/digital-art"
    artiste_url = f"https://www.deviantart.com/{nom_artiste}/gallery/all"
    #scraper = VolDeArt(artiste_url, filename=f"artiste_{nom_artiste}.csv", max_pages=83)
    #scraper.get_all_data()
    
