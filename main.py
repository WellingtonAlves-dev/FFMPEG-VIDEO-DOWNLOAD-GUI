###
import PySimpleGUI as sg
import os.path
import subprocess
import ptoaster
from threading import Thread
sg.theme("SystemDefault1")

class BaixarVideo(Thread):
    def __init__(self, path_ffmpeg, link_file, name_file, diretorio):
        Thread.__init__(self)
        self.path_ffmpeg = path_ffmpeg
        self.link_file = link_file
        self.name_file = name_file
        self.diretorio = diretorio
    def run(self):
        new_name = self.name_file + ".mp4"
        arquivo_salvar = os.path.join(self.diretorio, new_name)
        ffmpeg = self.path_ffmpeg
        cmd = f'"{ffmpeg}" -i "{self.link_file}" -c copy "{arquivo_salvar}"'
        resultado = subprocess.getstatusoutput(cmd)
        print(resultado)
        if(resultado[0] == 0):
            ptoaster.notify("Sucesso", f"O seu video foi {self.name_file} foi baixado com sucesso")
        else:
            ptoaster.notify("Erro", f"Não foi possivel baixar o video", icon=ptoaster.icon_error)
class Gui:
    def __init__(self, baixarVideo):
        self.path_ffmpeg = ""
        self.link_file = ""
        self.name_file = ""
        self.diretorio = ""
        self.baixarVideo = baixarVideo
        self.main_window()

    def carregar_pastas(self):
        try:
            file_list = os.listdir(self.diretorio)
        except:
            file_list = []
        return file_list
    def main_window(self):
        layout = [[
            sg.Text("Diretorio: ", size=(6, 1)),
            sg.In(size=(25, 1), enable_events=True, justification='center', key="-FOLDER-"),
            sg.FolderBrowse(),
        ], [
            sg.Text("Nome: ", size=(6, 1)),
            sg.InputText(key="-NOME-", size=(25, 1), justification="center")
        ], [
            sg.Text("Link: ", size=(6, 1)),
            sg.InputText(key="-LINK-", size=(25, 1), justification="center")
        ], [
            sg.Text("", size=(6, 1)),
            sg.Button("Baixar", key="baixar", size=(20, 1))
        ], [
            sg.Listbox(key="-ITENS-", values=[], enable_events=True, size=(40, 20))
        ],
            [
                sg.Button("config", key="-CONFIG-", size=(10, 1))
            ]
        ]

        window = sg.Window("Video download", layout)

        while True:
            event, values = window.read()
            file_list = self.carregar_pastas()
            window['-ITENS-'].update(file_list)
            if event == "Exit" or event == sg.WIN_CLOSED:
                break

            elif event == "-FOLDER-":
                self.diretorio = values["-FOLDER-"]
                file_list = self.carregar_pastas()
                window['-ITENS-'].update(file_list)
            elif event == "baixar":
                self.link_file = values["-LINK-"]
                self.name_file = values["-NOME-"]
                ptoaster.notify("Começou", f"O download do {self.name_file} começou")
                video_download = self.baixarVideo(
                    self.path_ffmpeg, self.link_file, self.name_file, self.diretorio)
                video_download.start()
            elif event == "-CONFIG-":
                self.config_window()

    def config_window(self):
        layout = [
            [sg.Text("FFMPEG", size=(8, 1)),
             sg.In(size=(25, 1), enable_events=True, key="-FOLDER_FFMPEG-"),
             sg.FileBrowse(file_types=(("Executavel", "*.exe"),))
             ],
            [
                sg.Text("", size=(6, 2)),
                sg.Button("Confirmar", key="confirmar", size=(20, 1))
            ]
        ]

        window = sg.Window("Configs", layout=layout, modal=True)
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == "confirmar":
                self.path_ffmpeg = values["-FOLDER_FFMPEG-"]
                sg.Popup("ffmpeg caminho: " + self.path_ffmpeg)
                break
        window.close()


if __name__ == "__main__":
    Gui(baixarVideo=BaixarVideo)