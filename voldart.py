import sys
import time
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
} 


class VolDeArt:
    def __init__(self, url, max_pages=100, override_results=True) -> None:
        self.url = url 
        self.max_pages = max_pages
        self.filename = "images_links.txt"
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
            for lien in lien_images:
                file_writer.write(str(lien) + "\n")
        
    def get_images_links(self):
        liens = self.soup.find_all('a')
        liens_images = set()
        for lien in liens:
            if lien.get('data-icon'):
                liens_images.add(lien['data-icon'].strip().split("?")[0])
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
            time.sleep(2)
            self.next_page()
            compteur += 1


if __name__ == "__main__":
    site_url = "https://www.deviantart.com/topic/digital-art"
    scraper = VolDeArt(site_url, max_pages=3)
    scraper.get_all_data()
