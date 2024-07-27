import os
import requests
import bs4
import threading
import mimetypes

class ThreadedScraper:

    def __init__(self):
        self.download_threads = []
        self.url = 'https://unsplash.com'

    def download_images(self):
        print(f"Downloading images from {self.url}...")
        res = requests.get(self.url)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        # Use a CSS selector to find image elements
        img_tags = soup.select('img')  

        for img in img_tags:
            img_url = img.get('src')
            if img_url and img_url.startswith('http'):
                print(f"Downloading image {img_url}...")
                img_res = requests.get(img_url)
                img_res.raise_for_status()

                # Get the Content-Type to determine the file extension
                content_type = img_res.headers['Content-Type']
                extension = mimetypes.guess_extension(content_type)

                if extension is None:
                    if 'image/jpeg' in content_type:
                        extension = '.jpg'
                    elif 'image/png' in content_type:
                        extension = '.png'
                    elif 'image/gif' in content_type:
                        extension = '.gif'
                    else:
                        extension = '.jpg'  # Default to .jpg if the extension is not recognized

                # Sanitize and save the image
                img_name = os.path.basename(img_url).split('?')[0]  # Remove query parameters
                if not img_name.endswith(extension):
                    img_name += extension
                
                img_path = os.path.join('unsplash_images', img_name)
                
                with open(img_path, 'wb') as img_file:
                    for chunk in img_res.iter_content(100000):
                        img_file.write(chunk)
                print(f"Downloaded {img_path}")

    def create_and_start_thread_objects(self):
        # Creating a directory to save the images
        os.makedirs('unsplash_images', exist_ok=True)
        
        download_thread = threading.Thread(target=self.download_images)
        self.download_threads.append(download_thread)
        download_thread.start()

        for download_thread in self.download_threads:
            download_thread.join()
        print("Done.")
    
    def run(self):
        self.create_and_start_thread_objects()

if __name__ == '__main__':
    scraper = ThreadedScraper()
    scraper.run()