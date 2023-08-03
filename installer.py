import wget
import zipfile
import os
import winshell
from win32com.client import Dispatch

print("MCLauncher telepítése")
print("Érdemes mindig a default értékeket választani! Jelőlés: I=Igen, N=Nem")

v = input("Telepítés helye (default: c:/Games/mclauncher/): ")
if v == "":
    v = "c:/Games/mclauncher/"

if not os.path.exists(v):
    os.makedirs(v)

print(os.path.join(v))

wget.download("https://komaweb.eu/mclauncher/base_mclauncher.zip",v)
file = "base_mclauncher.zip"

with zipfile.ZipFile(v+""+file, 'r') as elem:
    elem.extractall(v)
os.remove(v+""+file)

v2 = input("Parancsikon (I,N)(default: I):")
if v2 == "":
    v2 = "I"
if v2.upper() == "I":

    desktop = winshell.desktop()
    path = os.path.join(desktop, "MCLauncher.lnk")
    target = r""+v+"updater.exe"
    wDir = r""+v
    icon = r""+v+"MCLauncher.ico"
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation = icon
    shortcut.save()