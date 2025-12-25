#!/usr/bin/env python3
"""
COGNITION ONE VIDEO SOFTWARE
A simple video player application with playback controls

Author: KENNETH MICHAEL DUPUY
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
from PIL import Image, ImageTk
import threading
import time


class VideoPlayer:
    """Main Video Player class with GUI and playback controls"""
    
    def __init__(self, root):
        """Initialize the video player"""
        self.root = root
        self.root.title("COGNITION ONE VIDEO SOFTWARE")
        self.root.geometry("900x700")
        
        # Video playback variables
        self.video_capture = None
        self.is_playing = False
        self.is_paused = False
        self.current_frame = 0
        self.total_frames = 0
        self.fps = 0
        self.video_path = None
        self.play_thread = None
        
        # Setup GUI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Video", command=self.open_video)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit_application)
        
        # Video display area
        self.video_frame = tk.Frame(self.root, bg="black")
        self.video_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.video_label = tk.Label(self.video_frame, bg="black")
        self.video_label.pack(fill=tk.BOTH, expand=True)
        
        # Control panel
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Playback buttons
        button_frame = tk.Frame(control_frame)
        button_frame.pack(pady=5)
        
        self.play_button = tk.Button(button_frame, text="Play", command=self.play_video, width=10)
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = tk.Button(button_frame, text="Pause", command=self.pause_video, width=10, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_video, width=10, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        progress_frame = tk.Frame(control_frame)
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Scale(progress_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                      variable=self.progress_var, command=self.seek_video)
        self.progress_bar.pack(fill=tk.X, padx=5)
        
        # Status bar
        status_frame = tk.Frame(control_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = tk.Label(status_frame, text="No video loaded", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        self.time_label = tk.Label(status_frame, text="00:00 / 00:00", anchor=tk.E)
        self.time_label.pack(side=tk.RIGHT, padx=5)
        
    def open_video(self):
        """Open a video file"""
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video Files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.load_video(file_path)
            
    def load_video(self, path):
        """Load a video file"""
        try:
            # Stop current video if playing
            if self.is_playing:
                self.stop_video()
                
            # Open video file
            self.video_capture = cv2.VideoCapture(path)
            
            if not self.video_capture.isOpened():
                messagebox.showerror("Error", "Could not open video file")
                return
                
            # Get video properties
            self.video_path = path
            self.total_frames = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.video_capture.get(cv2.CAP_PROP_FPS)
            self.current_frame = 0
            
            # Update UI
            filename = os.path.basename(path)
            self.status_label.config(text=f"Loaded: {filename}")
            self.play_button.config(state=tk.NORMAL)
            
            # Show first frame
            self.show_frame(0)
            
            # Update progress bar
            self.progress_bar.config(to=self.total_frames-1)
            self.update_time_label()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load video: {str(e)}")
            
    def show_frame(self, frame_number):
        """Display a specific frame"""
        if self.video_capture is None:
            return
            
        try:
            # Set frame position
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = self.video_capture.read()
            
            if ret:
                # Convert BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Resize frame to fit display
                display_width = self.video_label.winfo_width()
                display_height = self.video_label.winfo_height()
                
                if display_width > 1 and display_height > 1:
                    # Calculate aspect ratio
                    aspect_ratio = frame.shape[1] / frame.shape[0]
                    
                    if display_width / display_height > aspect_ratio:
                        new_height = display_height
                        new_width = int(new_height * aspect_ratio)
                    else:
                        new_width = display_width
                        new_height = int(new_width / aspect_ratio)
                    
                    frame = cv2.resize(frame, (new_width, new_height))
                
                # Convert to ImageTk format
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Update label
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
                
                self.current_frame = frame_number
                
        except Exception as e:
            print(f"Error showing frame: {e}")
            
    def play_video(self):
        """Start playing the video"""
        if self.video_capture is None:
            messagebox.showwarning("Warning", "Please load a video first")
            return
            
        if not self.is_playing:
            # Wait for previous thread to finish if exists
            if self.play_thread and self.play_thread.is_alive():
                return
                
            self.is_playing = True
            self.is_paused = False
            self.play_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            
            # Start playback thread
            self.play_thread = threading.Thread(target=self.play_loop, daemon=True)
            self.play_thread.start()
            
    def play_loop(self):
        """Main playback loop"""
        while self.is_playing and not self.is_paused:
            if self.current_frame >= self.total_frames - 1:
                # End of video
                self.stop_video()
                break
                
            # Show next frame
            self.show_frame(self.current_frame + 1)
            self.progress_var.set(self.current_frame)
            self.update_time_label()
            
            # Wait based on FPS
            time.sleep(1.0 / self.fps if self.fps > 0 else 0.033)
            
    def pause_video(self):
        """Pause the video"""
        if self.is_playing:
            self.is_paused = not self.is_paused
            
            if self.is_paused:
                self.pause_button.config(text="Resume")
            else:
                self.pause_button.config(text="Pause")
                # Wait for previous thread to finish if exists
                if self.play_thread and self.play_thread.is_alive():
                    return
                # Resume playback
                self.play_thread = threading.Thread(target=self.play_loop, daemon=True)
                self.play_thread.start()
                
    def stop_video(self):
        """Stop the video"""
        self.is_playing = False
        self.is_paused = False
        self.current_frame = 0
        
        if self.video_capture:
            self.show_frame(0)
            
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED, text="Pause")
        self.stop_button.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.update_time_label()
        
    def seek_video(self, value):
        """Seek to a specific position in the video"""
        if self.video_capture is None:
            return
            
        frame_number = int(float(value))
        
        # Only seek if not currently playing (to avoid conflicts)
        if not self.is_playing or self.is_paused:
            self.show_frame(frame_number)
            self.update_time_label()
            
    def update_time_label(self):
        """Update the time display"""
        if self.video_capture is None or self.fps == 0:
            self.time_label.config(text="00:00 / 00:00")
            return
            
        current_seconds = int(self.current_frame / self.fps)
        total_seconds = int(self.total_frames / self.fps)
        
        current_time = f"{current_seconds // 60:02d}:{current_seconds % 60:02d}"
        total_time = f"{total_seconds // 60:02d}:{total_seconds % 60:02d}"
        
        self.time_label.config(text=f"{current_time} / {total_time}")
        
    def quit_application(self):
        """Clean up and quit"""
        self.is_playing = False
        if self.video_capture:
            self.video_capture.release()
        self.root.quit()
        

def main():
    """Main entry point"""
    root = tk.Tk()
    app = VideoPlayer(root)
    root.protocol("WM_DELETE_WINDOW", app.quit_application)
    root.mainloop()


if __name__ == "__main__":
    main()
