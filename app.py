from tkinter import *
from tkinter.ttk import Frame
from tkinter import filedialog, messagebox
import os

class MainWindow(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.master.title('Unziper')
        self.pack(fill=BOTH, expand=1)
        self.centerWindow()

        subFrame = Frame()

        self.dirPath = StringVar()

        self.dirPathedit = Entry(subFrame, width=31, textvariable=self.dirPath)
        self.dirPathedit.configure(state='disabled')
        self.dirPathedit.grid(row = 0, column=0, columnspan=2)
        
        selectDir = Button(subFrame, text="폴더 선택", command=self.openDlg)
        selectDir.grid(row = 0, column=2)

        passwdLabel = Label(subFrame, text='password')
        passwdLabel.grid(row = 1, column=0)

        passwd = Entry(subFrame)
        passwd.grid(row = 1, column=1)

        self.chNmParam = BooleanVar()
        self.chNmParam.set(False)

        chNmOption = Checkbutton(subFrame,variable=self.chNmParam, text="이름 변경")
        chNmOption.grid(row = 2, column=0)

        unzipBtn = Button(subFrame, text="압축 풀기", command=self.unzip)
        unzipBtn.grid(row = 3, column=0, columnspan=3)

        subFrame.pack()
        subFrame.place(x = 10, y = 10)

    def centerWindow(self):

        w = 500
        h = 300

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
        # self.dirPathedit.insert(0, filename)

        # self.dirPath.set(filename)

        # print(self.dirPath.get())

    def fileScan(self):
        path = self.dirPath.get()
        if self.dirPath.get():
            print(path)

        else :
            dlg = messagebox.showerror("실패", "폴더 경로를 먼저 선택해주세요.")         


    def unzip(self):
        print("click unzip")
        print(self.chNmParam.get())

        self.fileScan()

def main():
    root = Tk()
    root.resizable(False, False)
    ex = MainWindow()
    root.mainloop()


if __name__=='__main__':
    main()


# root = Tk()
# root.title('Unziper')
# root.geometry('300x300+100+100')
# root.mainloop()
