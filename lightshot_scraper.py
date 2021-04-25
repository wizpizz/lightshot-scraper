import json
import requests
import bs4
import string
import random
import fake_useragent
import datetime
from PIL import Image
import os
from tkinter import Tk, filedialog
import time

root = Tk()
root.withdraw() # Hides small tkinter window.
root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.

ua = fake_useragent.UserAgent()

letters_and_digits = string.ascii_letters + string.digits

def create_config():
  f = open('config.json', 'w')
  def_dict = {"scraped_directory": "./Scraped"}
  json.dump(def_dict, f)
  f.close()

if not os.path.isfile('config.json'):
  create_config()

def scraper(directory):
  if not os.path.exists(directory):
    os.mkdir(directory)
  while True:
    headers = {'User-Agent': str(ua.random)}
    ss_code = ''.join((random.choice(letters_and_digits) for i in range(6))) 
    r = requests.get(f'https://prnt.sc/{ss_code}', headers=headers).text
    soup = bs4.BeautifulSoup(r, 'html.parser')
    image = soup.find("img", class_="no-click screenshot-image")
    if image is not None:
      image_url = image.get('src')
      if "211be8ff" not in image_url:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {image_url}")
        f = open(f'{directory}/{ss_code}.png', 'wb')
        f.write(requests.get(image_url, headers=headers).content)
        f.close()
        if 'imgur' in image_url:
          file = Image.open(f'{directory}/{ss_code}.png')
          width, height = file.size
          file.close()
          if str(width) == "161" and str(height) == "81":
            os.remove(f'{directory}/{ss_code}.png')
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {ss_code} Removed")
      elif "211be8ff" in image_url:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Deleted")

def choice_prompt():
  os.system('cls')
  choice = input('==============================================================\n'
                 'Select option:\n'
                 '1) Start scraping\n'
                 '2) Choose directory\n'
                 '3) Exit\n'
                 '==============================================================\n'
                 'Your option:')
  if str(choice) == "1":
    try:
      directory = json.load(open('config.json', encoding='utf-8'))['scraped_directory']
    except KeyError:
      create_config()
      directory = json.load(open('config.json', encoding='utf-8'))['scraped_directory']
    scraper(directory)
  elif str(choice) == "2":
    open_file = filedialog.askdirectory()
    if str(open_file) == "":
      print("You didn't choose any directory!")
      time.sleep(2)
      choice_prompt()
    elif not str(open_file) == "":
      with open('config.json', 'r') as f:
        data = json.load(f)
      data['scraped_directory'] = str(open_file)
      with open('config.json', 'w') as f:
        json.dump(data, f)
      choice_prompt()
  elif str(choice) == "3":
    exit()

choice_prompt()
