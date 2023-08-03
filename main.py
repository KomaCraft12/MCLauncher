#!/usr/bin/env python3
# This example shows how to write a basic launcher with Tkinter.

import mll as minecraft_launcher_lib
import subprocess
import os
import PySimpleGUI as sg
import psutil
import json

name = ""

def setting():

    if(os.path.exists("settings.json")):
        print("Jó")
        with open("settings.json") as f:
            data = json.load(f)
            print(data['java'])
            jvm = data['jvmArguments'].replace("G"," GB")
            print(jvm)
    else:
        java = minecraft_launcher_lib.utils.get_java_executable()
        data = {'java': java,'jvmArguments':'1G'}
        jvm = '1 GB'
        with open("settings.json", "w") as outfile:
            json.dump(data, outfile)

    memory = []

    max_momory = round(psutil.virtual_memory().total*pow(10,-9))-4

    for i in range(1,max_momory+1):
        memory.append(str(i)+" GB")

    java_column = [
        [sg.Text("Java")],
        [sg.InputText(default_text=data['java'],key="-JAVA-")],
        [sg.Button("Beállít",key="set-java")],
    ]

    memory_column = [
        [sg.Text("Memória")],
        [sg.Combo(values=memory,default_value=jvm,key="-MEMORY-")],
        [sg.Button("Beállít",key="set-memory")],
    ]

    layout = [
        [sg.Text("Beállitások", key="new", justification="center",size=(50,2),font=("Arial","14"))],
        [sg.HSeparator()],
        [sg.Column(java_column)],
        [sg.HSeparator()],
        [sg.Column(memory_column)]
    ]

    window = sg.Window("MineCraft Beállitások", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "set-memory":
            memorys = values['-MEMORY-']
            memorys = memorys.replace(" GB","G")
            print(memorys)
            data['jvmArguments'] = memorys
            if os.path.exists("settings.json"):
                os.remove("settings.json")
            with open("settings.json", "w") as outfile:
                json.dump(data,outfile)

        if event == "set-java":
            java = values['-JAVA-']
            data['java'] = java
            if os.path.exists("settings.json"):
                os.remove("settings.json")
            with open("settings.json", "w") as outfile:
                json.dump(data,outfile)


    window.close()

def install_vanilla_version():

    new_version = []
    for v in minecraft_launcher_lib.utils.get_version_list():
        print(v['id'])
        new_version.append(v['id'])

    layout = [
        [sg.Text("Vanilla verzió telepítése")],
        [sg.Combo(values=new_version)],
        [sg.Text(key="response")],
        [sg.Button('Telepítés', key="-NEWV-")],
    ]

    window = sg.Window("MineCraft Vanilla", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-NEWV-":
            print(values[0])
            minecraft_launcher_lib.install.install_minecraft_version(values[0],minecraft_directory)
            window['response'].update("Sikeres teleítés")
    window.close()

def install_forge_version():

    new_version = minecraft_launcher_lib.forge.list_forge_versions()

    layout = [
        [sg.Text("Forge verzió telepítése")],
        [sg.Combo(values=new_version)],
        [sg.Text(key="response")],
        [sg.Button('Telepítés', key="-NEWV-")],
    ]

    window = sg.Window("MineCraft Forge", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-NEWV-":
            minecraft_launcher_lib.forge.install_forge_version(values[0],minecraft_directory)
            window['response'].update("Sikeres teleítés")
    window.close()

version = []

# Get Minecraft directory
minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

print(minecraft_directory)

version_raw = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)

for v in version_raw:
    print(v['id'])
    version.append(v['id'])

if(os.path.exists("user.json")):
    with open('user.json') as json_file:
        username = json.load(json_file)['name']
else:
    username = ""
print(version)


sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
column_user = [
    [sg.Text('Név beállitása',size=(15,2))],
    [sg.Text('Név:')],
    [sg.InputText(key="-NAME-")],
    [sg.Text(username,key="-name-now-")],
    [sg.Button('Beállitás',key="-SET-")],
]
column_version = [
    [sg.Text('Minecraft Inditása',size=(15,2))],
    [sg.Text('Verzió:')],
    [sg.Combo(values=version,key="-VERSION-",size=(30, 6))],
    [sg.Text("")],
    [sg.Button('Inditás',key="-START-")],
]

column_action = [
    [sg.Text("Telepités",size=(15,3))],
    [sg.Button("Vanilla",key="-VANILLA-",size=(6,1))],
    [sg.Button("Forge",key="-FORGE-",size=(6,1))],
]

column_setting = [
    [sg.Text("Egyéb",size=(15,3))],
    [sg.Button("Beállitások",key="-SETTING-")],
]

layout = [
    [sg.Text("Minecraft Launcher",justification="center",size=(80,2),font=("Arial","14"))],
    [sg.HSeparator()],
    [
     sg.Column(column_user,vertical_alignment="t"),
     sg.VSeperator(),
     sg.Column(column_version,vertical_alignment="t"),
     sg.VSeperator(),
     sg.Column(column_action,vertical_alignment="t"),
     sg.VSeperator(),
     sg.Column(column_setting,vertical_alignment="t"),
    ]
]

# Create the Window
window_launcher = sg.Window('MCLauncher', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window_launcher.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == "-VANILLA-":
        install_vanilla_version()
    if event == "-FORGE-":
        install_forge_version()
    if event == "-SETTING-":
        setting()
    if event == "-SET-":
        name = values["-NAME-"]
        users = {'name': name}
        window_launcher["-name-now-"].update(name)
        with open("user.json", "w") as outfile:
            json.dump(users, outfile)
    if event == "-START-":
        options = minecraft_launcher_lib.utils.generate_test_options()
        print(values)

        with open("settings.json") as f:
            settings = json.load(f)

        options["username"] = values["-NAME-"]

        if os.path.exists("settings.json"):
            options["jvmArguments"] = ["-Xmx"+settings['jvmArguments'], "-Xms"+settings['jvmArguments']]
            options["executablePath"] = settings['java']

        version = values["-VERSION-"]
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory,options)
        print(minecraft_command)
        minecraft_command += " &"
        # Start Minecraft
        subprocess.call(minecraft_command)
window_launcher.close()