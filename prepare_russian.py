###
###             Эта сука транскрибирует текст иногда без точки в конце
###             Это надо блять исправить
###

import os
import re
import subprocess
from pytimeparse import parse

audio_file = "audio.wav"        ### Имя файла которое будет обрезано
timecodes_file = "audio.vtt"    ### Имя файла, содержащего таймкоды (можно получить, прописав в терминале -> whisper audio.wav)
output_dir = "output"           ### Имя папки для вывода
output_list = "lists.txt"                   ### Имя файла для вывода

def transcribe():
    subprocess.run(["whisper", "audio.wav"])    ### Транскрибация

    ### Создаём папку для вывода
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ### Ищем строки определённого формата
    def parse_timecodes(text):
        times = re.findall(r"(\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}\.\d{3})", text)
        return [(parse(start), parse(end)) for start, end in times]

    with open(timecodes_file, encoding='utf-8') as f:
        text = f.read()
        
    timecodes = parse_timecodes(text)

    for i, (start, end) in enumerate(timecodes):
        output = f"{output_dir}/audio_{i+1:04}.wav"
        start_str = str(start) 
        end_str = str(end)

        subprocess.call([
            "ffmpeg", "-i", audio_file,
            "-ss", start_str,
            "-to", end_str,
            output
        ])

    if os.path.exists(output_list):
        os.remove(output_list) 

    with open(output_list, "a") as f:

        with open("audio.txt", encoding='utf-8') as transcripts:
            lines = transcripts.readlines()

        for i, (start, end) in enumerate(timecodes):
            audio_path = f"{output_dir}/audio_{i+1:04}.wav"
            f.write(f"{audio_path}|{lines[i].strip()}\n")

    

    print("""
        )         (                  )    )   (         
    ( /(         )\ )            ( /( ( /(   )\ )      
    )\())    (  (()/(   (   (    )\()))\()) (()/( (    
    ((_)\     )\  /(_))  )\  )\  ((_)\((_)\   /(_)))\   
    _((_) _ ((_)(_))   ((_)((_)  _((_) ((_) (_)) ((_)  
    | || || | | ||_ _|  \ \ / /  |_  / / _ \ | _ \| __| 
    | __ || |_| | | |    \ V /    / / | (_) ||  _/| _|  
    |_||_| \___/ |___|    \_/    /___| \___/ |_|  |___| 
    """)

def clear():
    files = ['.json', '.srt', '.tsv', ".txt", ".vtt"]

    for f in files:
        for file in os.listdir():
            if file.endswith(f):
                os.remove(file)

    if os.path.exists(output_dir):
        os.remove(os.path.join('output', f))

    print("[+] Deleted Successfully!")

options = {
    '1': transcribe,
    '2': clear,
    '3': exit
}

### Основной цикл
while True:
    print("""
    
        .__    .__                                             .__ 
__  _  _|  |__ |__| ____________   ___________          _____  |__|
\ \/ \/ /  |  \|  |/  ___/\____ \_/ __ \_  __ \  ______ \__  \ |  |
 \     /|   Y  \  |\___ \ |  |_> >  ___/|  | \/ /_____/  / __ \|  |
  \/\_/ |___|  /__/____  >|   __/ \___  >__|            (____  /__|
             \/        \/ |__|        \/                     \/    
                                    v1.0
          
    [1] Transcribe Audio
    [2] Delete Files
    [3] Exit
    """)

    option = input("Choose an option: ")

    if option in options:
        options[option]()
    else:
        print("Я твою мать ебал, пидор. Введи нормально")










