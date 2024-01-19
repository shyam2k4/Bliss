import pyglet,os
import pickle
import customtkinter as c
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer
from PIL import Image
from tkinter.font import Font

pyglet.font.add_file('RC.ttf')

class Player(c.CTkFrame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.configure(fg_color='#DD4DB3')
		self.pack()
		mixer.init()
		if os.path.exists('songs.pickle'):
			with open('songs.pickle', 'rb') as f:
				self.playlist = pickle.load(f)
		else:
			self.playlist=[]

		self.current = 0
		self.paused = True
		self.played = False

		self.create_frames()
		self.track_widgets()
		self.control_widgets()
		self.tracklist_widgets()

	def create_frames(self):
		self.track = tk.LabelFrame(self, text='Song Track', 
					font=("Upheaval TT (BRK)",15,"bold"),
					bg="#B43C91",fg="white",bd=5,relief='flat')
		self.track.config(width=410,height=300)
		self.track.grid(row=0, column=0, padx=10,pady=5)

		self.tracklist = tk.LabelFrame(self, text=f'PlayList - {str(len(self.playlist))}',
							font=("Upheaval TT (BRK)",15,"bold"),
							bg="#B43C91",fg="white",bd=5,relief='flat')
		self.tracklist.config(width=190,height=400)
		self.tracklist.grid(row=0, column=1, rowspan=3, pady=5)

		self.controls = tk.LabelFrame(self,
							font=("Upheaval TT (BRK)",15,"bold"),
							bg="#B43C91",fg="white",bd=2,relief='flat')
		self.controls.config(width=410,height=80,background='#B43C91')
		self.controls.grid(row=2, column=0, pady=5, padx=10)

	def track_widgets(self):
		self.canvas = c.CTkLabel(self.track, image=img,text='',corner_radius=100)
		self.canvas.configure(width=400, height=240)
		self.canvas.grid(row=0,column=0)

		self.songtrack = c.CTkLabel(self.track, font=("Upheaval TT (BRK)",25,"bold"),
						text_color='white',fg_color="#B43C91",text='Bliss'+'™')
		self.songtrack.configure(width=30, height=1)
		self.songtrack.grid(row=1,column=0,padx=10)

	def control_widgets(self):
		self.loadSongs = c.CTkButton(self.controls, fg_color='#DD4DB3',bg_color='#B43C91',text_color='white',hover=False,text='Load Songs',font=("Retro Computer",10),command=self.retrieve_songs)
		self.loadSongs.grid(row=0, column=0, padx=10)

		self.prev = c.CTkButton(self.controls, image=prev,hover=False,fg_color="#B43C91",text="",height=0,width=0,command=self.prev_song)
		self.prev.grid(row=0, column=1)

		self.pause = c.CTkButton(self.controls, image=play,hover=False,fg_color="#B43C91",text="",height=0,width=0,command=self.pause_song)
		self.pause.grid(row=0, column=2)

		self.next = c.CTkButton(self.controls, image=next_,hover=False,fg_color="#B43C91",text="",height=0,width=0,command=self.next_song)
		self.next.grid(row=0, column=3)

		self.volume = tk.DoubleVar(self)
		self.slider = c.CTkSlider(self.controls,fg_color='#B43C91', from_ = 0, to = 10, orientation = 'horizontal',variable=self.volume,command=self.change_volume,button_color='#EF60C6',progress_color='#8F216E',width=100,hover=False)
		self.slider.set(8)
		mixer.music.set_volume(0.8)
		self.slider.grid(row=0, column=4, padx=5)


	def tracklist_widgets(self):
		self.scrollbar = c.CTkScrollbar(self.tracklist, orientation='vertical',fg_color='#B43C91',button_color='#8F216E',hover=False,corner_radius=50)
		self.scrollbar.grid(row=0,column=1, rowspan=5, sticky='ns')

		self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE, yscrollcommand=self.scrollbar.set,bg="#00177D",fg='#9A13CD',selectbackground='#9A13CD',selectforeground='#00177D',relief='flat',borderwidth=0,highlightthickness=0)
		self.enumerate_songs()
		self.list.config(height=23)
		self.list.bind('<Double-1>', self.play_song) 

		self.scrollbar.configure(command=self.list.yview)
		self.list.grid(row=0, column=0, rowspan=5)

	def retrieve_songs(self):
		self.songlist = []
		directory = filedialog.askdirectory()
		for root_, dirs, files in os.walk(directory):
				for file in files:
					if os.path.splitext(file)[1] == '.mp3':
						path = (root_ + '/' + file).replace('\\','/')
						self.songlist.append(path)

		with open('songs.pickle', 'wb') as f:
			pickle.dump(self.songlist, f)
		self.playlist = self.songlist
		self.tracklist['text'] = f'PlayList - {str(len(self.playlist))}'
		self.list.delete(0, tk.END)
		self.enumerate_songs()

	def enumerate_songs(self):
		for index, song in enumerate(self.playlist):
			self.list.insert(index, os.path.basename(song))


	def play_song(self, event=None):
		if event is not None:
			self.current = self.list.curselection()[0]
			for i in range(len(self.playlist)):
				self.list.itemconfigure(i, bg="white")

		print(self.playlist[self.current])
		mixer.music.load(self.playlist[self.current])
		self.songtrack.configure(anchor='w',text="NOW PLAYING - "+os.path.basename(self.playlist[self.current])[:-4],font=("Upheaval TT (BRK)",20))

		self.pause.configure(image=pause)
		self.paused = False
		self.played = True
		self.list.activate(self.current) 
		self.list.itemconfigure(self.current)

		mixer.music.play()

	def pause_song(self):
		if not self.paused:
			self.paused = True
			mixer.music.pause()
			self.pause.configure(image=play)
		else:
			if self.played == False:
				self.play_song()
			self.paused = False
			mixer.music.unpause()
			self.pause.configure(image=pause)

	def prev_song(self):
		if self.current > 0:
			self.current -= 1
			self.list.itemconfigure(self.current + 1)
		elif self.current==0:
			self.current=len(self.playlist)-1
			self.list.itemconfigure(self.current)
		else:
			self.current = 0
			self.list.itemconfigure(self.current + 1)
		self.play_song()

	def next_song(self):
		if self.current < len(self.playlist) - 1:
			self.current += 1
			self.list.itemconfigure(self.current - 1)
		elif self.current==len(self.playlist)-1:
			self.current = 0
			self.list.itemconfigure(self.current)
		else:
			pass
		self.play_song()

	def change_volume(self, event=None):
		self.v = self.volume.get()
		mixer.music.set_volume(self.v / 10)

# ----------------------------- Main -------------------------------------------

root = tk.Tk()
root.geometry('730x400')
root.title('Bliss')
root.iconbitmap("bliss.ico")
root.config(background="#DD4DB3")
root.option_add('*Font',('Retro Computer',8))
root.resizable(0,0)

img = c.CTkImage(dark_image=Image.open(r'music.png'),size=(400,240))
next_ =c.CTkImage(dark_image=Image.open(r'next.png'),size=(50,50))
prev = c.CTkImage(dark_image=Image.open(r'prev.png'),size=(50,50))
play = c.CTkImage(dark_image=Image.open(r'play.png'),size=(50,50))
pause = c.CTkImage(dark_image=Image.open(r'pause.png'),size=(50,50))

app = Player(master=root)
app.mainloop()