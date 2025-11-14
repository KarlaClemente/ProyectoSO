import tkinter as tk
from tkinter import ttk
import psutil

class MonitorSistema:
    def __init__(self, ventana):
        # Configuración de la ventana principal
        self.ventana = ventana
        self.ventana.title("Monitor de Sistema")
        # Tamaño inicial de la ventana
        self.ventana.geometry("700x500")
        # Diccionario que almacena las vistas, para poder alternar entre ellas
        self.vistas = {}

        self.create_buttons()
        # Marco para el contenido de las vistas, debajo de los botones
        self.content_frame = ttk.Frame(self.ventana, padding="10")
        self.content_frame.pack(side="top", fill="both", expand=True)
        self.create_views()
        self.show_view('Procesos')
        self.update()

    def create_buttons(self):
        """Crea el marco y los botones 'Procesos', 'Rendimiento'"""
        # Se crea marco superior donde se ubican los botones
        self.top_frame = ttk.Frame(self.ventana, padding="5 5 0 0")
        self.top_frame.pack(side="top", fill="x")
        # Botón Procesos
        ttk.Button(
            self.top_frame, 
            text="Procesos", 
            command=lambda: self.show_view('Procesos')
        ).pack(side="left", padx=2, pady=2)
        # Botón Rendimiento
        ttk.Button(
            self.top_frame, 
            text="Rendimiento", 
            command=lambda: self.show_view('Rendimiento')
        ).pack(side="left", padx=2, pady=2)

    def create_views(self):
        """Crea las vistas del monitor de sistema"""
        # VISTA DE PROCESOS
        # Se crea y almacena el marco de la vista de procesos
        frame_process = ttk.Frame(self.content_frame)
        self.vistas['Procesos'] = frame_process
        # Se definen las columnas
        columnas = ('pid', 'nombre', 'usuario', 'memoria')
        self.tree = ttk.Treeview(frame_process, columns=columnas, show='headings')
        # Encabezados de las columnas
        self.tree.heading('pid', text='PID')
        self.tree.heading('nombre', text='Nombre')
        self.tree.heading('usuario', text='Usuario')
        self.tree.heading('memoria', text='Memoria (MB)')
        # Ancho de columnas
        self.tree.column('pid', width=60, anchor='center')
        self.tree.column('nombre', width=250, anchor='w')
        self.tree.column('usuario', width=100, anchor='w')
        self.tree.column('memoria', width=120, anchor='center')
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_process, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.tree.pack(fill="both", expand=True)

        # VISTA DE RENDIMIENTO(MEMORIA, DISCO)
        rendimiento_frame = ttk.Frame(self.content_frame)
        self.vistas['Rendimiento'] = rendimiento_frame

    def show_view(self, view):
        """Muestra la vista seleccionada en la interfaz gráfica"""
        # Se ocultan todas las vistas
        for vista in self.vistas.values():
            vista.pack_forget()
        # Se muestra la vista seleccionada
        self.vistas[view].pack(fill="both", expand=True)
        if view == "Procesos":
            self.show_processes()

    def update(self):
        """Actualiza la información del monitor de sistema"""
        # Se actualiza la vista la cual este siendo mostrada
        if self.vistas['Procesos'].winfo_ismapped():
            self.show_processes()
        # Se actualiza la interfaz
        self.ventana.after(1000, self.update)

    def show_processes(self):
        """Muestra los procesos en la interfaz gráfica"""
        mb = 1024 * 1024
        # Se limpia el contenido anterior de la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        procesos_ordenados = self.get_processes()
        # 3. Insertar cada proceso en el Treeview
        # Se muestran solo los 50 primeros para evitar sobrecargar la GUI
        for proceso in procesos_ordenados:
            # Se convierte la memoria de bytes a megabytes
            memoria_mb = proceso['memoria_rss'] / mb
            self.tree.insert('', 'end', values=(
                proceso['pid'],
                proceso['nombre'],
                proceso['usuario'] or 'N/A', # Se muestra 'N/A' si no hay usuario
                f"{memoria_mb:.2f}"
            ))

    def get_disk(self):
        """Obtiene el uso del disco"""
        disco = psutil.disk_usage('/')
        return {'Total del disco': disco.total, 'En uso': disco.used, 'Libre': disco.free, 'Porcentaje': disco.percent}
    
    def get_memory(self):
        """Obtiene el uso de la memoria RAM"""
        memoria = psutil.virtual_memory()
        return {'Total de memoria': memoria.total, 'En uso': memoria.used, 'Libre': memoria.available, 'Porcentaje': memoria.percent}
    
    def get_processes(self):
        """Obtiene todos los procesos en ejecución ordenados por uso de memoria"""
        procesos = []
        # Se obtienen todos los procesos en ejecución
        for proc in psutil.process_iter(['name', 'username', 'memory_info', 'pid']):
            try:
                p_info = proc.info
                # Se obtiene el uso de la memoria física usada
                procesos.append({
                    'pid': p_info['pid'],
                    'usuario': p_info['username'],
                    'nombre': p_info['name'],
                    'memoria_rss': p_info['memory_info'].rss
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        # Se ordenan los procesos por uso de memoria
        procesos_ordenados = sorted(procesos, key=lambda p: p['memoria_rss'], reverse=True)
        return procesos_ordenados

if __name__ == "__main__":
    # Crear la ventana principal
    ventana = tk.Tk()
    monitor = MonitorSistema(ventana)
    # Mostrar la ventana, manteniéndola abierta
    ventana.mainloop()
        