from tkinter.filedialog import askdirectory
import customtkinter as tk
from pytube import YouTube
import urllib.request
from PIL import Image
import threading
import pytube



window = tk.CTk()  # Head
window.title("GUITube")
window.wm_iconbitmap("icon.ico")
window.geometry("400x500+500+200")
window.wm_resizable(False, False)
window._set_appearance_mode("light")

print("Message : Program started")

selected_directory = ""
default_thumb_size = (216, 106)


def progress():
    print("download completed")


def open_as_func():
    global selected_directory
    print("Message : Dialog opened")
    ask = askdirectory()
    print(f"Message : Directory opened : {ask}")
    selected_directory = ask


def hide_label():  ### Alert label ###
    Title_Label.configure(text="")


def download_video():  ### Full video function ###
    url = Main_entry.get()
    thread = threading.Thread(target=download_thread, args=(url,))
    thread.start()


def download_audio_only():  ### Audio only function ###
    url = Main_entry.get()
    thread = threading.Thread(target=download_thread_audio_only, args=(url,))
    thread.start()


def download_thread_audio_only(url):  ### Audio only download thread ###
    try:
        yt = YouTube(url)
        Title_Label.configure(text=f"Title: {yt.title[:30]}")
        print("Video = ", yt.title)
        video = yt.streams.get_audio_only()
        video.download(output_path=selected_directory)

    except:
        print("Error : Video not found or user didn't provided the url")
        Title_Label.configure(text="Video not provided / Video not found", text_color="Red")
        window.after(4000, hide_label)


def download_thread(url):  ### Full video download thread ###
    try:
      yt = YouTube(url)
      Title_Label.configure(text=f"Title: {yt.title[:30]}")
      print("Video = ", yt.title)
      video = yt.streams.get_highest_resolution()
      video.download(output_path=selected_directory)
      #yt.register_on_complete_callback(progress)

    except:
     print("Error : Video not found or user didn't provided the url")
     Title_Label.configure(text="Video not provided / Video not found", text_color="red")
     window.after(4000, hide_label)


def check_video():
    try:
        url = Main_entry.get()
        video = pytube.YouTube(url)
        thumb = video.thumbnail_url
        title = video.title
        urllib.request.urlretrieve(thumb, "imgs/thumb2.png")
        newthumb = tk.CTkImage(light_image=Image.open("imgs/thumb2.png  "), size=default_thumb_size)
        thumbail_label.configure(image=newthumb)
        video_title_label.configure(text="Video Title :  " + title[:25])
    except:
        print("Error : Video not found or user didn't provided the url")
        Title_Label.configure(text="Video not provided / Video not found", text_color="red")
        window.after(4000, hide_label)


def process_quit(event):  ### Quit with bind function ###
    window.quit()


window.bind("<Escape>", process_quit)  ### Quit Bind ###


# Images definitions
check_image = tk.CTkImage(light_image=Image.open("imgs/check.png"), size=(20, 20))
youtube_image = tk.CTkImage(light_image=Image.open("imgs/youtube.png"), size=(40, 40))
openas_image = tk.CTkImage(light_image=Image.open("imgs/openas.png"), size=(35, 35))
lines_image = tk.CTkImage(light_image=Image.open("imgs/lines.png"), size=(400, 400))
logo_image = tk.CTkImage(light_image=Image.open("imgs/guitube.png"), size=(200, 200))
download_image = tk.CTkImage(light_image=Image.open("imgs/download.png"), size=(20, 20))
thumbnail = tk.CTkImage(light_image=Image.open("imgs/thumb.png"), size=default_thumb_size)
newthumb = tk.CTkImage(light_image=Image.open("imgs/thumb2.png"), size=default_thumb_size)

Main_frame = tk.CTkFrame(
    master=window,
    height=360,
    width=300,
    border_color="Black"

)
Main_Label = tk.CTkLabel(
    master=window,
    text="",
    image=logo_image
)
Main_Label.configure(font=("Arial Bold", 25))

Main_entry = tk.CTkEntry(
    master=window,
    width=200,
    height=30,
    placeholder_text="Insert YouTube URL",
    bg_color="#DBDBDB",
    border_width=1,
    border_color="Black",
    fg_color="#8e8e8e",
    placeholder_text_color="#Ffffff",
    text_color="#7BFF9A"
)
Main_entry.configure(font=("Arial", 12))

Youtube_label_icon = tk.CTkLabel(
    master=window,
    image=youtube_image,
    text=""
)

open_as_button = tk.CTkButton(
    master=window,
    image=openas_image,
    text="",
    width=0,
    height=0,
    border_width=1,
    command=open_as_func,
    fg_color="#DBDBDB",
    hover_color="#737373"

)

Download_button = tk.CTkButton(
    master=window,
    text="Download \n full video",
    bg_color="#DBDBDB",
    command=download_video,
    text_color="Black",
    fg_color="#FF696D",
    corner_radius=50,
    border_color="Black",
    hover_color="#818181",
    border_width=1,
    image=download_image,
    width=115
)
Download_button.configure(font=("Arial", 10))

Download_audio_only_button = tk.CTkButton(
    master=window,
    text="Download \n Audio only",
    bg_color="#DBDBDB",
    command=download_audio_only,
    text_color="Black",
    hover_color="#818181",
    fg_color="#FF696D",
    corner_radius=50,
    border_color="Black",
    border_width=1,
    image=download_image,
    width=100
)
Download_audio_only_button.configure(font=("Arial", 10))

check_video_btn = tk.CTkButton(
    master=window,
    text="Check Video",
    bg_color="#DBDBDB",
    text_color="Black",
    hover_color="#818181",
    fg_color="#96be25",
    corner_radius=50,
    border_color="#041014",
    border_width=2,
    image=check_image,
    width=100,
    command=check_video)
check_video_btn.configure(font=("Arial", 13))

Title_Label = tk.CTkLabel(
    master=window,
    text="",
    fg_color="#DBDBDB",
    bg_color="#DBDBDB"
)
Title_Label.configure(font=("Arial", 12))

thumbail_label = tk.CTkLabel(
    master=window,
    text="",
    image=thumbnail

)

video_title_label = tk.CTkLabel(
    master=window,
    text="Title : not defined ",
    fg_color="#DBDBDB",
)
video_title_label.configure(font=("Arial bold", 12))

lines_label = tk.CTkLabel(
    master=window,
    image=lines_image,
    text=""
)

Main_frame.pack()
Main_entry.pack()
Youtube_label_icon.pack()
open_as_button.pack()
Download_button.pack()
Download_audio_only_button.pack()
check_video_btn.pack()
thumbail_label.pack()
Title_Label.pack()
video_title_label.pack()
Main_Label.pack()
lines_label.pack()


Main_frame.place(x=50, y=50)
Main_Label.place(x=100, y=-150)
Main_entry.place(x=95, y=100)
Youtube_label_icon.place(x=55, y=95)
open_as_button.place(x=300, y=90)
Download_button.place(x=70, y=350)
Download_audio_only_button.place(x=220, y=350)
check_video_btn.place(x=130, y=140)
thumbail_label.place(x=90, y=190)
Title_Label.place(x=100, y=65)
video_title_label.place(x=90, y=300)
lines_label.place(x=0, y=400)


window.mainloop()
