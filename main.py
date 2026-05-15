#!/usr/bin/env python3
"""Main orchestration script for Savage Joke Bot"""

import os
import sys
import json
import schedule
import time
import argparse
from dotenv import load_dotenv
from datetime import datetime
from loguru import logger

from src.joke_generator import JokeGenerator
from src.activity_selector import ActivitySelector
from src.video_creator import VideoCreator
from src.tiktok_uploader import TikTokUploader


# Configure logging
logger.remove()
logger.add(sys.stderr, format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
logger.add("logs/savage_bot.log", rotation="500 MB", retention="7 days")


class SavageJokeBot:
    """Main bot orchestrator"""

    def __init__(self, config_path: str = "config.json"):
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        with open(config_path, "r") as f:
            self.config = json.load(f)
        
        # Initialize modules
        self.joke_generator = JokeGenerator(self.config)
        self.activity_selector = ActivitySelector(self.config)
        self.video_creator = VideoCreator(self.config)
        self.tiktok_uploader = TikTokUploader(self.config)
        
        logger.info("🤖 Savage Joke Bot initialized successfully!")

    def generate_video(self) -> dict:
        """Generate a complete video"""
        logger.info("📹 Starting video generation...")
        
        # Step 1: Select activity
        activity = self.activity_selector.get_activity()
        logger.info(f"📍 Activity selected: {activity}")
        
        # Step 2: Generate script
        script = self.joke_generator.generate_video_script(activity)
        logger.info(f"📝 Script generated with {len(script['jokes'])} jokes")
        
        # Step 3: Create video
        video_path = self.video_creator.create_video(script)
        logger.info(f"✨ Video created: {video_path}")
        
        # Step 4: Generate caption
        caption = self.tiktok_uploader.generate_caption(script)
        
        return {
            "video_path": video_path,
            "script": script,
            "caption": caption,
            "timestamp": datetime.now().isoformat()
        }

    def upload_video(self, video_data: dict) -> dict:
        """Upload generated video to TikTok"""
        logger.info("🚀 Uploading video to TikTok...")
        
        result = self.tiktok_uploader.upload_video(
            video_path=video_data["video_path"],
            caption=video_data["caption"]
        )
        
        logger.info(f"✅ Upload result: {result}")
        return result

    def run_once(self):
        """Run one generation and upload cycle"""
        logger.info("🎬 Running single video generation...")
        try:
            video_data = self.generate_video()
            upload_result = self.upload_video(video_data)
            logger.info("✅ Single run completed successfully!")
            return True
        except Exception as e:
            logger.error(f"❌ Error in single run: {e}")
            return False

    def run_scheduled(self):
        """Run bot on a schedule"""
        logger.info("⏰ Starting scheduled mode...")
        
        schedule_config = self.config.get("schedule", {})
        upload_time = schedule_config.get("upload_time", "14:00")
        
        # Schedule the job
        schedule.every().day.at(upload_time).do(self.run_once)
        logger.info(f"📅 Scheduled daily uploads at {upload_time}")
        
        # Keep scheduler running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("⛔ Scheduler stopped by user")

    def test(self):
        """Test all components"""
        logger.info("🧪 Running component tests...")
        
        try:
            # Test joke generator
            logger.info("Testing JokeGenerator...")
            jokes = self.joke_generator.generate_jokes(2)
            assert jokes, "Failed to generate jokes"
            logger.info(f"✅ JokeGenerator OK: Generated {len(jokes)} jokes")
            
            # Test activity selector
            logger.info("Testing ActivitySelector...")
            activity = self.activity_selector.get_activity()
            assert activity, "Failed to select activity"
            logger.info(f"✅ ActivitySelector OK: Selected {activity}")
            
            # Test video creator
            logger.info("Testing VideoCreator...")
            test_script = {
                "activity": activity,
                "jokes": jokes,
                "narration": "Test narration"
            }
            video_path = self.video_creator.create_video(test_script)
            assert video_path, "Failed to create video"
            logger.info(f"✅ VideoCreator OK: Video path generated")
            
            # Test TikTok uploader
            logger.info("Testing TikTokUploader...")
            caption = self.tiktok_uploader.generate_caption(test_script)
            assert caption, "Failed to generate caption"
            logger.info(f"✅ TikTokUploader OK: Caption generated")
            
            logger.info("🎉 All tests passed!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Test failed: {e}")
            return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Savage Joke Bot - AI-powered TikTok content generator"
    )
    parser.add_argument(
        "--mode",
        choices=["once", "schedule", "test"],
        default="once",
        help="Run mode (default: once)"
    )
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to config file (default: config.json)"
    )
    
    args = parser.parse_args()
    
    # Create bot instance
    bot = SavageJokeBot(config_path=args.config)
    
    # Run based on mode
    if args.mode == "once":
        success = bot.run_once()
        sys.exit(0 if success else 1)
    elif args.mode == "schedule":
        bot.run_scheduled()
    elif args.mode == "test":
        success = bot.test()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
