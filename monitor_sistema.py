import tkinter as tk
from tkinter import ttk
import psutil
import time

class MonitorSistema:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Monitor de Sistema")
        #Tamaño inicial de la ventana.
        self.ventana.geometry("1100x600")  
        #Diccionario que almacena las vistas, para poder alternar entre ellas.
        self.vistas = {}

        # Para cálculo de I/O del disco
        self.last_disk = psutil.disk_io_counters()
        self.last_time = time.time()

        self.create_buttons()
        #Marco para el contenido de las vistas, debajo de los botones
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
        #Botón procesos
        ttk.Button(self.top_frame, text="Procesos",
                   command=lambda: self.show_view('Procesos')).pack(side="left", padx=2)
        #Boton Rendimiento
        ttk.Button(self.top_frame, text="Rendimiento",
                   command=lambda: self.show_view('Rendimiento')).pack(side="left", padx=2)

    def create_views(self):
        # VISTA DE PROCESOS
        #Se crea y almacena el marco de la vista de procesos.
        frame_process = ttk.Frame(self.content_frame)
        self.vistas['Procesos'] = frame_process
        #Se definen las columnas
        columnas = (
            'pid', 'nombre', 'usuario', 'cpu', 'memoria', 'estado',
            'prioridad', 'read', 'write', 'tiempo'
        )

        self.tree = ttk.Treeview(frame_process, columns=columnas, show='headings')

        # Encabezados de las columnas
        headers = {
            'pid': "PID",
            'nombre': "Nombre",
            'usuario': "Usuario",
            'cpu': "CPU (%)",
            'memoria': "Memoria (MB)",
            'estado': "Estado",
            'prioridad': "Nice",
            'read': "Lecturas (KB)",
            'write': "Escrituras (KB)",
            'tiempo': "Tiempo (s)"
        }

        for col, text in headers.items():
            self.tree.heading(col, text=text)

        # Anchura adecuada para cada columna
        ancho = {
            'pid': 60,
            'nombre': 200,
            'usuario': 120,
            'cpu': 60,
            'memoria': 100,
            'estado': 80,
            'prioridad': 70,
            'read': 110,
            'write': 110,
            'tiempo': 80
        }

        for col, w in ancho.items():
            self.tree.column(col, width=w, anchor='center')
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_process, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        self.tree.pack(fill="both", expand=True)

        # VISTA RENDIMIENTO
        rendimiento_frame = ttk.Frame(self.content_frame)
        self.vistas['Rendimiento'] = rendimiento_frame

        # ------- CPU GENERAL -------
        ttk.Label(rendimiento_frame, text="CPU Total (%)", font=("Arial", 13, "bold")).pack(anchor="w")
        self.cpu_bar = ttk.Progressbar(rendimiento_frame, orient="horizontal", length=400, mode="determinate")
        self.cpu_bar.pack(pady=4)
        self.cpu_label = ttk.Label(rendimiento_frame, text="0 %")
        self.cpu_label.pack(anchor="w")

        # ------- CPU POR NÚCLEO -------
        ttk.Label(rendimiento_frame, text="CPU por Núcleo (%)", font=("Arial", 12)).pack(anchor="w", pady=(10, 2))
        self.core_bars = []
        self.core_labels = []

        for i in range(psutil.cpu_count()):
            frame = ttk.Frame(rendimiento_frame)
            frame.pack(anchor="w", fill="x")

            bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
            bar.pack(side="left", padx=5, pady=2)
            self.core_bars.append(bar)

            lbl = ttk.Label(frame, text="0 %")
            lbl.pack(side="left")
            self.core_labels.append(lbl)

        ttk.Separator(rendimiento_frame).pack(fill="x", pady=10)

        # ------- RAM -------
        ttk.Label(rendimiento_frame, text="Memoria RAM", font=("Arial", 13, "bold")).pack(anchor="w")
        self.ram_bar = ttk.Progressbar(rendimiento_frame, orient="horizontal", length=400, mode="determinate")
        self.ram_bar.pack(pady=4)
        self.ram_label = ttk.Label(rendimiento_frame, text="")
        self.ram_label.pack(anchor="w")

        ttk.Separator(rendimiento_frame).pack(fill="x", pady=10)

        # ------- SWAP -------
        ttk.Label(rendimiento_frame, text="Memoria Swap", font=("Arial", 13, "bold")).pack(anchor="w")
        self.swap_bar = ttk.Progressbar(rendimiento_frame, orient="horizontal", length=400, mode="determinate")
        self.swap_bar.pack(pady=4)
        self.swap_label = ttk.Label(rendimiento_frame, text="")
        self.swap_label.pack(anchor="w")

        ttk.Separator(rendimiento_frame).pack(fill="x", pady=10)

        # ------- DISCO -------
        ttk.Label(rendimiento_frame, text="Uso del Disco", font=("Arial", 13, "bold")).pack(anchor="w")
        self.disk_bar = ttk.Progressbar(rendimiento_frame, orient="horizontal", length=400, mode="determinate")
        self.disk_bar.pack(pady=4)
        self.disk_label = ttk.Label(rendimiento_frame, text="")
        self.disk_label.pack(anchor="w")

        self.disk_io_label = ttk.Label(rendimiento_frame, text="", font=("Arial", 10))
        self.disk_io_label.pack(anchor="w", pady=5)

    def show_view(self, view):
        """Muestra la vista seleccionada en la interfaz gráfica"""
        # Se ocultan todas las vistas
        for vista in self.vistas.values():
            vista.pack_forget()
        # Se muestra las vista seleccionada
        self.vistas[view].pack(fill="both", expand=True)

        if view == "Procesos":
            self.show_processes()
        elif view == "Rendimiento":
            self.update_performance()

    def update(self):
        """Actualiza la información del monitor de sistema"""
        # Se actualiza la vista la cual este siendo mostrada
        if self.vistas['Procesos'].winfo_ismapped():
            self.show_processes()

        if self.vistas['Rendimiento'].winfo_ismapped():
            self.update_performance()
        # Se actualiza la interfaz
        self.ventana.after(1000, self.update)

    # ========== TABLA DE PROCESOS ==========
    def show_processes(self):
        """Muestra los procesos en la interfaz gráfica"""
        mb = 1024 * 1024
        # Se limpia el contenido anterior de la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        procesos = self.get_processes()
        # Se muestran solo los 50 primeros para evitar sobrecargar la GUI
        for p in procesos[:50]:
            self.tree.insert('', 'end', values=(
                p['pid'],
                p['nombre'],
                p['usuario'],
                f"{p['cpu']:.1f}",
                f"{p['memoria'] / mb:.1f}",
                p['estado'],
                p['nice'],
                f"{p['read_bytes']/1024:.1f}",
                f"{p['write_bytes']/1024:.1f}",
                f"{p['tiempo']:.1f}"
            ))

    # ========== CPU, RAM y DISCO ==========
    def update_performance(self):

        # -------- CPU GENERAL --------
        cpu = psutil.cpu_percent(interval=0)
        self.cpu_bar['value'] = cpu
        self.cpu_label.config(text=f"{cpu:.1f} %")

        # -------- CPU POR NÚCLEO --------
        cores = psutil.cpu_percent(interval=0, percpu=True)
        for bar, label, value in zip(self.core_bars, self.core_labels, cores):
            bar['value'] = value
            label.config(text=f"{value:.1f} %")

        # -------- RAM --------
        ram = psutil.virtual_memory()
        self.ram_bar['value'] = ram.percent

        ram_total = ram.total / (1024**3)
        ram_used = ram.used / (1024**3)
        ram_free = ram.available / (1024**3)

        self.ram_label.config(
            text=f"Usada: {ram_used:.2f} GB | Libre: {ram_free:.2f} GB | Total: {ram_total:.2f} GB ({ram.percent}%)"
        )

        # -------- SWAP --------
        swap = psutil.swap_memory()
        self.swap_bar['value'] = swap.percent

        swap_total = swap.total / (1024**3)
        swap_used = swap.used / (1024**3)
        swap_free = swap.free / (1024**3)

        self.swap_label.config(
            text=f"Usada: {swap_used:.2f} GB | Libre: {swap_free:.2f} GB | Total: {swap_total:.2f} GB ({swap.percent}%)"
        )

        # -------- DISCO --------
        disco = psutil.disk_usage('/')
        self.disk_bar['value'] = disco.percent

        total = disco.total / (1024**3)
        usado = disco.used / (1024**3)
        libre = disco.free / (1024**3)

        self.disk_label.config(
            text=f"Usado: {usado:.2f} GB | Libre: {libre:.2f} GB | Total: {total:.2f} GB ({disco.percent}%)"
        )

        # -------- I/O --------
        new_disk = psutil.disk_io_counters()
        t = time.time()

        dt = t - self.last_time
        read_ps = (new_disk.read_bytes - self.last_disk.read_bytes) / dt
        write_ps = (new_disk.write_bytes - self.last_disk.write_bytes) / dt

        self.disk_io_label.config(
            text=f"Lectura: {read_ps/1024:.2f} KB/s | Escritura: {write_ps/1024:.2f} KB/s"
        )

        self.last_disk = new_disk
        self.last_time = t


    # ========== OBTENER PROCESOS ==========
    def get_processes(self):
        """Obtiene todos los procesos en ejecución ordenados por uso de memoria"""
        procesos = []
        # Se obtienen todos los procesos en ejecución
        for proc in psutil.process_iter([
            'pid', 'name', 'username', 'cpu_percent', 'memory_info',
            'status', 'nice', 'io_counters', 'create_time'
        ]):
            try:
                info = proc.info

                procesos.append({
                    'pid': info['pid'],
                    'nombre': info['name'],
                    'usuario': info['username'],
                    'cpu': info['cpu_percent'],
                    'memoria': info['memory_info'].rss,
                    'estado': info['status'],
                    'nice': info['nice'],
                    'read_bytes': info['io_counters'].read_bytes if info['io_counters'] else 0,
                    'write_bytes': info['io_counters'].write_bytes if info['io_counters'] else 0,
                    'tiempo': time.time() - info['create_time']
                })

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        # Se ordenan los procesos por uso de memoria
        return sorted(procesos, key=lambda p: p['cpu'], reverse=True)

# ========== EJECUCIÓN ==========
if __name__ == "__main__":
    #Crear la ventana principal
    ventana = tk.Tk()
    monitor = MonitorSistema(ventana)
    "Mostrar la ventana, manteniendola abierta"
    ventana.mainloop()
