import sqlite3,xlrd,datetime
from tkinter import Tk, StringVar, Label, Entry, Button, Checkbutton, IntVar , Pack , Toplevel , Radiobutton,RADIOBUTTON
from functools import partial
import math
import tkinter.font as tkFont # ou «import TkFont» pour python 2
import random
import _random
import copy

def CheckDomainAllFunction(CheckDomainAll,CheckDomain):
    # set / unset all buttons for Domain
    for i in range(len(CheckDomain)):
      CheckDomain[i].set(CheckDomainAll.get())


def EraseDB(db):
    LabelPreviousFraPal = str
    LabelPreviousEspPal = str
    cursor=db.cursor()
    cursor.execute("""DROP TABLE vocabularios""")
    db.commit()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vocabularios(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        fecha DATE,
        palabra TEXT,
        traduction TEXT,
        type TEXT ,
        genre TEXT ,
        domaine TEXT,
        level INTEGER
    )""")

def LoadDB(filename,db):
    # Give the location of the file
    cursor = db.cursor()
    # To open Workbook
    wb = xlrd.open_workbook(filename)
    sheet = wb.sheet_by_name("palabras")
    for ligne in range (1,sheet.nrows):
       # For row 0 and column 0
       inputrec = []
       inputrec.append(sheet.cell_value(ligne, 1))
       inputrec.append(sheet.cell_value(ligne, 2))
       inputrec.append(sheet.cell_value(ligne, 3))
       inputrec.append(sheet.cell_value(ligne, 4))
       inputrec.append(sheet.cell_value(ligne, 5))
       inputrec.append(sheet.cell_value(ligne, 6))
       inputrec.append(datetime.datetime(*xlrd.xldate.xldate_as_tuple(sheet.cell_value(ligne, 0),wb.datemode)))
       rc = cursor.execute("""INSERT INTO vocabularios(palabra,traduction,type,genre,domaine,level,fecha) VALUES(?,?,?,?,?,?,?)""",inputrec)





def CheckFechaAllFunction(CheckFechaAll,CheckFecha):
    # set / unset all buttons for Fecha
     for i in range(len(CheckFecha)):
        CheckFecha[i].set(CheckFechaAll.get())



def Next (label,LabelPreviousFra,LabelPreviousEsp, text,cursor, CheckDomain,ListDomain,CheckLevel,ListLevel,CheckFecha,ListFecha,varGr):
    print(" dans next" )
    global LabelPreviousFraPal
    global LabelPreviousEspPal
    LabelPreviousEsp.config(text=LabelPreviousEspPal)
    LabelPreviousFra.config(text=LabelPreviousFraPal)

    SelectDomain = "("
    for i in range(len(ListDomain)):
        if CheckDomain[i].get()== 1 :
#           print("domaine selectionné : ", ListDomain[i][0])
            SelectDomain=SelectDomain+ "'"+ ListDomain[i][0]+"'"+","
#            print("Selected Domain",SelectDomain)
    SelectDomain = SelectDomain + "'kiki')"
    SelectLevel = "("
    for i in range(len(ListLevel)):
        if CheckLevel[i].get()== 1 :
 #           print("Level selectionné : ", ListLevel[i][0])
            SelectLevel = SelectLevel+ "'" + str(ListLevel[i][0]) + "',"
 #           print("Selected Level",SelectLevel)
    SelectLevel=SelectLevel+"'kiki')"

    SelectFecha = "("
    for i in range(len(ListFecha)):
        if CheckFecha[i].get() == 1:
            #           print("Level selectionné : ", ListLevel[i][0])
            SelectFecha = SelectFecha + "'" + str(ListFecha[i][0]) + "',"
    #           print("Selected Level",SelectLevel)
    SelectFecha = SelectFecha + "'kiki')"
    print(" Selectfecha ",SelectFecha)
    Query = "SELECT * from vocabularios  where domaine in " + SelectDomain + " and level in " + SelectLevel + " and fecha in " + SelectFecha
    print("query=", Query)
    cursor.execute(Query)
    Palabra = cursor.fetchall()
    PalabraLen= len(Palabra)
    if PalabraLen == 0 :
        PalabraSelectada="Nadita de nada selectado"
        print("Palabra Selectada =", PalabraSelectada)
        label.config(text="nadita selectado !")
    else :
        iSelectado = random.randint(0, PalabraLen - 1)
        PalabraSelectada = Palabra[iSelectado]
        print("Total = ",PalabraLen," Selectado =  ", iSelectado)
 #       print("Palabra Selectada =",PalabraSelectada)
 #       print("varGr=",varGr.get())
        if varGr.get()=='ES':
          label.config(text=PalabraSelectada[2])
          LabelPreviousFraPal = PalabraSelectada[3]
          LabelPreviousEspPal = PalabraSelectada[2]
        else:
          label.config(text=PalabraSelectada[3])
          LabelPreviousFraPal=PalabraSelectada[2]
          LabelPreviousEspPal = PalabraSelectada[3]


XLpath="C:"+"\\"+"Drives"+"\\"+"G_drive"+ "\\"+"kutta75"+"\\"+"kutta75d"+"\\"+"MOOC"+"\\"+"2020-10-Espanol"
XLpath="C:"+"\\"+"Drives"+"\\"+"Google"+"\\"+"kutta75d"+"\\"+"MOOC"+"\\"+"2020-10-Espanol"
db=sqlite3.connect('vocabularios.db')
#XLFILE= ("C:"+"\\"+"drive"+"\\"+"Google"+"\\"+"kutta75d"+"\\"+"MOOC"+"\\"+"2020-10-Espanol"+"\\"+"vocabulaire.xlsx")
XLFILE= XLpath + "\\"+"vocabulaire.xlsx"

EraseDB(db)
LoadDB(XLFILE,db)

cursor=db.cursor()

# preparation des inserts sql pour charger les textes
#myfile= "C:"+"\\"+"drive"+"\\"+"Google"+ "\\"+"kutta75d"+"\\"+"MOOC"+"\\"+"2020-10-Espanol"+"\\"+"palabra.sql"
myfile= XLpath+ "\\"+"palabra.sql"

outputfile= open(myfile,"w",encoding='utf8')

# 1 palabratipo
freccord = " delete from verbos_palabratipo ; "
outputfile.write(str(freccord)+"\n")
Query = "select type from vocabularios group by type"
rc=cursor.execute(Query)
ListAll= cursor.fetchall()
for i in range(0,len(ListAll)):
    freccord = "Insert into verbos_palabratipo   (palabratipo) values ("+ "'" + ListAll[i][0] + "'" + ");"
    outputfile.write(str(freccord)+"\n")

# palabragenero
freccord = " delete from verbos_palabragenero ; "
outputfile.write(str(freccord)+"\n")
Query = "select genre  from vocabularios group by genre"
rc=cursor.execute(Query)
ListAll= cursor.fetchall()
for i in range(0,len(ListAll)):
    freccord = "Insert into verbos_palabragenero  (palabragenero) values ("+ "'" + ListAll[i][0] + "'" + ");"
    outputfile.write(str(freccord)+"\n")

# palabranivel
freccord = " delete from verbos_palabranivel ; "
outputfile.write(str(freccord)+"\n")
Query = "select level  from vocabularios group by level"
rc=cursor.execute(Query)
ListAll= cursor.fetchall()
for i in range(0,len(ListAll)):
    freccord = "Insert into verbos_palabranivel  (palabranivel) values ("+ "'" + str(ListAll[i][0]) + "'" + ");"
    outputfile.write(str(freccord)+"\n")


# chargement des domaines qui deviennent palabrafamilia
freccord = " delete from verbos_palabrafamilia ; "
outputfile.write(str(freccord)+"\n")
Query = "select domaine  from vocabularios group by domaine"
rc=cursor.execute(Query)
ListAll= cursor.fetchall()
for i in range(0,len(ListAll)):

    freccord = "Insert into verbos_palabrafamilia  (palabrafamilia) values ("+ "'" + ListAll[i][0] + "'" + ");"
#    freccord = ListAll[i][0]+";"+ListAll[i][1]+";"+ListAll[i][2]+";"+ListAll[i][3]+";"+ListAll[i][4]+";"+str(ListAll[i][5])
    outputfile.write(str(freccord)+"\n")

# palabrafecha
freccord = " delete from verbos_palabrafecha ; "
outputfile.write(str(freccord)+"\n")
Query = "select fecha from vocabularios group by fecha"
rc=cursor.execute(Query)
ListAll= cursor.fetchall()
for i in range(0,len(ListAll)):
    sqldate = ListAll[i][0]
    print("sqldate=" + sqldate)
    #      sqlannee = sqldate.split("/")[2]
    #  sqlmois = sqldate.split("/")[1]
    #  sqljour = sqldate.split("/")[0]
    #  sqldate= ListAll[i][0].split("/")[2] + "-" + ListAll[i][0].split("/")[1] + "-" + ListAll[i][0].split("/")[0] + " 18:30:00.0"
    freccord = "Insert into verbos_palabrafecha   (palabrafecha) values ("+ "'" + ListAll[i][0] + "'" + ");"
#    freccord = "Insert into verbos_palabrafecha   (palabrafecha) values ("+ "'" + sqldate + "'" + ");"
#    freccord = ListAll[i][0]+";"+ListAll[i][1]+";"+ListAll[i][2]+";"+ListAll[i][3]+";"+ListAll[i][4]+";"+str(ListAll[i][5])
    outputfile.write(str(freccord)+"\n")






#  chargement des mots + rege aux tables

freccord = " delete from verbos_palabra ; "
outputfile.write(str(freccord)+"\n")
Query = "Select palabra, traduction, fecha , type , genre, domaine, level from vocabularios"
rc=cursor.execute(Query)
ListAll= cursor.fetchall()
for i in range(0,len(ListAll)):
#   freccord = ListAll[i][0]
    freccord = "Insert into verbos_palabra  ( palabra , traduccion, palabrafecha_id , palabratipo_id, palabragenero_id, palabrafamilia_id, palabranivel_id ) values  "  + \
               "('" + ListAll[i][0] + "' , '" + ListAll[i][1] + "',"  + \
                "(SELECT id FROM  verbos_palabrafecha   WHERE palabrafecha    = '" + ListAll[i][2]  + "')," + \
                "(SELECT id FROM  verbos_palabratipo    WHERE palabratipo     = '" + ListAll[i][3] + "'),"  + \
                "(SELECT id FROM  verbos_palabragenero  WHERE palabragenero   = '" + ListAll[i][4] + "')," + \
                "(SELECT id FROM  verbos_palabrafamilia WHERE palabrafamilia  = '" + ListAll[i][5] + "')," + \
                "(SELECT id FROM  verbos_palabranivel   WHERE palabranivel    = '" + str(ListAll[i][6]) + "')" + \
                                                                                             "); "
    outputfile.write(str(freccord)+"\n")
#              "(SELECT id FROM  verbos_palabrafecha   WHERE palabrafecha    = '" + ListAll[i][2].split("/")[2] + "-" + ListAll[i][2].split("/")[1] + "-" + ListAll[i][2].split("/")[0] + " 18:30:00.0" + "')," +
outputfile.close()

domain=("casa","ropa")
level = 0
cursor.execute("""SELECT domaine,count(domaine)  from vocabularios group by domaine  """)
ListDomain = cursor.fetchall()
print("domaine=",ListDomain)
print("nombre de domaine =",len(ListDomain))

cursor.execute("""SELECT level,count(level) from vocabularios group by level  """)
ListLevel = cursor.fetchall()
print("level=",ListLevel)

cursor.execute("""SELECT fecha,count(fecha) from vocabularios group by fecha  """)
ListFecha = cursor.fetchall()
print("Fecha=",ListFecha)

query= "SELECT * from vocabularios  where domaine in "+ str(domain)
print("query=",query )
cursor.execute(query)
palabra1=cursor.fetchall()
print("palabra =",palabra1)
# db.close()
gui = Tk(className='Vocabulario-Palabras')
MyFont = tkFont.Font(size=11)
# set window size
Y=20+len(ListDomain)*30
Yc=str(Y)
XY="400x" + Yc
print("XY=",XY)
gui.geometry(XY)

label=Label(gui,text="Estas listo ?  ",font=MyFont)
text = StringVar(gui)
LabelPreviousEsp=Label(gui,text="",font=MyFont)
LabelPreviousFra=Label(gui,text="",font=MyFont)


CheckDomain = []
CheckDomainButton = []
CheckDomainAll = IntVar()
CheckDomainAll.set(1)
CheckDomainButtonAll=Checkbutton(gui, text = "todos" , variable = CheckDomainAll, onvalue = 1, offvalue = 0,font=MyFont,command=partial(CheckDomainAllFunction,CheckDomainAll,CheckDomain))
CheckDomainButtonAll.grid(column=2, row=6, sticky="W")
i=0
for dom in ListDomain:
    print("keys=",i,dom)
    CheckDomain.append(IntVar())
    CheckDomainButton.append(Checkbutton())
    CheckDomain[i].set(1)
    CheckDomainButton[i]=Checkbutton(gui, text =dom[0]+" ("+str(dom[1])+")", variable = CheckDomain[i], onvalue = 1, offvalue = 0,font=MyFont)
    CheckDomainButton[i].grid(column=2, row=i+7, sticky="W")
    i=i+1
CheckLevel = []
CheckLevelButton = []
j=0
for level in ListLevel:
    print("level=",j,level)
    CheckLevel.append(IntVar())
    CheckLevelButton.append(Checkbutton())
    CheckLevel[j].set(1)
    CheckLevelButton[j]=Checkbutton(gui, text ="level "+ str(level[0]) +" ("+str(level[1])+")", variable = CheckLevel[j], onvalue = 1, offvalue = 0,font=MyFont)
    CheckLevelButton[j].grid(column=1, row=j+8, sticky="W")
    j=j+1

CheckFecha = []
CheckFechaButton = []
CheckFechaAll = IntVar()
CheckFechaAll.set(1)
CheckFechaButtonAll=Checkbutton(gui, text = "todos" , variable = CheckFechaAll, onvalue = 1, offvalue = 0,font=MyFont,command=partial(CheckFechaAllFunction,CheckFechaAll,CheckFecha))
CheckFechaButtonAll.grid(column=3, row=6, sticky="W")
k=0
for fecha in ListFecha:
    print("Fecha=",k,fecha)
    CheckFecha.append(IntVar())
    CheckFechaButton.append(Checkbutton())
    CheckFecha[k].set(1)
    CheckFechaButton[k]=Checkbutton(gui, text =str(fecha[0]) +" ("+str(fecha[1])+")", variable = CheckFecha[k], onvalue = 1, offvalue = 0,font=MyFont)
    CheckFechaButton[k].grid(column=3, row=k+7, sticky="W")
    k=k+1
# sens de l'exercice ES vers FR ou FR vers ES
vals = ['ES', 'FR']
etiqs = ['ES->FR?', 'FR->ES?']
varGr = StringVar()
varGr.set(vals[1])
for i in range(2):
    b = Radiobutton(gui, variable=varGr, text=etiqs[i], value=vals[i],font=MyFont)
    b.grid(column=1,row=2+i,sticky="W")
# preparation de la query avec les critères selectionnés
# sur les domaines
NextButton = Button(gui, text='Next',command=partial(Next, label,LabelPreviousFra,LabelPreviousEsp, text,cursor, CheckDomain,ListDomain,CheckLevel,ListLevel,CheckFecha,ListFecha,varGr),font=MyFont)
NextButton.grid(column=1,row=1,sticky="W")



label.grid(column=2,row=1,sticky="W")
LabelPreviousEsp.grid(column=2,row=2,sticky="W")
LabelPreviousFra.grid(column=3,row=2,sticky="W")
gui.mainloop()

