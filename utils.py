import requests,os,tqdm
from bs4 import BeautifulSoup

PATH = 'D:/Manga/' #Change this to your own Directory
BASE_URL = "https://m.manganelo.com/"

def MakeSoup(url):
    get = requests.get(url)
    return BeautifulSoup(get.content,"lxml")

def SearchName(query):
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
    if ('s7' in url):
        url.replace('s7','s8')
    # if (manipulatedUrl[8:10] == "s7" and manipulatedUrl[18:20] == "v7"):
    #     print("True")
    #     manipulatedUrl.replace("s7","s8")
    #     manipulatedUrl.replace("v7","v8")
    return url

def singleChapManga(url,dir,chap):
    soup = MakeSoup(url)
    div = soup.find('div',class_='container-chapter-reader')#Scrap
    special = div.find_all('img')
    curDir = makeDir(dir,chap)+"/"
    imageLink = []
    for image in special:
        data = image.get('src')
        if (data[8:10] == "s7" and data[18:20] == "v7"):
            aa = data.replace('s7','s8')
            bb = aa.replace('v7','v8')
            imageLink.append(bb)
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
