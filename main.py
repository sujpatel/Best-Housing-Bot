import discord 
import requests #imports requests which is used to send HTTP requests (e.g. GET and POST)
import sqlite3 #included by default
from datetime import datetime #included by default, used for working with dates and times
import asyncio #included by default , allows bot to perform tasks concurrently 


DISCORD_TOKEN = "your-discord-token"
CHANNEL_ID = 123456789 
RAPIDAPI_KEY = "your-rapidapi-key"
CITY = "New Brunswick" 
STATE = "NJ" 
MAX_PRICE = 2000 

class SimpleHousingBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.setup_database()
        
    def setup_database(self):
        with sqlite3.connect('housing.db') as db:
            db.execute('''
                       CREATE TABLE IF NOT EXISTS listings(
                           address TEXT PRIMARY KEY,
                           date_seen TEXT
                       )
                       ''')
    
    def is_listing_new(self, address):
        with sqlite3.connect('housing.db') as db:
            result =  db.execute(
                'SELECT 1 FROM listings WHERE address = ?',
                (address,)
            ).fetchone()
            
            return result is None
            
    def save_listing(self, address):
        with sqlite3.connect('housing.db') as db:
            db.execute(
                'INSERT INTO listings (address, date_seen) VALUES (?, ?)',
                (address, datetime.now().strftime('%Y-%m-%d'))
            )
            
    def clean_old_listings(self):
        
        with sqlite3.connect('housing.db') as db:
            db.execute('''
                       DELETE FROM listings
                       WHERE date_seen < date('now', '-30 days')
                       ''')
            
    def get_listings(self):
        
        url = ""
        
        querystring = {
            "city": CITY,
            "state_code": STATE,
            "limit": "10",
            "sort": "newest",
            "price_max":str(MAX_PRICE)
        }
        
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": ""
        }
        
        try:
            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()
            
            new_listing = []
            for listing in data.get('listings', []):
                address = f"{listings.get('address')} {listing.get('city')}"
                
                if self.is_listing_new(address):
                    new_listings.append()
            