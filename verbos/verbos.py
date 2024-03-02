# programme de tranformation d'un fichier xl des conjugaison de verbes en espagnol ver
# 1) un fichier d'insert sql dans une base
# 2) une ihm posant des questions  facon exercices sur ces verbes
#
# derniere maj  : le 02/04/22

import sqlite3
import sqlite3,xlrd,datetime
from tkinter import Tk, StringVar, Label, Entry, Button, Checkbutton, IntVar , Pack , Toplevel , Radiobutton,RADIOBUTTON,END
from functools import partial
import math
import tkinter.font as tkFont # ou «import TkFont» pour python 2
import random
import _random
import copy

def CheckTiempoAllFunction(CheckTiempoAll,CheckTiempo):
    # set / unset all buttons for Tiempo
    for i in range(len(CheckTiempo)):
      CheckTiempo[i].set(CheckTiempoAll.get())



def CheckPronombreAllFunction(CheckPronombreAll,CheckPronombre):
    # set / unset all buttons for Pronombre
     for i in range(len(CheckPronombre)):
        CheckPronombre[i].set(CheckPronombreAll.get())

def CheckTipoAllFunction(CheckTipoAll,CheckTipo):
    # set / unset all buttons for Pronombre
     for i in range(len(CheckTipo)):
        CheckTipo[i].set(CheckTipoAll.get())

def Next (label,LabelPreviousFra,LabelPreviousEsp, RespuestaText,cursor, CheckTiempo,ListTiempo,CheckLevel,ListLevel,CheckPronombre,ListPronombre,CheckTipo,ListTipo,varGr):
    print(" dans next",RespuestaText.get())
    global LabelPreviousFraPal
    global LabelPreviousEspPal
    global RespuestaEntry
    global ScoreRun
    global ScoreOk
    LabelPreviousEsp.config(text=LabelPreviousEspPal)
    LabelPreviousFra.config(text=LabelPreviousFraPal)
    print("RespuestaText=", RespuestaText.get(), "ESP=", LabelPreviousEspPal, " FRa=", LabelPreviousFraPal)
    R1=str
    R2=str
    R1= RespuestaText.get()
    R2=LabelPreviousFraPal
    if ( R1.strip(" ") ==  R2.strip(" ") ):
        # Buena Respuesta
        print("Buena respuesta")
        ScoreOk=ScoreOk+ 1
        ScoreRun=ScoreRun+1
        LabelScore.config(font=MyFontOK)
        Bandera = ""
        ScoreLabelText = Bandera
    else:
        Bandera=""
        print("Mala respuesta")
        LabelScore.config(font=MyFontKO)
        print(RespuestaText.get(),"<==")
        print(LabelPreviousFraPal,"<==")
        ScoreLabelText= "(" + R1 + ")"
        ScoreRun = ScoreRun + 1
    ScoreLabelText= ScoreLabelText + str(ScoreOk) + "/" + str(ScoreRun)
    LabelScore.config(text=ScoreLabelText)
    # raz entry

    RespuestaEntry.delete(0,END)

    SelectTiempo = "("
    for i in range(len(ListTiempo)):
        if CheckTiempo[i].get()== 1 :
#           print("Tiempoe selectionné : ", ListTiempo[i][0])
            SelectTiempo=SelectTiempo+ "'"+ ListTiempo[i][0]+"'"+","
#            print("Selected Tiempo",SelectTiempo)
    SelectTiempo = SelectTiempo + "'kiki')"
    SelectLevel = "("
    for i in range(len(ListLevel)):
        if CheckLevel[i].get()== 1 :
 #           print("Level selectionné : ", ListLevel[i][0])
            SelectLevel = SelectLevel+ "'" + str(ListLevel[i][0]) + "',"
 #           print("Selected Level",SelectLevel)
    SelectLevel=SelectLevel+"'kiki')"

    SelectPronombre = "("
    for i in range(len(ListPronombre)):
        if CheckPronombre[i].get() == 1:
            #           print("Level selectionné : ", ListLevel[i][0])
            SelectPronombre = SelectPronombre + "'" + str(ListPronombre[i][0]) + "',"
    #           print("Selected Level",SelectLevel)
    SelectPronombre = SelectPronombre + "'kiki')"
    print(" SelectPronombre ",SelectPronombre)

    SelectTipo = "("
    for i in range(len(ListTipo)):
        if CheckTipo[i].get() == 1:
            #           print("Level selectionné : ", ListLevel[i][0])
            SelectTipo = SelectTipo + "'" + str(ListTipo[i][0]) + "',"
    #           print("Selected Level",SelectLevel)
    SelectTipo = SelectTipo + "'kiki')"
    print(" SelectTipo", SelectTipo)

    SelectLevel = "("
    for i in range(len(ListLevel)):
        if CheckLevel[i].get() == 1:
            #           print("Level selectionné : ", ListLevel[i][0])
            SelectLevel = SelectLevel + "'" + str(ListLevel[i][0]) + "',"
    #           print("Selected Level",SelectLevel)
    SelectLevel = SelectLevel + "'kiki')"
    print(" SelectLevel", SelectLevel)

#   If RespuestaText.get()==
#    Query = "SELECT * from verbos  where Tiempo in " + SelectTiempo + " and level in " + SelectLevel + " and Pronombre in " + SelectPronombre
    Query = "SELECT * from verbos  where Tiempo in " + SelectTiempo  + " and Pronombre in " + SelectPronombre + " and tipo in " + SelectTipo + " and level in " + SelectLevel
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
        Pregunta=PalabraSelectada[2]+ " / "+  PalabraSelectada[3] + " / "+ PalabraSelectada[1]
        print("Total = ",PalabraLen," Selectado =  ", iSelectado)
 #       print("Palabra Selectada =",PalabraSelectada)
 #       print("varGr=",varGr.get())
        if varGr.get()=='FR':
          label.config(text=Pregunta)
          LabelPreviousFraPal = PalabraSelectada[4]
          LabelPreviousEspPal = Pregunta
        else:
          label.config(text=PalabraSelectada[4])
          LabelPreviousFraPal= Pregunta
          LabelPreviousEspPal = PalabraSelectada[4]

def Erase_DB_verbos(db):
    LabelPreviousFraPal = str
    LabelPreviousEspPal = str
    cursor=db.cursor()
    cursor.execute("""DROP TABLE verbos""")
    db.commit()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS verbos(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     verbo text,
     tiempo TEXT,
     pronombre TEXT,
     conjugacion TEXT ,
     tipo TEXT ,
     level text,
     testRun INTEGER,
     testKo INTEGER
)
""")
def LoadDB_verbos_csv():
    # methode v0 de lecture des donnees depuis un csv => manip penible d'enregistrement en csv de la feuille xl avant
    # supprimé le 19/1/22 au profit lecture xl direct et pour prendre en compte l'imperatif et le passe composé
    sep = ";"
    i = 0
    TiempoList = []
    with open(filename, 'r', encoding='ansi') as mon_csvfile:
        for ligne in mon_csvfile:
            i = i + 1
            palabra_rec = ligne.strip().split(sep)
            if i == 1:
                TiempoTotal = len(palabra_rec) - 3
                print("TiempoTotal=", TiempoTotal)
                print("palabra_rec=", palabra_rec)
                for j in range(0, TiempoTotal):
                    print("Tiempo ", j, " = ", palabra_rec[j + 3])
                    TiempoList.append(palabra_rec[j + 3])
            if i > 1:  # zape le premier reccord qui contient l'entete des colonnes xl
                print(palabra_rec)
                for j in range(0, TiempoTotal):
                    if len(palabra_rec[j + 3]) > 0:
                        Query = "Insert into verbos(verbo,tiempo,pronombre,conjugacion,tipo,level) values ('" + \
                                palabra_rec[1].replace(" ", "") + "','" + TiempoList[j] + "','" + \
                                palabra_rec[2].replace(" ", "") + "','" + palabra_rec[j + 3] + "','" + palabra_rec[
                                    0] + "', 1 )"
                        print("Query insert = ", Query)
                        rc = cursor.execute(Query)
                    else:
                        # ici le verbe conjugué n'est pas renseigné / on cree l'enregistrement à blanc ("missing" )  qu'on completera avec le template des  verbes réguliers
                        Query = "Insert into verbos(verbo,tiempo,pronombre,conjugacion,tipo,level) values ('" + \
                                palabra_rec[
                                    1].replace(" ", "") + "','" + TiempoList[j] + "','" + \
                                palabra_rec[2].replace(" ", "") + "','" + "missing" + "','" + palabra_rec[0] + "', 0 )"
                        print("Query insert missing = ", Query)
                        rc = cursor.execute(Query)
        #  print("rc=",rc)

def LoadDB_verbos(filename,file_sheet,db):
    # ici on fait un premier chargement de la table verbos par les conjugaisons présentes dans l'xl  : les cellule vides xl sont chargées avec "missing"
    # on memorise les formes composées ( passé composé , imperatif negatif )  pour les templates ( _xx) et on applique ensuite le format composé aux verbes
    # irreguliers du meme temps
    cursor = db.cursor()
    # To open Workbook
    wb = xlrd.open_workbook(filename)
    sheet = wb.sheet_by_name(file_sheet)
    ncols_total=sheet.ncols
    print(" nombre de colonnes",ncols_total, " nombre de lignes ",sheet.nrows)
    # 10/3/22 ici si le nombre de lignes ne colle pas avec la feuille xl  c'est que des caracteres parasites sont dans la feuille xl
    # le contournement est de recreer la feuille xl conjugaison via un copier coller
    Tiempo_Compuesto=[]
    for ligne in range (1,sheet.nrows):
        template=False
        verbo = sheet.cell_value(ligne, 1)
        # print(" verbo=",verbo)
        if (verbo[0] == "_"):
            # ici template
            template=True
        tipo = sheet.cell_value(ligne, 0)
        pronumbre = sheet.cell_value(ligne,2)
        for colonne in range(3,ncols_total):
            tiempo=sheet.cell_value(0,colonne)
            conjugacion=sheet.cell_value(ligne, colonne)
            if template:
                ConjugacionFinal_list = conjugacion.split()
                if len(ConjugacionFinal_list) == 2:
                    # ici on est dans une template avec une forme composée
                    Tiempo_Compuesto.append([tiempo,pronumbre])
            level="irreg"
            if conjugacion=="":
                conjugacion="missing"
                level="regul"
            Query = "Insert into verbos(verbo,tiempo,pronombre,conjugacion,tipo,level) values ('" + verbo.replace(" ", "") + "','" + tiempo + "','" + \
                   pronumbre.replace(" ","") + "','" + conjugacion + "','" + tipo + "','" + level + "' )"
            # print(Query)
            # ici on filtre les conjugaisons "N/A" qui ne portent pas sur les templates
            if (template or conjugacion!="N/A"):
                rc = cursor.execute(Query)

    print("nombre de temps composés avec supp doublons",len(Tiempo_Compuesto))
    Tiempo_Compuesto_solo = []
    Tiempo_Compuesto_dict = {}
    for i in range(0,len(Tiempo_Compuesto)):
        if Tiempo_Compuesto[i] not in Tiempo_Compuesto_solo:
            Tiempo_Compuesto_solo.append(Tiempo_Compuesto[i])
            tiempo = Tiempo_Compuesto[i][0]
            pronumbre= Tiempo_Compuesto[i][1].replace(" ","")
            key=tiempo+pronumbre
            # ici on crée un dictionnaire avec comme clié tiempo-pronumbre et comme valeur le mot à composer
            Query="select conjugacion from verbos where verbo='_ar' and tiempo='" + tiempo + "' and pronombre = '" + pronumbre + "' "
            # print(Query)
            rc = cursor.execute(Query)
            ConjugacionFinal = cursor.fetchall()
            # print(ConjugacionFinal)
            # print(len(ConjugacionFinal[0]))
            # print(ConjugacionFinal[0][0])
            if (len(ConjugacionFinal[0])==1):
                # en principe un seul resultat
                prefixe=ConjugacionFinal[0][0].split()[0]
                # print("key=",key,"prefixe=",prefixe)
                Tiempo_Compuesto_dict[key] = prefixe
    print("nombre de temps composés apres supp doublons", len(Tiempo_Compuesto_solo))
    # traitements des temps composés pour les conjugaisons irrégulieres ( ajouter des complements .. )
    print("dictionnaire mbre de temps composés ", Tiempo_Compuesto_dict)
    # on balaye maintenant toutes la base des conjugaisons pour les enregistrement non missing et on check si il  match
    #  avec une entrée du dictionnaire  / si oui  on met à jour l'entrée en question
    Query="select conjugacion,verbo, tiempo,pronombre from  verbos where conjugacion != 'missing' and verbo !='_er' and verbo !='_ir' and verbo!='_ar'"
    rc = cursor.execute(Query)
    list_conjugacion_irr= cursor.fetchall()
    for i in range(0, len(list_conjugacion_irr)):

        key=list_conjugacion_irr[i][2]+list_conjugacion_irr[i][3]
        if key in Tiempo_Compuesto_dict:
            conjugacion_corigida=Tiempo_Compuesto_dict[key].replace(" ","")+ " " + list_conjugacion_irr[i][0].replace(" ","")
            print("correction à faire sur ", conjugacion_corigida)
            Query = "update verbos set conjugacion ='" + conjugacion_corigida + "'  where verbo='" + list_conjugacion_irr[i][1] +  \
                "' and tiempo='" + list_conjugacion_irr[i][2] + "' and pronombre ='" + list_conjugacion_irr[i][3] + "'"
            print(Query)
            rc = cursor.execute(Query)


LabelPreviousFraPal = str
LabelPreviousEspPal = str
db=sqlite3.connect('verbos.db')
cursor=db.cursor()
# remise à blanc de la table verbos existante
Erase_DB_verbos(db)
# identificaton du fichier xl source des conjugaisons
# la feuille xl designé contient en premiere ligne : les
#

XLpath="C:"+"\\"+"localdrive"+"\\"+"drive_G"+ "\\"+"kutta75d"+"\\"+"Mon Drive"+"\\"+"MOOC"+"\\"+"2020-10-Espanol"
#myfile= ("C:"+"\\"+"drive"+"\\"+"Google"+"\\"+"kutta75d"+"\\"+"MOOC"+"\\"+"2020-10-Espanol"+"\\"+"vocabulaire.xlsx")
XLpath="C:"+"\\"+"Drives"+"\\"+"G_drive"+ "\\"+"kutta75"+"\\"+"kutta75d"+"\\"+"MOOC"+"\\"+"2020-10-Espanol"
XLpath="C:"+"\\"+"Drives"+"\\"+"Google"+N"\\"+"kutta75d"+"\\"+"MOOC"+"\\"+"2020-10-Espanol"
myfile= XLpath + "\\"+"vocabulaire.xlsx"

filename=myfile
# chargement de la table db avec les reccords xl / les champs manquant sont mis à "missing"
LoadDB_verbos(myfile,"conjugaison",db)





# traitement des conjugaisons absentes
Query = "select verbo,tiempo,pronombre,tipo from verbos where conjugacion = 'missing'"
rc = cursor.execute(Query)
ListVerbosFaltan = cursor.fetchall()
print("Missing verbos = ", len(ListVerbosFaltan))
for i in range(0,len(ListVerbosFaltan)):
    Verbo=ListVerbosFaltan[i][0].replace(" ","")
    Groupo = "_" + Verbo[len(Verbo)-2:]
    # ici pour les verbes comme freír  reír  on modifie le groupe trouver via les 2 dernieres lettres pour retrouver la conjugaison en _ir
    Groupo = Groupo.replace("í","i")
    VerboBaso=Verbo[0:len(Verbo)-2]
    # print("verbos= ",ListVerbosFaltan[i][0], " groupo", Groupo)
    Query="Select conjugacion from verbos where verbo = '" + Groupo + "' and Tiempo='" + ListVerbosFaltan[i][1] + "' and pronombre ='" + ListVerbosFaltan[i][2] + "' and tipo = 'template'"
    rc = cursor.execute(Query)
    ConjugacionFinal=cursor.fetchall()
    if len(ConjugacionFinal)==1:
        Query_End=" where verbo='"+Verbo + "' and Tiempo = '" + ListVerbosFaltan[i][1] + \
             "' and pronombre ='" + ListVerbosFaltan[i][2] + "' and tipo = '" + ListVerbosFaltan[i][3] + "'"
        if ConjugacionFinal[0][0]=="N/A":
            # forme impossible ( ex imperatif 1ier personne ) => on supprime le reccord correspondand)
            Query_Start= "Delete FROM verbos "
        else:
            # ici on complete les formes regulieres
            ConjugacionFinal_list= ConjugacionFinal[0][0].split()
            ConjugacionCalculada = VerboBaso + ConjugacionFinal_list[-1]
            if len(ConjugacionFinal_list)==2:
                #contexte des passés composés ( hemos xxido .. )
                ConjugacionCalculada= ConjugacionFinal_list[0] + " " + ConjugacionCalculada
            Query_Start="Update verbos set conjugacion='"+ ConjugacionCalculada + "'"
        Query=Query_Start+Query_End
        # print("Query = ", Query, " ==>", ConjugacionCalculada)
        # print("Query update = ",Query)
        rc = cursor.execute(Query)


# question pour savoir si on produit un fhichier sql avec tout ou sans pronombre - tiempos ( quand ca ne change pas )
mode=input("produire la table tiempos  - la table pronombre ?  Y/N")
if mode=="Y":
    print(" => la totale)")
else:
    mode=""
if mode:
    "mode set to true"
else:
    print("mode set to false")


# preparation des fichiers structurés servant à recevoir les ordres sql de creation d'enregistrements


# type de verbe
#myfile="C:"+"\\"+"Gdrive"+"\\"+"kutta75d"+"\\"+"MOOC"+"\\"+"2020-10-Espanol"+"\\"+"verbos.sql"
#myfile="C:"+"\\"+"drive"+"\\"+"Google"+"\\"+"kutta75d"+"\\"+"MOOC"+"\\"+"2020-10-Espanol"+"\\"+"verbos.sql"

myfile=XLpath+"\\"+"verbos.sql"
#myfile="C:"+"\\"+"Gdrive"+"\\"+"kutta75d"+"\\"+"MOOC"+"\\"+"2020-10-Espanol"+"\\"+"01-verbotipo.sql"
outputfile= open(myfile,"w",encoding='utf8')
freccord = "Delete from verbos_conjugacion;"
outputfile.write(str(freccord)+"\n")
freccord = "Delete from verbos_verbo;"
outputfile.write(str(freccord)+"\n")
if mode:
    freccord = "Delete from verbos_pronombre;"
    outputfile.write(str(freccord)+"\n")
    freccord = "Delete from verbos_tiempo;"
    outputfile.write(str(freccord)+"\n")
freccord = "Delete from verbos_level;"
outputfile.write(str(freccord)+"\n")
freccord = "Delete from verbos_verbotipo;"
outputfile.write(str(freccord)+"\n")

Query = "Select tipo  from verbos group by tipo"
#Query = "Select verbo,tiempo,pronombre,conjugacion,tipo,level from verbos"
rc=cursor.execute(Query)
ListAll= cursor.fetchall()
for i in range(0,len(ListAll)):
    freccord = "Insert into verbos_verbotipo (verbotipo) values ("+ "'" + ListAll[i][0] + "'" + ");"
#    freccord = ListAll[i][0]+";"+ListAll[i][1]+";"+ListAll[i][2]+";"+ListAll[i][3]+";"+ListAll[i][4]+";"+str(ListAll[i][5])
    outputfile.write(str(freccord)+"\n")


# type de temps
#myfile="C:"+"\\"+"Gdrive"+"\\"+"kutta75d"+"\\"+"MOOC"+"\\"+"2020-10-Espanol"+"\\"+"02-tiempo.sql"
#outputfile= open(myfile,"w")
Query = "select tiempo from verbos group by tiempo"
#Query = "Select verbo,tiempo,pronombre,conjugacion,tipo,level from verbos"
rc=cursor.execute(Query)
ListAll= cursor.fetchall()
for i in range(0,len(ListAll)):
    freccord = "Insert into verbos_tiempo (tiempo) values ("+ "'" + ListAll[i][0] + "'" + ");"
#    freccord = ListAll[i][0]+";"+ListAll[i][1]+";"+ListAll[i][2]+";"+ListAll[i][3]+";"+ListAll[i][4]+";"+str(ListAll[i][5])
    if mode:
        outputfile.write(str(freccord)+"\n")
#outputfile.close()

# type de level
#myfile="C:"+"\\"+"Gdrive"+"\\"+"kutta75d"+"\\"+"MOOC"+"\\"+"2020-10-Espanol"+"\\"+"02-level.sql"
#outputfile= open(myfile,"w")
Query = "select level  from verbos group by level"
#Query = "Select verbo,tiempo,pronombre,conjugacion,tipo,level from verbos"
rc=cursor.execute(Query)
ListAll= cursor.fetchall()
for i in range(0,len(ListAll)):
    freccord = "Insert into verbos_level (level) values ("+ "'" + str(ListAll[i][0]) + "'" + ");"
#    freccord = ListAll[i][0]+";"+ListAll[i][1]+";"+ListAll[i][2]+";"+ListAll[i][3]+";"+ListAll[i][4]+";"+str(ListAll[i][5])
    outputfile.write(str(freccord)+"\n")
#outputfile.close()

# type de pronoms
#myfile="C:"+"\\"+"Gdrive"+"\\"+"kutta75d"+"\\"+"MOOC"+"\\"+"2020-10-Espanol"+"\\"+"03-pronombre.sql"
#outputfile= open(myfile,"w")
Query = "select pronombre  from verbos group by pronombre"
#Query = "Select verbo,tiempo,pronombre,conjugacion,tipo,level from verbos"
rc=cursor.execute(Query)
ListAll= cursor.fetchall()
for i in range(0,len(ListAll)):
    freccord = "Insert into verbos_pronombre (pronombre) values ("+ "'" + ListAll[i][0] + "'" + ");"
#    freccord = ListAll[i][0]+";"+ListAll[i][1]+";"+ListAll[i][2]+";"+ListAll[i][3]+";"+ListAll[i][4]+";"+str(ListAll[i][5])
    if mode:
        outputfile.write(str(freccord)+"\n")
#outputfile.close()

# type de verbe + tipo
#myfile="C:"+"\\"+"Gdrive"+"\\"+"kutta75d"+"\\"+"MOOC"+"\\"+"2020-10-Espanol"+"\\"+"04-verbo-tipo.sql"
#outputfile= open(myfile,"w")
Query = "Select verbo,tipo  from verbos group by verbo"
#Query = "Select verbo,tiempo,pronombre,conjugacion,tipo,level from verbos"
rc=cursor.execute(Query)
ListAll= cursor.fetchall()
for i in range(0,len(ListAll)):
    freccord = "Insert into verbos_verbo (verbo,tipo_id) values ('" + ListAll[i][0] + "' , (SELECT id FROM verbos_verbotipo WHERE verbotipo = '"+ ListAll[i][1] + "'));"
#    freccord = ListAll[i][0]+";"+ListAll[i][1]+";"+ListAll[i][2]+";"+ListAll[i][3]+";"+ListAll[i][4]+";"+str(ListAll[i][5])
    outputfile.write(str(freccord)+"\n")
#outputfile.close()

# type de conjugacion
#myfile="C:"+"\\"+"Gdrive"+"\\"+"kutta75d"+"\\"+"MOOC"+"\\"+"2020-10-Espanol"+"\\"+"05-conjugacion.sql"
#outputfile= open(myfile,"w")
#Query = "Select pronombre  from verbos group by pronombre"
Query = "Select conjugacion,verbo,pronombre,tiempo,level from verbos"
rc=cursor.execute(Query)
ListAll= cursor.fetchall()
for i in range(0,len(ListAll)):
#   freccord = ListAll[i][0]
    freccord = "Insert into verbos_conjugacion  (conjugacion,verbo_id,pronombre_id,tiempo_id,level_id ) values  "  + \
               "('" + ListAll[i][0] + "' , " + \
                "(SELECT id FROM verbos_verbo WHERE verbo = '"+ ListAll[i][1] + "')," + \
                 "(SELECT id FROM verbos_pronombre  WHERE pronombre  = '" +  ListAll[i][2] + "'),"  + \
            "(SELECT id FROM verbos_tiempo  WHERE tiempo  = '" + ListAll[i][3] + "')," + \
            "(select id FROM verbos_level where level = '" + str(ListAll[i][4])  +"')" + \
                                                                                  "); "

    outputfile.write(str(freccord)+"\n")
outputfile.close()




level = 0
cursor.execute("""SELECT verbo,count(verbo)  from verbos group by verbo """)
ListVerbos = cursor.fetchall()
print("Verbos=",ListVerbos)
print("nombre de verbes =",len(ListVerbos))

cursor.execute("""SELECT tiempo,count(tiempo) from verbos group by tiempo  """)
ListTiempo = cursor.fetchall()
print("Tiempo=",ListTiempo)

cursor.execute("""SELECT pronombre,count(pronombre) from verbos group by pronombre  """)
ListPronombre = cursor.fetchall()
print("ProNombre",ListPronombre)

cursor.execute("""SELECT tipo,count(tipo) from verbos group by tipo""")
ListTipo = cursor.fetchall()
print("ProTipo = ",ListTipo)

cursor.execute("""SELECT level,count(level) from verbos group by level""")
ListLevel = cursor.fetchall()
print("ProLevel = ",ListLevel)

query= "SELECT count(*) from verbos "
print("query=",query )
cursor.execute(query)
palabra1=cursor.fetchall()
print("palabra =",palabra1)
# db.close()

# Interface graphique
gui = Tk(className='Vocabulario-Verbos')
MyFont = tkFont.Font(size=11)
MyFontOK = tkFont.Font(size=11)
MyFontKO = tkFont.Font(size=12,weight="bold",)
# set window size
Y=20+len(ListTipo)*40
Yc=str(Y)
XY="600x" + Yc
print("XY=",XY)
gui.geometry(XY)
ScoreRun = int
ScoreOk= int
ScoreOk=0
ScoreRun=0
LabelScore= Label(gui,text="Selectar por favor",font=MyFontOK)
LabelScore.grid(column=2,row=2,sticky="E")
RespuestaText  = StringVar(gui)
RespuestaEntry = Entry(gui, textvariable=RespuestaText,font=MyFont)
label=Label(gui,text="Estas listo ?  ",font=MyFont)
text = StringVar(gui)
LabelPreviousEsp=Label(gui,text="",font=MyFontOK)
LabelPreviousFra=Label(gui,text="",font=MyFontOK)


CheckTiempo = []
CheckTiempoButton = []
CheckTiempoAll = IntVar()
CheckTiempoAll.set(1)
CheckTiempoButtonAll=Checkbutton(gui, text = "todos" , variable = CheckTiempoAll, onvalue = 1, offvalue = 0,font=MyFont,command=partial(CheckTiempoAllFunction,CheckTiempoAll,CheckTiempo))
CheckTiempoButtonAll.grid(column=2, row=6, sticky="W")
i=0
for dom in ListTiempo:
    print("keys=",i,dom)
    CheckTiempo.append(IntVar())
    CheckTiempoButton.append(Checkbutton())
    CheckTiempo[i].set(1)
    CheckTiempoButton[i]=Checkbutton(gui, text =dom[0]+" ("+str(dom[1])+")", variable = CheckTiempo[i], onvalue = 1, offvalue = 0,font=MyFont)
    CheckTiempoButton[i].grid(column=2, row=i+7, sticky="W")
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

CheckPronombre = []
CheckPronombreButton = []
CheckPronombreAll = IntVar()
CheckPronombreAll.set(1)
CheckPronombreButtonAll=Checkbutton(gui, text = "todos" , variable = CheckPronombreAll, onvalue = 1, offvalue = 0,font=MyFont,command=partial(CheckPronombreAllFunction,CheckPronombreAll,CheckPronombre))
CheckPronombreButtonAll.grid(column=3, row=6, sticky="W")
k=0
for Pronombre in ListPronombre:
    print("Pronombre=",k,Pronombre)
    CheckPronombre.append(IntVar())
    CheckPronombreButton.append(Checkbutton())
    CheckPronombre[k].set(1)
    CheckPronombreButton[k]=Checkbutton(gui, text =str(Pronombre[0]) +" ("+str(Pronombre[1])+")", variable = CheckPronombre[k], onvalue = 1, offvalue = 0,font=MyFont)
    CheckPronombreButton[k].grid(column=3, row=k+7, sticky="W")
    k=k+1

CheckTipo = []
CheckTipoButton = []
CheckTipoAll = IntVar()
CheckTipoAll.set(1)
CheckTipoButtonAll=Checkbutton(gui, text = "todos" , variable = CheckTipoAll, onvalue = 1, offvalue = 0,font=MyFont,command=partial(CheckTipoAllFunction,CheckTipoAll,CheckTipo))
CheckTipoButtonAll.grid(column=4, row=6, sticky="W")
k=0
for Tipo in ListTipo:
    print("Tipo =",k,Tipo)
    CheckTipo.append(IntVar())
    CheckTipoButton.append(Checkbutton())
    CheckTipo[k].set(1)
    CheckTipoButton[k]=Checkbutton(gui, text =str(Tipo[0]) +" ("+str(Tipo[1])+")", variable = CheckTipo[k], onvalue = 1, offvalue = 0,font=MyFont)
    CheckTipoButton[k].grid(column=4, row=k+7, sticky="W")
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
# sur les Tiempoes
NextButton = Button(gui, text='Next',command=partial(Next, label,LabelPreviousFra,LabelPreviousEsp, RespuestaText,cursor, \
                                                     CheckTiempo,ListTiempo,CheckLevel,ListLevel,CheckPronombre,ListPronombre,CheckTipo,ListTipo,varGr,),font=MyFont)
NextButton.grid(column=4,row=1,sticky="W")


RespuestaEntry.grid(column=3, row=1,sticky="W")
label.grid(column=2,row=1,sticky="E")
LabelPreviousEsp.grid(column=3,row=2,sticky="E")
LabelPreviousFra.grid(column=4,row=2,sticky="W")
gui.mainloop()

