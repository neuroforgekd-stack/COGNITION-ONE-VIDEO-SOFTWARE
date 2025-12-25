#!/usr/bin/env python3
"""
Unit tests for COGNITION ONE VIDEO SOFTWARE
Tests basic functionality without requiring actual video files
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_info import get_video_info


class TestVideoInfo(unittest.TestCase):
    """Test cases for video_info module"""
    
    def test_nonexistent_file(self):
        """Test that non-existent file returns None"""
        result = get_video_info("nonexistent_file.mp4")
        self.assertIsNone(result)
        
    def test_invalid_file(self):
        """Test that invalid file returns None"""
        # Create a temporary non-video file
        test_file = "/tmp/test_invalid.txt"
        with open(test_file, "w") as f:
            f.write("This is not a video file")
        
        result = get_video_info(test_file)
        self.assertIsNone(result)
        
        # Clean up
        os.remove(test_file)


class TestVideoPlayer(unittest.TestCase):
    """Test cases for video_player module"""
    
    def test_import(self):
        """Test that video_player can be imported"""
        try:
            import video_player
            self.assertTrue(hasattr(video_player, 'VideoPlayer'))
            self.assertTrue(hasattr(video_player, 'main'))
        except ImportError as e:
            self.fail(f"Failed to import video_player: {e}")
            

if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
