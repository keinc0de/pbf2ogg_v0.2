import tkinter as tk
from tkinter import ttk
from pathlib import Path
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
from pbf_decode import ArchivoPbf
import io


class Interfaz2(TkinterDnD.Tk):
    def __init__(self):
        super(Interfaz2, self).__init__()
        self.geometry('400x250')

        s = ttk.Style()
        s.theme_use('clam')
        s.configure(
            'Treeview', rowheight=56, background='gray10',
            fieldbackground='gray10', foreground='white'
        )
        s.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        s.map('Treeview', background=[('selected', '#1C4A5C')], foreground=[('selected', '#D5D3C1')])

        cols = ['TIEMPO', 'TAGS']
        self.arbol = ttk.Treeview(self, columns=cols)
        self.arbol.heading('#0', text='IMAGEN')
        self.arbol.heading('TIEMPO', text='TIEMPO')
        self.arbol.heading('TAGS', text='TAGS')
        self.columnconfigure(0, weight=1)
        self.arbol.pack(fill='both', expand=1)
        scroll = tk.Scrollbar(self, orient='vertical', command=self.arbol.yview)
        self.arbol.config(yscrollcommand=scroll.set)
        scroll.pack(fill='y', expand=0, side='right', in_=self.arbol)

        self.arbol.column('TIEMPO', width=80)
        self.arbol.column('#0', width=120)
        fmb = tk.Frame(self, bg='gray10')
        fmb.pack(expand=0, fill='x')
        self.lb = tk.Label(fmb,bg='gray10', fg='#F0EAD6', justify='left')
        self.lb.pack(side='left', fill='x', expand=1)
        self.bt_save = tk.Button(
            fmb, text='CREAR OGG', bg='gray10', fg='#F0EAD6', command=self.crea_archivo_ogg
        )
        self.bt_save.pack(side='left')

        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drop_archivo)
        self.valores_iniciales()

    def _muestra_imagen(self):
        with Image.open('3.jpg') as img:
            self.ico = ImageTk.PhotoImage(img.resize((100,55)))
        for x in range(8):
            self.arbol.insert(
                parent='',
                index='end',
                values=("01:40:1-{0}", 'marcador con n{0}'.format(x+1)),
                image=self.ico
            )

    def valores_iniciales(self):
        for item in self.arbol.get_children():
            self.arbol.delete(item)
        self.contenido = []
        self.archivo = None
        self.contenido = []
        self.title('PBF2OGG v0.2')
        ico_data = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACyUlEQVR4nG2SS2hddRjEf9/3P+fek9xCm2KCrSlVUhUSimIF8bUQN+KjRUVBEBTMSpEo9QFu4qW40FYUVKgiiIpKrcbYCBURtIW2C4mI9SK14IOSVlttavO45557zn9cJNGNsxoGZuZj+Kz3yU8PkNY3qsxnTXoNfJdCeoqqOOHihejssTQ7RNH+bHHnnW+AAYJlkgitplh43/ARYTeYada6+Tvy8JRcGxCnFp+7ZSvAlte3pLH/6KZNZfHT3nupANyMeUt77sLsSpmOCusj633a0Bdy/8GMoeyJ/d8NPD92H2unD2LWPK7w1eaPGQRwsIhZkVA9k0qHzUgoy7eA60LVvcKkk4aaSTg77fBo6MYpx4bqRWYA7orryzI/dH7n3e/NhUYaPDSgOmOmwXlrrOlYUnZ23frJzPZ3j8dYe6xTU/NcqtELTuenx8dxnw+rJvuq/NdfHui/8Or2j+05apPy5PoF7xu7Y/HItxfFP49F6gzvS4cXMw32n6M1tGAPT19aH2w2iaZt3EiNVzAux5mh4PEwwVS1jRep8yAij/C2/8w462iS8RCQAQeoGLXyHmuFGsPkOkKda6uuH+uajWWZPo9tzchoBGkNMErKm7HkDOJ372EzbbZ7QKsp1AEeoeBkUKynZbURxehRe4M0RQIxchkQER+52EGAKAYShGNAoIuoAA+GAMdoAK8SmZTTR8C9Sw+Bb8i5343vE1ZQ4ctRAgIlADcjbqNi1sQ+CiAyAuwnUEfsdv4PhjAAzmJkOCNRZMvaHHCelEuiGPgvIBBXnhwRWbrta2APjjC6BABaODsAYXR82WRFl4BI4N9VBNQQvQjzpV2EkxDpXelNMP4iYX0iXiJhHSWtMvJbUmHAVoxVVORutFjSbkdcQ8RcnHAiz1LxhyfcFOFvnJeTwJd0mCBwMc5ajN3M8SElH+BsIOUq2hwkMvEPnwA3TMGBCg4AAAAASUVORK5CYII='
        ico = tk.PhotoImage(data=ico_data)
        self.iconphoto(True, ico)

    def drop_archivo(self, event):
        try:
            e = event.data
            if e.startswith('{'):
                e = e[1:]
            if e.endswith('}'):
                e = e[:-1]
            nom = Path(e).name
            self.title(nom)

            pbf = ArchivoPbf(e)
            self.imagenes = []
            uno = pbf.decode()
            self.valores_iniciales()

            linea_texto = f"CHAPTER01=00:00:00.000\n"\
                        f"CHAPTER01NAME=01 inicio\n"
            self.contenido.append(linea_texto)
            for x, d in enumerate(uno):
                img1 = d.get('imagen hex')
                indice, tiempo, titulo = x+1, d.get('tiempo'), d.get('titulo')
                valores = tiempo, titulo
                self.ico = ImageTk.PhotoImage(self.quita_bordes_negros(img1))
                self.imagenes.append(self.ico)
                self.arbol.insert(parent='', index='end', image=self.ico, values=valores)
                
                linea_texto = f"CHAPTER{indice+1:02d}={tiempo}\n"\
                            f"CHAPTER{indice+1:02d}NAME={indice+1:02d} {titulo}\n"
                self.contenido.append(linea_texto)
                self.lb.config(text=f"{str(indice)} marcadores. - {nom}", fg='#A2C776')
            self.archivo = Path(e)
        except Exception as err:
            self.lb.config(text=f"ERR: {err}", fg='#E45C68')

    def quita_bordes_negros(self, img_hex, md=16):
        filei = io.BytesIO(img_hex)
        img_pil = Image.open(filei)
        w, h = img_pil.size
        return img_pil.crop((0,md,w,h-md)).resize((100,55))

    def crea_archivo_ogg(self):
        if self.archivo is not None:
            nom = f"OGG {self.archivo.stem}.txt"
            ruta = f"{self.archivo.with_name(nom)}"
            with open(ruta, 'w') as txt:
                txt.writelines(self.contenido)
            self.lb.config(text='archivo OGG creado.')
        

if __name__=="__main__":
    app = Interfaz2()
    app.mainloop()