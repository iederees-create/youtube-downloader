import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
from yt_dlp import YoutubeDL
import threading

class YoutubeDownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Video Downloader")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        """
        Create all the widgets for the application window.
        """
        # Main frame for padding
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # URL Input
        url_label = tk.Label(main_frame, text="YouTube Video URL:")
        url_label.pack(pady=(0, 5), anchor="w")

        self.url_entry = tk.Entry(main_frame, width=80)
        self.url_entry.pack(fill=tk.X, pady=(0, 10))

        # Save Directory Input
        path_frame = tk.Frame(main_frame)
        path_frame.pack(fill=tk.X)

        path_label = tk.Label(path_frame, text="Save Directory:")
        path_label.pack(side=tk.LEFT, pady=(0, 5))

        self.path_entry = tk.Entry(path_frame, width=60)
        self.path_entry.insert(0, "/home/iedrees/Desktop/iederees tiktok/deriv") # Default Linux path
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        browse_button = tk.Button(path_frame, text="Browse", command=self.browse_path)
        browse_button.pack(side=tk.RIGHT)

        # Download Button
        self.download_button = tk.Button(main_frame, text="Download Video", command=self.start_download_thread)
        self.download_button.pack(fill=tk.X, pady=10)

        # Status Log
        status_label = tk.Label(main_frame, text="Status Log:")
        status_label.pack(pady=(10, 5), anchor="w")

        self.status_log = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=10)
        self.status_log.pack(fill=tk.BOTH, expand=True)
        self.status_log.config(state=tk.DISABLED) # Make log read-only

    def browse_path(self):
        """
        Open a file dialog to select the download directory.
        """
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, selected_dir)

    def log_message(self, message):
        """
        Insert a message into the status log widget.
        """
        self.status_log.config(state=tk.NORMAL)
        self.status_log.insert(tk.END, message + "\n")
        self.status_log.see(tk.END) # Auto-scroll to the bottom
        self.status_log.config(state=tk.DISABLED)

    def download_hook(self, d):
        """
        Hook function to update the GUI with download progress.
        """
        if d['status'] == 'downloading':
            p_str = d['_percent_str']
            self.log_message(f"Downloading: {p_str}")
        if d['status'] == 'finished':
            filename = d['filename']
            self.log_message(f"Finished downloading: {filename}")

    def download_video(self):
        """
        Main function to handle the video download logic.
        This function runs in a separate thread.
        """
        url = self.url_entry.get()
        save_dir = self.path_entry.get()

        if not url:
            self.log_message("Error: Please enter a YouTube video URL.")
            return

        if not save_dir:
            self.log_message("Error: Please enter a save directory.")
            return

        # Disable the download button to prevent multiple clicks
        self.download_button.config(state=tk.DISABLED)
        self.log_message(f"Starting download for: {url}")
        self.log_message(f"Saving to: {save_dir}")

        # Create the directory if it doesn't exist
        if not os.path.exists(save_dir):
            try:
                os.makedirs(save_dir)
            except OSError as e:
                self.log_message(f"Error creating directory: {e}")
                self.download_button.config(state=tk.NORMAL)
                return

        # Configure yt-dlp options
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(save_dir, '%(title)s.%(ext)s'),
            'progress_hooks': [self.download_hook], # Use the hook for progress updates
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            self.log_message(f"An error occurred: {e}")
        finally:
            self.log_message("Download process finished.")
            self.download_button.config(state=tk.NORMAL)

    def start_download_thread(self):
        """
        Start the download process in a new thread to keep the GUI responsive.
        """
        download_thread = threading.Thread(target=self.download_video, daemon=True)
        download_thread.start()

if __name__ == "__main__":
    app = YoutubeDownloaderApp()
    app.mainloop()
