import yaml, requests, shutil, os, subprocess, json
with open('config.yml', 'r') as file:
  config = yaml.safe_load(file)

name = config["information"]["name"]
repo = config["information"]["repo"]
useChunks = config["downloads"]["useChunks"]
chunkSize = config["downloads"]["chunkSize"]
setupsUrl = config["urls"]["setupsUrl"]
tagsUrl = config["urls"]["tagsUrl"].format(repo)

def getTags(tagsUrl):
  tagsList = []
  tagsDeserialized = json.loads(requests.get(tagsUrl, headers={"Authorization":"token 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"}).text)
  for tag in tagsDeserialized: 
    tagsList.append(tag["name"])
  return tagsList, tagsDeserialized

def validateTag(tagToValidate,tags):
  for tag in tags:
    if tag["name"] == tagToValidate:
      return True
  return False

def download(url, path):
  filename = url.split('/')[-1]
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

def runInstall (version, app):
  tempDir = os.path.expandvars(r'%TEMP%'.format(name))
  path = download(setupsUrl.format(repo, version, app), tempDir)
  cmd = f"{path} batch.exe"
  returncode = subprocess.call(cmd, shell=True)
  if os.path.exists(path):
    os.remove(path)
    print("removed ig")
  return True
  
tagsList, tagsDeserialized = getTags(tagsUrl)
