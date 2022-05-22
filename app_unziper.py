from tkinter import *
# from tkmacosx import Button
from tkinter import Frame
from tkinter.ttk import Progressbar
from tkinter import filedialog, messagebox
import os
import py7zr
import shutil
import threading

DEFAULT_BGCOLOR = "white"
TEMP_DIR = os.path.join(os.getcwd(),'table')
class MainWindow(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.master.title('Unziper')
        self.pack(fill=BOTH, expand=1)
        self.configure(bg=DEFAULT_BGCOLOR)
        self.centerWindow()

        self.dirPath = StringVar()

        self.dirPathedit = Entry(self, width=32, textvariable=self.dirPath,readonlybackground='ghost white',state='readonly')
        self.dirPathedit.grid(row = 0, column=0, columnspan=2)
        
        selectDir = Button(self, text="폴더 선택", command=self.openDlg)
        selectDir.grid(row = 0, column=2)

        passwdLabel = Label(self, text='password',bg=DEFAULT_BGCOLOR)
        passwdLabel.grid(row = 1, column=0)

        self.pwd = StringVar()

        passwd = Entry(self,textvariable=self.pwd, bg='ghost white')
        passwd.grid(row = 1, column=1)

        self.chNmParam = BooleanVar()
        self.chNmParam.set(False)

        chNmOption = Checkbutton(self,variable=self.chNmParam, text="이름 변경",bg=DEFAULT_BGCOLOR)
        chNmOption.grid(row = 2, column=0)

        #0f4c81
        unzipBtn = Button(self, text="압축 풀기", command=self.unzip, bg='#0f4c81', fg='white')
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

        # self.dirPathedit.delete(0, END)
        # self.dirPathediii t.insert(0, filename)

        # self.dirPath.set(filename)

        # print(self.dirPath.get())

    def fileScan(self):
        path = self.dirPath.get()
        if path:
            self.progress.grid(row = 4, column=0, columnspan=2)
            self.progressLabal.grid(row=4, column=2)
            i = 1
            fileList = self.getFileList(path)
            self.progress.configure(maximum=len(fileList))
            for zipFile in fileList:
                
                self.progressLabelVar.set(str(i)+"/"+str(len(fileList)))
                self.progressVar.set(i)
                self.progress.update()
                # print(zipFile)
                try:
                    shutil.rmtree(TEMP_DIR)
                except:
                    pass
                z = py7zr.SevenZipFile(zipFile, mode='r', password=self.pwd.get())
                try:
                    z.extractall(path=TEMP_DIR)#os.path.dirname(os.path.abspath(zipFile)))
                    if self.chNmParam.get():
                        # print('check!!')
                        tempList = os.listdir(TEMP_DIR)
                        for t in tempList:
                            toFile = os.path.join(os.path.dirname(os.path.abspath(zipFile)),'.'.join(str(os.path.basename(zipFile)).split('.')[:-1]))
                            # print(toFile)
                            shutil.move(os.path.join(TEMP_DIR, t),toFile)
                    else:
                        print('non check!!')
                        tempList = os.listdir(TEMP_DIR)
                        for t in tempList:
                            shutil.move(os.path.join(TEMP_DIR, t),os.path.dirname(os.path.abspath(zipFile)))

                except py7zr.exceptions.Bad7zFile as e:
                    messagebox.showerror("실패", str(e) + '\n\n' + '비밀번호를 확인해주세요.')
                    return
                    
                except shutil.Error as e:
                    messagebox.showerror("실패", str(e) + '\n\n' + '같은 파일이 존재합니다.')
                    return
                    
                finally:
                    try:
                        shutil.rmtree(TEMP_DIR)
                        i+=1
                    except:
                        pass
                    
            messagebox.showinfo("완료", '압축풀기가 완료되었습니다.')
            self.progress.grid_forget()
            self.progressLabal.grid_forget()
        else :
            try:
                shutil.rmtree(TEMP_DIR)
            except:
                pass
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
                    if str(f).endswith('.7z'):
                        resultList.append(fullPath)

        return resultList


    def unzip(self):
        print("click unzip")
        print(self.chNmParam.get())
        thread = threading.Thread(target=self.fileScan)
        # self.fileScan()
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
