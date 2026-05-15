"""
Selects random activities for the bot character each video.
Ensures variety and keeps content fresh daily.
"""

import json
import random
from typing import List, Dict

class ActivitySelector:
    def __init__(self, config_path: str = "config.json"):
        """Initialize activity selector with config."""
        with open(config_path) as f:
            self.config = json.load(f)
        self.activities = self.config["activities"]
        self.used_activities = []
    
    def get_daily_activity(self) -> str:
        """Get a random activity for today's video."""
        available = [a for a in self.activities if a not in self.used_activities]
        
        # If all activities are used, reset the list
        if not available:
            self.used_activities = []
            available = self.activities
        
        selected = random.choice(available)
        self.used_activities.append(selected)
        
        return selected
    
    def get_activity_description(self, activity: str) -> Dict[str, str]:
        """Get detailed description for video generation."""
        descriptions = {
            "playing_pool": {
                "setting": "A cool billiards hall with neon lights",
                "action": "Shooting pool balls with swagger",
                "vibe": "Competitive and smooth",
                "props": "Pool cue, billiard balls, pool table"
            },
            "playing_darts": {
                "setting": "A casual bar with a dartboard",
                "action": "Throwing darts with precision and jokes",
                "vibe": "Confident and cocky",
                "props": "Darts, dartboard, beer bottles"
            },
            "chillin_in_lounge": {
                "setting": "A laid-back lounge with couch and music",
                "action": "Relaxing and making jokes from the couch",
                "vibe": "Cool and chill",
                "props": "Couch, speakers, remote control"
            },
            "smokey_bar_vibes": {
                "setting": "A smokey dive bar with dim lighting",
                "action": "Sitting at the bar, roasting everyone",
                "vibe": "Cynical and hilarious",
                "props": "Bar stool, drinks, pool table, jukebox"
            },
            "arcade_games": {
                "setting": "A retro arcade with neon lights and games",
                "action": "Playing arcade games while trash talking",
                "vibe": "Energetic and competitive",
                "props": "Arcade machines, joysticks, high scores"
            },
            "card_games": {
                "setting": "A poker table with friends",
                "action": "Playing cards and bluffing with jokes",
                "vibe": "Strategic and funny",
                "props": "Cards, chips, betting tables"
            },
            "skateboarding": {
                "setting": "A skate park with ramps and obstacles",
                "action": "Skateboarding tricks while being cocky",
                "vibe": "Rebellious and cool",
                "props": "Skateboard, ramps, concrete"
            },
            "gym_workout": {
                "setting": "A modern gym with weights and equipment",
                "action": "Flexing and roasting gym bros",
                "vibe": "Confident and sarcastic",
                "props": "Dumbbells, barbells, mirrors"
            }
        }
        
        return descriptions.get(activity, {
            "setting": "An unknown cool place",
            "action": "Doing cool things",
            "vibe": "Awesome",
            "props": "Whatever's needed"
        })
    
    def reset_weekly(self):
        """Reset used activities weekly for rotation."""
        self.used_activities = []

if __name__ == "__main__":
    selector = ActivitySelector()
    
    print("=== DAILY ACTIVITY ===")
    activity = selector.get_daily_activity()
    print(f"Today's activity: {activity}")
    
    print("\n=== ACTIVITY DETAILS ===")
    details = selector.get_activity_description(activity)
    for key, value in details.items():
        print(f"{key}: {value}")
