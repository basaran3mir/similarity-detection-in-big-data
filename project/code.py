import time
import threading

from tkinter import messagebox
from tkinter import *
from pandas import *

#BACK
edited_data = read_csv("edited_data.csv")

data = {
    "benzerlikler" : [
        {

        }
    ]
}

benzerlikler = data["benzerlikler"]

#Thread'lerin listesi
thread_list = []
#Thread'lerin çalışma zamanının listesi
time_list = []
#name+time
tt_list = []

def compare_two_sentences(sentence1, sentence2): #2 cümlenin birbiri ile kıyaslanması

    if(sentence1 == sentence2):
        return 100

    counter = 0

    sentence1_list = sentence1.split()
    sentence2_list = sentence2.split()

    for i in sentence1_list:
        for j in sentence2_list:
            if (i.lower() == j.lower()):
                counter = counter + 1

    if(len(sentence1_list) > len(sentence2_list)):
            return round ( (counter/len(sentence1_list) * 100) , 1 )
    if(len(sentence1_list) == len(sentence2_list)):
            return round ( (counter/len(sentence1_list) * 100) , 1 )
    if(len(sentence1_list) < len(sentence2_list)):
            return round ( (counter/len(sentence2_list) * 100) , 1 )

def compare_with_search_limit(selected_column, selected_data_num, selected_percent, case, selected_first_range, selected_second_range, thread_name): #Product, 33.3, 4000, 500, 549, 2, buyuk esit, 10

    #Product için 4000 veride 33.3 benzerlik aranacak ve benzerlik datasına eklenecek
    #500-549 arası kelimeler 500-4000 arası kelimeler ile karşılaştırılacak
    #Mesela 500. kelime 501-4000 arası kelimeler ile, 501. kelime 502-4000 arası kelimeler ile... 549. kelime 550-4000 arası kelimeler ile karşılaştırılacak

    #print("Thread -" , thread_name , "başladı.")

    list_selected_column = edited_data[selected_column].tolist()
    float_percent = float(selected_percent)

    time1 = time.time()
        
    for i in range(selected_first_range, selected_second_range):
        for j in range(i+1, selected_data_num):
            if(case == "buyuk esit"):
                if(compare_two_sentences(list_selected_column[i], list_selected_column[j]) >= float_percent): #buyuk esit olanları ekle
                    benzerlikler.append({
                        "col_1" : i,
                        "col_2" : j,
                        "sen_1" : list_selected_column[i],
                        "sen_2" : list_selected_column[j],
                        "sim" : compare_two_sentences(list_selected_column[i], list_selected_column[j])
                    })
            if(case == "esit"):
                if(compare_two_sentences(list_selected_column[i], list_selected_column[j]) == float_percent): #esit olanları ekle
                    benzerlikler.append({
                        "col_1" : i,
                        "col_2" : j,
                        "sen_1" : list_selected_column[i],
                        "sen_2" : list_selected_column[j],
                        "sim" : compare_two_sentences(list_selected_column[i], list_selected_column[j])
                    })

    time2 = time.time()
    #print("Thread -", thread_name, "bitti.")

    #print("Thread -", thread_name, "çalışma süresi:", time2-time1)
    time_list.append(time2-time1)

    tt = "T-" + str(thread_name) + ": " +  str(time2-time1)
    tt_list.append(tt)

def main(column, data_number, thread_number, percent, case):

    int_data_number = int(data_number)
    int_thread_number = int(thread_number)

    #Thread'lere atanacak sayı aralığı için
    #Mesela 4000 veri 10 thread olacak ise:
    #0.Thread = 0-399 , 1.Thread = 400-799 ... 9.Thread = 3600-3999
    parts = int_data_number/int_thread_number 
    int_parts = int(parts)

    code_time_1 = time.time() #Toplam çalışma zamnını bulmak için

    for i in range(int_thread_number):
        #print(str(i), ". thread:" , i*int_parts , "-", (i+1)*int_parts-1)
        t = threading.Thread(target=compare_with_search_limit, args=(column, int_data_number, percent, case, i*int_parts, (i+1)*int_parts-1, i), name="Thread-"+str(i))
        thread_list.append(t)

    for i in thread_list: #Thread'leri çalıştır
        i.start()

    for i in thread_list: #Thread'lerin bitmesini bekle
        i.join()

    code_time_2 = time.time()

    text_field_setThreadTime.insert(INSERT, ["Toplam çalışma zamanı:", code_time_2-code_time_1, "\n"])

def senaryo_2(selected_data_num): #2. senaryo

    product = edited_data["Product"].tolist()
    issue = edited_data["Issue"].tolist()
    company = edited_data["Company"].tolist()

    for i in range(0, selected_data_num):
        for j in range(i+1, selected_data_num):
            if(compare_two_sentences(product[i], product[j]) == 100.0):
                if(compare_two_sentences(issue[i], issue[j]) >= 70.0):
                    text_field_result.insert(INSERT, [i, j, company[i], company[j], "\n"] )

def senaryo_3(selected_data_num): #3. senaryo

    complaint_id = edited_data["Complaint ID"].tolist()
    issue = edited_data["Issue"].tolist()

    for i in complaint_id:
        if i == 3198084:
            for i in range(0, selected_data_num):
                for j in range(i+1, selected_data_num):
                    if(compare_two_sentences(issue[i], issue[j]) >= 50.0):
                        text_field_result.insert(INSERT, [i, j, issue[i], issue[j], "\n"] )

#FRONT
master=Tk()
master.title("APP")
canvas=Canvas(master,height=600,width=900)#ANA PENCERE
canvas.pack()

frame_ust=Frame(master,bg='orange')
frame_ust.place(relx=0.03,rely=0.02,relwidth=0.96,relheight=0.1)

frame_alt_sol=Frame(master,bg='orange')
frame_alt_sol.place(relx=0.03,rely=0.15,relwidth=0.35,relheight=0.81)

frame_alt_sag=Frame(master,bg='orange')
frame_alt_sag.place(relx=0.39,rely=0.15,relwidth=0.60,relheight=0.81)

setColumn_label=Label(frame_ust,bg='orange',text='Sütun Seçiniz: ',font='Verdana 12 bold')
setColumn_label.pack(padx=10,pady=10,side=LEFT)

sutun_tipi_opsiyon=StringVar(frame_ust)
sutun_tipi_opsiyon.set("\t")
setColumn_dropdown_menu=OptionMenu(frame_ust,sutun_tipi_opsiyon,
                                      "Product",
                                      "Issue",
                                      "Company",
                                      "State"
                                      ,"Complaint ID"
                                      ,"ZIP CODE")
setColumn_dropdown_menu.pack(padx=10,pady=10,side=LEFT)


setThreshold_label=Label(frame_alt_sol,bg='orange',text='Benzerlik oranını giriniz: ',font='Verdana 10 bold')
setThreshold_label.pack(padx=3,pady=3,anchor=NW)

text_field_setThreshold=Text(frame_alt_sol,height=1,width=25)
text_field_setThreshold.pack(padx=6,pady=2,anchor=NW)


setComesWith_label=Label(frame_alt_sol,bg='orange',text='Eylem seçiniz: ',font='Verdana 10 bold')
setComesWith_label.pack(padx=6,pady=20,anchor=W)
var=IntVar()

R1=Radiobutton(frame_alt_sol,text='Seçilen sütunu kıyasla(Senaryo 1-4)',variable=var,value=1,bg='orange',font='Verdana 8  bold')
R1.pack(padx=1,pady=2,anchor=NW)

R2=Radiobutton(frame_alt_sol,text='Senaryo 2',variable=var,value=2,bg='orange',font='Verdana 8 bold ')
R2.pack(padx=0,pady=6,anchor=NW)

R3=Radiobutton(frame_alt_sol,text='Senaryo 3',variable=var,value=3,bg='orange',font='Verdana 8 bold ')
R3.pack(padx=0,pady=6,anchor=NW)

setThreadNumber_label=Label(frame_alt_sol,bg='orange',text='Thread sayınızı giriniz: ',font='Verdana 10 bold')
setThreadNumber_label.pack(padx=6,pady=10,anchor=NW)

text_field_setThreadNumber=Text(frame_alt_sol,height=1,width=25)
text_field_setThreadNumber.pack(padx=3,pady=1,anchor=NW)

threadTime_label=Label(frame_alt_sol,bg='orange',text='Thread çalışma süreleri: ',font='Verdana 10 bold')
threadTime_label.pack(padx=6,pady=40,anchor=NW)

text_field_setThreadTime=Text(frame_alt_sol,height=17,width=50)
text_field_setThreadTime.pack(padx=3,pady=1,side=LEFT)

threadWorks_label=Label(frame_alt_sag,bg='orange',text='SONUÇ EKRANI: ',font='Verdana 10 bold')
threadWorks_label.pack(padx=6,pady=1,side='top')

text_field_result=Text(frame_alt_sag,height=39,width=130)
text_field_result.pack(padx=6,pady=2,anchor=NW)

dataNumber_label=Label(frame_ust,bg='orange',text='Veri sayınızı girin: ',font='Verdana 12 bold')
dataNumber_label.pack(padx=0,pady=0,side=LEFT)

text_field_setDataNumber=Text(frame_ust,height=1,width=20)
text_field_setDataNumber.pack(padx=0,pady=0,side=LEFT)

def calistir():
    if var.get():

        if var.get() == 1:
            selected_column = sutun_tipi_opsiyon.get()
            selected_data_number = int(text_field_setDataNumber.get("0.0" , "end"))
            selected_thread_number = int(text_field_setThreadNumber.get("0.0" , "end"))
            selected_percent = float(text_field_setThreshold.get("0.0" , "end"))
            
            main(selected_column, selected_data_number, selected_thread_number, selected_percent, "buyuk esit")

            for i in benzerlikler:
                text_field_result.insert(INSERT, [i, "\n"])

            for i in range(len(tt_list)):
                text_field_setThreadTime.insert(INSERT, [tt_list[i], "\n"])

            messagebox.showinfo("Bildirim" , "Bitti")

        if var.get() == 2:
            senaryo_2(1000)
            messagebox.showinfo("Bildirim" , "Bitti")

        if var.get() == 3:
            senaryo_3(1000)
            messagebox.showinfo("Bildirim" , "Bitti")

    return

calistir_butonu = Button(frame_ust, text="Çalıştır", command=calistir)

calistir_butonu.pack(padx=50,pady=0,side=LEFT)

master.mainloop()