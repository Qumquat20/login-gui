#!/usr/bin/python3

#   Author: Qumquat
#   Date: May 2020
#   Project: GUI Login interface and admin panel

# Importing necessary libraries
import tkinter 
import pickle
from time import sleep
import os

# Declaring font
LARGE_FONT = ("Verdana", 12)

# Main App class
class LoginApp(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
      
        container = tkinter.Frame(self)
        container.pack(side='top',fill='both',expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # List of all pages
        self.pages = [StartPage,LogPage,RegPage,Panel,vClog,DelUser,ListUsers,ResetDB,Ifconfig,Ping]

        for F in self.pages:
            self.frame = F(container, self)
            self.frames[F] = self.frame
            self.frame.grid(row=0, column=0, sticky='nesw')
        
        self.showFrame(StartPage)

    # Function to show page
    def showFrame(self, cont):
        self.frame = self.frames[cont]
        self.frame.tkraise()


class StartPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        label = tkinter.Label(self, text='Choose an option',font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        logButton = tkinter.Button(self, text='Login',width=20,height=2,command=lambda: controller.showFrame(LogPage))
        logButton.pack(pady=8,padx=10)
          
        regButton = tkinter.Button(self, text='Register',width=20,height=2,command=lambda: controller.showFrame(RegPage))
        regButton.pack(pady=6,padx=10)

        regLabel = tkinter.Label(self, text='')
        regLabel.pack()
   

class Panel(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        label = tkinter.Label(self, text='Choose an option below: ')
        label.pack()

        clogButton = tkinter.Button(self, text='View Changelog',command=lambda: controller.showFrame(vClog))
        clogButton.pack()

        addUserButton = tkinter.Button(self, text='Add User', command=lambda: controller.showFrame(RegPage))
        addUserButton.pack()

        delUserButton = tkinter.Button(self, text='Delete User', command=lambda: controller.showFrame(DelUser))
        delUserButton.pack()

        listUsersButton = tkinter.Button(self, text='List Users', command=lambda: controller.showFrame(ListUsers))
        listUsersButton.pack()
        
        resetDbButton = tkinter.Button(self, text='Reset Database', command=lambda: controller.showFrame(ResetDB))
        resetDbButton.pack()
        
        ifconfigButton = tkinter.Button(self, text='Ifconfig', command=lambda: controller.showFrame(Ifconfig))
        ifconfigButton.pack()

        pingButton = tkinter.Button(self, text='Ping Host', command=lambda: controller.showFrame(Ping))
        pingButton.pack()

        backButton = tkinter.Button(self,text='Back',width=5,height=1,command=lambda: controller.showFrame(StartPage))
        backButton.pack(side='left',padx=5)


class vClog(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        label = tkinter.Label(self, text='Here are the contents of the changelog: ')
        label.pack()

        file = open('changelog.txt').read()
        
        log = tkinter.Text(self, height=14, width=60)
        log.pack()
        log.insert(tkinter.END,file)

        backButton = tkinter.Button(self,text='Back',width=5,height=1,command=lambda: controller.showFrame(Panel))
        backButton.pack(side='left',padx=5)


class DelUser(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        label = tkinter.Label(self, text='Input the user you would like to delete: ')
        label.pack()
        
        userVar = tkinter.StringVar()

        self.userEnt = tkinter.Entry(self, textvariable=userVar)
        self.userEnt.pack()

        delButton = tkinter.Button(self, text='Delete User',command=lambda: self.deleteUser(userVar.get()))
        delButton.pack()

        backButton = tkinter.Button(self,text='Back',width=5,height=1,command=lambda: controller.showFrame(Panel))
        backButton.pack(side='left',padx=5)

        self.resLabel = tkinter.Label(self, text='')
        self.resLabel.pack()

    def deleteUser(self, user):
        logInfo = pickle.load(open('users.p','rb'))

        if user in logInfo:
            logInfo.pop(user)
            pickle.dump(logInfo, open('users.p','wb'))
            self.resLabel.config(text='User Deleted',fg='green')
            self.userEnt.delete(0,'end')
        else:
            self.resLabel.config(text="User doesn't exist",fg='red')
            self.userEnt.delete(0,'end')


class ListUsers(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        label = tkinter.Label(self, text='All registered users are listed below: ')
        label.pack()

        self.listBox = tkinter.Text(self, height=14, width=60)
        self.listBox.pack()

        backButton = tkinter.Button(self,text='Back',width=5,height=1,command=lambda: controller.showFrame(Panel))
        backButton.pack(side='left',padx=5)

        refreshButton = tkinter.Button(self,text='Refresh',width=5,height=1,command=self.refresh)
        refreshButton.pack(side='left',padx=5)

        self.logInfo = pickle.load(open('users.p','rb'))    

        for user in self.logInfo.keys():
            user = user+'\n'
            self.listBox.insert(tkinter.END,user)

    def refresh(self):
        self.logInfo = pickle.load(open('users.p','rb'))    
        self.listBox.delete('1.0',tkinter.END)
        for user in self.logInfo.keys():
            user = user+'\n'
            self.listBox.insert(tkinter.END,user)


class ResetDB(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        label = tkinter.Label(self, text='To reset the database input the admin password below: ')
        label.pack()

        self.adminPassEntry = tkinter.StringVar()

        self.adminEntry = tkinter.Entry(self, textvariable=self.adminPassEntry)
        self.adminEntry.pack()

        self.resLabel = tkinter.Label(self, text='')
        self.resLabel.pack()

        backButton = tkinter.Button(self,text='Back',width=5,height=1,command=lambda: controller.showFrame(Panel))
        backButton.pack(side='left',padx=5)

        resetButton = tkinter.Button(self,text='Reset DB',width=5,height=1,command=self.DBReset)
        resetButton.pack(side='right',padx=5)

    def DBReset(self):
        f = open('adminpass','r')
        adminpass = f.read()
        f.close()

        if self.adminPassEntry.get() == adminpass:
            logInfo = { 'admin':'admin' }
            pickle.dump(logInfo, open('users.p','wb'))
            self.resLabel.config(text='Database reset',fg='green')
            self.adminEntry.delete(0,'end')
        elif self.adminPassEntry != adminpass:
            self.resLabel.config(text='Invalid password',fg='red')
            self.adminEntry.delete(0,'end')
        else:
            self.resLabel.config(text='Error',fg='red')
            self.adminEntry.delete(0,'end')


class Ifconfig(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        label = tkinter.Label(self, text="Here is the output of the command 'ifconfig': ")
        label.pack()

        self.ifconOutText = tkinter.Text(self,height=20,width=70)
        self.ifconOutText.pack()

        self.ifconfig()

        backButton = tkinter.Button(self,text='Back',width=5,height=1,command=lambda: controller.showFrame(Panel))
        backButton.pack(side='left',padx=5)

        refreshButton = tkinter.Button(self,text='Refresh',width=5,height=1,command=self.ifconfig)
        refreshButton.pack(side='right',padx=5)


    def ifconfig(self):
        self.ifconOutText.delete('1.0',tkinter.END)
        os.system('ifconfig > ifconfig.out')
        
        f = open('ifconfig.out','r')
        ifconfigOut = f.read()
        f.close

        self.ifconOutText.insert(tkinter.END,ifconfigOut)

        os.system('rm ifconfig.out')


class Ping(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        label = tkinter.Label(self, text='Input the address you would like to ping: ')
        label.pack()

        self.addr = tkinter.StringVar()

        self.addrEntry =  tkinter.Entry(self, textvariable=self.addr)
        self.addrEntry.pack()

        self.pingOutText = tkinter.Text(self,height=20,width=70)
        self.pingOutText.pack()

        backButton = tkinter.Button(self,text='Back',width=5,height=1,command=lambda: controller.showFrame(Panel))
        backButton.pack(side='left',padx=5)

        pingButton = tkinter.Button(self,text='Ping',width=5,height=1,command=self.ping)
        pingButton.pack(side='right',padx=5)


    def ping(self):
        self.pingOutText.delete('1.0',tkinter.END)
        os.system("ping -c 2 {} > ping.txt".format(self.addr.get()))
        f = open('ping.txt','r')
        pingOut = f.read()
        f.close()

        if pingOut != '':
            self.pingOutText.insert(tkinter.END,pingOut)
            os.system('rm ping.txt')
        else:
            self.pingOutText.insert(tkinter.END,'Error')



class LogPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        #self.app.bind('')

        label = tkinter.Label(self,text='Enter details below: ')
        label.pack(pady=10,padx=10)

        self.userLog = tkinter.StringVar()
        self.pwdLog = tkinter.StringVar()

        userLogLabel = tkinter.Label(self,text='Username * ')
        userLogLabel.pack()
        self.userLogEntry = tkinter.Entry(self,textvariable=self.userLog)
        self.userLogEntry.focus()
        self.userLogEntry.pack()

        pwdLogLabel = tkinter.Label(self,text='Password * ')
        pwdLogLabel.pack()
        self.pwdLogEntry = tkinter.Entry(self,textvariable=self.pwdLog,show='*')
        self.pwdLogEntry.pack()

        logButton = tkinter.Button(self,text='Login',width=5,height=1,command=self.login)
        logButton.pack(side='right')
        backButton = tkinter.Button(self,text='Back',width=5,height=1,command=lambda: controller.showFrame(StartPage))
        backButton.pack(side='left',padx=5)

        self.logResLabel = tkinter.Label(self,text='')
        self.logResLabel.pack()

    def login(self):
        user = self.userLog.get()
        pwd = self.pwdLog.get()

        logInfo = pickle.load(open('users.p','rb'))       
 
        if user in logInfo:
            if logInfo[user] == pwd:
                self.logResLabel.config(text=' ')
                self.userLogEntry.delete(0,'end')
                self.pwdLogEntry.delete(0,'end')
                app.showFrame(Panel)
        else:
            self.logResLabel.config(text='Invalid username or password',fg='red')
            self.userLogEntry.delete(0,'end')
            self.pwdLogEntry.delete(0,'end')


class RegPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        self.userReg = tkinter.StringVar()
        self.pwdReg1 = tkinter.StringVar()
        self.pwdReg2 = tkinter.StringVar()

        label = tkinter.Label(self,text='Enter details below: ')
        label.pack(pady=10,padx=10)

        userLabel = tkinter.Label(self,text='Username * ')
        userLabel.pack()
        userEntry = tkinter.Entry(self,textvariable=self.userReg)
        userEntry.focus()
        userEntry.pack()

        pwd1Label = tkinter.Label(self,text='Password * ')
        pwd1Label.pack()
        pwdEntry1 = tkinter.Entry(self,textvariable=self.pwdReg1,show='*')
        pwdEntry1.pack()
        
        pwd2Label = tkinter.Label(self,text='Re-enter Password * ')
        pwd2Label.pack()
        pwdEntry2 = tkinter.Entry(self,textvariable=self.pwdReg2,show='*')
        pwdEntry2.pack()
        
        regButton = tkinter.Button(self,text='Register',width=5,height=1,command=self.regUser)
        regButton.pack(side='right')
        backButton = tkinter.Button(self,text='Back',width=5,height=1,command=lambda: controller.showFrame(StartPage))
        backButton.pack(side='left')

        self.resLabel = tkinter.Label(self,text='')
        self.resLabel.pack()

    def regUser(self):
        user = self.userReg.get()
        pwd1 = self.pwdReg1.get()
        pwd2 = self.pwdReg2.get()

        logInfo = pickle.load(open('users.p','rb'))

        if user in logInfo:
            self.resLabel.config(text='User already exists',fg='red')
        else:
            if pwd1 == pwd2:
                logInfo.update( {user: pwd1} )
                pickle.dump(logInfo, open('users.p','wb'))
                self.resLabel.config(text='User registered',fg='green')
                app.showFrame(StartPage)


if __name__ == "__main__":
    app = LoginApp()
    app.title('Account')
    #app.geometry('500x300')
    app.mainloop()
