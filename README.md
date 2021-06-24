# portable-youtube-downloader
An portable youtube downloader with linux and windows support. Download binary package from here and run it. No installation, no depencities!


## Compiling on linux (for devs)
First, we need to install depencities in order to run it directly from source and pyinstaller in order to compile it.
```
[your python interpreter] -m pip install pysimplegui youtube-dl pyinstaller

Example: python3.9 -m pip install pysimplegui youtube-dl pyinstaller
```
After installation try running script with `python3.9 ./downloader.py` and see if it works. If it works then you can compile it using pyinstaller. 

If you are using an ubuntu or debian based distro then you must install python dev package

```
sudo apt install [your python interpreter]-dev

Example: sudo apt install python3.9-dev
```
Once it finishes installing you can compile it by this command `python3.9 -m PyInstaller --onefile --console  "./downloader.py"`. The executable will be moved into dist folder inside the project folder. You can delete other folders if you wish.

![](image.png)

*you can delete these files if you wish*
