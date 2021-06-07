import os
import pickle                       # use to save a list / dictionary
import tkinter as tk
from tkinter import filedialog       # open window - like 'Browse' and select folder for songs
from tkinter import PhotoImage         # for mp3 player images
from pygame import mixer              # functions for player, play the music play_song()


class Player(tk.Frame):                 # tk.Frame - root window as Tk()
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		mixer.init()    # initialize 'mixer' 
		
		# pickle - if player is closed and open it will display previous folder which was opened, not an empty folder.
		if os.path.exists('songs.pickle'):
			with open('songs.pickle', 'rb') as f:    # if the file exists, read the songlist pickle file
				self.playlist = pickle.load(f)
		else:
			self.playlist=[]        # else empty 'playlist' for music

		self.current = 0      # value of current playing song
		self.paused = True    # when player/app is opened song is paused so its True 
		self.played = False   # and played is False

        # call the functions created below in main __init__() function.
		self.create_frames()
		self.track_widgets()
		self.control_widgets()
		self.tracklist_widgets()

		self.master.bind('<Left>', self.prev_song)
		self.master.bind('<space>', self.play_pause_song)
		self.master.bind('<Right>', self.next_song)

    # 1st function -to Create 3 frames in player : 1.media plays, 2.playlist, 3.buttons , then 3 more functions for these 3 frames created
    # when create function in class 1st argument is 'self' what is initialize above in __init__() , 'self' is master window
	def create_frames(self):
        # 1.media plays frame
		self.track = tk.LabelFrame(self, text='Track Player', font=("times new roman",15,"bold"), bg="grey", fg="white", bd=5, relief=tk.GROOVE)
		self.track.config(width=410,height=300)
		self.track.grid(row=0, column=0, padx=10)   # grid() -this will set the frames in position
        # 2.playlist frame
		self.tracklist = tk.LabelFrame(self, text=f'PlayList - {str(len(self.playlist))}', font=("times new roman",15,"bold"), bg="grey", fg="white", bd=5, relief=tk.GROOVE)
		self.tracklist.config(width=190,height=400)
		self.tracklist.grid(row=0, column=1, rowspan=3, pady=5)
        # 3.buttons / controls
		self.controls = tk.LabelFrame(self,	font=("times new roman",15,"bold"), bg="white", fg="white", bd=2, relief=tk.GROOVE)
		self.controls.config(width=410,height=80)
		self.controls.grid(row=2, column=0, pady=5, padx=10)

    # function for the '1.media plays frame'
	def track_widgets(self):
		self.canvas = tk.Label(self.track, image=img)    # self.track - parent frame 'media plays frame', display image in label
		self.canvas.configure(width=400, height=240)
		self.canvas.grid(row=0,column=0)

		self.songtrack = tk.Label(self.track, font=("times new roman",16,"bold"), bg="white", fg="dark blue")
		self.songtrack['text'] = 'Media Player'
		self.songtrack.config(width=30, height=1)
		self.songtrack.grid(row=1,column=0,padx=10)

    # function for the '2.playlist frame' , It has list of songs and scrollbar
	def tracklist_widgets(self):
		self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)  # self.tracklist - parent frame is playlist frame
		self.scrollbar.grid(row=0,column=1, rowspan=5, sticky='ns')
		# selectmode=tk.SINGLE - select/play single song at one time and make bg='sky blue'
		self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE, yscrollcommand=self.scrollbar.set, selectbackground='sky blue')
		self.enumerate_songs()          # enumerate_songs()
		self.list.config(height=22)
		self.list.bind('<Double-1>', self.play_song)    # when 'double click' on song 'play the song'

		self.scrollbar.config(command=self.list.yview)   # yview
		self.list.grid(row=0, column=0, rowspan=5)

    # function for the '3.buttons / controls frame', also created here 'Buttons' and functions for buttons created below
	def control_widgets(self):
		self.loadSongs = tk.Button(self.controls, bg='green', fg='white', font=10)
		self.loadSongs['text'] = 'Load Songs'
		self.loadSongs['command'] = self.retrieve_songs        # to bind functions use ['command'] - retrieve_songs()
		self.loadSongs.grid(row=0, column=0, padx=10)

		self.prev = tk.Button(self.controls, image=prev)
		self.prev['command'] = self.prev_song                  # bind function- prev_song()
		self.prev.grid(row=0, column=1)

		self.pause = tk.Button(self.controls, image=pause)
		self.pause['command'] = self.pause_song                # bind function- pause_song()
		self.pause.grid(row=0, column=2)

		self.next = tk.Button(self.controls, image=next_)
		self.next['command'] = self.next_song
		self.next.grid(row=0, column=3)

		# volume
		self.volume = tk.DoubleVar(self)     # DoubleVar() -store float values  # tk.BooleanVar, tk.StringVar, tk.IntVar
		self.slider = tk.Scale(self.controls, from_ = 0, to = 10, orient = tk.HORIZONTAL)   # Scale() -create slider
		self.slider['variable'] = self.volume     # bind 'volume' var with 'slider'
		self.slider.set(8)                        # 8 - default value, and set() will set the volume.
		mixer.music.set_volume(0.8)               # set_volume(), in mixer music value is from '0 to 1' i.e. using 0.8
		self.slider['command'] = self.change_volume    # here bind- change_volume()
		self.slider.grid(row=0, column=4, padx=5)

	# open window - liek 'Browse' to select folder for songs
	def retrieve_songs(self):
		self.songlist = []
		directory = filedialog.askdirectory()       # askopenfilename()
		for root_, dirs, files in os.walk(directory):
				for file in files:
					if os.path.splitext(file)[1] == '.mp3':
						path = (root_ + '/' + file).replace('\\','/')
						self.songlist.append(path)

		# pickle - if player is closed and open it will display previous folder which was opened, not an empty folder.
		with open('songs.pickle', 'wb') as f:
			pickle.dump(self.songlist, f)       # dump / write the songs name in file
		self.playlist = self.songlist
		self.tracklist['text'] = f'PlayList - {str(len(self.playlist))}'     # text on 'Playlist' and total no. of songs
		self.list.delete(0, tk.END)    # delete earlier list of songs
		self.enumerate_songs()         # then this will display current list of songs which selected

	# put all the songs name in playlist box
	def enumerate_songs(self):
		for index, song in enumerate(self.playlist):           # index - is no. , song - path directory of song
			self.list.insert(index, os.path.basename(song))    # use insert() , basename -give value which is song name

	def play_pause_song(self, event):
		if self.paused:
			self.play_song()
		else:
			self.pause_song()

	def play_song(self, event=None):
		if event is not None:                              # event not None - means double click on song
			self.current = self.list.curselection()[0]     # find the index of song in list
			for i in range(len(self.playlist)):
				self.list.itemconfigure(i, bg="white")    # when double click on song it will play and previous playing song which bg='blue' turns to bg='white'

		print(self.playlist[self.current])
		mixer.music.load(self.playlist[self.current])    # load the current song name below mp3 frame player
		self.songtrack['anchor'] = 'w' 
		self.songtrack['text'] = os.path.basename(self.playlist[self.current])

		self.pause['image'] = play    # changes image when double click on song and it will 'play'
		self.paused = False           # making the pause - False , which initially True
		self.played = True            # and play - True
		self.list.activate(self.current)    # play song which 'double clicked'
		self.list.itemconfigure(self.current, bg='sky blue')

		mixer.music.play()    # mixer - play the music

	def pause_song(self):
		if not self.paused:             # song is paused
			self.paused = True
			mixer.music.pause()
			self.pause['image'] = pause
		else:
			if self.played == False:       # song is played
				self.play_song()
			self.paused = False
			mixer.music.unpause()
			self.pause['image'] = play

	def prev_song(self, event=None):
		self.master.focus_set()
		if self.current > 0:           # if value greater than 0 then decrease 
			self.current -= 1
		else:
			self.current = 0           # else 0 , it can not decrease
		self.list.itemconfigure(self.current + 1, bg='white')   # change bg color 'white' of previous song
		self.play_song()                                        # and play the current song

	def next_song(self, event=None):
		self.master.focus_set()
		if self.current < len(self.playlist) - 1:     # press 'next' button until 'len of playlist - 1'
			self.current += 1
		else:
			self.current = 0                                         # current song index 0
		self.list.itemconfigure(self.current - 1, bg='white')
		self.play_song()

	def change_volume(self, event=None):
		self.v = self.volume.get()
		mixer.music.set_volume(self.v / 10)   # 10 bcoz we using volume scale '0 to 10' above , if scale 100 then divide by 100


# ----------------------------- Main -------------------------------------------

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('600x400')
	root.title('Media Player')

	img = PhotoImage(file='icons/music.gif')
	next_ = PhotoImage(file = 'icons/next.gif')
	prev = PhotoImage(file='icons/previous.gif')
	play = PhotoImage(file='icons/play.gif')
	pause = PhotoImage(file='icons/pause.gif')

	app = Player(master=root)
	app.mainloop()


# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# from tkinter.ttk import *   # for progressbar
# from tkinter import * 
# import time


# window = Tk()

# percent = StringVar()    # this allows to update % with some new text

# bar = Progressbar(window, orient=HORIZONTAL, length=200)
# bar.pack(pady=10)

# percentlabel = Label(window, textvariable=percent).pack()   # textvariable - so we update this label with text / %




# # --------------------------------------------
# # Length of music
# from mutagen.mp3 import MP3
# import time 

# def length_bar():
#     # Current song length
#     current_time = mixer.music.get_pos() / 1000    # get the current time of playing song in sec.
#     convert_current_time = time.strftime('%M:%S', time.gmtime(current_time))

#     # song length
#     song_mut = MP3(filename)    # filename - selelct mp3 song
#     song_mut_length = song_mut.info.length    # length of song in sec. float
#     convert_song_mut_length = time.strftime('%M:%S', time.gmtime(song_mut_length))    # in "min : sec""

#     # display song {current length : total length}
#     self.lengthbar.config(text=f"Total Length : {convert_current_time} : {convert_song_mut_length}")  # get the both length and display
#     self.lengthbar.after(1000, length_bar)    # 1000 - function call per sec., length_bar() -is function


# # display
# self.lengthbar = Label(self.root, text="Total Length:00:00", font=10, bg='grey', fg='white')
# self.lengthbar.palce(x=5, y=270)



# # --------------------------------------------
# # progressbar
# import datetime
# from mutagen.mp3 import MP3

# totalsonglength = 0

# # inside the play music function
# Song = MP3(ad)    # ad -filepath var.
# totalsonglength = int(Song.info.length)
# ProgressbarMusic['maximum'] = totalsonglength
# ProgressbarMusicEndTimeLabel.configure(text='{}'.format(str(datetime.timedelta(seconds=totalsonglength))))    # convert into sec.
# def Progresbarmusictick():
#     CurrenSongLength = mixer.music.get_pos()//1000    # get the current time of playing song in sec.
#     ProgressbarMusic['value'] = CurrenSongLength      # 
#     ProgressbarMusicStartTimeLabel.configure(text='{}'.format(str(datetime.timedelta(seconds=CurrenSongLength))))
#     ProgressbarMusic.after(2, Progresbarmusictick)    # after every 2 mili sec. call the function Progresbarmusictick()
# Progresbarmusictick()





#     ProgressbarMusicLabel = Label(root,text='',bg='red')
#     ProgressbarMusicLabel.grid(row=3,column=0,columnspan=3,padx=20,pady=20)
#     ProgressbarMusicLabel.grid_remove()

#     ProgressbarMusicStartTimeLabel = Label(ProgressbarMusicLabel, text='0:00:0', bg='red',width=6)
#     ProgressbarMusicStartTimeLabel.grid(row=0, column=0)

#     ProgressbarMusic = Progressbar(ProgressbarMusicLabel,orient=HORIZONTAL,mode='determinate',value=0)
#     ProgressbarMusic.grid(row=0,column=1,ipadx=370,ipady=3)

#     ProgressbarMusicEndTimeLabel = Label(ProgressbarMusicLabel,text='0:00:0', bg='red')
#     ProgressbarMusicEndTimeLabel.grid(row=0, column=2)




# https://github.com/rahulmis/MusicPlayerUsingPython/blob/master/simplemusicplayer.py
