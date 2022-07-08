import PySimpleGUI as sg
import subprocess, requests, shutil, os, filecmp, yaml, sys, json

# I added this in github. behold the power of sync!!!!
# Configuration and Definitions
with open('config.yml', 'r') as file:
  config = yaml.safe_load(file)
name = config["information"]["name"]
repo = config["information"]["repo"]
useChunks = config["downloads"]["useChunks"]
chunkSize = config["downloads"]["chunkSize"]
setupsUrl = config["urls"]["setupsUrl"]
tagsUrl = config["urls"]["tagsUrl"].format(repo)
token = config["token"]
filteredList = ["Choose App First"]
compared = "DerivativeClientUpdated.py"

## Define Functions ##
# Gets the tags from a url
def getTags(tagsUrl, token=token):
  tagsList = []
  tagsDeserialized = json.loads(
    requests.get(
      tagsUrl, 
      headers={
        "Authorization":f"token {token}"
        }
      ).text
  )
  for tag in tagsDeserialized: 
    tagsList.append(tag["name"])
  return tagsList, tagsDeserialized
tagsList, tagsDeserialized = getTags(tagsUrl)

# Deprecated!
# Validate Tag to check for tags in a repo
def validateTag(tagToValidate,tags):
  for tag in tags:
    if tag["name"] == tagToValidate:
      return True
  return False

# Downloads large files such as installers
def download(url, path, overridenName=None):
  filename = url.split('/')[-1]
  if (overridenName!=None): filename=overridenName
  path = path+"\\"+filename
  with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open(path, 'wb') as f:
      if useChunks:
        for chunk in r.iter_content(chunk_size=8192): 
          f.write(chunk)
      else:
        shutil.copyfileobj(r.raw, f)
  return path
def downloadSimple(url,path):
  r = requests.get(url)
  open(path, 'wb').write(r.content)
def runInstall (version, app):
  tempDir = os.path.expandvars(r'%TEMP%'.format(name))
  path = download(setupsUrl.format(repo, version, app), tempDir)
  cmd = f"{path} batch.exe"
  returncode = subprocess.call(cmd, shell=True)
  if os.path.exists(path):
    os.remove(path)
  return True
def restart():
  os.chdir(os.getcwd())
  os.execv(sys.executable, args)

version = tagsList[0]

# Auto-Updater Script
args = sys.argv[:]
args.insert(0, sys.executable)
downloadSimple(
  "https://raw.githubusercontent.com/AarushX/DerivativeMC/main/DerivativeClient.py",
  compared
)
if not filecmp.cmp(__file__,compared):
  shutil.move(compared,__file__)
  restart()

# # Currently Unused Instance Reading (check out for future updates--- that'll autoinstall lol)
# instancePath = os.path.expandvars(r'%APPDATA%\gdlauncher_next\instances')
# instances = [name for name in os.listdir(instancePath) if os.path.isdir(os.path.join(instancePath, name))]

# Application GUI Config
sg.theme('DarkTeal12')
layout = [[sg.Text('Welcome to the new installer!')],
  [sg.Text('Choose Type',size=(20, 1), font='Lucida',justification='left')],
  [sg.Combo(["HPFC","HPFS"],key='type',size=(30,2),default_value="Choose", enable_events=True)],
  [sg.Text('Choose Version',size=(20, 1), font='Lucida',justification='right')],
  [sg.Combo(filteredList,default_value="latest",key='version', enable_events=True)],
  [sg.Button('Install', font=('Times New Roman',12), key="Install"),
  sg.Button('Cancel', font=('Times New Roman',12), key="Cancel")]
]
window = sg.Window('High Performance Installer', layout, finalize=True)

# GUI Event Loop
while True:
  event, values = window.read()
  if event == sg.WIN_CLOSED or event == 'Cancel':
    break
  if event == 'type':
    filteredList = getTags(
      "https://api.github.com/repos/AarushX/{}/tags"
      .format(
        values["type"])
      )[0]
    window['version'].update(value="latest", values=filteredList)
    window.refresh()
  if event == 'Install':
    type = values['type']
    identifier = values['version']
    match identifier:
      case "latest":
        identifier = version
    runInstall(identifier, type)
window.close()
