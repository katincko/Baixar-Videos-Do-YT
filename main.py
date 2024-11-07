import customtkinter
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from pytubefix import YouTube
from pytubefix.cli import on_progress
import urllib.request
from PIL import Image, ImageTk
import os
from io import BytesIO
import threading

# Tema usado no app
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
tema = "dark"

# definições da janela.

root = customtkinter.CTk()

root.geometry("1024x768")
root.title("Downloader de vídeos do YouTube!") 
root.after(201, lambda :root.iconbitmap('C:/Users/RES0072862.EDUCA/OneDrive - Firjan/CURSO/Logica de programação/VisualStudioCode/downloads/icon.ico'))

# Frame da janela
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)


def mudar_tema():
    global tema
    global button_sol
    global button_lua

    if tema == "dark":
        customtkinter.set_appearance_mode("light")
        tema = "light"
        button_lua.place_forget()  # Remove the previous button
        button_sol = customtkinter.CTkButton(
            master=frame, text="", command=mudar_tema, width=10, image=img3)
        button_sol.pack(pady=12, padx=10)
        button_sol.place(
            x=200,
            y=65
        )
    else:
        customtkinter.set_appearance_mode("dark")
        tema = "dark"
        button_sol.place_forget()  # Remove the previous button
        button_lua = customtkinter.CTkButton(
            master=frame, text="", command=mudar_tema, width=10, image=img4)
        button_lua.pack(pady=12, padx=10)
        button_lua.place(
            x=200,
            y=65
        )


# funções de download abaixo.
def buscar():

    # função de download
    def downloadbttn():

        def start_download():

            # baixar video
            try:

                # se for mp3, baixar mp3, se não baixar video
                if my_option.get() == "MP3":

                    # baixar mp3
                    out_file = yt.streams.filter(only_audio=True).first().download(
                        output_path=filedialog.askdirectory())
                    label3.configure(
                        text="DOWNLOAD CONCLUÍDO!", text_color="green")
                    label3.place(
                        x=300,
                        y=270
                    )

                    # RENOMEAR ARQUIVO PARA MP3
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)

                else:
                    # baixar video
                    yt.streams.filter(res=my_option.get()).first().download(
                        output_path=filedialog.askdirectory())
                    label3.configure(text="DOWNLOAD CONCLUÍDO!",
                                     text_color="green")
                    label3.place(
                        x=300,
                        y=270
                    )

            except:
                label3.configure(
                    text="Ocorreu um erro, tente novamente", text_color="red")

        # thread
        thread = threading.Thread(target=start_download)
        thread.start()

    # Função de progresso de download

    def on_progress(stream, chunk, bytes_remaining):

        # Pegar a porcentagem de download
        totalsize = stream.filesize
        bytes_downloaded = totalsize - bytes_remaining
        percentage_completion = bytes_downloaded / totalsize * 100

        # atualiza o label que diz o progresso
        per = str(int(percentage_completion)) + "%"
        pPercentage.configure(text=per)

        if pPercentage.cget("text") == "100%":
            pPercentage.place(x=261)

        # atualiza a barra de progresso
        barra_progresso.set(float(percentage_completion) / 100)

    # SE o usuário falhou, e agora acertou, ele vai tirar o texto de erro.
    if label3.cget("text") == "URL/LINK INVÁLIDO.":
        label3.configure(text="")
        label3.place(
            x=300,
            y=270
        )

    # ESSE try serve pra verificar se a url é válida, se não for, ele vai dar um erro.
    try:

        # declarar a url como variável
        yt = YouTube(entry.get(), on_progress_callback=on_progress)

        if yt == False:
            label3.configure(
                text="Ocorreu um erro, tente novamente", text_color="red")
            label3.place(
                x=300,
                y=270
            )

        # BARRA DE PROGRESSO!!!
        barra_progresso = customtkinter.CTkProgressBar(
            master=frame, width=340, orientation="horizontal")
        barra_progresso.pack(pady=12, padx=10)

        barra_progresso.place(
            x=300,
            y=250
        )
        barra_progresso.set(0)

        # Porcentagem de download
        pPercentage = customtkinter.CTkLabel(
            master=frame, text="0%", font=("roboto bold", 15))
        pPercentage.pack(pady=12, padx=10)
        pPercentage.place(
            x=268,
            y=240
        )

        # TITULO DO VIDEO.

        label = customtkinter.CTkLabel(

            master=frame, text=yt.title, font=("roboto bold", 16))

        label.pack(pady=12, padx=10)

        label.place(

            x=275,
            y=200
        )

        # THUMBNAIL DO VIDEO.
        url_image = yt.thumbnail_url

        response = urllib.request.urlopen(url_image)
        image_data = response.read()

        img = customtkinter.CTkImage(light_image=Image.open(BytesIO(
            image_data)), dark_image=Image.open(BytesIO(image_data)), size=(220, 180))
        label = customtkinter.CTkLabel(master=frame, text="", image=img)
        label.pack(pady=12, padx=10)
        label.place(
            x=40,
            y=130
        )

        # Busca stream da resolução
        mp3 = yt.streams.filter(only_audio=True).first()
        res1080 = yt.streams.filter(res="1080p").first()
        res720 = yt.streams.filter(res="720p").first()
        res480 = yt.streams.filter(res="480p").first()
        res360 = yt.streams.filter(res="360p").first()
        res240 = yt.streams.filter(res="240p").first()
        res144 = yt.streams.filter(res="144p").first()

        # if e else para mudar a resolução e Se nao achar a res é falsa e nao existe
        if mp3 != None:
            mp3 = "MP3"
        else:
            mp3 = "MP3 NAO DISPONÍVEL."

        if res1080 != None:
            res1080 = "1080p"
        else:
            res1080 = "1080p não disponível."

        if res720 != None:
            res720 = "720p"
        else:
            res720 = "720p não disponível."

        if res480 != None:
            res480 = "480p"
        else:
            res480 = "480p não disponível."

        if res360 != None:
            res360 = "360p"
        else:
            res360 = "360p não disponível."

        if res240 != None:
            res240 = "240p"
        else:
            res240 = "240p não disponível."

        if res144 != None:
            res144 = "144p"
        else:
            res144 = "144p não disponível."

        # Opções na caixinha
        opções = [mp3, res1080, res720, res480, res360, res240, res144]
        my_option = customtkinter.CTkOptionMenu(master=frame, values=opções)
        my_option.pack(pady=12, padx=10)
        my_option.place(
            x=662,
            y=198
        )

        # Imagem do botão de download
        imgdownload = "https://i.ibb.co/bsq5qKj/imagem-2024-11-02-230637827.png"

        response_download = urllib.request.urlopen(imgdownload)
        image_data_download = response_download.read()

        img2 = customtkinter.CTkImage(light_image=Image.open(BytesIO(
            image_data_download)), dark_image=Image.open(BytesIO(image_data_download)), size=(25, 25))

        # botão pra chamar a função de download
        button = customtkinter.CTkButton(
            master=frame, text="Download!", command=downloadbttn, image=img2)
        button.pack(pady=12, padx=10)
        button.place(
            x=662,
            y=238
        )
    except:
        label3.configure(
            text="URL/LINK INVÁLIDO.", text_color="red")
        label3.place(
            x=333,
            y=110
        )


# Label, downloader de videos
label = customtkinter.CTkLabel(
    master=frame, text="Downloader de videos", font=("roboto bold", 24))
label.pack(pady=12, padx=10)


# box de colocar link
entry = customtkinter.CTkEntry(
    master=frame, placeholder_text="Link do Video:", width=400)
entry.pack(pady=12, padx=10)

# função de avisar que o download foi feito
label3 = customtkinter.CTkLabel(
    master=frame, text="", font=("roboto bold", 24))
label3.pack(pady=12, padx=10)


# Buscar
button = customtkinter.CTkButton(master=frame, text="BUSCAR", command=buscar)
button.pack(pady=12, padx=10)
button.place(
    x=662,
    y=65
)

# LUA
img_theme2 = "https://i.ibb.co/WGvwND5/imagem-2024-11-02-232939527.png"

response_theme2 = urllib.request.urlopen(img_theme2)
image_data_theme2 = response_theme2.read()

img4 = customtkinter.CTkImage(light_image=Image.open(BytesIO(
    image_data_theme2)), dark_image=Image.open(BytesIO(image_data_theme2)), size=(25, 25))


# SOL
img_theme = "https://i.ibb.co/4pgG4rK/imagem-2024-11-02-232759452.png"

response_theme = urllib.request.urlopen(img_theme)
image_data_theme = response_theme.read()

img3 = customtkinter.CTkImage(light_image=Image.open(BytesIO(
    image_data_theme)), dark_image=Image.open(BytesIO(image_data_theme)), size=(25, 25))

# botão pra mudar tema
# Declare and initialize the button_lua variable before using it
button_lua = customtkinter.CTkButton(
    master=frame, text="", command=mudar_tema, width=10, image=img4)
button_lua.pack(pady=12, padx=10)
button_lua.place(
    x=200,
    y=65
)


# fazer loop
root.mainloop()