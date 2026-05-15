"""
Handles uploading generated videos to TikTok.
Manages scheduling, hashtags, captions, and analytics.
"""

import json
import os
from typing import Dict, List
from datetime import datetime

class TikTokUploader:
    def __init__(self, config_path: str = "config.json"):
        """Initialize TikTok uploader with credentials and config."""
        with open(config_path) as f:
            self.config = json.load(f)
        
        # Load credentials from environment variables
        self.access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
        self.video_uploader_id = os.getenv("TIKTOK_VIDEO_UPLOADER_ID")
        self.api_endpoint = self.config["tiktok_api"]["api_endpoint"]
        self.hashtags = self.config["tiktok_api"]["hashtags"]
    
    def upload_video(self, video_path: str, caption: str = None) -> Dict:
        """
        Upload a video to TikTok.
        
        Args:
            video_path: Path to the video file
            caption: Optional custom caption (auto-generated if not provided)
        
        Returns:
            Response with video URL and upload status
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        # Generate caption if not provided
        if not caption:
            caption = self._generate_caption()
        
        print(f"📤 Uploading to TikTok: {video_path}")
        print(f"📝 Caption: {caption}")
        
        # TikTok API upload would go here
        # This is a placeholder for the actual API call
        
        upload_response = {
            "status": "success",
            "video_id": "mock_video_id_12345",
            "tiktok_url": "https://www.tiktok.com/@savage_joke_bot/video/mock_video_id_12345",
            "uploaded_at": datetime.now().isoformat(),
            "caption": caption,
            "hashtags": self.hashtags
        }
        
        return upload_response
    
    def _generate_caption(self) -> str:
        """Generate an engaging caption with hashtags."""
        captions = [
            "No filter, no chill, all jokes! 🔥",
            "Catch these jokes before they catch you slipping 😂",
            "This lil guy got NO FILTER and we love it 💯",
            "Savage jokes incoming! 🎯",
            "TikTok's coolest joke machine 🤖💬"
        ]
        
        import random
        base_caption = random.choice(captions)
        hashtag_string = " ".join(self.hashtags)
        
        return f"{base_caption}\n\n{hashtag_string}"
    
    def schedule_upload(self, video_path: str, caption: str = None, scheduled_time: str = None) -> Dict:
        """
        Schedule a video for upload at a specific time.
        
        Args:
            video_path: Path to the video file
            caption: Optional custom caption
            scheduled_time: ISO format datetime for upload (e.g., "2026-05-16T14:00:00")
        
        Returns:
            Scheduling confirmation
        """
        if not scheduled_time:
            scheduled_time = self.config["upload_schedule"]["upload_time"]
        
        print(f"📅 Scheduling upload for: {scheduled_time}")
        
        return {
            "status": "scheduled",
            "video_path": video_path,
            "scheduled_time": scheduled_time,
            "caption": caption or self._generate_caption()
        }
    
    def batch_upload(self, video_paths: List[str], stagger_hours: int = 24) -> List[Dict]:
        """
        Upload multiple videos with staggered times.
        
        Args:
            video_paths: List of video file paths
            stagger_hours: Hours between each upload
        
        Returns:
            List of upload confirmations
        """
        results = []
        for i, video_path in enumerate(video_paths):
            caption = self._generate_caption()
            result = self.upload_video(video_path, caption)
            results.append(result)
        
        return results
    
    def get_upload_stats(self, video_id: str) -> Dict:
        """Get views, likes, comments, shares for a video."""
        # This would call TikTok Analytics API
        return {
            "video_id": video_id,
            "views": 0,
            "likes": 0,
            "comments": 0,
            "shares": 0,
            "engagement_rate": 0.0
        }

if __name__ == "__main__":
    uploader = TikTokUploader()
    
    # Test caption generation
    print("=== GENERATED CAPTIONS ===")
    for i in range(3):
        print(f"{i+1}. {uploader._generate_caption()}\n")
