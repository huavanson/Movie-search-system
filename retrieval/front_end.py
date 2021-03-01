from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import tkinter.font as Tkfont
from tkinter import ttk
import cv2
import numpy as np
## part 1
from back_end import append_new_query_to_tail
from back_end import search_engine
from back_end import remove_tail
### part 2
from back_end import append_new_query_to_tail_df2
from back_end import remove_tail_df2
from back_end import cate_query
from back_end import get_rank

import webbrowser


window = Tk()
window.title('Search your movie')
window.minsize(1300,650)


def create_treeview(df_result):
    def selectItem(a):
        curItem = tree.focus()
        url = tree.item(curItem)['values'][0]
        print(url)
        webbrowser.open(url)
    global window
    tree = ttk.Treeview(window)
    df_col = df_result.columns.values
    tree["columns"]=(df_col)
    counter = len(df_result)
  
    style = ttk.Style()
    style.theme_use("vista")
    style.configure("Treeview.Heading", font=("Time New Roman", 18))
    style.configure("Treeview", font=("Time New Roman", 12))
    style.configure('Treeview', rowheight=40)

    tree.column('#0', width=0)
    tree.column(0, width=400 )
    tree.heading(0, text="Link")
    tree.column(1, width=300 )
    tree.heading(1, text="Tên")
    tree.column(2, width=300)
    tree.heading(2, text="Thể loại")

    for i in range(counter):
        tree.insert('', i, values=df_result.iloc[i,:].tolist())


    tree.bind('<ButtonRelease-1>', selectItem)
    tree.place(x=50, y=200)
def checkisCate():
    for boxval in var:
        if boxval.get() != 0:
            return True
    return False
def clickSearch():
    input_query = name.get()
    isCate = checkisCate()
    if not isCate:
        Search_1(input_query)
    else:
        Search_2(input_query)

def Search_1(input_query):
    print("search 1")
    df = append_new_query_to_tail(input_query)
    df_result = search_engine(df,k=20)
    df_result = df_result[["URL", "Viet-name", "Category"]]
    df_result = df_result.drop([df_result.index[0]],axis=0)

    print(df_result)
    create_treeview(df_result=df_result)
    #remove_tail()

def Search_2(input_query):
    print("search 2")
    list_cate = []
    for boxval in var:
        a = boxval.get()
        if a!=0:
            list_cate.append(category_dict[a])
    print('List cate:', list_cate)
    df = cate_query(list_cate=list_cate)
    df = append_new_query_to_tail_df2(df, input_query)

    df_result = search_engine(df, k=20)
    df_result = get_rank(df_result)

    df_result = df_result[["URL", "Viet-name", "Category"]]
    
    create_treeview(df_result=df_result)


 
lbl_input = ttk.Label(window, text = "Nhập mô tả", width = 200)
lbl_input.config(font=("Time New Roman", 20))
lbl_input.place(x=130, y=150)
 
name = tk.StringVar()
nameEntered = ttk.Entry(window, width = 15, textvariable = name, font=("Time New Roman", 20))
nameEntered.place(x=290, y = 140, height=50, width=500)
 
myFont = Tkfont.Font(size=20)
button = tk.Button(window, text = "Tìm kiếm", command = clickSearch)
button['font'] = myFont
button.place(x= 800, y= 135)

category = [('Tình cảm - Lãng mạn', 1), ('Võ thuật', 2), ("Cổ trang", 3), ("Hành động", 4),
            ("Hài hước", 5), ("Gia đình", 6), ("Chiến tranh", 7), ("Chính kịch", 8),
            ("Học đường", 9), ("Giải trí", 10), ("Hình sự", 11), ("Khoa học - Viễn tưởng", 12),
            ("Phiêu lưu", 13), ("Thần thoại", 14), ("Tâm lý", 15), ("Tài liệu", 16),
            ("Webdrama", 17), ("Đam Mỹ - Bách Hợp", 18)]
category_dict = {1: 'Tình cảm - Lãng mạn', 2: 'Võ thuật', 3: 'Cổ trang', 4: 'Hành động', 
                5: 'Hài hước', 6: 'Gia đình', 7: 'Chiến tranh', 8: 'Chính kịch', 9: 'Học đường', 
                10: 'Giải trí', 11: 'Hình sự', 12: 'Khoa học - Viễn tưởng', 13: 'Phiêu lưu', 
                14: 'Thần thoại', 15: 'Tâm lý', 16: 'Tài liệu', 17: 'Webdrama', 18: 'Đam Mỹ - Bách Hợp'}
                
                

X_radio = 1080
Y_radio = 110
var = []
lst_checkbtn = []
check_btn_font = Tkfont.Font(family='Time New Roman', size=12, weight='normal')
for cate, id in category:
    adBoxVal = IntVar()
    var.append(adBoxVal)
    checkbutton = tk.Checkbutton(window, text=cate, variable=adBoxVal, 
                   onvalue=id, offvalue=0, 
                   font=check_btn_font).place(x=X_radio,y=Y_radio)
    lst_checkbtn.append(checkbutton)
    Y_radio+=30


window.mainloop()
