import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube, Playlist
from threading import Thread

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Playlist Downloader")
        self.root.geometry("400x300")

        self.link_label = tk.Label(self.root, text="Playlist Link:")
        self.link_label.grid(row=0, column=0, padx=10, pady=10)

        self.link_entry = tk.Entry(self.root, width=40)
        self.link_entry.grid(row=0, column=1, padx=10, pady=10)

        self.destination_label = tk.Label(self.root, text="Destination Folder:")
        self.destination_label.grid(row=1, column=0, padx=10, pady=10)

        self.destination_entry = tk.Entry(self.root, width=30)
        self.destination_entry.grid(row=1, column=1, padx=10, pady=10)

        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_folder)
        self.browse_button.grid(row=1, column=2, padx=10, pady=10)

        self.download_button = tk.Button(self.root, text="Download Playlist", command=self.download_playlist)
        self.download_button.grid(row=2, column=1, padx=10, pady=10)

        self.progress_label = tk.Label(self.root, text="")
        self.progress_label.grid(row=3, column=1, padx=10, pady=10)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.destination_entry.delete(0, tk.END)
            self.destination_entry.insert(0, folder_path)

    def download_playlist(self):
        playlist_link = self.link_entry.get()
        destination = self.destination_entry.get()

        if not playlist_link or not destination:
            messagebox.showerror("Error", "Please enter playlist link and select destination folder.")
            return

        self.progress_label.config(text="Downloading Playlist...")
        self.download_button.config(state="disabled")

        def download_videos():
            try:
                playlist = Playlist(playlist_link)
                for video in playlist.video_urls:
                    yt = YouTube(video)
                    stream = yt.streams.first()
                    stream.download(destination)
                self.progress_label.config(text="Playlist Download Complete!")
            except Exception as e:
                self.progress_label.config(text="Download Failed!")
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.download_button.config(state="normal")

        thread = Thread(target=download_videos)
        thread.start()

def main():
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()
