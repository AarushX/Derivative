import PySimpleGUI as sg
import subprocess, requests, shutil, os
import filecmp, yaml, sys
from modules import *

version = tagsList[0]
print(tagsList)

args = sys.argv[:]
args.insert(0, sys.executable)
def restart():
  os.chdir(os.getcwd())
  os.execv(sys.executable, args)
#download(,".")
compared = "DerivativeClient - Copy.py"
if not filecmp.cmp(__file__,compared):
  shutil.move(compared,__file__)
  restart()



instancePath = os.path.expandvars(r'%APPDATA%\gdlauncher_next\instances')

instances = [name for name in os.listdir(instancePath) if os.path.isdir(os.path.join(instancePath, name))]

print (instances)


# # Interactive Part of Application
filteredList = ["Choose App First"]
sg.theme('DarkAmber')
layout = [[sg.Text('Welcome to the new installer!')],
  [sg.Text('Choose Type',size=(20, 1), font='Lucida',justification='left')],
  [sg.Combo(["HPFC","HPFS"],key='type',size=(30,2),default_value="Choose", enable_events=True)],
  [sg.Text('Choose Version',size=(20, 1), font='Lucida',justification='left')],
  [sg.Combo(filteredList,default_value="latest",key='version', enable_events=True)],
  [sg.Button('Install', font=('Times New Roman',12), key="Install"),
  sg.Button('Cancel', font=('Times New Roman',12), key="Cancel")]
]
window = sg.Window('High Performance Installer', layout, finalize=True)
while True:
  event, values = window.read()
  if event == sg.WIN_CLOSED or event == 'Cancel':
    break
  if event == 'type':
    filteredList = getTags("https://api.github.com/repos/AarushX/{}/tags".format(values["type"]))[0]
    window['version'].update(value="latest", values=filteredList)
    window.refresh()
  if event == 'Install':
    type = values['type']
    identifier = values['version']
    match identifier:
      case "latest":
        identifier = version
    print("hi")
    runInstall(identifier, type)

window.close()

tags = requests.get(tagsUrl)
tagsList = []
tagsDeserialized = json.loads(tags.text)
for tag in tagsDeserialized: 
  tagsList.append(tag["name"])