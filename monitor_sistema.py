import tkinter as tk
from tkinter import ttk
import psutil
import time

class MonitorSistema:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Monitor de Sistema")
        self.ventana.geometry("1200x750")  
        #Diccionario que almacena las vistas, para poder alternar entre ellas
        self.vistas = {}

        #Para cálculo de I/O del disco
        self.last_disk = psutil.disk_io_counters()
        self.last_time = time.time()

        #Estado para Ordenamiento
        self.sort_criteria = 'cpu' 
        self.sort_reverse = True

        #Historial para Gráficas (60 puntos) 
        self.history_limit = 60
        self.cpu_history = [0] * self.history_limit
        self.ram_history = [0] * self.history_limit

        self.create_buttons()
        
        #Marco para el contenido de las vistas, debajo de los botones
        self.content_frame = ttk.Frame(self.ventana, padding="10")
        self.content_frame.pack(side="top", fill="both", expand=True)

        self.create_views()
        self.show_view('Procesos')

        self.update()

    def create_buttons(self):
        """Crea el marco y los botones 'Procesos', 'Rendimiento y Gráficas'"""
        #Se crea marco superior donde se ubican los botones
        self.top_frame = ttk.Frame(self.ventana, padding="5 5 0 0")
        self.top_frame.pack(side="top", fill="x")
        #Boton Procesos
        ttk.Button(self.top_frame, text="Procesos",
                   command=lambda: self.show_view('Procesos')).pack(side="left", padx=2)
        #Boton Rendimiento y Gráficas
        ttk.Button(self.top_frame, text="Rendimiento y Gráficas",
                   command=lambda: self.show_view('Rendimiento')).pack(side="left", padx=2)

    def create_views(self):
        #VISTA DE PROCESOS
        frame_process = ttk.Frame(self.content_frame)
        self.vistas['Procesos'] = frame_process

        # Panel de controles de Ordenamiento
        sort_frame = ttk.LabelFrame(frame_process, text="Ordenar Procesos por:", padding="5")
        sort_frame.pack(fill="x", pady=(0, 5))

        ttk.Button(sort_frame, text="Mayor CPU", 
                   command=lambda: self.set_sort('cpu', True)).pack(side="left", padx=5)
        ttk.Button(sort_frame, text="Mayor Memoria", 
                   command=lambda: self.set_sort('memoria', True)).pack(side="left", padx=5)
        ttk.Button(sort_frame, text="Mayor I/O (Disco)", 
                   command=lambda: self.set_sort('io_total', True)).pack(side="left", padx=5)
        ttk.Button(sort_frame, text="Prioridad (Nice)", 
                   command=lambda: self.set_sort('nice', False)).pack(side="left", padx=5)

        #Definición de Columnas
        columnas = ('pid', 'nombre', 'usuario', 'cpu', 'memoria', 'estado', 'nice', 'runtime', 'read', 'write')

        self.tree = ttk.Treeview(frame_process, columns=columnas, show='headings')

        # Encabezados de las columnas
        headers = {
            'pid': "PID", 
            'nombre': "Nombre", 
            'usuario': "Usuario",
            'cpu': "CPU (%)", 
            'memoria': "Memoria (MB)", 
            'estado': "Estado",
            'nice': "Nice", 
            'runtime': "Tiempo (s)", 
            'read': "Lecturas (KB)", 
            'write': "Escrituras (KB)"
        }

        for col, text in headers.items():
            self.tree.heading(col, text=text)
            

        # Anchura adecuada para cada columna
        ancho = {
            'pid': 50, 
            'nombre': 150, 
            'usuario': 90, 
            'cpu': 60, 
            'memoria': 90, 
            'estado': 70, 
            'nice': 50, 
            'runtime': 80, 
            'read': 80, 
            'write': 80
        }

        for col, w in ancho.items():
            self.tree.column(col, width=w, anchor='center')

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_process, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.tree.pack(fill="both", expand=True)

        #VISTA RENDIMIENTO
        rendimiento_frame = ttk.Frame(self.content_frame)
        self.vistas['Rendimiento'] = rendimiento_frame

       
        paned = ttk.PanedWindow(rendimiento_frame, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)

    
        left_container = ttk.Frame(paned)
        paned.add(left_container, weight=1)

        canvas_left = tk.Canvas(left_container, borderwidth=0, background="#f0f0f0")
        scrollbar_left = ttk.Scrollbar(left_container, orient="vertical", command=canvas_left.yview)
        self.scrollable_frame = ttk.Frame(canvas_left)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_left.configure(scrollregion=canvas_left.bbox("all"))
        )

        canvas_left.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas_left.configure(yscrollcommand=scrollbar_left.set)

        canvas_left.pack(side="left", fill="both", expand=True)
        scrollbar_left.pack(side="right", fill="y")

        #MÉTRICAS 
        ttk.Label(self.scrollable_frame, text="Métricas Generales", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
        
        #CPU Global
        self.cpu_label = ttk.Label(self.scrollable_frame, text="CPU Total: 0%")
        self.cpu_label.pack(anchor="w")
        self.cpu_bar = ttk.Progressbar(self.scrollable_frame, length=300)
        self.cpu_bar.pack(anchor="w", pady=2)

        #CPU por Núcleo
        ttk.Label(self.scrollable_frame, text="Por Núcleo:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.core_bars = []
        self.core_labels = []
        
        #Generar widgets para cada núcleo
        for i in range(psutil.cpu_count()):
            f = ttk.Frame(self.scrollable_frame)
            f.pack(anchor="w", fill="x")
            lbl = ttk.Label(f, text=f"Core {i}:", width=8)
            lbl.pack(side="left")
            bar = ttk.Progressbar(f, length=200)
            bar.pack(side="left", padx=5)
            percent_lbl = ttk.Label(f, text="0%", width=6)
            percent_lbl.pack(side="left")
            
            self.core_bars.append(bar)
            self.core_labels.append(percent_lbl)

        ttk.Separator(self.scrollable_frame).pack(fill="x", pady=10)

        #RAM
        self.ram_label = ttk.Label(self.scrollable_frame, text="RAM: 0%")
        self.ram_label.pack(anchor="w")
        self.ram_bar = ttk.Progressbar(self.scrollable_frame, length=300)
        self.ram_bar.pack(anchor="w", pady=2)

        #SWAP
        self.swap_label = ttk.Label(self.scrollable_frame, text="SWAP: 0%")
        self.swap_label.pack(anchor="w", pady=(5,0))
        self.swap_bar = ttk.Progressbar(self.scrollable_frame, length=300)
        self.swap_bar.pack(anchor="w", pady=2)

        ttk.Separator(self.scrollable_frame).pack(fill="x", pady=10)

        #DISCO USO
        ttk.Label(self.scrollable_frame, text="Almacenamiento (Disco Principal):", font=("Arial", 10, "bold")).pack(anchor="w")
        self.disk_label = ttk.Label(self.scrollable_frame, text="Cargando...")
        self.disk_label.pack(anchor="w")
        self.disk_bar = ttk.Progressbar(self.scrollable_frame, length=300)
        self.disk_bar.pack(anchor="w", pady=2)

        #DISCO I/O
        self.disk_io_label = ttk.Label(self.scrollable_frame, text="I/O: ...", font=("Arial", 9))
        self.disk_io_label.pack(anchor="w", pady=10)

        #GRÁFICAS
        right_panel = ttk.Frame(paned, padding="10")
        paned.add(right_panel, weight=2)
        
        ttk.Label(right_panel, text="Historial en Tiempo Real (60s)", font=("Arial", 12, "bold")).pack(pady=5)
        
        #Gráfica CPU
        ttk.Label(right_panel, text="Uso de CPU").pack(anchor="w")
        self.canvas_cpu = tk.Canvas(right_panel, height=200, bg="black")
        self.canvas_cpu.pack(fill="x", pady=5)
        
        #Gráfica RAM
        ttk.Label(right_panel, text="Uso de RAM").pack(anchor="w")
        self.canvas_ram = tk.Canvas(right_panel, height=200, bg="black")
        self.canvas_ram.pack(fill="x", pady=5)

    def set_sort(self, criteria, reverse):
        self.sort_criteria = criteria
        self.sort_reverse = reverse
        self.show_processes()

    def show_view(self, view):
        for vista in self.vistas.values():
            vista.pack_forget()
        self.vistas[view].pack(fill="both", expand=True)

        if view == "Procesos":
            self.show_processes()
        elif view == "Rendimiento":
            self.update_performance()

    def update(self):
        if self.vistas['Procesos'].winfo_ismapped():
            self.show_processes()
        
        self.update_performance() 
        self.ventana.after(1000, self.update)

    def draw_chart(self, canvas, data, color):
        """Dibuja línea en el canvas"""
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 10: return

        step = w / (len(data) - 1) if len(data) > 1 else w
        coords = []
        for i, val in enumerate(data):
            x = i * step
            y = h - (val / 100 * h)
            coords.append(x)
            coords.append(y)
        
        #Rejilla simple
        canvas.create_line(0, h/2, w, h/2, fill="#333", dash=(2,2))
        if len(coords) >= 4:
            canvas.create_line(*coords, fill=color, width=2)

    def show_processes(self):
        mb = 1024 * 1024
        for item in self.tree.get_children():
            self.tree.delete(item)

        procesos = self.get_processes()
        # Mostrar top 50
        for p in procesos[:50]:
            self.tree.insert('', 'end', values=(
                p['pid'], 
                p['nombre'], 
                p['usuario'],
                f"{p['cpu']:.1f}", 
                f"{p['memoria'] / mb:.1f}",
                p['estado'], p['nice'], 
                f"{p['runtime']:.2f}",
                f"{p['read_bytes']/1024:.0f}", 
                f"{p['write_bytes']/1024:.0f}"
            ))

    def update_performance(self):
        #Obtener Datos
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        #Actualizar Historiales
        self.cpu_history.append(cpu)
        self.cpu_history.pop(0)
        self.ram_history.append(ram.percent)
        self.ram_history.pop(0)

        #Dibujar UI
        if self.vistas['Rendimiento'].winfo_ismapped():
            #CPU Global
            self.cpu_bar['value'] = cpu
            self.cpu_label.config(text=f"CPU Total: {cpu}%")
            
            #CPU por Núcleo
            cores = psutil.cpu_percent(percpu=True)
            # Asegurarse de que coincida el número de cores 
            for i, (bar, lbl, val) in enumerate(zip(self.core_bars, self.core_labels, cores)):
                bar['value'] = val
                lbl.config(text=f"{val:.1f}%")

            #RAM & SWAP
            self.ram_bar['value'] = ram.percent
            self.ram_label.config(text=f"RAM: {ram.percent}% (Usada: {ram.used/1024**3:.1f}GB)")
            
            self.swap_bar['value'] = swap.percent
            self.swap_label.config(text=f"SWAP: {swap.percent}%")

            #Disco
            try:
                disk_usage = psutil.disk_usage('/')
                self.disk_bar['value'] = disk_usage.percent
                self.disk_label.config(text=f"Disco (/): {disk_usage.percent}% (Libre: {disk_usage.free/1024**3:.1f}GB)")
            except:
                pass

            #I/O
            new_disk = psutil.disk_io_counters()
            dt = time.time() - self.last_time
            if dt > 0:
                read_spd = (new_disk.read_bytes - self.last_disk.read_bytes) / dt
                write_spd = (new_disk.write_bytes - self.last_disk.write_bytes) / dt
                self.disk_io_label.config(text=f"I/O Lectura: {read_spd/1024:.1f} KB/s | Escritura: {write_spd/1024:.1f} KB/s")
                self.last_disk = new_disk
                self.last_time = time.time()

            #Gráficas
            self.draw_chart(self.canvas_cpu, self.cpu_history, "#00ff00") 
            self.draw_chart(self.canvas_ram, self.ram_history, "#00ccff") 

    def get_processes(self):
        procesos = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info', 
                                         'status', 'nice', 'io_counters', 'cpu_times']):
            try:
                info = proc.info
                read_b = info['io_counters'].read_bytes if info['io_counters'] else 0
                write_b = info['io_counters'].write_bytes if info['io_counters'] else 0
                
                #Runtime = User time + System time
                runtime = (info['cpu_times'].user + info['cpu_times'].system) if info['cpu_times'] else 0

                procesos.append({
                    'pid': info['pid'], 
                    'nombre': info['name'], 
                    'usuario': info['username'],
                    'cpu': info['cpu_percent'] or 0, 
                    'memoria': info['memory_info'].rss,
                    'estado': info['status'], 
                    'nice': info['nice'] or 0, 
                    'runtime': runtime, 'read_bytes': read_b, 
                    'write_bytes': write_b,
                    'io_total': read_b + write_b
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        return sorted(procesos, key=lambda p: p[self.sort_criteria], reverse=self.sort_reverse)

#EJECUCIÓN
if __name__ == "__main__":
    #Crear la ventana principal
    ventana = tk.Tk()
    monitor = MonitorSistema(ventana)
    "Mostrar la ventana, manteniendola abierta"
    ventana.mainloop()
