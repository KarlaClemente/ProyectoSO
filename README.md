<a name="readme-top"></a>

# ProyectoSO: Monitor de Sistema

> Aplicación de un monitor de recursos desarrollada en Python para visualizar en tiempo real el rendimiento del sistema operativo e información detallada de los procesos en ejecución.

## Características Principales

- **Monitoreo de Procesos**: Visualización completa de todos los procesos activos con información detallada
- **Métricas de Rendimiento**: Seguimiento en tiempo real de CPU, RAM, SWAP y disco
- **Gráficas**: Visualización del uso de CPU y RAM en los últimos 60 segundos
- **Ordenamiento**: Múltiples criterios de ordenamiento como la CPU, Memoria, I/O y Prioridad


## Herramientas Utilizadas

- **Python 3.6+**
- **tkinter** para la interfaz gráfica
- **psutil** para la información del sistema


### Vista de Procesos
Visualiza hasta 50 procesos simultáneamente con información detallada:
- PID, nombre y usuario
- Uso de CPU y memoria
- Estado y prioridad
- Operaciones de I/O

### Vista de Rendimiento
Métricas en tiempo real:
- CPU total y por núcleo
- Uso de RAM y SWAP
- Almacenamiento y velocidad de I/O
- Gráficas históricas (60 segundos)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Prerequisitos de Ejacución

- Python 3.6 o superior
- pip (gestor de paquetes de Python)
* tkinter (generalmente incluido con Python)
* psutil (debe instalarse)
- Editor de texto 

### Instalación

1. Clonar el repositorio
```sh
   git clone https://github.com/KarlaClemente/ProyectoSO.git
```

2. Navega al directorio del proyecto
```sh
   cd ProyectoSO-main
```

3. Instalar las dependencias necesarias
```sh
   pip install psutil
```
   

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Uso

1. Ejecuta la aplicación
```sh
   python monitor_sistema.py
```

2. **Navegación por la interfaz:**
   
   **Vista de Procesos:**
   - Haz clic en los botones de ordenamiento para cambiar el criterio
   - Observa los procesos actualizándose cada segundo
   - Usa la barra de desplazamiento para ver más procesos

   **Vista de Rendimiento:**
   - Observa las métricas en tiempo real en el panel izquierdo
   - Monitorea las gráficas históricas en el panel derecho
   - Usa la barra de desplazamiento si es necesario

3. **Criterios de Ordenamiento:**
   - **Mayor CPU**: Ordena por uso de CPU (descendente)
   - **Mayor Memoria**: Ordena por uso de RAM (descendente)
   - **Mayor I/O**: Ordena por operaciones de disco (descendente)
   - **Prioridad (Nice)**: Ordena por valor nice (ascendente)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Características Técnicas


- **PID**: Identificador del proceso
- **Nombre**: Nombre del ejecutable
- **Usuario**: Usuario propietario
- **CPU (%)**: Porcentaje de uso de CPU
- **Memoria (MB)**: Memoria RAM utilizada
- **Estado**: Estado actual del proceso
- **Nice**: Prioridad del proceso
- **Tiempo (s)**: Tiempo de ejecución acumulado
- **Lecturas (KB)**: Operaciones de lectura en disco
- **Escrituras (KB)**: Operaciones de escritura en disco



### Métricas de Rendimiento

- **CPU**: Uso global y desglose por núcleo individual
- **RAM**: Porcentaje y cantidad en GB
- **SWAP**: Porcentaje de memoria swap utilizada
- **Disco**: Uso del sistema de archivos y velocidad de I/O en KB/s
- **Gráficas**: Historial de 60 segundos para CPU y RAM

### Frecuencia de Actualización

- Todas las métricas se actualizan cada **1 segundo**
- Las gráficas mantienen un historial de **60 puntos** 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Compatibilidad

Sistemas operativos compatibles:
- Windows 
- Linux 
- macOS 

**Nota**: En Linux/macOS, algunos procesos pueden requerir privilegios elevados:
```sh
sudo python monitor_sistema.py
```


## Autores

- Clemente Herrera Karla / GitHub: [@KarlaClemente](https://github.com/KarlaClemente)
- López Cortes Adamari Gianina / GitHub: [@adamariglc](https://github.com/adamariglc)
- Reyes Arteaga Angel David / GitHub: [@DavidReyesArt](https://github.com/DavidReyesArt)
<p align="right">(<a href="#readme-top">back to top</a>)</p>
