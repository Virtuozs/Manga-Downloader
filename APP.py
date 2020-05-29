import os,re
from PIL import Image
from tkinter import Entry, Button, Checkbutton, Frame, Tk, Label, Listbox, END, IntVar, messagebox
from tkinter.ttk import Combobox, Progressbar
from manganelo import searchChap, searchName, singleChapManga

class UI(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.window = parent
        self.ALL = IntVar()
        self.initUIKit()
        self.initUI()

    def initUI(self):
        self.window.title("MANGA DOWNLOADER")

    def initUIKit(self): 
        #Label
        self.searchLabel = Label(self.window,text="Search!!")
        self.mangaLabel = Label(self.window,text="Manga Name")
        self.chapLabel = Label(self.window,text="Chapter")

        #Entry
        self.searchEntry = Entry(self.window,width=80)

        #ProgressBar
        self.progress = Progressbar(self.window,length=80,mode='determinate')

        #Combobox
        self.cbMangaName = Combobox(self.window,width=80,state='readonly')
        self.cbChapList = Combobox(self.window,width=80,state='readonly')

        #Button
        self.searchBtn = Button(self.window,text="Search",command=self.SearchManga)
        self.getChapBtn = Button(self.window,text="Get",command=self.SearchChapter)
        self.downloadBtn = Button(self.window,text="Download",command=self.Download)

        #CheckBox
        self.chkDownloadAll = Checkbutton(self.window,text="Download All Chapter",variable=self.ALL,onvalue =1,offvalue=0)
        #Init
            #search
        self.searchLabel.grid(row=0,column=0)
        self.searchEntry.grid(row=0,column=1,padx=12,pady=16)
        self.searchBtn.grid(row=0,column=2)
            #CB Manga
        self.mangaLabel.grid(row=1,column=0)
        self.cbMangaName.grid(row=1,column=1)
        self.getChapBtn.grid(row=1,column=2)
            #CB Chapter
        self.chapLabel.grid(row=3,column=0)
        self.cbChapList.grid(row=3,column=1)
            #CheckBox
        self.chkDownloadAll.grid(row=2,column=1)
            #Download Button
        self.downloadBtn.grid(row=4,column=1,pady=16)

    def SearchManga(self):
        self.sQuery = self.searchEntry.get()
        self.searchContent = searchName(self.sQuery)
        self.cbMangaName['values']= list(self.searchContent.keys())

    def SearchChapter(self):
        if self.ALL.get() == 1:
            self.cbChapList.config(state='disable')
        else:
            self.cbChapList.config(state='readonly')
            self.keyContent = self.cbMangaName.get()
            self.sMangaCahpter = searchChap(self.searchContent.get(self.keyContent))
            self.cbChapList['values'] = list(self.sMangaCahpter.keys())

    def saveFilename(self,name):
        key = self.chapKey
        chapName = self.sMangaCahpter.get(key)
        return re.sub(r'(?u)[^-\w.]', ' ', name)
    
    def Download(self):
        self.chapKey = self.cbChapList.get()
        self.sChapList = self.sMangaCahpter.get(self.chapKey)
        if self.ALL.get() == 1:
            for chap,link in self.sMangaCahpter.items():
                singleChapManga(link,self.cbMangaName.get(),self.saveFilename(chap))
            messagebox.showinfo('Information','Your download has been complete')
        else:
            singleChapManga(self.sChapList,self.cbMangaName.get(),self.saveFilename(self.chapKey))
            messagebox.showinfo('Information','Your download has been complete') 

if __name__ == "__main__":
    root = Tk()
    app = UI(root)
    root.mainloop()
