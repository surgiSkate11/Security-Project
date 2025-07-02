@echo off
REM Crear entorno virtual
python -m venv venv

REM Activar entorno virtual
call venv\Scripts\activate

REM Instalar dependencias personalizadas
pip install -r dependencias.txt

REM Ejecutar migraciones
python manage.py migrate

REM Crear superusuario automáticamente
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='emiro@gmail.com').exists() or User.objects.create_superuser('emiro', 'emiro@gmail.com', '123') | python manage.py shell

REM Ejecutar el servidor
python manage.py runserver
