import requests,os,tqdm
from bs4 import BeautifulSoup

PATH = 'D:/Manga/' #Change this to your own Directory
BASE_URL = "https://m.manganelo.com/"

def MakeSoup(url):
    get = requests.get(url)
    return BeautifulSoup(get.content,"lxml")

def searchName(query):
    name = query.lower().replace(' ','_') #Change Search Query
    searchQuery = BASE_URL+"search/"+name #Change Search Query
    soup = MakeSoup(searchQuery)
    special = soup.find_all('a',class_="a-h text-nowrap item-title")#Scrap
    mangaTitle =[]
    mangaLink=[]
    for i in special:
        mangaTitle.append(i.get_text())
        mangaLink.append(i.get('href'))
    return dict(zip(mangaTitle,mangaLink))

def searchChap(url):
    soup = MakeSoup(url)
    specialContainer = soup.find_all('a',class_='chapter-name text-nowrap')#Scrap
    chapterName =[]
    chapterLink=[]
    for i in specialContainer:
        chapterName.append(i.get_text())
        chapterLink.append(i.get('href'))
    return dict(zip(chapterName,chapterLink))

def makeDir(dir,chap):
    dirPath = PATH+dir
    if (os.path.isdir(dirPath)):
        os.chdir(dirPath)
        if (os.path.isdir(chap)):
            os.chdir(chap)
            return os.getcwd()
        elif (not os.path.isdir(chap)):
            os.mkdir(chap)
            os.chdir(chap)
            return os.getcwd()
    elif (not os.path.isdir(dirPath)):
        os.mkdir(dirPath)
        os.chdir(dirPath)
        if (os.path.isdir(chap)):
            os.chdir(chap)
            return os.getcwd()
        elif (not os.path.isdir(chap)):
            os.mkdir(chap)
            os.chdir(chap)
            return os.getcwd()

def linkManipulation(url):
    if (url[8:10] == "s7" and url[18:20] == "v7"):
        a = url.replace('s7','s8')
        b = a.replace('v7','v8')
    elif(url[8:10] == "s5" and url[18:20] == "v5"):
        a = url.replace('s5','s8')
        b = a.replace('v5','v8')
    else:
        b = url
    return b

def singleChapManga(url,dir,chap):
    soup = MakeSoup(url)
    div = soup.find('div',class_='container-chapter-reader')#Scrap
    special = div.find_all('img')
    curDir = makeDir(dir,chap)+"/"
    imageLink = []
    for image in special:
        data = image.get('src')
        freshLink = linkManipulation(data)
        imageLink.append(freshLink)
        # imageLink.append(image.get('src'))
    for data in imageLink:
        r = requests.get(data,stream=True)
        file_size = int(r.headers.get('Content-Length'))
        chunk =1
        chunk_size = 1024
        num_bars = int(file_size/chunk_size)
        if r.status_code == 200:    
            with open(curDir+data.split('/')[-1],'wb')as i:
                downloadBar = tqdm.tqdm(r.iter_content(chunk_size=chunk_size),total=num_bars,unit='KB',desc=data.split('/')[-1])
                for chunk in downloadBar:
                    i.write(chunk)
