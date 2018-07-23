try:
	# for Python2
	from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
	# for Python3
	from tkinter import * 
# from tables import *
from tkintertable import TableCanvas, TableModel
from PIL import Image,ImageTk
import MySQLdb
import time
import tkMessageBox
import ttk
import tkFileDialog,random,string
from time import asctime
from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import path,listdir
from os.path import isfile, join
import time
import imghdr

aa= MySQLdb.connect(host='127.0.0.1',port= 3306,user="root",passwd="root",db="kitpage1",autocommit=True)
mm = aa.cursor()

class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

gw = '#134e86'
g="#0a2845"
gg ="white"
text=''
filekey=''
privatekey=''
pk=''
t=''

def viewd():
	R3.destroy()
	viewupload()

def viewda():
	R2.destroy()
	viewdata()

def viewdata():
	def update_data():
		if privatekey:
			pk=privatekey.get()
		if text:
			t=text.get('1.0', 'end-1c')
		key = pk+'**********'
		enc = Encryptor(key)

		t=enc.encrypt(t,key)

		ok=mm.execute('UPDATE upload_data SET datas = "{}" WHERE filekey = "{}"'.format(t,pk))
		if ok:	
			tkMessageBox.showinfo("Success" , "your data updated Successfully")
		else:
			tkMessageBox.showinfo("Failed" , "your privatekey is unknown")

	def viewuploads():
		if privatekey:
			pk=privatekey.get()
		ok=mm.execute('select datas,filetype,filename from upload_data where filekey = "{}"'.format(pk))
		if ok:
			datas =mm.fetchone()
			key = pk+'**********'
			enc = Encryptor(key)
			s=enc.decrypt(datas[0],key)

			if datas[1] == 'Doc':
				text = Text(R4)
				text.insert(INSERT,s )
				global text
				text.place(x=50,y=150)
			else:
				image1 = PhotoImage(file=datas[2])
				pic = Label(R4,image=image1,font=("Arial Bold", 100))
				pic.photo = image1
				pic.place(x=100,y=20)
		else:
			tkMessageBox.showinfo("Failed" , "your privatekey is unknown")

	global R4
	R4 = Tk()
	img = PhotoImage(file='cloud.png')
	R4.tk.call('wm', 'iconphoto', R4._w, img)
	R4.geometry('712x712')
	R4.title('View File Now')
	R4.resizable(width = FALSE ,height= FALSE)
	Image_open = Image.open("kitsignup.png")
	image = ImageTk.PhotoImage(Image_open)
	sigup = Label(R4,image=image,bg=gg)
	sigup.place(x=0,y=0,bordermode="outside")
	label3= Label(R4,text="Oruta:Privacy Preserving Public Auditing for Shared Data in the Cloud",font=("Arial Bold", 9),fg="#0157f8")
	label3.place(x=150,y=10)
	privatekey = Label(R4,text="Enter Privatekey",font=("Arial Bold", 15),bg="#05c4fb")
	privatekey.place(x=10,y=120)
	privatekey=Entry(R4,width=15,font=("bold",15),highlightthickness=2,bg=gg,relief=SUNKEN)
	privatekey.place(x=190,y= 120 )
	global privatekey
	viewbtn1 = Button(R4,text = "View Blocks",width=10,height=1,bg=g,fg="white",font="5",relief=RAISED,overrelief=RIDGE,command=viewuploads)
	updatebtn1 = Button(R4,text = "Update",width=10,height=1,bg=g,fg="white",font="5",relief=RAISED,overrelief=RIDGE,command=update_data)
	backbtn = Button(R4,text = "Back to home",width=10,height=1,bg=g,fg="white",font="5",relief=RAISED,overrelief=RIDGE,command=home)
	viewbtn1.place(x =100 ,y=550)
	updatebtn1.place( x =300,y=550)
	backbtn.place(x=500,y=550)
	R4.mainloop()

def viewupload():
	key = filekey+'**********'
	enc = Encryptor(key)
	def update_data():
		t=text.get('1.0', 'end-1c')
		t=enc.encrypt(t,key)
		ok=mm.execute('UPDATE upload_data SET datas = "{}" WHERE filekey = "{}"'.format(t,filekey))
		if ok:	
			tkMessageBox.showinfo("Success" , "your data updated Successfully")
		else:
			tkMessageBox.showinfo("Failed" , "your privatekey is unknown")

	def viewuploads():
		ok=mm.execute('select datas,filetype,filename from upload_data where filekey = "{}"'.format(filekey))
		if ok:
			datas =mm.fetchone()
			s=enc.decrypt(datas[0],key)
			if datas[1] == 'Doc':
				text = Text(R4)
				text.insert(INSERT,s )
				global text
				text.place(x=50,y=150)
			else:
				image1 = PhotoImage(file=datas[2])
				pic = Label(R4,image=image1,font=("Arial Bold", 100))
				pic.photo = image1
				pic.place(x=100,y=20)
		else:
			tkMessageBox.showinfo("Failed" , "your privatekey is unknown")

	global R4
	R4 = Tk()
	img = PhotoImage(file='cloud.png')
	R4.tk.call('wm', 'iconphoto', R4._w, img)
	R4.geometry('712x712')
	R4.title('View File Now')
	R4.resizable(width = FALSE ,height= FALSE)
	Image_open = Image.open("kitsignup.png")
	image = ImageTk.PhotoImage(Image_open)
	sigup = Label(R4,image=image,bg=gg)
	sigup.place(x=0,y=0,bordermode="outside")
	label3= Label(R4,text="Oruta:Privacy Preserving Public Auditing for Shared Data in the Cloud",font=("Arial Bold", 9),fg="#0157f8")
	label3.place(x=150,y=10)
	label1= Label(R4,text="View File Now",font=("Arial Bold", 15),bg="#05c4fb")
	label1.place(x=240,y=80)
	viewbtn1 = Button(R4,text = "View Blocks",width=10,height=1,bg=g,fg="white",font="5",relief=RAISED,overrelief=RIDGE,command=viewuploads)
	updatebtn1 = Button(R4,text = "Update",width=10,height=1,bg=g,fg="white",font="5",relief=RAISED,overrelief=RIDGE,command=update_data)
	backbtn = Button(R4,text = "Back to home",width=10,height=1,bg=g,fg="white",font="5",relief=RAISED,overrelief=RIDGE,command=home)
	viewbtn1.place(x =100 ,y=500)
	updatebtn1.place( x =300,y=500)
	backbtn.place(x=500,y=500)
	R4.mainloop()

def deupload():
	R2.destroy()
	upload()

def upload():
	def uploads():
		filekey=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
		global filekey
		R3.filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files","*.*"),("jpeg files","*.jpg")))
		fn=R3.filename
		f = open(fn, 'rb')
		global da
		da = f.read()
		key = filekey+'**********'
		enc = Encryptor(key)
		da=enc.encrypt(da,key)
		filenames = fn
		t=asctime()
		v = StringVar(R3, value=filenames)
		v1 = StringVar(R3, value=filekey)
		v2 = StringVar(R3, value=t)
		label1= Label(R3,text="Select File Now",state='disabled',font=("Arial Bold", 15),bg="#05c4fb",fg="#05c4fb")
		label1.place(x=100,y=350)
		filebtn = Button(R3,text = "Click",state='disabled',width=8,height=1,bg="#0071f5",fg="white",font="5",relief=RAISED,overrelief=RIDGE)
		filebtn.place(x =280 ,y=350)
		filename1 = Label(R3,text="Filename",font=("Arial Bold", 15),bg="#05c4fb")
		filename1.place(x=10,y=162)
		privatekey = Label(R3,text="Privatekey",font=("Arial Bold", 15),bg="#05c4fb")
		privatekey.place(x=10,y=222)
		uploaddate = Label(R3,text="Uploaddate",font=("Arial Bold", 15),bg="#0087fc")
		uploaddate.place(x=10,y=282)
		filename1=Entry(R3,width=15,textvariable=v,font=("bold",15),highlightthickness=2,bg=gg,relief=SUNKEN)
		filename1.place(x=135,y= 160 )
		privatekey=Entry(R3,width=15,textvariable=v1,font=("bold",15),highlightthickness=2,bg=gg,relief=SUNKEN)
		privatekey.place(x=135,y= 220 )
		uploaddate=Entry(R3,width=15,textvariable=v2,font=("bold",15),highlightthickness=2,bg=gg,relief=SUNKEN)
		uploaddate.place(x=135,y= 280 )

		def upload_data():
			filename_u=filename1.get()
			privatekey_u=privatekey.get()
			uploaddate_u=str(uploaddate.get())
			mm.execute('select * from singupc1 where email LIKE  %s ', [Email])
			data=mm.fetchone()
			mm.execute("CREATE TABLE IF NOT EXISTS upload_data (id int(11) NOT NULL AUTO_INCREMENT, filename varchar(100) not null,  filetype varchar(100) not null,datas varchar(10000), filekey varchar(100) not null,uploaddate varchar(100) not null,userid int(11) NOT NULL,PRIMARY KEY (id),  FOREIGN KEY (userid) REFERENCES singupc1(id))")
			check=imghdr.what(fn)
			if check:
				filetype='Image'
			else:
				filetype='Doc'
			ok=mm.execute('insert into upload_data (filename,filetype,datas,filekey,uploaddate,userid) values (%s,%s,%s,%s,%s,%s)',(filename_u,filetype,da,privatekey_u,uploaddate_u,int(data[0])))
			if ok:
				tkMessageBox.showinfo("Success" , "your data uploaded Successfully & click back button to view or update File")
				viewd()
			else:
				tkMessageBox.showinfo("Failed" , "Big file not uploaded ")
			
		uploadbtn = Button(R3,text = "Upload",width=8,height=1,bg=g,fg="white",font="5",relief=RAISED,overrelief=RIDGE,command=upload_data)
		uploadbtn.place(x =360 ,y=280)

	global R3
	R3 = Tk()
	img = PhotoImage(file='cloud.png')
	R3.tk.call('wm', 'iconphoto', R3._w, img)
	R3.geometry('712x712')
	R3.title('Upload Now')
	R3.resizable(width = FALSE ,height= FALSE)
	Image_open = Image.open("kitsignup.png")
	image = ImageTk.PhotoImage(Image_open)
	sigup = Label(R3,image=image,bg=gg)
	sigup.place(x=0,y=0,bordermode="outside")
	label3= Label(R3,text="Oruta:Privacy Preserving Public Auditing for Shared Data in the Cloud",font=("Arial Bold", 9),fg="#0157f8")
	label3.place(x=150,y=10)
	label1= Label(R3,text="Upload File Now",font=("Arial Bold", 15),bg="#05c4fb")
	label1.place(x=240,y=80)
	label1= Label(R3,text="Select File Now",font=("Arial Bold", 15),bg="#05c4fb")
	label1.place(x=100,y=350)
	filebtn = Button(R3,text = "Click",width=8,height=1,bg=g,fg="white",font="5",relief=RAISED,overrelief=RIDGE,command=uploads)
	filebtn.place(x =280 ,y=350)
	R3.mainloop()

def desigup():
	R.destroy()
	sigup()

def sigup():
	def Sigups():
		firstnames = firstname.get()
		lastnames = lastname.get()
		Emails = Email.get()
		passwords = password.get()
		if firstnames == '' and lastnames == '' and Emails == '' and passwords == '':
			tkMessageBox.showinfo("Sorry" , "Please fill all information")
		else:
			mm.execute("CREATE TABLE IF NOT EXISTS singupc1 (id int(20) NOT NULL AUTO_INCREMENT, firstname varchar(30) not null,lastname varchar(20),email varchar(30) not null, password varchar(30) not null,PRIMARY KEY (id))")
			mm.execute(" SELECT * FROM singupc1 WHERE email LIKE %s ",[Emails])
			d=mm.fetchone()
			if d:
				tkMessageBox.showinfo("Try Again", "User Already Exist")
			else:
				mm.execute("""INSERT INTO singupc1 (firstname,lastname,email,password) VALUES (%s,%s,%s,%s)""",(firstnames,lastnames,Emails,passwords))
				tkMessageBox.showinfo("Let Login", "Welcome  %s" %firstnames)
				deslogin()
			
	global R1
	R1 = Tk()
	img = PhotoImage(file='cloud.png')
	R1.tk.call('wm', 'iconphoto', R1._w, img)
	R1.geometry('712x712')
	R1.title('SigUp Now')
	R1.resizable(width = FALSE ,height= FALSE)
	Image_open = Image.open("kitsignup.png")
	image = ImageTk.PhotoImage(Image_open)
	sigup = Label(R1,image=image,bg=gg)
	sigup.place(x=0,y=0,bordermode="outside")
	label3= Label(R1,text="Oruta:Privacy Preserving Public Auditing for Shared Data in the Cloud",font=("Arial Bold", 9),fg="#0157f8")
	label3.place(x=150,y=10)
	label1= Label(R1,text="Create My Cloud Account",font=("Arial Bold", 15),bg="#05c4fb")
	label1.place(x=240,y=80)
	firstname = Label(R1,text="Firstname",font=("Arial Bold", 15),bg="#05c4fb")
	firstname.place(x=100,y=162)
	lastname = Label(R1,text="Lastname",font=("Arial Bold", 15),bg="#05c4fb")
	lastname.place(x=100,y=222)
	Email = Label(R1,text="Email",font=("Arial Bold", 15),bg="#0087fc")
	Email.place(x=100,y=282)
	password = Label(R1,text="Password",font=("Arial Bold", 15),bg="#007dfb")
	password.place(x=100,y=342)
	firstname=Entry(R1,width=20,font=("bold",15),highlightthickness=2,bg=gg,relief=SUNKEN)
	firstname.place(x=242,y= 160 )
	lastname=Entry(R1,width=20,font=("bold",15),highlightthickness=2,bg=gg,relief=SUNKEN)
	lastname.place(x=242,y= 220 )
	Email=Entry(R1,width=20,font=("bold",15),highlightthickness=2,bg=gg,relief=SUNKEN)
	Email.place(x=242,y= 280 )
	password=Entry(R1,width=20,show="*",font=("bold",15),highlightthickness=2,bg=gg,relief=SUNKEN)
	password.place(x=242,y=340 )
	loginbt = Button(R1,text = "Login",width=10,height=2,bg=g,fg="white",font="5",relief=RAISED,overrelief=RIDGE,command=deslogin)
	signUpbt = Button(R1,text = "SignUp",width=10,height=2,bg=g,fg="white",font="5",relief=RAISED,overrelief=RIDGE,command=Sigups)
	loginbt.place(x =225 ,y=450)
	signUpbt.place( x =400,y=450)
	R1.mainloop()

R4=''
def logout1():
	R2.destroy()
	login()

def home():
	if R4:
		R4.destroy()

	global R2
	R2=Tk()
	img = PhotoImage(file='cloud.png')
	R2.tk.call('wm', 'iconphoto', R2._w, img)
	R2.geometry('712x712')
	R2.title('Welcome to Our Cloud')
	R2.resizable(height=FALSE,width=FALSE)
	Image_open = Image.open('kitsignup.png')
	image = ImageTk.PhotoImage(Image_open)
	sigup1 = Label(R2,image=image,bg=gg)
	sigup1.place(x=0,y=0,bordermode="outside")
	Image_open = Image.open('q3.png')
	image1 = ImageTk.PhotoImage(Image_open)
	pic = Label(R2,image=image1)
	pic.place(x=80,y=110)
	logout = Button(R2,text = "Logout",width=10,height=1,bg=g,fg="white",font="5",relief=RAISED,overrelief=RIDGE,command = logout1)
	logout.place(x=500,y=50)
	label4= Label(R2,text="Oruta:Privacy Preserving Public Auditing for Shared Data in the Cloud",font=("Arial Bold", 9),fg="#0157f8")
	label4.place(x=150,y=10)
	label5= Label(R2,text="Data Owner",font=("Arial Bold", 15),bg="#05c4fb")
	label5.place(x=300,y=50)
	uploadbtn = Button(R2,text = "Upload Blocks",width=10,height=1,bg=g,fg="white",font="5",relief=RAISED,overrelief=RIDGE,command = deupload)
	updatebtn = Button(R2,text = "Update",width=10,height=1,bg=g,fg="white",font="5",relief=RAISED,overrelief=RIDGE,command=viewda)
	enduserbtn = Button(R2,text = "End User",width=10,height=1,bg=g,fg="white",font="5",relief=RAISED,overrelief=RIDGE)
	uploadbtn.place(x =100 ,y=500)
	updatebtn.place( x =300,y=500)
	enduserbtn.place(x=500,y=500)
	R2.mainloop()

def login():
	def loginto():
		global Email
		Email = e1.get()
		password = e2.get()
		mm.execute('SELECT * FROM singupc1 WHERE email LIKE %s AND password = %s', (Email, password))
		d=mm.fetchone()
		if d:
			tkMessageBox.showinfo("Let GO", "Welcome  %s" %Email)
			R.destroy()
			home()
		else:
			tkMessageBox.showinfo("Sorry" , "User Doesn't Exist")

	global R
	R = Tk()
	img = PhotoImage(file='cloud.png')
	R.tk.call('wm', 'iconphoto', R._w, img)
	R.geometry('720x720')
	R.title('Login')
	R.resizable(width = FALSE ,height= FALSE)
	Image_open = Image.open("kitsignup.png")
	image = ImageTk.PhotoImage(Image_open)
	logo = Label(R,image=image,bg=gg)
	logo.place(x=0,y=0,bordermode="outside")
	label3= Label(R,text="Oruta:Privacy Preserving Public Auditing for Shared Data in the Cloud",font=("Arial Bold", 9),fg="#0157f8")
	label3.place(x=150,y=10)
	label2= Label(R,text="Login Your Account",font=("Arial Bold", 15),bg="#05c4fb")
	label2.place(x=220,y=220)
	Email = Label(R,text="Email",font=("Arial Bold", 15),bg="#0087fc")
	Email.place(x=180,y=300)
	password = Label(R,text="Password",font=("Arial Bold", 15),bg="#0087fc")
	password.place(x=180,y=360)
	e1=Entry(R,width=15,font=("bold",15),highlightthickness=2,bg=gg,relief=SUNKEN)
	e1.place(x=300,y=300 )
	e2=Entry(R,width=15,show="*",font=("bold",15),highlightthickness=2,bg=gg,relief=SUNKEN)
	e2.place(x=300,y=360 )
	loginbt = Button(R,text = "Login",width=8,height=1,bg=g,fg="white",font="5",relief=RAISED,overrelief=RIDGE,command = loginto)
	signUpbt = Button(R,text = "SignUp",width=8,height=1,bg=g,fg="white",font="5",relief=RAISED,overrelief=RIDGE,command=desigup)
	loginbt.place(x =200 ,y=440)
	signUpbt.place( x =350,y=440)
	R.mainloop()

def deslogin():
	R1.destroy()
	login()

sigup()