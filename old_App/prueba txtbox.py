from tkinter import *

#Texbox

root=Tk()

solo_una_nota=""
textbox_solo_una_nota=Entry(root, width=50,borderwidth=5)
textbox_solo_una_nota.pack()

def clear():
    my_text.delete(1.0,END)
    my_label.config(text="")

def get_text():
    url=my_text.get(1.0,END)
    print(textbox_solo_una_nota.get())


my_text= Text(root,width=60,height=20,font=("Courier",12))
my_text.pack(pady=20)


ment=StringVar()

button_Frame= Frame(root)
button_Frame.pack()

botonLimpiar=Button(button_Frame, text="Limpiar", command=clear)
botonLimpiar.grid(row=0,column=0)

get_text_btn= Button(button_Frame, text="Enviar nota", command=get_text)
get_text_btn.grid(row=0,column=1,padx=20)

my_label= Label(root,text='')
my_label.pack(pady=20)


root.mainloop()
