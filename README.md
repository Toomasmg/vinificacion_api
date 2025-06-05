# 🍷 Sistema de Gestión de Vinificación - API Flask RESTful

## 👥 Integrantes
- Mateo Gomez  
- Leandro Briceño  
- Tomaz Muñoz  
- Villarroel Franco

---

## 🎯 Descripción del Proyecto

Aplicación web desarrollada con **Flask** que permite a una **bodega** gestionar digitalmente el proceso completo de **vinificación del vino**, desde la recepción de la uva hasta el embotellado final.  
Incluye:

- Gestión de variedades de uva (con imágenes).
- Registro y seguimiento técnico por etapas.
- Interfaz web con buscador y visualización de fotos.
- CRUD completo con API RESTful.
- Base de datos conectada con **MySQL** usando **UUIDs** como identificadores únicos.

---

## Requisitos

- Python 3
- MySQL

## Configuración del entorno

### 1. Crear un entorno virtual

#### En Linux / macOS:
```sh
python3 -m venv <nombre_del_entorno>
```

#### En Windows:
```sh
python -m venv <nombre_del_entorno>
```

### 2. Activar el entorno virtual

#### En Linux / macOS:
```sh
source <nombre_del_entorno>/bin/activate
```

#### En Windows:
```sh
<nombre_del_entorno>\Scripts\activate
```

### 3. Instalar dependencias

```sh
pip install Flask Flask-SQLAlchemy PyMySQL python-dotenv
```

## Configuración de la base de datos

Antes de ejecutar la aplicación, debes configurar las siguientes variables de entorno:

```sh
MYSQL_USER=<tu_usuario>
MYSQL_PASSWORD=<tu_contraseña>
MYSQL_DATABASE=<nombre_de_la_base_de_datos>
MYSQL_HOST=<host_de_mysql>
```

## Instalación y ejecución

1. Clona el repositorio:
```sh
git clone <url_del_repositorio>
```

2. Accede al directorio del proyecto:
```sh
cd <nombre_del_proyecto>
```

3. Instala las dependencias desde el archivo `requirements.txt`:
```sh
pip install -r requirements.txt
```

4. Ejecuta la aplicación:
```sh
python app.py
```