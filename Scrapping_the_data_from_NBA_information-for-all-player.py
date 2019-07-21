# NBA Project - To extract the data of NBA 

# Importing the required libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os
import csv
import pandas as pd

# Creating a Class of players to save the player data
class Player(object):
    """docstring for Player"""
    def __init__(self):
        self.name = ""
        self.link = ""
        self.Height = ""
        self.Weight = ""
        self.DOB = ""
        self.Age = ""
        self.From = ""
        self.Debuted = ""

# Creating a function to find all the NBA players and their hyperlink in website
def get_player_list():
    
    # Create driver
    driver = webdriver.PhantomJS(executable_path = r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')

    # Hyperlink of all the players
    url = 'https://www.nba.com/players'

    # Download html page
    driver.get(url)

    # Create soup
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Find the section/aread where the list of players contains
    div = soup.find('div', class_= 'row players-wrapper')

    # Initialize url_head with the main website
    url_head = 'https://www.nba.com'

    player_list = []

    # Initiate for loop to add the player information and link in Player Class
    for a in div.find_all('a'):
        new_play = Player()
        new_play.name = a['title']
        new_play.link = url_head + a['href']
        player_list.append(new_play)

    # Quit the driver
    driver.quit() 

    return player_list


# Create a function to download the images of players
def get_nba_player_image(player_list):

    # Create driver
    driver = webdriver.PhantomJS(executable_path = r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    
    # Create directory if not exisits
    if not os.path.exists('nba_player'):
        os.makedirs('nba_player')

    # Loop in player list to download the images    
    for player in player_list:

        #Player link
        url = player.link

        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'lxml')

        # Find the image 
        div = soup.find('section', class_ = 'nba-player-header__item nba-player-header__headshot')

        img = div.find('img')

        #print(img['src'])

        f = open('nba_player\{0}.jpg'.format(player.name), 'wb')

        # Save the image of a player
        f.write(requests.get('https:' + img['src']).content)

        f.close()

    driver.quit()


# Create a function to get all the details of the players
def get_details_for_all_players(player_list):
    
    # Create a driver
    driver = webdriver.PhantomJS(executable_path = r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    
    # Loop in player list to extract the details
    for p in player_list:
        url = p.link

        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'lxml')

        # Initalize the variables
        Height = ""
        Weight = ""
        DOB = ""
        Age = ""
        From = ""
        Debuted = ""

        # Find the height vale=ue
        height_bloc = soup.find('section', class_ = 'nba-player-vitals__top-left small-6')

        Height_f = height_bloc.find('p', class_ = 'nba-player-vitals__top-info-imperial').text
        Height_m = height_bloc.find('p', class_ = 'nba-player-vitals__top-info-metric').text

        H_m = Height_m.replace('\n', '').split('/')

        a = H_m[1].strip()

        Height = Height_f + '/' + a

        #print(Height)

        # Find Weight value
        weight_bloc = soup.find('section', class_ = 'nba-player-vitals__top-right small-6')

        Weight_l = weight_bloc.find('p', class_ = 'nba-player-vitals__top-info-imperial').text
        Weight_k = weight_bloc.find('p', class_ = 'nba-player-vitals__top-info-metric').text

        W_k = Weight_k.replace('\n', '').split('/')

        b = W_k[1].strip()

        Weight = Weight_l + '/' + b

        ## Other Information

        Other_Info_Bloc = soup.find('section', class_ = 'nba-player-vitals__bottom menu vertical')

        li_blocs = Other_Info_Bloc.find_all('li')

        # DOB value
        DOB = li_blocs[0].find('span', class_ = 'nba-player-vitals__bottom-info').text
        DOB = DOB.strip ()

        # Age value
        Age = li_blocs[1].find('span', class_ = 'nba-player-vitals__bottom-info').text
        Age = Age.strip ()

        # From value
        From = li_blocs[2].find('span', class_ = 'nba-player-vitals__bottom-info').text
        From = From.strip()

        # Debuted value
        Debuted = li_blocs[3].find('span', class_ = 'nba-player-vitals__bottom-info').text
        Debuted = Debuted.strip ()

        p.Height = Height
        p.Weight = Weight
        p.DOB = DOB
        p.Age = Age
        p.From = From
        p.Debuted = Debuted

    driver.quit()

    return player_list

player_list = get_details_for_all_players(get_player_list())

# Calling the function to get the images of all the players
get_nba_player_image(get_player_list())


# Declaring the list to store the data in CSV file
names = []
links = []
Heights = []
Weights = []
DOBs = []
Ages = []
Froms = []
Debuteds = []

for p in player_list:
  names.append(p.name)
  links.append(p.link)
  Heights.append(p.Height)
  Weights.append(p.Weight)
  DOBs.append(p.DOB)
  Ages.append(p.Age)
  Froms.append(p.From)
  Debuteds.append(p.Debuted)

nba_players = pd.DataFrame({'Name':names, 
                            'link':links,
                            'Height':Heights,
                            'Weight':Weights,
                            'DOB':DOBs,
                            'Age':Ages,
                            'From':Froms,
                            'Debuted':Debuteds})


nba_players.to_csv('nba_players.csv')