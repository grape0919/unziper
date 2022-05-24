from tkinter import *
# from tkmacosx import Button
from tkinter import Frame
from tkinter.ttk import Progressbar
from tkinter import filedialog, messagebox
import os
import threading

DEFAULT_BGCOLOR = "white"
class MainWindow(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.master.title('Renamer')
        self.pack(fill=BOTH, expand=1)
        self.configure(bg=DEFAULT_BGCOLOR)
        self.centerWindow()

        self.dirPath = StringVar()

        self.dirPathedit = Entry(self, width=32, textvariable=self.dirPath,readonlybackground='ghost white',state='readonly')
        self.dirPathedit.grid(row = 0, column=0, columnspan=2)
        
        selectDir = Button(self, text="폴더 선택", command=self.openDlg)
        selectDir.grid(row = 0, column=2)

        newExtLabel = Label(self, text=' 확장자명',bg=DEFAULT_BGCOLOR)
        newExtLabel.grid(row = 1, column=0)

        self.new_ext = StringVar()

        new_ext_edit = Entry(self,textvariable=self.new_ext, bg='ghost white')
        new_ext_edit.grid(row = 1, column=1)

        unzipBtn = Button(self, text="확장자 변경", command=self.rename, bg='#0f4c81', fg='white')
        unzipBtn.grid(row = 3, column=0, columnspan=3)

        self.progressVar = IntVar()
        self.progressVar.set(0)
        self.progress = Progressbar(self,orient=HORIZONTAL,length=250, mode='determinate',variable=self.progressVar)
        self.progress.grid(row = 4, column=0, columnspan=2)

        self.progressLabelVar = StringVar()
        self.progressLabelVar.set("0/0")
        self.progressLabal = Label(self, text="0/0", textvariable=self.progressLabelVar, bg=DEFAULT_BGCOLOR)
        self.progressLabal.grid(row=4, column=2)

        self.progress.grid_forget()
        self.progressLabal.grid_forget()


        self.place(x = 40, y = 20)

    def centerWindow(self):

        w = 380
        h = 150

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        x = (sw - w)/2
        y = (sh - h)/2

        self.master.geometry('%dx%d+%d+%d' % (w,h,x,y))

    def openDlg(self):
        print("click openDlg")

        filename = filedialog.askdirectory(initialdir=os.getcwd(), title="Select directory")

        self.dirPath.set(filename)


    def fileScan(self):
        path = self.dirPath.get()
        print("path : ", path)
        if path:
            self.progress.grid(row = 4, column=0, columnspan=2)
            self.progressLabal.grid(row=4, column=2)
            i = 1
            fileList = self.getFileList(path)
            self.progress.configure(maximum=len(fileList))
            for file in fileList:
                
                self.progressLabelVar.set(str(i)+"/"+str(len(fileList)))
                self.progressVar.set(i)
                self.progress.update()
                
                try:
                    file_name = file[:file.rindex('.')]
                    ext = file[file.rindex('.'):]
                    
                    print("file_name : " , file_name)
                    print("ext : ", ext)
                    remove_ext_str = self.new_ext.get()
                    if len(remove_ext_str):
                        if not remove_ext_str.startswith('.'):
                            remove_ext_str = '.' + remove_ext_str
                    if ext.endswith(remove_ext_str):
                        os.rename(file, file_name)
                    
                    
                except Exception as e:
                    messagebox.showerror("실패", str(e) + '\n\n' + '확장자 변경에 실패하였습니다.')
                    return
                    
                finally:
                    try:
                        i+=1
                    except:
                        pass
                    
            messagebox.showinfo("완료", '확장자 변경이 완료되었습니다.')
            self.progress.grid_forget()
            self.progressLabal.grid_forget()
        else :
            messagebox.showerror("실패", "폴더 경로를 먼저 선택해주세요.")   



    def getFileList(self, dirPath):
        resultList = []
        if os.path.exists(dirPath):
            subList = os.listdir(dirPath)
            for f in subList:
                fullPath = os.path.join(dirPath,f)
                if os.path.isdir(fullPath):
                    resultList.extend(self.getFileList(fullPath))
                else :
                    resultList.append(fullPath)

        return resultList


    def rename(self):
        print("click rename")
        thread = threading.Thread(target=self.fileScan)
        thread.start()

def main():
    root = Tk()
    root.resizable(False, False)
    root.configure(bg=DEFAULT_BGCOLOR)
    ex = MainWindow()
    root.mainloop()


if __name__=='__main__':
    main()


# root = Tk()
# root.title('Unziper')
# root.geometry('300x300+100+100')
# root.mainloop()
