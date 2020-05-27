import os,img2pdf,glob

def makeComic(path,name,chap):
    with open (path+name+chap,'wb') as f:
        f.write(img2pdf.convert(sorted(glob.glob(path+name+chap+"*.jpg"))))

makeComic("/home/taufiq/Desktop/manga/MangaCollection/","Kanojo, Okarishimasu/","Chapter7/")