import discord 
import requests #imports requests which is used to send HTTP requests (e.g. GET and POST)
import sqlite3 #included by default
from datetime import datetime #included by default, used for working with dates and times
import asyncio #included by default , allows bot to perform tasks concurrently 


DISCORD_TOKEN = "your-discord-token" #bot's token needed to authenticate with Discord's API
CHANNEL_ID = 123456789 #ID of DIscord channel where bot will send updates
RAPIDAPI_KEY = "your-rapidapi-key" #RapidAPI key for authenticating API requests
CITY = "New Brunswick" #target city for rental searches
STATE = "NJ" #state abbreviation for rental search
MAX_PRICE = 2000 #sets maximum rent value for listings 

class SimpleHousingBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.create_database()
        
    def create_database(self):
        db = sqlite3.connect('housing.db')
        
        db.execute('''
                   CREATE TABLE IF NOT EXISTS listings (
                       address TEXT,
                       date_seen TEXT,
                       PRIMARY KEY (address)
                   )
                   ''')
        db.close()
        
    def have_we_seen_this_listing(self, address):
        db = sqlite3.connect('housing.db')
        
        result = db.execute(
            'SELECT 1 FROM listings WHERE address = ?',
            (address,)
        ).fetchone()
        
        db.close()
        
        return result is None
    