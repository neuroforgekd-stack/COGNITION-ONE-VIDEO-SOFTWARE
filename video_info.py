#!/usr/bin/env python3
"""
COGNITION ONE VIDEO SOFTWARE - Video Information Tool
Extract and display information about video files

Author: KENNETH MICHAEL DUPUY
"""

import cv2
import sys
import os


def get_video_info(video_path):
    """Get detailed information about a video file"""
    
    if not os.path.exists(video_path):
        print(f"Error: File '{video_path}' does not exist")
        return None
        
    try:
        video = cv2.VideoCapture(video_path)
        
        if not video.isOpened():
            print(f"Error: Could not open video file '{video_path}'")
            return None
            
        # Extract video properties
        info = {
            'filename': os.path.basename(video_path),
            'path': os.path.abspath(video_path),
            'frame_count': int(video.get(cv2.CAP_PROP_FRAME_COUNT)),
            'fps': video.get(cv2.CAP_PROP_FPS),
            'width': int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'codec': int(video.get(cv2.CAP_PROP_FOURCC))
        }
        
        # Calculate duration
        if info['fps'] > 0:
            duration_seconds = info['frame_count'] / info['fps']
            info['duration'] = f"{int(duration_seconds // 60):02d}:{int(duration_seconds % 60):02d}"
            info['duration_seconds'] = duration_seconds
        else:
            info['duration'] = "Unknown"
            info['duration_seconds'] = 0
            
        # Decode codec
        codec_int = info['codec']
        try:
            codec_str = "".join([chr((codec_int >> 8 * i) & 0xFF) for i in range(4)])
            # Filter non-printable characters
            codec_str = ''.join(c if c.isprintable() else '?' for c in codec_str)
            info['codec_name'] = codec_str if codec_str.strip() else "Unknown"
        except (ValueError, OverflowError):
            info['codec_name'] = "Unknown"
        
        video.release()
        return info
        
    except Exception as e:
        print(f"Error processing video: {e}")
        return None


def display_video_info(info):
    """Display video information in a formatted way"""
    print("\n" + "="*60)
    print("COGNITION ONE VIDEO SOFTWARE - Video Information")
    print("="*60)
    print(f"\nFilename:     {info['filename']}")
    print(f"Path:         {info['path']}")
    print(f"Resolution:   {info['width']}x{info['height']}")
    print(f"Frame Rate:   {info['fps']:.2f} fps")
    print(f"Duration:     {info['duration']} ({info['duration_seconds']:.2f} seconds)")
    print(f"Total Frames: {info['frame_count']}")
    print(f"Codec:        {info['codec_name']}")
    print("="*60 + "\n")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python video_info.py <video_file>")
        print("\nExample:")
        print("  python video_info.py my_video.mp4")
        sys.exit(1)
        
    video_path = sys.argv[1]
    info = get_video_info(video_path)
    
    if info:
        display_video_info(info)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
