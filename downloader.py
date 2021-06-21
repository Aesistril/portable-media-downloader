from pytube import YouTube
from urllib.request import urlretrieve
import PySimpleGUI as psg
import multiprocessing

psg.LOOK_AND_FEEL_TABLE['Dark_Minimalist'] = {'BACKGROUND': '#212324', 
                                        'TEXT': '#FFFFFF', 
                                        'INPUT': '#454545', 
                                        'TEXT_INPUT': '#FFFFFF', 
                                        'SCROLL': '#FFFFFF', 
                                        'BUTTON': ('#FFFFFF', '#454545'), 
                                        'PROGRESS': ('#FFFFFF', '#FFFFFF'), 
                                        'BORDER': 0, 'SLIDER_DEPTH': 0,  
                                        'PROGRESS_DEPTH': 0} 
psg.theme('Dark_Minimalist')

mainMenu =   [  [psg.Button('', visible=False, disabled=True), psg.Text('Ne indircen')],
                [psg.Button('Oynatma Listesi', key='SelList'), psg.Button('Video', key='SelVid')]  ]

listLayout =  [ [psg.Button('', visible=False, disabled=True), psg.Button('<', key='backToMenu')], 
                [psg.Text("Link: "), psg.InputText(key='psg-listlink')],
                [psg.Button(button_text='İndir', key='list-Down')]  ]

vidLayout  =  [ [psg.Button('', visible=False, disabled=True), psg.Button('<', key='backToMenu')],
                [psg.Text("Link: "), psg.InputText(key='psg-vidlink')],
                [psg.Button(button_text='İndir', key='vid-Down')],
                [psg.Text(key='VL-Title')],
                [psg.Image(key='VL-Thumbnail')]  ]

layout = [  [psg.Column(listLayout, key='listLayout', visible=False), psg.Column(vidLayout, key='vidLayout', visible=False), psg.Column(mainMenu, key='mainMenu')]  ]

window = psg.Window('Youtube Downloader', layout)

def vidDownloader(url):
        print(url + ' [Work in progress]')

def listDownloader(url):
        print(url + ' [Work in progress]')

while True:
    event, values = window.read()
    print(str(event) + '           ' + str(values))
    if event == psg.WIN_CLOSED or event == 'Cancel':
        break
    if event == 'SelList':
        window['mainMenu'].update(visible=False)
        window['listLayout'].update(visible=True)
    if event == 'SelVid':
        window['mainMenu'].update(visible=False)
        window['vidLayout'].update(visible=True)
    if event[:10] == 'backToMenu':
        window['vidLayout'].update(visible=False)
        window['listLayout'].update(visible=False)
        window['mainMenu'].update(visible=True)
    if event == 'vid-Down':
        vidDownloader(values['psg-vidlink'])
    if event == 'list-Down':
        listDownloader(values['psg-listlink'])
