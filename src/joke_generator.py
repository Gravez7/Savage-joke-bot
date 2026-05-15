"""
Joke Generator Module
Generates savage yo momma jokes, roasts, and sarcasm using OpenAI API.
"""

import os
import json
import random
from openai import OpenAI

class JokeGenerator:
    def __init__(self, config_path: str = "config.json"):
        """Initialize the joke generator with OpenAI API."""
        with open(config_path) as f:
            self.config = json.load(f)
        
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.bot_personality = self.config.get("bot_personality", {})
    
    def generate_yo_momma_joke(self) -> str:
        """Generate a savage yo momma joke."""
        prompt = """You are a hilarious, sassy 10-year-old with ZERO filter. 
        Generate ONE funny 'Yo Momma' joke. Keep it PG-13 but savage.
        Just the joke, no preamble. Make it about 1-2 sentences."""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a sassy kid who tells savage jokes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=80
        )
        
        return response.choices[0].message.content.strip()
    
    def generate_roast(self) -> str:
        """Generate a savage roast/insult."""
        prompt = """Generate ONE hilarious roast or insult that sounds like it's from a confident kid.
        Keep it PG-13 and funny. Just the roast, no preamble."""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a sassy kid with attitude."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=80
        )
        
        return response.choices[0].message.content.strip()
    
    def generate_video_script(self, activity: str) -> dict:
        """Generate a complete video script with jokes for a given activity."""
        jokes = [
            self.generate_yo_momma_joke(),
            self.generate_roast(),
            self.generate_yo_momma_joke()
        ]
        
        catchphrase = self.bot_personality.get("catchphrase", "Tik Tak Toe, I knew she was a hoe!")
        
        script = {
            "activity": activity,
            "opening_joke": jokes[0],
            "punchline": jokes[1],
            "outro": f"{jokes[2]}... {catchphrase}",
            "jokes": jokes,
            "catchphrase": catchphrase
        }
        
        return script
