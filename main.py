import geocoder
import tkinter as tk
import time
from tksheet import Sheet
from tkinter import *
from tkinter import ttk
import pymysql
import pymysql.cursors 

con = pymysql.connect(host='localhost', user='root',passwd='12345',db='TEST')
class connection_on_mysql():
    
    def truncate():
        try:
            
            with con.cursor() as cur:
                cur.execute("TRUNCATE TABLE neighborhoodt;")
                con.commit()
            
        except Exception as error:
            return str(error)
        
    
    def insert_on_database(street,ll,barrio):
        try:
            
            with con.cursor() as cur:
                cur.execute("INSERT INTO neighborhoodt (Adress,lititudlongitud,Neighborhood) VALUES ('"+street+"','"+ll+"','"+barrio+"');")
                con.commit()

            
        except Exception as error:
            return str(error)
    def load_info():
        try:
            
            with con.cursor() as cur:
                cur.execute("SELECT Adress,lititudlongitud,Neighborhood FROM neighborhoodt order by Neighborhood desc ;")
                result = cur.fetchall()
                con.commit()
                
            return result
            
        except Exception as error:
            return str(error)
        
    def load_neigh():
        try:
            
            with con.cursor() as cur:
                cur.execute("SELECT Neighborhood FROM neighborhoodt GROUP BY Neighborhood;")
                result = cur.fetchall()
                con.commit()
                
            return result
            
        except Exception as error:
            return str(error)
        
    def delete_on_database(barrio):
        try:
            
            with con.cursor() as cur:
                cur.execute("DELETE FROM neighborhoodt WHERE Neighborhood LIKE '%"+barrio+"%';")
                con.commit()

            
        except Exception as error:
            return str(error)
        
    
    

    


if __name__ == "__main__":
    try:
        def unlock():
            items = connection_on_mysql.load_neigh()
            combo_box.config(values=items)
            combo_box.config(state = NORMAL )
            btn_del.config(state = NORMAL )
            
            
        def del_element():
            
            n = str(combo_box.get())
            n = n.replace('{','')
            n = n.replace('}','')
            
            if n != 'Seleccione Barrio':
                connection_on_mysql.delete_on_database(n)
                btn_reload.config(state= NORMAL)
            
        def reload():
            info = connection_on_mysql.load_info()
            insert_in_sheet(info)
            
            
        def preload():
            
            read_entry.delete(0,END)
            read_entry.insert(0,"300 SE Stark Street, Portland")
            read_entry.config(state=DISABLED)
            
        def insert_in_sheet(elements):
            rs_sheet.set_sheet_data(data=elements, reset_col_positions = True,reset_row_positions = True,redraw = True,verify = False,reset_highlights = False)
            
        def cal():
            read_entry.config(state=NORMAL)
            ins = str(read_entry.get())
            vec = ins.split(' ')
            num = int(vec[0])
            y = 0
            c = 1
            #vec = []
            old_n = ''
            while y < 1:
                new_r = num*c
                snum = str(new_r)+' SE Stark Street, Portland'
                location = geocoder.osm(snum)
                c += 1
                get_location = str(location)
                get_location = get_location.replace('<[OK] Osm - Geocode [','')
                get_location = get_location.replace(', United States]>','')
                elements_of_location = get_location.split(',')
                night = str(elements_of_location[2])
                res=str(location.latlng)
                res=res.replace('[','')
                res=res.replace(']','')
                res=res.replace(' ','')
                #elements = [snum,res,night]
                #vec.append(elements)
                
                current_n = elements_of_location[2]
                
                time.sleep(1)
                
                if current_n != old_n:
                    old_n = elements_of_location[2]
                    connection_on_mysql.insert_on_database(str(snum),res,str(old_n))

                if c == 76:
                    y+=1
                    
                
                    
                
            info = connection_on_mysql.load_info()
            insert_in_sheet(info)
            
            read_entry.config(state=NORMAL)
            read_entry.delete(0,END)
            read_entry.insert(0,snum)
            read_entry.config(state=DISABLED)
            
            unlock()
        
        win = tk.Tk()

        win.title("Test Geocoding")
        win.minsize(850,1000)
        win.maxsize(850,1000)
        
        fast_frame = Frame(win,bg = "#434552",highlightbackground="#13193D",highlightthickness=2)
        fast_frame.pack(fill=tk.BOTH,expand=1)
        fast_frame.place(relx=0,rely=0,relwidth=1,relheight=1)
        
        txt0 = tk.Label(fast_frame,text="Tabla de direcciones almacenadas.",font=('Arial',15),bg = "#434552",fg="white")
        txt0.place(relx=0.270,rely=0.01,relwidth=0.45,relheight=0.020)
        
        txt1 = tk.Label(fast_frame,text="Ingrese la direccion: ",font=('Arial',15),bg = "#434552",fg="white")
        txt1.place(relx=0.01,rely=0.6,relwidth=0.4,relheight=0.020)
        
        txt2 = tk.Label(fast_frame,text="Lista de barrios: ",font=('Arial',15),bg = "#434552",fg="white")
        txt2.place(relx=0.01,rely=0.75,relwidth=0.4,relheight=0.020)
        
        read_entry = tk.Entry(fast_frame,font=('Arial',15),bg = "#434552",fg="white")
        read_entry.place(relx=0.5,rely=0.6,relwidth=0.4,relheight=0.020)
        
        btn_search = tk.Button(fast_frame,text="Buscar la dirección ",font=('Arial',15),bg = "#434552",fg="white",command=cal)
        btn_search.place(relx=0.5,rely=0.635,relwidth=0.4,relheight=0.020)
        
        btn_del = tk.Button(fast_frame,text="Eliminar ",font=('Arial',15),bg = "#434552",fg="white",command=del_element)
        btn_del.place(relx=0.5,rely=0.825,relwidth=0.4,relheight=0.020)
        btn_del.config(state=DISABLED)
        
        btn_reload = tk.Button(fast_frame,text="Recargar ",font=('Arial',15),bg = "#434552",fg="white",command=reload)
        btn_reload.place(relx=0.5,rely=0.925,relwidth=0.4,relheight=0.020)
        btn_reload.config(state=DISABLED)
        
        
        combo_box = ttk.Combobox(fast_frame, values=["Red", "Green", "Blue"])
        combo_box.place(relx=0.5,rely=0.75,relwidth=0.4,relheight=0.020)
        combo_box.insert(0, "Seleccione Barrio")
        combo_box.config(state = DISABLED )
        
        rs_sheet = Sheet(fast_frame,column_width=180)
        rs_sheet.headers(['Dirección','Latitud y Longitud','Vecindario'])
        rs_sheet.place(relx=0.075,rely=0.045,relwidth=0.85,relheight=0.5)
        rs_sheet.change_theme(theme = "dark green")
        rs_sheet.font=('Arial',12)
        rs_sheet.enable_bindings("single_select","drag_select", "edit_cell", "select_all",
                                   "column_select",
                                   "row_select",
                                   "column_width_resize",
                                   "arrowkeys",
                                   "row_height_resize",
                                   "double_click_row_resize",
                                   "right_click_popup_menu",
                                   "rc_select")
        
        connection_on_mysql.truncate()
        preload()

        
        win.mainloop()
        
        
    except Exception as error:
        print(str(error))
