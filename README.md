# Banco de Horas

Aplicación web local para registrar y visualizar el tiempo dedicado a proyectos personales.

---

## Qué hace

- **Proyectos**: Crea y gestiona proyectos con nombre, descripción y color identificativo.
- **Imputación manual**: Registra horas y minutos pasados en un proyecto para una fecha concreta.
- **Timer en vivo**: Inicia un contador que se actualiza en tiempo real. Al detenerlo, guarda la entrada automáticamente.
- **Dashboard**: Vista resumen con total de horas por proyecto y listado de imputaciones recientes.

---

## Requisitos

- Python 3.11 o superior
- pip

---

## Instalación

```bash
# Clonar o descargar el repositorio
git clone <repo-url>
cd banco-de-horas

# Crear entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt
```

---

## Uso

```bash
streamlit run app.py
```

Se abrirá el navegador en `http://localhost:8501`.

### Navegación

La barra lateral izquierda tiene tres secciones:

| Sección | Descripción |
|---|---|
| **Dashboard** | Resumen de horas totales por proyecto y últimas imputaciones |
| **Imputar horas** | Formulario para añadir tiempo manualmente |
| **Timer** | Contador en vivo para registrar mientras trabajas |

### Primeros pasos

1. Ve a **Dashboard** y crea tu primer proyecto con el botón "Nuevo proyecto".
2. Usa **Imputar horas** para añadir tiempo pasado.
3. Usa **Timer** para contar tiempo en curso — pulsa "Iniciar" y "Detener" cuando termines.

---

## Datos

La aplicación guarda todos los datos en dos ficheros JSON dentro de la carpeta `data/`:

| Fichero | Contenido |
|---|---|
| `data/projects.json` | Lista de proyectos |
| `data/entries.json` | Lista de imputaciones |

La carpeta `data/` se crea automáticamente al primer uso. No se envía nada a ningún servidor.

Para hacer una copia de seguridad, copia la carpeta `data/`. Para empezar de cero, bórrala.

---

## Licencia

Uso personal. Sin licencia formal.
