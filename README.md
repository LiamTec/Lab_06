# 🚀 Mi Proyecto de Django 

Este es mi primera proyecto de django realizado en Tecsup, laboratorio 7

## 📋 Descripción general

La estructura de mi proyecto de django es el siguiente:

"src" : Directorio de codigo principal 

"config" : Configuracion de Proyecto 

"core" : Aplicacion principal 

"venv" : Entorno virtual (No registrado en git)

## ✨ Caracteristicas

Estrucutura de Django limpio y ordenado 

Separacion de la confisuracion y codigo de la aplicacion

Listo para utilizar frameworks fronted 

Interfaz de admin para gestion de contenido 

## 🔧 Intalacion 

1. Clona el repositorio 

2. Crea y activa el entorno virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate

3. Intalacion de las dependencias:
    ```bash
    cd src
    pip install -r requirements.txt
    pip install django pillow

4. Aplica Miagraciones:
    ```bash
    python manage.py migrate

5. Aplicar los seed :
   ```bash
   python manage.py seed_data

5. Crear el superusuario:
    ```bash
    python3 manage.py createsuperuser

## 🚀 Running the Project

Para la ejecucion del proyecto se realiza los siguientes comandos.

      cd src
      python manage.py runserver
    
acceso al sitio web en http://127.0.0.1:8000/ y al admin en http://127.0.0.1:8000/admin/

## 🛠️ Desarrollo

Agregar modelos a core/models.py

Crear vistas en core/views.py

Agregar patrones de URL en core/urls.py

Crear plantillas en core/templates/

## 📝 Licencia

Este proyecto está licenciado bajo la licencia MIT: consulte el archivo de LICENCIA para obtener más detalles.

## 👤 Autor

Alessandro Davila Perez 
Liam Gonzales Rojas
Gean Santana Luna 

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Creado con ❤️ y Django 
