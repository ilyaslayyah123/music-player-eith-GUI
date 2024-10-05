import os
import pygame
import tkinter as tk
from tkinter import messagebox, simpledialog

class Node:
    def __init__(self, song_name, song_path):
        self.song_name = song_name
        self.song_path = song_path
        self.next = None

class CircularPlaylist:
    def __init__(self):
        self.head = None
        self.current_song = None
        pygame.mixer.init()

    def add_song(self, song_name, song_path):
        new_node = Node(song_name, song_path)
        if not self.head:
            self.head = new_node
            new_node.next = self.head  
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head
        print(f"Song '{song_name}' added to the playlist.")

    def display_playlist(self):
        if not self.head:
            return "Playlist is empty!"
        songs = []
        temp = self.head
        while True:
            songs.append(temp.song_name)
            temp = temp.next
            if temp == self.head:
                break
        return "Your Playlist:\n" + "\n".join(songs)

    def play_song(self, position):
        if not self.head:
            return "Playlist is empty!"
        temp = self.head
        count = 1
        while count < position:
            temp = temp.next
            count += 1
        self.current_song = temp
        self.play_current_song()
        return f"Now playing: {self.current_song.song_name}"

    def play_current_song(self):
        if self.current_song:
            pygame.mixer.music.load(self.current_song.song_path)  
            pygame.mixer.music.play()  

    def next_song(self):
        if self.current_song is None:
            return "No song is currently playing!"
        self.current_song = self.current_song.next
        self.play_current_song()
        return f"Playing next song: {self.current_song.song_name}"

    def stop_song(self):
        pygame.mixer.music.stop()
        return "Music stopped."

class MusicPlayerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Player")
        self.playlist = CircularPlaylist()

        self.text_area = tk.Text(master, width=40, height=15)
        self.text_area.pack()

        self.add_button = tk.Button(master, text="Add Song", command=self.add_song)
        self.add_button.pack()

        self.play_button = tk.Button(master, text="Play Song", command=self.play_song)
        self.play_button.pack()

        self.next_button = tk.Button(master, text="Next Song", command=self.next_song)
        self.next_button.pack()

        self.stop_button = tk.Button(master, text="Stop Song", command=self.stop_song)
        self.stop_button.pack()

        self.display_button = tk.Button(master, text="Display Playlist", command=self.display_playlist)
        self.display_button.pack()

    def add_song(self):
        song_name = simpledialog.askstring("Input", "Enter the name of the song:")
        song_path = simpledialog.askstring("Input", "Enter the path of the song file:")
        if song_name and song_path:
            self.playlist.add_song(song_name, song_path)
            messagebox.showinfo("Success", f"Song '{song_name}' added to the playlist!")

    def play_song(self):
        position = simpledialog.askinteger("Input", "Enter the position of the song (starting from 1):")
        if position:
            message = self.playlist.play_song(position)
            self.text_area.insert(tk.END, message + "\n")

    def next_song(self):
        message = self.playlist.next_song()
        self.text_area.insert(tk.END, message + "\n")

    def stop_song(self):
        message = self.playlist.stop_song()
        self.text_area.insert(tk.END, message + "\n")

    def display_playlist(self):
        playlist_display = self.playlist.display_playlist()
        self.text_area.insert(tk.END, playlist_display + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()
