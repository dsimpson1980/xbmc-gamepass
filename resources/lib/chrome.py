import os
import subprocess
import xbmcaddon
import xbmc

addon = xbmcaddon.Addon()
translation = addon.getLocalizedString
osWin = xbmc.getCondVisibility('system.platform.windows')
osOsx = xbmc.getCondVisibility('system.platform.osx')
osLinux = xbmc.getCondVisibility('system.platform.linux')
osAndroid = xbmc.getCondVisibility('system.platform.android')

def openChrome(url):
    chrome_path = ''
    if osWin:
        path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        path64 = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
        if os.path.exists(path):
            chrome_path = path
        elif os.path.exists(path64):
            chrome_path = path64
        subprocess.Popen([chrome_path, url])
    elif osOsx:
        # chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        subprocess.Popen(['open', '-a', 'Google Chrome', url])
    elif osAndroid:
        subprocess.Popen(
            ['am', 'start', '-n',
             'com.android.chrome/com.google.android.apps.chrome.Main', '-d',
             url])
    else:
        xbmc.executebuiltin('XBMC.Notification(Info:,'+str(translation(30005))+'!,5000)')

