import os
import tkinter as tk
from tkinter import filedialog
from pytube import Playlist

# Function to download a YouTube playlist
def download_playlist():
    playlist_url = url_entry.get()
    download_path = path_entry.get()

    if not playlist_url or not download_path:
        update_status("Please enter both URL and download path.", "red")
        return

    playlist = Playlist(playlist_url)
    playlist_title = playlist.title

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    download_folder = os.path.join(download_path, playlist_title)

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for video in playlist.videos:
        try:
            update_status(f"Downloading {video.title}...", "black")
            stream = video.streams.get_highest_resolution()
            stream.download(output_path=download_folder)
            update_status(f"Downloaded {video.title}", "green")
        except Exception as e:
            update_status(f"Error: {str(e)}", "red")

# Function to browse and select a download path
def browse_path():
    folder_selected = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, folder_selected)

# Function to update the status label in the main thread
def update_status(text, color):
    root.after(0, status_label.config, {"text": text, "fg": color})

# Create a Tkinter window
root = tk.Tk()
root.title("YouTube Playlist Downloader")
root.geometry("800x600")

# Create and configure widgets
url_label = tk.Label(root, text="Enter YouTube Playlist URL:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

path_label = tk.Label(root, text="Select Download Path:")
path_label.pack()

path_entry = tk.Entry(root, width=50)
path_entry.pack()

browse_button = tk.Button(root, text="Browse", command=browse_path)
browse_button.pack()

download_button = tk.Button(root, text="Download Playlist", command=download_playlist)
download_button.pack()

status_label = tk.Label(root, text="", fg="black")
status_label.pack()

# Create and configure a navigation bar with margins
navbar = tk.Frame(root)
navbar.pack(anchor="w", padx=5, pady=10)

# Add the text "Savetube" in green color with a custom font
savetube_label = tk.Label(navbar, text="Save", font=("Helvetica", 20, "bold"), fg="green")
savetube_label.pack()

# Start the Tkinter main loop
root.mainloop()
