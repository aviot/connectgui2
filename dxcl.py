# -*- coding: utf-8 -*-
from Tkinter import *
from ttk import *
import win32ras,time
import tkMessageBox
import re,urllib2 
from subprocess import Popen, PIPE

# init and set frame
master = Tk()
master.title('反共救国刻不容缓')
fm=Frame(master, padding="3 3 9 9")
fm.grid(column=0, row=0, sticky=(N, W, E, S))
fm.columnconfigure(0, weight=1)
fm.rowconfigure(0, weight=1)

#set label
Label(fm, text='宽带名称:',width = 8).grid(row=1,sticky=W)
Label(fm, text='宽带账户:',width = 8).grid(row=2,sticky=W)
Label(fm, text='宽带密码:',width = 8).grid(row=3,sticky=W)

#define var
entyname = StringVar()
account = StringVar()
passport = StringVar()	

#set entry
entry1=Entry(fm ,width = 18,textvariable=entyname)
entry1.grid(row=1,column=1,sticky=W)
entry2=Entry(fm ,width = 18,textvariable=account)
entry2.grid(row=2,column=1,sticky=W)
entry3=Entry(fm ,width = 18,show='*',textvariable=passport)
entry3.grid(row=3,column=1,sticky=W)

#read date
f = file('alist.txt','r')
line = f.readline()
f.close()
if len(line) != 0:
	list1=line.split()
	entyname.set(list1[0])
	account.set(list1[1])
	passport.set(list1[2])
	
def connect2(a,b,c):
	i =3
	dial_params = (a, '', '', b, c, '')
	handle, result=win32ras.Dial(None, None, dial_params, None)	
	#if can't connect,sleep 3s and retry 5 times
	while result !=0 and i !=0:
		time.sleep(2)
		handle, result=win32ras.Dial(None, None, dial_params, None)
		i-=1
	#get ip
	if result == 0:
		try:
			ip_addidas= "连接成功！本机的公网IP是： " + re.search('\d+\.\d+\.\d+\.\d+',urllib2.urlopen("http://www.whereismyip.com").read()).group(0) 
			tkMessageBox.showinfo("",ip_addidas)
	#else show error
		except:
			pass
	tkMessageBox.showinfo("","无法连接")
def connect1():
	f = file('alist.txt','r')
	line = f.readline()
	f.close()
	a=entyname.get()
	b=account.get()
	c=passport.get()
	if len(line) == 0:
		write(a,b,c)
		connect2(a,b,c)
	elif line != a+' '+b+' '+c:
		write(a,b,c)
		connect2(a,b,c)
	else:
		connect2(a,b,c)
		
def write(a,b,c):
	f = file('alist.txt','w')
	f.write(a+' ')
	f.write(b+ ' ')
	f.write(c)
	f.close()
	
def disconnect():
	sts=win32ras.EnumConnections()
	if len(sts) == 0:
		tkMessageBox.showinfo("","无连接")
	else:
		for k in sts:
			try:
				win32ras.HangUp (k[0])
				tkMessageBox.showinfo("","连接中断")
			except:
				tkMessageBox.showinfo("","中断失败")

#set button
b=Button(fm, text="连接",command=connect1)
b.grid(column=0, row=5)
Button(fm, text="断开连接", command=disconnect).grid(column=1, row=5,sticky=E)

for child in fm.winfo_children(): child.grid_configure(padx=5, pady=5)
#focus on button
b.focus_force()
#Enter on button
b.bind("<Return>", lambda event: b.invoke())

master.mainloop()