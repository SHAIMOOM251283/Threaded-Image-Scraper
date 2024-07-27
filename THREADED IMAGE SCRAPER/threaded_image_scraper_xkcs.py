import os
import requests
import bs4
import threading

class ThreadedScraper:

    def __init__(self):
        self.download_threads = []
        self.ranges = []
        self.index = 0  # to keep track of the current range index

    def initialize_ranges(self):
        for i in range(0, 140, 10):
            start = i
            end = i + 9
            if start == 0:
                start = 1
            self.ranges.append((start, end))

    def set_range(self):
        if self.index < len(self.ranges):
            self.start, self.end = self.ranges[self.index]
            self.index += 1

    def download_images(self):
        self.set_range()
        for url_number in range(self.start, self.end + 1):
            print('Downloading page https://xkcd.com/%s...' % (url_number))
            res = requests.get('https://xkcd.com/%s' % (url_number))
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, 'html.parser')

            comic_element = soup.select('#comic img')
            if not comic_element:
                print('Could not find comic image.')
            else:
                comic_url = comic_element[0].get('src')
                print("Downloading image %s..." % (comic_url))
                res = requests.get('https:' + comic_url)
                res.raise_for_status()

                os.makedirs('xkcd', exist_ok=True)
                imageFile = open(os.path.join('xkcd', os.path.basename(comic_url)), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()

    def create_and_start_thread_objects(self):
        self.initialize_ranges()
        for _ in range(len(self.ranges)):
            download_thread = threading.Thread(target=self.download_images)
            self.download_threads.append(download_thread)
            download_thread.start()
    
        for download_thread in self.download_threads:
            download_thread.join()
        print("Done.")
    
    def run(self):
        self.create_and_start_thread_objects()

if __name__ == '__main__':
    Download = ThreadedScraper()
    Download.run()
