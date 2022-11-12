import tkinter as tk
import pandas as pd
import subprocess
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx



class Interfaz:
    def __init__(self):
        
        #Variables iniciales
        self.N=0
        self.inicio=True
        
        #Ventana
        self.ventana=tk.Tk()
        self.ventana.title("Cálculo caminos")
        self.ventana.geometry("230x100")
        
        #Indicador para decir que ingrese por teclado
        self.indicador_origen=tk.Label(self.ventana,text='Origen = ')
        self.indicador_origen.grid(column=0,row=0)
        
        self.indicador_destino=tk.Label(self.ventana,text='Destino = ')
        self.indicador_destino.grid(column=0,row=1)
        
        #Entrada por teclado de origen y destino
        self.origen=tk.IntVar()
        self.teclado_origen=tk.Entry(self.ventana,width=20,textvariable=self.origen)
        self.teclado_origen.grid(column=1,row=0)
        
        self.destino=tk.IntVar()
        self.teclado_destino=tk.Entry(self.ventana,width=20,textvariable=self.destino)
        self.teclado_destino.grid(column=1,row=1)
        
        #Boton de Calcular
        self.bot_calcular=tk.Button(self.ventana,text='Calcular',command=self.boton_calcular_ruta)
        self.bot_calcular.grid(column=0,row=4)
        
        #Boton Abrir archivo
        self.bot_abrir=tk.Button(self.ventana,text='Abrir red',command=self.boton_abrir_red)
        self.bot_abrir.grid(column=0,row=3)
        
        #Etiqueta Valor de N
        self.indicador_N=tk.Label(self.ventana,text='N = '+str(self.N))
        self.indicador_N.grid(column=1,row=3)
        
        self.ventana.mainloop()
        
    #Método para calcular Rutas (cuando le das al boton calcular)
    def boton_calcular_ruta(self):
        #Llamas el programa en C
        if(self.llamar_C()):
            #Desplegar ventana si es la primera vez que das al boton
            """
            if(self.inicio):
                self.desplegar()
                self.desplegar_grafica()
            """
            #Escribir el resultado
            self.resultado()
            #Graficar red 1a vez
            self.actualizar_grafica()
        
    #Metodo que te permite visualizar red seleccioonada del .csv
    def boton_abrir_red(self):
        
        if(self.seleccionar_red()):
            self.desplegar_grafica()
            self.desplegar()
        
    
    #Método abre y almacena info necesaria de la red que hay en red.csv
    def seleccionar_red(self):
        self.red = pd.read_csv('red.csv',sep=';',header=None)
        
        #Comprobar que la matriz es adecuada para que funcione el algoritmo
        #fils=cols
        if (self.red.shape[0]!=self.red.shape[1]):
            tk.messagebox.showerror("Error", "Matriz no puede representar red (cols!=filas)")
            return False
        if(self.simetrica(self.red)==False):
            tk.messagebox.showerror("Error", "Matriz no puede representar red (no simétrica)")
            return False
        
        #Escribir valor N en la interfaz
        self.N=len(self.red.index)
        self.indicador_N.config(text ='N = '+str(self.N)) #Cambio de la etiqueta de N
        
        #Definir un objeto network para representarlo
        self.G = nx.from_pandas_adjacency(df=self.red)
        
        return True #Esto es para que siga el proceso de boton_abrir_red()
        
    def desplegar_grafica(self):
        #Representacion, aspecto básico y fijo
        
        self.posicion_red = nx.spring_layout(self.G) #Forma red decente
        self.etiquetas_nodos={node: node for node in self.G.nodes()}
        self.etiquetas_links = nx.get_edge_attributes(self.G,'weight') #Si no especificas edge_labels te sale el weight:valor
        self.colores_nodos=['pink']*self.G.number_of_nodes() #Color nodos  
        
        self.ventana.geometry("900x620")
        
        #Graficar
        self.figura=plt.figure(figsize=(9.5,6.25))
        nx.draw(
            self.G, self.posicion_red, edge_color='black', 
            width=5.5, linewidths=5,
            node_size=500, node_color=self.colores_nodos, alpha=0.9,
            labels=self.etiquetas_nodos,
            font_weight='bold')
        nx.draw_networkx_edge_labels(self.G, pos=self.posicion_red,
                                     edge_labels=self.etiquetas_links)
        
        self.bar = FigureCanvasTkAgg(self.figura, self.ventana)
        self.bar.get_tk_widget().grid(row=6, column=2)
        
     
    #Método para ejecutar el programa en C que calcula caminos
    def llamar_C(self):
        #Comprobacion de que antes hay que elegir archivo
        if(self.N==0):
            tk.messagebox.showerror("Error", "Selecciona primero .csv adecuado")
            return False
        
        else:
            #Comprobación previa de que los valores origen/destino entran en rango
            if (self.origen.get()>=self.N or self.origen.get()<0 or 
                self.destino.get()>=self.N or self.destino.get()<0):
                tk.messagebox.showerror("Error", "Origen y/o destino no válidos (0<=valor<N)")
                
            else:
                if(self.origen.get()==self.destino.get()):
                    tk.messagebox.showerror("Error", "Origen y destino deben ser distintos")
                else:
                    #Llamar a C (subprocess)
                    self.texto=str(self.origen.get())+"\n"+str(self.destino.get())+"\n"
                    self.proceso=subprocess.run(
                            ["calculo_camino_interfaz.exe"],
                            capture_output=True,
                            input=self.texto,
                            encoding="utf-8")
            
        return True

    #Método para que la 1a vez amplia ventana y representas red 
    def desplegar(self):
        #Ampliar ventana
        #self.ventana.geometry("230x230")
        
        #Crear etiquetas de las respuestas
        self.indicador_ruta=tk.Label(self.ventana,text='Ruta = ')
        self.indicador_ruta.grid(column=1,row=5)
        self.indicador_coste=tk.Label(self.ventana,text='Coste = ')
        self.indicador_coste.grid(column=0,row=5)
        
        self.inicio=False
        
    #Método que muestra resultado del calculo de las rutas    
    def resultado(self):
        #Captar string y los resultados
        self.outputs=self.proceso.stdout.split('\n')
        self.coste=int(self.outputs[-2])
        self.ruta=[]
        i=5
        while(self.outputs[i]!='Nodo_contiguo \tNodo_ord\tCoste_nodo'):
            self.ruta.append(int(self.outputs[i]))
            i+=1;
        
        #Etiquetas ruta y coste
        texto_ruta='Ruta = '+str(self.ruta[0])
        for i in range(1,len(self.ruta)):
            texto_ruta+='<-'+str(self.ruta[i])
        
        #Modificar etiquetas
        self.indicador_ruta.config(text =texto_ruta) #Cambio de la etiqueta de N
        self.indicador_coste.config(text ='Coste = '+str(self.coste))

        #Poner en color diferente los enlaces de la ruta
            #Por defecto todos los links en negro
        for i in self.G.edges():
            self.G[i[0]][i[1]]['color'] = 'black'
            # Poner los links de la ruta en otro color
        for i in range(0,len(self.ruta)-1):
            self.G[self.ruta[i]][self.ruta[i+1]]['color'] = 'blue'
            # Almacenas los valores de los colores de los links para graficar
        self.color_links = [ self.G[e[0]][e[1]]['color'] for e in self.G.edges() ]
        
        #Poner en color diferente los nodos origen/destino
        for i in range(0,self.G.number_of_nodes()):
            if(i==self.origen.get()): self.colores_nodos[i]='blue'
            elif(i==self.destino.get()): self.colores_nodos[i]='red'
            else: self.colores_nodos[i]='pink'
        

    def actualizar_grafica(self):
        #Limpiar contenido de la figura
        self.figura.clear()
        
        #Aplicar cambios
        nx.draw(
            self.G, self.posicion_red, edge_color=self.color_links, 
            width=5.5, linewidths=5,
            node_size=500, node_color=self.colores_nodos, alpha=0.9,
            labels=self.etiquetas_nodos,
            font_weight='bold')
        nx.draw_networkx_edge_labels(self.G, pos=self.posicion_red,
                                     edge_labels=self.etiquetas_links)
        #Limpiar el canvas que había en la ventana
        self.bar.draw_idle()
        
        #Representarlo
        self.bar = FigureCanvasTkAgg(self.figura, self.ventana)
        self.bar.get_tk_widget().grid(row=6, column=2)
        
    #Funcion para saber si una matriz es simétrica
    def simetrica(self,df):
        for i in range(0,df.shape[0]):
            for j in range(i+1,df.shape[1]):
                if(df.loc[i][j]!=df.loc[j][i]):
                    print(i,j)
                    return False     
        return True


a=Interfaz()