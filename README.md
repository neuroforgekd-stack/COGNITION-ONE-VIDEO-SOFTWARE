# COGNITION-ONE-VIDEO-SOFTWARE
COGNITION ONE VIDEO SOFTWARE ASSET CODED BY KENNETH MICHAEL DUPUY

## Overview

COGNITION ONE VIDEO SOFTWARE is a comprehensive video processing toolkit that provides:
- **Video Player**: A GUI-based video player with full playback controls
- **Video Info Tool**: A command-line utility to extract and display video file information

## Features

### Video Player (`video_player.py`)
- ✅ Graphical user interface with tkinter
- ✅ Play, pause, and stop controls
- ✅ Video seeking with progress bar
- ✅ Time display (current/total)
- ✅ Support for multiple video formats (MP4, AVI, MOV, MKV, FLV, WMV)
- ✅ Automatic aspect ratio preservation
- ✅ Frame-by-frame control

### Video Info Tool (`video_info.py`)
- ✅ Extract video metadata
- ✅ Display resolution, frame rate, duration
- ✅ Show codec information
- ✅ Command-line interface

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/neuroforgekd-stack/COGNITION-ONE-VIDEO-SOFTWARE.git
cd COGNITION-ONE-VIDEO-SOFTWARE
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Video Player

Launch the GUI video player:
```bash
python video_player.py
```

**Controls:**
- **File > Open Video**: Select a video file to play
- **Play**: Start video playback
- **Pause**: Pause/resume playback
- **Stop**: Stop playback and return to start
- **Progress Bar**: Click or drag to seek to any position

### Video Info Tool

Get information about a video file:
```bash
python video_info.py <path_to_video>
```

**Example:**
```bash
python video_info.py sample_video.mp4
```

**Output:**
```
============================================================
COGNITION ONE VIDEO SOFTWARE - Video Information
============================================================

Filename:     sample_video.mp4
Path:         /path/to/sample_video.mp4
Resolution:   1920x1080
Frame Rate:   30.00 fps
Duration:     02:35 (155.00 seconds)
Total Frames: 4650
Codec:        avc1
============================================================
```

## Supported Video Formats

- MP4 (MPEG-4)
- AVI (Audio Video Interleave)
- MOV (QuickTime)
- MKV (Matroska)
- FLV (Flash Video)
- WMV (Windows Media Video)

## Dependencies

- **opencv-python**: Video processing and frame manipulation
- **numpy**: Numerical operations
- **Pillow**: Image processing for display

See `requirements.txt` for specific version requirements.

## Project Structure

```
COGNITION-ONE-VIDEO-SOFTWARE/
├── video_player.py      # GUI video player application
├── video_info.py        # Command-line video info tool
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore patterns
```

## Architecture

### Video Player Architecture
- **GUI Layer**: Tkinter-based interface with menu, controls, and display
- **Video Processing**: OpenCV for video capture and frame extraction
- **Playback Engine**: Threading-based playback loop for smooth performance
- **Frame Display**: PIL/ImageTk for efficient frame rendering

### Video Info Tool Architecture
- **File Parser**: OpenCV-based metadata extraction
- **Info Processor**: Calculation of derived properties (duration, codec name)
- **Display Formatter**: Clean console output

## Technical Details

- **Frame Rate Control**: Accurate timing based on video FPS
- **Thread Safety**: Daemon threads for non-blocking playback
- **Aspect Ratio**: Automatic preservation during resize
- **Memory Efficient**: Frame-by-frame processing without loading entire video

## Contributing

Contributions are welcome! Please ensure any modifications maintain compatibility with the existing codebase.

## License

COGNITION ONE VIDEO SOFTWARE ASSET CODED BY KENNETH MICHAEL DUPUY

## Author

**Kenneth Michael Dupuy**

## Troubleshooting

### Video won't play
- Ensure the video file format is supported
- Check that all dependencies are installed correctly
- Verify the video file is not corrupted

### GUI doesn't display
- Ensure tkinter is installed (comes with most Python installations)
- On Linux, you may need: `sudo apt-get install python3-tk`

### Poor playback performance
- Try smaller resolution videos
- Close other applications to free up system resources
- Check video codec compatibility

## Future Enhancements

Potential features for future versions:
- Volume control
- Playlist support
- Video editing capabilities
- Additional codec support
- Export/conversion tools
- Subtitle support
