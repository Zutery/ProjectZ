# ClothesUpdater Alpha Version to use download python 3.5.x works perfect
# using python 3.5.1, all work done by ExZachLy / Zutery. Thanks for using
# my project. Please add me on discord if you have any questions Zach#6237
import urllib.request
from bs4 import BeautifulSoup
import time
import os



#This may need to be generated from vars in the future.
figureDataURL = "https://www.habbo.com/gamedata/figuredata/0"
#Begin the time for analytical reasons
timeStart = time.time()

#count how many items were downloaded
count = 0
target="../../AU-exports"
# If there isn't an export folder, make one!
if not os.path.exists(target):
    os.makedirs(target)
    os.makedirs('{}/swf'.format(target))
    os.makedirs('{}/xml'.format(target))

# if there is an existing figure data file
# log all existing items to ensure they wont
# be downloaded twice
items = []
if os.path.exists('import.xml'):
    openClothes = open("import.xml","r")
    soup = BeautifulSoup(openClothes,"html.parser")
    for lib in soup.find_all("lib"):
        file = lib['id'] 
        if lib:
            items.append(file)
    

getProduction = ('https://www.habbo.com/gamedata/external_variables/')

# Download the external variables file from Habbo as vars.txt
urllib.request.urlretrieve(getProduction, 'vars.txt')
with open('vars.txt') as f:
    lines = f.readlines()
    for line in lines:
        #find the line that contains production infortmation
        if line.startswith('flash.client.url'):
            #strip all irrelevant information
            line = line.replace('flash.client.url=','')
            line = line.replace('images.habbo.com/gordon','')
            line = line.replace('/','')
            line = line.replace('\n', '')
            #print the production in the terminal
            print(line)
            #create a production variable to access later
            production = 'http://images.habbo.com/gordon/{}'.format(line)
            #close out of the vars file, and remove it. Piss on it :P
            f.close()
            os.remove('vars.txt')
            

getfigureMap = '{}/figuremap.xml'.format(production)
#download the figuredata file, we'll use this to find the .swf file
urllib.request.urlretrieve(getfigureMap, 'figuremap.xml')


urllib.request.urlretrieve(figureDataURL, 'figuredata.xml')

clothes = open("figuremap.xml","r")
data = BeautifulSoup(open("figuredata.xml","r"),"html.parser")
# load up beatifulsoup, find all items containing <lib id="itemname" ...
# and retrieve the ID name :P
soup = BeautifulSoup(clothes,"html.parser")

#Create figuredata
t = open("{}/xml/figuremap.xml".format(target),"w+")
p = open("{}/xml/figuredata.xml".format(target), "w+")
#Grab all the IDs of the associated items
#this will allow us to get the proper 
#figuredata code
parts = []
#create a loop for all items that are lib ids
for lib in soup.find_all("lib"):
    file = lib['id'] 
        
    if lib:
        #check if it exist in the old figuredata file
        if file not in items:
            for part in lib.find_all("part"):
                partID = part['id']
                if partID not in parts:

                    parts.append(partID)
                    #print(partID)
            #if not download that sucker
            print('Downloading {}.swf'.format(file))
            t.write("{}\n".format(lib))
            url = '{}/{}.swf'.format(production, file)
            urllib.request.urlretrieve(url, '{}/swf/{}.swf'.format(target,file))
            #add one to the download count, need to know this :P
            count = count + 1
done = []
count1 = 0
exs = data.find_all("set")
for ex in exs:
    lulz = ex.find_all("part")
    for lul in lulz:
        if lul['id'] in parts:
           if lul.parent['id'] not in done:
                print(lul.parent['id'])
                done.append(lul.parent['id'])
                p.write("{}".format(lul.parent))






#alright enough with sulake, we got their clothes, close out of their shitty file           
clothes.close()
if not os.path.exists('figuremap-old.xml'):
    os.rename('figuredata.xml', 'figuremap-old.xml')
timeEnd = time.time()
timeTotal = timeEnd - timeStart

if count == 0:
    saying = "Looks like you're all up to date!"
else:
    saying = "{} new items found!".format(count)
print('Total elapsed time: {} seconds, {} sets generated \n{}\n'.format(timeTotal,count1,saying))
print('Thank you for using AssetUpdater v0.1 by Zutery')
