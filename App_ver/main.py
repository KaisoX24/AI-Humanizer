from tkinterdnd2 import TkinterDnD, DND_FILES
from customtkinter import *
from PIL import Image
from tkinter import messagebox,PhotoImage
from tkinter.filedialog import askopenfilenames,askdirectory
import os
from modules.text_extractor import extract_text,extract_text_from_pdf
from modules.humanizer import humanize_content
import threading
from concurrent.futures import ThreadPoolExecutor
# Window configs
app = TkinterDnD.Tk()
app.geometry("1340x900")

icon=PhotoImage(file=r"assets//icon.png")
app.iconphoto(True,icon)
app.title("AI Humanizer")
app.resizable(False, False)
set_appearance_mode("dark")
set_default_color_theme("dark-blue")

# Assets
header_data = Image.open(r"assets//header.png")
body_data = Image.open(r"assets//gradient.png")
header_text_data = Image.open(r"assets//header_txt.png")
info_txt_data = Image.open(r"assets//Text.png")
upload_area_data = Image.open(r"assets//Image.png")
instruction_area_data = Image.open(r"assets//Instructions.png")
button_img_data = Image.open(r"assets//Button.png")
paths_area_data=Image.open(r"assets//paths_area.png")
config_btn_data=Image.open(r"assets//config.png")
humanize_btn_data=Image.open(r"assets//Humanize_btn.png")

# Images
header_img = CTkImage(header_data, size=(1340, 53))
background_img = CTkImage(body_data, size=(1340, 847))
header_txt_img = CTkImage(header_text_data, size=(182, 33))
info_img = CTkImage(info_txt_data, size=(751, 100))
upload_area_img = CTkImage(upload_area_data, size=(917, 417))
instruction_area_img = CTkImage(instruction_area_data, size=(350, 360))
button_img = CTkImage(button_img_data, size=(230, 51))
config_img= CTkImage(config_btn_data,size=(156,29))
humanize_img=CTkImage(humanize_btn_data,size=(156,29))
paths_area_img=CTkImage(paths_area_data,size=(366,170))


# Labels
head_label = CTkLabel(app, image=header_img, text="")
background_label = CTkLabel(app, image=background_img, text="")
header_text_label = CTkLabel(app, image=header_txt_img, text="")
info_label = CTkLabel(app, image=info_img, text="")
upload_area_label = CTkLabel(app, image=upload_area_img, text="")
instruction_area_label = CTkLabel(app, image=instruction_area_img, text="")

file_paths=[]
selected_tone="Casual"
selected_intensity="Medium"

def open_new_window():
    new_window = CTkToplevel(app)
    new_window.title("Configs")
    new_window.geometry("300x200")
    new_window.attributes('-topmost', True)
    new_window.resizable(False, False)

    intensity_maps = {0: "Light", 1: "Medium", 2: "Heavy"}

    def on_tone_change(choice):
        global selected_tone
        selected_tone = choice 

    tones = CTkComboBox(new_window, values=["Casual", "Academic"], command=on_tone_change)
    tones.set("Casual")
    tones.pack(pady=20)

    intensity_label = CTkLabel(new_window, text=f'Intensity: Medium', text_color='#0affff', font=("Helvetica", 14, "bold"))
    intensity_label.pack()

    def on_slider(value):
        global selected_intensity
        step = round(value * 2)
        color_quotes = ['#29f086', '#0affff', '#ff0a0a']
        selected_intensity = intensity_maps.get(step, "Medium")
        intensity_label.configure(text=f'Intensity: {selected_intensity}', text_color=color_quotes[step])

    intensity = CTkSlider(new_window, number_of_steps=2, command=on_slider)
    intensity.pack()
    intensity.set(0.5)

def get_save_directory(event=None) ->str:
    location = None
    while location is None:
        location = askdirectory(
            title="Select Save Location"
        )
        if location:
            return str(location)
        
def forget(event=None) ->None:
    paths_textbox.place_forget()
    config_btn.place_forget()
    humanize_btn.place_forget()

def on_completion() -> None:
    file_paths.clear()
    forget()
    paths_textbox.configure(state='normal')
    paths_textbox.delete("0.0","end")
    paths_textbox.configure(state='disabled')

def process_file(file,directory):
    if file.endswith('.txt'):
        text=extract_text(file)
    else:
        text=extract_text_from_pdf(file)
    humanized_file=humanize_content(text=text,tone=selected_tone,intensity=selected_intensity)   
    file_name = "humanized_" + os.path.splitext(os.path.basename(file))[0] + ".txt"

    with open(file_name,'w',encoding='utf-8')as f:
        f.write(humanized_file)

def humanize_file():
    config_btn.configure(state='disabled')
    humanize_btn.configure(state='disabled')
    if not file_paths:
        return
    
    directory=get_save_directory()
    
    def run():
        with ThreadPoolExecutor(max_workers=min(len(file_paths),os.cpu_count())) as executor:
            executor.map(lambda f: process_file(f,directory),file_paths)
        app.after(0,on_completion)
        app.after(0,lambda:messagebox.showinfo(title="Completed ✅", message="All Files have successfully being Humanized", icon='info'))
        config_btn.configure(state='normal')
        humanize_btn.configure(state='normal')

    threading.Thread(target=run,daemon=True).start()
    
def area_placements():
    refresh_paths_display()
    paths_textbox.place(x=27, y=660)
    config_btn.place(x=420,y=700)
    humanize_btn.place(x=420,y=750)


def get_file_paths(event=None):
    files = None
    while files is None:
        files = askopenfilenames(
            title="Select your files",
            filetypes=[("Text Files", "*.txt"), ("Pdf Files", "*.pdf")]
        )
        if files:
            global file_paths
            file_paths.extend(files)
            file_paths=sorted(set(file_paths))
            area_placements()
            print(file_paths)

def clean_path(raw: str) -> str:
    files = []
    i = 0
    while i < len(raw):
        if raw[i] == '{':                  
            end = raw.index('}', i)        
            path = raw[i+1:end]            
            files.append(path)
            i = end + 1                    
        elif raw[i] == ' ':
            i += 1                         
        else:
            end = raw.find(' ', i)         
            if end == -1:
                end = len(raw)            
            files.append(raw[i:end])
            i = end

    allowed = ('.pdf', '.txt')
    return [f for f in files if f.lower().endswith(allowed)]

def refresh_paths_display() ->None:
    paths_textbox.configure(state="normal")
    paths_textbox.delete("0.0", "end")
    for path in file_paths:
        paths_textbox.insert("end", f"• {os.path.basename(path)}\n")
    paths_textbox.configure(state="disabled")

def on_file_drop(event):
    paths = clean_path(event.data)
    if not paths:
        messagebox.showwarning(title="Alert ⚠️", message="No valid files dropped (only PDF, TXT allowed)", icon='info')
        return
    global file_paths
    file_paths.extend(paths)
    file_paths=sorted(set(file_paths))
    area_placements()
    print(file_paths)

paths_textbox = CTkTextbox(
    app,
    width=366,
    height=170,
    fg_color="#D9E1E2",     
    text_color="#000000",
    font=("Segoe UI", 12),
    wrap="word",
    state="disabled",            
    bg_color="#D9E1E3",
    border_width=2,
    border_color="#C4C6C7",
    corner_radius=22
)

config_btn=CTkButton(
    app,
    image=config_img,
    width=156,
    height=29,
    text="",
    hover=True,
    border_width=0,
    hover_color="#CFE3E6",
    fg_color="transparent",
    bg_color="#E3E9EA",
    command=open_new_window
)

humanize_btn=CTkButton(
    app,
    image=humanize_img,
    width=156,
    height=29,
    text="",
    hover=True,
    border_width=0,
    hover_color="#CFE3E6",
    fg_color="transparent",
    bg_color="#E3E9EA",
    command=humanize_file
)


# Placements
head_label.pack(side="top")
background_label.pack(side="top", fill="both", expand=True)
header_text_label.place(x=33, y=14)
info_label.place(x=27, y=90)
upload_area_label.place(x=27, y=220)
instruction_area_label.place(x=960, y=225)
 

upload_area_label.drop_target_register(DND_FILES)
upload_area_label.dnd_bind("<<Drop>>", on_file_drop)

upload_btn = CTkButton(
    app,
    image=button_img,
    width=230,
    height=51,
    text="",
    hover=True,
    hover_color="#CFE3E6",
    fg_color="transparent",
    bg_color="#D9E1E3",
    command=get_file_paths
)
upload_btn.place(x=380, y=516)

app.mainloop()