from tkinter import *
from tkmacosx import Button
from tkinter import Frame
from tkinter import filedialog, messagebox
import os

DEFAULT_BGCOLOR = "white"
class MainWindow(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.master.title('Unziper')
        self.pack(fill=BOTH, expand=1)
        self.configure(bg=DEFAULT_BGCOLOR, highlightbackground=DEFAULT_BGCOLOR)
        self.centerWindow()

        self.dirPath = StringVar()

        self.dirPathedit = Entry(self, width=31, textvariable=self.dirPath, highlightbackground=DEFAULT_BGCOLOR,readonlybackground='ghost white',state='readonly')
        self.dirPathedit.grid(row = 0, column=0, columnspan=2)
        
        selectDir = Button(self, text="폴더 선택", command=self.openDlg, bd=0, highlightthickness=0, highlightbackground=DEFAULT_BGCOLOR)
        selectDir.grid(row = 0, column=2)

        passwdLabel = Label(self, text='password',bg=DEFAULT_BGCOLOR)
        passwdLabel.grid(row = 1, column=0)

        passwd = Entry(self, highlightbackground=DEFAULT_BGCOLOR, bg='ghost white')
        passwd.grid(row = 1, column=1)

        self.chNmParam = BooleanVar()
        self.chNmParam.set(False)

        chNmOption = Checkbutton(self,variable=self.chNmParam, text="이름 변경",bg=DEFAULT_BGCOLOR)
        chNmOption.grid(row = 2, column=0)

        #0f4c81
        unzipBtn = Button(self, text="압축 풀기", command=self.unzip, bg='#0f4c81', fg='white', bd=0, highlightthickness=0, highlightbackground=DEFAULT_BGCOLOR)
        unzipBtn.grid(row = 3, column=0, columnspan=3)

        self.place(x = 40, y = 20)

    def centerWindow(self):

        w = 450
        h = 180

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
        if self.dirPath.get():
            fileList = []
            stop = False
            while stop:
                os.listdir(path)

        else :
            dlg = messagebox.showerror("실패", "폴더 경로를 먼저 선택해주세요.")         


    def unzip(self):
        print("click unzip")
        print(self.chNmParam.get())

        self.fileScan()

def main():
    root = Tk()
    root.resizable(False, False)
    root.configure(bg=DEFAULT_BGCOLOR, highlightbackground=DEFAULT_BGCOLOR)
    ex = MainWindow()
    root.mainloop()


if __name__=='__main__':
    main()


# root = Tk()
# root.title('Unziper')
# root.geometry('300x300+100+100')
# root.mainloop()
