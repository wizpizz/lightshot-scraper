# imports
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

# Create config file
def create_config():
  f = open('config.json', 'w')
  def_dict = {"scraped_directory": "./Scraped"}
  json.dump(def_dict, f)
  f.close()

# Check if config exist
if not os.path.isfile('config.json'):
  create_config()

def scraper(directory):
  os.system('cls')
  if not os.path.exists(directory):
    os.mkdir(directory)
  while True:
    # Set a random user agent
    headers = {'User-Agent': str(ua.random)}
    # Generate a random code to try to get the screenshot from
    ss_code = ''.join((random.choice(letters_and_digits) for i in range(6))) 
    # Get the html data from the website
    r = requests.get(f'https://prnt.sc/{ss_code}', headers=headers).text
    soup = bs4.BeautifulSoup(r, 'html.parser')
    # Search for the screenshot in the html
    image = soup.find("img", class_="no-click screenshot-image")
    # Checks if the screenshot exists
    if image is not None:
      image_url = image.get('src')
      # Checks if the screenshot is deleted, deleted screenshots have "211be8ff" in their url
      if "211be8ff" not in image_url:
        # Prints the current time and the url
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {image_url}")
        # Requests the image and saves it in the directory
        f = open(f'{directory}/{ss_code}.png', 'wb')
        f.write(requests.get(image_url, headers=headers).content)
        f.close()
        # Checks whether the saved image is hosted on imgur
        if 'imgur' in image_url:
          file = Image.open(f'{directory}/{ss_code}.png')
          # Gets the resolution of the image
          width, height = file.size
          file.close()
          # Deleted imgur images are 161 by 81. If the resolution matches, deletes the image from the directory
          if str(width) == "161" and str(height) == "81":
            os.remove(f'{directory}/{ss_code}.png')
            # Prints the time and the removed imgur image
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {ss_code} Removed")
      # If the screenshot is deleted, prints the time and "Deleted"
      elif "211be8ff" in image_url:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Deleted")

def choice_prompt():
  # Cleares the console and prints the choices
  os.system('cls')
  choice = input('==============================================================\n'
                 'Select option:\n'
                 '1) Start scraping\n'
                 '2) Choose directory\n'
                 '3) Exit\n'
                 '==============================================================\n'
                 'Your option: ')
  # 1) Start scraping
  if str(choice) == "1":
    # Tries to get the directory that was selected from the config
    try:
      directory = json.load(open('config.json', encoding='utf-8'))['scraped_directory']
    # If the config is corrupted creates the default config
    except KeyError:
      create_config()
      directory = json.load(open('config.json', encoding='utf-8'))['scraped_directory']
    # Starts scraping
    scraper(directory)
  # 2) Select directory
  elif str(choice) == "2":
    # Pop-up window to select a directory
    open_file = filedialog.askdirectory()
    # If no directory is selected, prints  a warning
    if str(open_file) == "":
      print("You didn't select any directory!")
      time.sleep(2)
      choice_prompt()
    # If a directory is selected, edits the config accordingly
    elif not str(open_file) == "":
      with open('config.json', 'r') as f:
        data = json.load(f)
      data['scraped_directory'] = str(open_file)
      with open('config.json', 'w') as f:
        json.dump(data, f)
      choice_prompt()
  # 3) Exit
  elif str(choice) == "3":
    exit()

# Starts the script
choice_prompt()
