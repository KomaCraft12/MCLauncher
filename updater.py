import os
import mysql.connector
import json
import datetime
import wget
import zipfile
import time

# Creating connection object
mydb = mysql.connector.connect(
    host="komacloud.synology.me",
    user="jano",
    password="Katica.bogar2002",
    database="mclauncher",
    port=3306
)

def verify_client(client_id,serial):

    serial_v = ""

    cursor = mydb.cursor()

    cursor.execute("SELECT serial FROM client WHERE id = "+str(client_id))

    for x in cursor:
        serial_v = x[0]

    return serial == serial_v

def insert_data(serial):

    mycursor = mydb.cursor()

    sql = "INSERT INTO client (serial,version,date) VALUES (%s, %s, %s)"

    date = datetime.datetime.now()
    date = str(date.year) + "-" + str(date.month) + "-" + str(date.day)

    print(date)

    val = (serial, "1.0", date)
    mycursor.execute(sql, val)
    mydb.commit()

    return mycursor.lastrowid

def serial_verify(serial):

    maxi = 0
    used = 0
    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM serialkey WHERE serial = '" + str(serial) + "'")

    for x in cursor:
        print(x)
        maxi = x[2]
        used = x[3]

    return int(maxi)-int(used) > 0

def search_update(current_version):

    #print(current_version)

    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM updates WHERE version > "+str(current_version)+" ORDER BY version DESC LIMIT 1")

    van = False
    for elem in cursor:
        van = True
        url = elem[2]
        new_ver = elem[1]
        file = elem[3]

    if not van:
        print("A launcher naprakész")
        print("Launcher megnyitása...")
        time.sleep(3)
        os.system("start mclauncher.exe")
    else:
        print("Frissités szükséges. Új verzió: "+str(new_ver))
        valasz = ""
        while valasz.lower() not in ['i','n']:
            valasz = input("Frissités engedélyezése. (I vagy N):")
        if valasz.lower() == "n":
            print("Frissités elhalasztva!")
            print("Launcher megnyitása...")
            time.sleep(3)
            os.system("start mclauncher.exe")
        else:
            print("Frissités letöltése...")
            wget.download(url)
            print("Frissités telepítése...")
            with zipfile.ZipFile(file,'r') as elem:
                elem.extractall("")
            os.remove(file)
            registry_version(new_ver)

def registry_version(version):

    print(version)

    with open('launcher.json') as json_file:
        launcher = json.load(json_file)

    launcher['version'] = version
    client_id = launcher['client_id']

    cursor = mydb.cursor()

    cursor.execute("UPDATE client SET version = '"+str(version)+"' WHERE id = "+str(client_id))

    mydb.commit()

    with open("launcher.json", "w") as outfile:
        json.dump(launcher, outfile)

    print("Sikeres frissités")
    print("Launcher megnyitása...")
    time.sleep(3)
    os.system("start mclauncher.exe")

if(os.path.exists("launcher.json") == False):

    serial = input('Kérek a termék kulcsot: ')

    if serial_verify(serial):

        client_id = insert_data(serial)

        launcher = {'serial':serial,'client_id':client_id,'version':'1.0'}
        with open("launcher.json", "w") as outfile:
            json.dump(launcher, outfile)

        print("Sikeres kliens regisztráció! Inditsa újra a szoftvert!")
        time.sleep(3)
    else:
        print("Hibás termékkulcs!")
        print("Inditsa újra!")
        time.sleep(3)

else:

    with open('launcher.json') as json_file:
        launcher = json.load(json_file)

    if verify_client(launcher['client_id'], launcher['serial']):

        search_update(launcher['version'])
