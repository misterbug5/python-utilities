from sys import argv
from typing import List

from bs4 import BeautifulSoup
from PIL import ImageTk, Image

import requests
import tkinter as tk
import re

IMAGE_REGEX = r"(\w|%(\d|\w){2})*(.jpg|.jpeg|.png)"


class ImageLister:
    def __init__(self, site_url: str):
        self.imageList = []
        self.site_url = site_url
        request = requests.get(self.site_url)
        if not request.ok:
            raise ConnectionError('Url Don\'t exist')
        self.soup = BeautifulSoup(request.text, 'html.parser')
        self.parse()

    def parse(self) -> None:
        images = self.soup.find_all('img')
        images = [image.get('src') for image in images]
        self.imageList = list(
            filter(lambda link: re.search(IMAGE_REGEX, link) is not None,
                   images))


class Application(tk.Frame):
    def __init__(self, images: List[str], master=None):
        super().__init__(master)
        self.img = None
        self.canvas = None
        self.download = None
        self.back_img = None
        self.next_img = None
        self.quit = None
        self.master = master
        self.pack()
        self.images = images
        self.actual_image = 0
        self.create_widgets()
        self.update_image()

    def create_widgets(self):
        self.download = tk.Button(self, text='Download', command=self.download_image)
        self.download.pack(side='top')
        self.quit = tk.Button(self, text='QUIT', command=self.master.destroy)
        self.quit.pack(side='bottom')
        self.next_img = tk.Button(self, text='>', command=self.next_image)
        self.next_img.pack(side='right')
        self.canvas = tk.Canvas(self.master, bg='white', width=1600, height=900)
        self.canvas.pack()
        self.back_img = tk.Button(self, text='<', command=self.back_image)
        self.back_img.pack(side='left')

    def next_image(self) -> None:
        self.actual_image += 1
        if self.actual_image >= len(self.images):
            self.actual_image = 0
        self.update_image()

    def back_image(self) -> None:
        self.actual_image += 1
        if self.actual_image >= len(self.images):
            self.actual_image = 0
        self.update_image()

    def download_image(self) -> None:
        image = self.images[self.actual_image]
        r = requests.get(image)
        file_name = re.search(IMAGE_REGEX, image).group()
        with open(file_name, 'wb') as f:
            f.write(r.content)
            f.close()

    def update_image(self) -> None:
        image = requests.get(self.images[self.actual_image], stream=True)
        self.img = ImageTk.PhotoImage(Image.open(image.raw))
        self.canvas.create_image(0, 0, anchor='nw', state='normal', image=self.img)


if __name__ == '__main__':
    if len(argv) == 1:
        raise AttributeError('Please add an url')
    Application(ImageLister(site_url=argv[1]).imageList, master=tk.Tk()).mainloop()
