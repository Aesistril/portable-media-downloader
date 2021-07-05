import youtube_dl as ytdl
from time import sleep, strftime, gmtime
import PySimpleGUI as psg
import multiprocessing
from os import remove
from webbrowser import open as webopen
from urllib.request import urlopen
from platform import system

osname = system()
isDownLayoutOn = False
success = '1'
audioExtList = ['aac', 'm4a', 'mp3', 'wav', 'flac', 'opus', 'ogg']
videoExtList = ['mp4', 'flv', 'webm', 'mkv', 'avi']
filetype = ''
prog = '3'
curr = '0.1'
ver_url = 'https://github.com/yigitayaz262/portable-media-downloader/raw/master/curr-version'

latest = urlopen(ver_url).read()
latest = latest.decode('utf-8')
latest = latest[:-1]

print(latest)

if osname == 'Windows':
    osbinary = 'downloader.exe'

if osname == 'Linux':
    osbinary = 'downloader'

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

mainMenu =   [  [psg.Button('', visible=False, disabled=True), psg.Text('What are you going to download?')],
                [psg.Button('Playlist (Coming Soon)', key='SelList'), psg.Button('Video', key='SelVid')],
                [psg.Text('')],
                [psg.Text('')],
                [psg.Text('This downloader supports 1100+ websites.')], 
                [psg.Text('Click here for full list of websites', text_color='#00A6FF', key='list-web', click_submits=True)]  ]

listLayout =  [ [psg.Button('', visible=False, disabled=True), psg.Button('<', key='backToMenu')],
                [psg.Text("Link: "), psg.InputText(key='psg-listlink')],
                [psg.Button(button_text='Download', key='list-Down')]  ]

vidLayout  =  [ [psg.Button('', visible=False, disabled=True), psg.Button('<', key='backToMenu')],
                [psg.Text("Link: "), psg.InputText(key='psg-vidlink')],
                [psg.Text('Select file type: '), psg.DropDown(key='vid-filetype', values=['Only Audio', 'Audio And Video'])],
                [psg.Text('Select Quality: '), psg.DropDown(key='vid-quality', values=['Highest possibble', 'Lowest possible'])],
                [psg.Text('Select Extension: '), psg.DropDown(key='vid-ext', values=[], size=(19,1))],
                [psg.Checkbox('Download Subtitiles if its available', key='sub-bool')],
                [psg.Button(button_text='Download', key='vid-Down')]  ]

downLayout = [  [psg.Text('Downloading:'), psg.Text('', size=(45,1), key='vid-name')],
                [psg.Text('Duration:'), psg.Text('', size=(10,1), key='vid-dur')]  ]
#                [psg.Text('%'+prog+'  ', size=(6, 1)), psg.ProgressBar(1, orientation='h', size=(20, 20), key='progress', bar_color='#09d910', border_width=2)]  ]

layout = [  [psg.Column(listLayout, key='listLayout', visible=False), psg.Column(downLayout, key='downLayout', visible=False), psg.Column(vidLayout, key='vidLayout', visible=False), psg.Column(mainMenu, key='mainMenu')]  ]

window = psg.Window('Media Downloader', layout)

def getvidinfo(url):
    ydl_ext = {}

    with ytdl.YoutubeDL(ydl_ext) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title')
        video_dur = strftime('%H:%M:%S', gmtime(info_dict.get('duration')))
        window['vid-name'].update(video_title)
        window['vid-dur'].update(video_dur)

def vidDownloader(url):
    ext = values['vid-ext']
    if ext == 'ogg': ext = 'vorbis'
    if values['vid-quality'] == 'Highest possibble': quality = 'best'
    else: quality = 'worst'

    if values ['vid-filetype'] == 'Audio And Video': FFkey = 'FFmpegVideoConvertor'
    else: FFkey = 'FFmpegExtractAudio'

    ydl_opts = {
    'format':  quality,
    'outtmpl': '%(title)s.%(ext)s',
    "writesubtitles": values['sub-bool'],
    'postprocessors': [{
        'key': FFkey,
        'preferedformat': ext,
        }],}

    try:
        with ytdl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        success = '1'
    except Exception as err:
        print('DEBUG: An error occurared while downloading video \n \n' + str(err))
        success = '0'
    finally:
        successf = open('succ.temp', 'w')
        successf.write(str(success))
        successf.close()

def listDownloader(url):
    print('DEBUG: ' + url + ' [Work in progress]')
    sleep(10)

event, values = window.read(timeout=0.1)
listproc = multiprocessing.Process(target=listDownloader, args=(values['psg-listlink'],))
vidproc = multiprocessing.Process(target=vidDownloader, args=(values['psg-vidlink'],))

def chkProc():
    if vidproc.is_alive() or listproc.is_alive():
        return True
    else: return False

if curr != latest:
    psg.popup('There is a new update! You can download it from here: \n \n \n' + str('https://github.com/yigitayaz262/portable-media-downloader/releases/download/'+ latest +'/'+ osbinary))

while True:
    event, values = window.read(timeout=0.1)
    if event == psg.WIN_CLOSED or event == 'Cancel':
        break
    if chkProc() and isDownLayoutOn == False:
        event = lastEvent
        window['downLayout'].update(visible=True)
        window['listLayout'].update(visible=False)
        window['vidLayout'].update(visible=False)
        isDownLayoutOn = True

    if chkProc() == False and isDownLayoutOn:
        event = lastEvent
        window['downLayout'].update(visible=False)
        if lastEvent == 'list-Down':
            window['listLayout'].update(visible=True)
            listproc.join()
        if lastEvent == 'vid-Down':
            vidproc.join()
            window['vidLayout'].update(visible=True)
        isDownLayoutOn = False
        successf = open('succ.temp', 'r')
        success = successf.read(1)
        successf.close()
        remove('succ.temp')
        if success == '1': psg.popup('You can find files at the same folder as the program', title='Download Completed!')
        elif success == '0': psg.popup('An unknown error occurared', title='Error')

    if values['vid-filetype'] != filetype:
        if values['vid-filetype'] == 'Only Audio':
            window['vid-ext'].update(values=audioExtList)
        elif values['vid-filetype'] == 'Audio And Video':
            window['vid-ext'].update(values=videoExtList)
        else:
            window['vid-ext'].update(values=['Please select filetype first'])
        filetype = values['vid-filetype']

#    if event == 'SelList' and isDownLayoutOn == False:
#        window['mainMenu'].update(visible=False)
#        window['listLayout'].update(visible=True)
    if event == 'SelVid' and isDownLayoutOn == False:
        window['mainMenu'].update(visible=False)
        window['vidLayout'].update(visible=True)
    if event[:10] == 'backToMenu':
        window['vidLayout'].update(visible=False)
        window['listLayout'].update(visible=False)
        window['mainMenu'].update(visible=True)

    if event == 'list-web':
        webopen('https://github.com/yigitayaz262/portable-media-downloader/blob/master/Supported-sites.md')

    if event == 'vid-Down' and values['psg-vidlink'] != '' and (values['vid-filetype'] in ['Only Audio', 'Audio And Video'] and values['vid-quality'] in ['Highest possibble', 'Lowest possible']) and (values['vid-ext'] in audioExtList or values['vid-ext'] in videoExtList):
        lastEvent = 'SelVid'
        getvidinfo(values['psg-vidlink'])
        vidproc = multiprocessing.Process(target=vidDownloader, args=(values['psg-vidlink'],))
        vidproc.start()
    elif event == 'vid-Down' and (values['psg-vidlink'] == '' or values['vid-filetype'] not in ['Only Audio(mp3)', 'Audio And Video'] or values['vid-quality'] not in ['Highest possibble', 'Lowest possible'] or (values['vid-ext'] not in audioExtList or values['vid-ext'] not in videoExtList)):
        psg.popup('Invalid quality, extension, link or filetype', title='Error')
    
    if event == 'list-Down':
        lastEvent = 'SelList'
        listproc = multiprocessing.Process(target=listDownloader, args=(values['psg-listlink'],))
        listproc.start()

# test video = https://www.youtube.com/watch?v=RVMZxH1TIIQ