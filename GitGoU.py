# -*- coding: utf-8 -*-
import argparse
import sys
import os
import subprocess
try:
    import tkinter as tk 
except ImportError:
    import Tkinter as tk
from tkinter import *
from tkinter import scrolledtext


global commits
global messages

#INICIALIZA A JANELA
window = tk.Tk()
window.title("GitGoU")
#window.geometry('800x600')

#cria o LOGO
LOGO = tk.Label(window)
LOGO.grid(column=0, row=0,rowspan=6,columnspan=2,sticky=N+S+E+W)
LOGO.logo = tk.PhotoImage(file="gitgouimg.png")
LOGO['image'] = LOGO.logo

#CRIA O RESULT DA BUSCA
RESULT = scrolledtext.ScrolledText(window,state = 'disabled')
RESULT.grid(column=3, row=6,rowspan=1,columnspan=5,sticky=N+S+E+W)

#CRIA A LISTA DE COMMITS
COMMITS = scrolledtext.ScrolledText(window,state = 'disabled')
COMMITS.grid(column=0, row=6,rowspan=1,columnspan=3,sticky=N+S+E+W)
COMMITS.configure(width=20)

#CRIA O LOG
LOG = Label(window,width=30)
LOG.grid(column=0, row=8,rowspan=1,columnspan=8,sticky=N+S+E+W)

#CRIA OS CAMPOS DE INSERCAO
KEYLB = Label(text="Palavra-chave")
KEYLB.grid(column=2, row=0,rowspan=1,columnspan=1,sticky=N+S+W)
KEY = Entry(window)
KEY.grid(column=3, row=0,rowspan=1,columnspan=4,sticky=N+S+E+W)

AUTHORLB = Label(text="Autor")
AUTHORLB.grid(column=2, row=1,rowspan=1,columnspan=1,sticky=N+S+W)
AUTHOR = Entry(window)
AUTHOR.grid(column=3, row=1,rowspan=1,columnspan=4,sticky=N+S+E+W)

DATELB = Label(text="Data")
DATELB.grid(column=2, row=2,rowspan=1,columnspan=1,sticky=N+S+W)
DATE = Entry(window)
DATE.grid(column=3, row=2,rowspan=1,columnspan=4,sticky=N+S+E+W)

MSGLB = Label(text="Mensagem")
MSGLB.grid(column=2, row=3,rowspan=1,columnspan=1,sticky=N+S+W)
MSG = Entry(window)
MSG.grid(column=3, row=3,rowspan=1,columnspan=4,sticky=N+S+E+W)

ARQUILB = Label(text="Arquivo")
ARQUILB.grid(column=2, row=4,rowspan=1,columnspan=1,sticky=N+S+W)
ARQUI = Entry(window)
ARQUI.grid(column=3, row=4,rowspan=1,columnspan=4,sticky=N+S+E+W)

COMANDLB = Label(text="Parâmetros adicionais")
COMANDLB.grid(column=2, row=5,rowspan=1,columnspan=1,sticky=N+S+W)
COMAND = Entry(window)
COMAND.grid(column=3, row=5,rowspan=1,columnspan=4,sticky=N+S+E+W)

#CRIA BOTOES
def clicked():
	LOG.configure(text="")
	if(KEY.get()!=""):
		search_commits(KEY.get(),ARQUI.get(),AUTHOR.get(),DATE.get(),MSG.get(),COMAND.get())
	else:
		LOG.configure(text="A Palavra não pode estar em branco",font="Helvetica 15 bold",fg="red")
	
def reset_all():
	RESULT.configure(state = 'normal')
	RESULT.delete(0.0,END)
	RESULT.configure(state = 'disabled')
	COMMITS.configure(state = 'normal')
	COMMITS.delete(0.0,END)
	COMMITS.configure(state = 'disabled')
	KEY.delete(0,END)
	AUTHOR.delete(0,END)
	DATE.delete(0,END)
	MSG.delete(0,END)
	ARQUI.delete(0,END)
	COMAND.delete(0,END)


SEARCH = Button(window, text="Filtrar versões", command=clicked)
SEARCH.grid(column=7, row=0,rowspan=5,columnspan=1,sticky=N+S+E+W)

CLEAR = Button(window, text="Limpar parâmentros", command=reset_all)
CLEAR.grid(column=7, row=5,rowspan=1,columnspan=1,sticky=N+S+E+W)

COMMITS.config(cursor="hand2")

def showLink(LINK):
	atual_commit = LINK.widget.tag_names(CURRENT)[0]
	global commits
	global messages
	LOG.configure(text="")
	#commits = subprocess.getoutput(COMAND).split()
	for i in range(len(commits)-1):
		COMMITS.tag_config(commits[i],foreground="blue",font="Helvetica 10")
		if(commits[i]==atual_commit):
			prox=commits[i+1]
	COMMITS.tag_config(atual_commit, foreground="red",font="Helvetica 10 bold")
	RESULT.configure(state = 'normal')
	RESULT.delete(0.0,END)
	KEY_STR=KEY.get()
	arquivos=[]
	arquivos2=[]
	arquivos_aux=subprocess.getoutput("git diff "+prox+" "+atual_commit+" | grep ^\+++").split("\n")
	arquivos_aux2=subprocess.getoutput("git diff "+prox+" "+atual_commit+" | grep ^\---").split("\n")

	subprocess.getoutput('git checkout -f '+prox)
	for i in range(len(arquivos_aux2)):
		if(subprocess.getoutput("ag '"+KEY_STR+"' "+arquivos_aux2[i][6:])!="" and arquivos_aux2[i][6:8]!="evasdf"):
			arquivos2.append(arquivos_aux2[i][6:])

	subprocess.getoutput('git checkout -f '+atual_commit)
	for i in range(len(arquivos_aux)):
		if(subprocess.getoutput("ag '"+KEY_STR+"' "+arquivos_aux[i][6:])!="" and arquivos_aux2[i][6:8]!="evasdf"):
			arquivos.append(arquivos_aux[i][6:])
	if(KEY_STR!=""):
		cabecalho=subprocess.getoutput("git show |grep commit")+"\n"
		cabecalho+=subprocess.getoutput("git show |grep Author")+"\n"
		cabecalho+=subprocess.getoutput("git show |grep Date")+"\n"
		RESULT.insert(END,cabecalho+"\n","cor_cab")
		
		
		for i in arquivos:
			busca=subprocess.getoutput("ag '"+KEY_STR+"' "+i)
			if(busca[0:3]!="ERR"):			
				RESULT.insert(END,"\nArquivo: "+i+"\n","cor_adicionados")
				RESULT.insert(END,busca,"cor_adicionados")

		RESULT.insert(END,"\n\n")
		subprocess.getoutput('git checkout -f '+prox)
		for i in arquivos2:
			busca=subprocess.getoutput("ag '"+KEY_STR+"' "+i)
			if(busca[0:3]!="ERR"):		
				RESULT.insert(END,"\nArquivo: "+i+"\n","cor_removidos")
				RESULT.insert(END,busca,"cor_removidos")
		RESULT.tag_config("cor_cab", foreground="saddle brown",font="Helvetica 10 bold")
		RESULT.tag_config("cor_adicionados", foreground="green",font="Helvetica 10")
		RESULT.tag_config("cor_removidos", foreground="red",font="Helvetica 10")
	else:
		LOG.configure(text="A Palavra KEY é obrigatória",font="Helvetica 15 bold",fg="red")
	RESULT.configure(state = 'disabled')


def search_commits(KEY,file,autor,DATE,msg,adit):
	global commits
	global messages
	subprocess.getoutput('git checkout -f master')
	if(autor!=""):autor=" --author='"+autor+"'"
	if(DATE!=""):DATE=" --since='"+DATE+"'"
	if(msg!=""):msg=" --grep '"+msg+"'"
	if(file!=""):file=" -- '*"+file+"'"
	if(adit!=""):adit=" "+adit
	print('git log --pretty=format:"%s"'+autor+DATE+file+msg+adit)
	messages = subprocess.getoutput('git log --pretty=format:"%s"'+autor+DATE+file+msg+adit).split('\n')
	commits = subprocess.getoutput('git log --pretty=format:"%H"'+autor+DATE+file+msg+adit).split('\n')
	COMMITS.configure(state = 'normal')
	COMMITS.delete(0.0,END)
	for i in range(len(commits)-1):
		if(subprocess.getoutput("git diff "+commits[i+1]+" "+commits[i]+" | grep ^\[+-] | grep "+KEY)!=""):
			COMMITS.insert(END, messages[i]+"\n",commits[i])
			COMMITS.tag_config(commits[i], foreground="blue",font="Helvetica 10")
			COMMITS.tag_bind(commits[i], '<Button-1>', showLink)

	if(len(commits)==1):
		COMMITS.insert(END, messages[0]+"\n",commits[0])
		COMMITS.tag_config(commits[0], foreground="blue",font="Helvetica 10")
		COMMITS.tag_bind(commits[0], '<Button-1>', search_all)
	COMMITS.configure(state = 'disabled')

def search_all(LINK):
	atual_commit = LINK.widget.tag_names(CURRENT)[0]
	global commits
	global messages
	LOG.configure(text="")
	for i in range(len(commits)):
		COMMITS.tag_config(commits[i],foreground="blue",font="Helvetica 10")
	COMMITS.tag_config(atual_commit, foreground="red",font="Helvetica 10 bold")
	RESULT.configure(state = 'normal')
	RESULT.delete(0.0,END)
	cabecalho=subprocess.getoutput("git show |grep commit")+"\n"
	cabecalho+=subprocess.getoutput("git show |grep Author")+"\n"
	cabecalho+=subprocess.getoutput("git show |grep Date")+"\n"
	RESULT.insert(END,cabecalho+"\n","cor_cab")
	RESULT.tag_config("cor_cab", foreground="saddle brown",font="Helvetica 10 bold")
	KEY_STR=KEY.get()
	subprocess.getoutput('git checkout -f '+atual_commit)
	if(KEY_STR!=""):
		result=subprocess.getoutput("ag '"+KEY_STR+"'").split("\n")
		for i in result:
			RESULT.insert(END,i+"\n")
	RESULT.configure(state = 'disabled')


if __name__ == "__main__":
    #subprocess.getoutput('sudo apt-get install silversearcher-ag')
    global commits
    commits = []

    window.mainloop()
