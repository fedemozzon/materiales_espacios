# materiales_espacios
- Para hacer migraciones docker-compose exec backend python ./api_materiales/manage.py makemigrations
- Para crear usuario docker-compose exec backend python ./api_materiales/manage.py createsuperuser
- Para volver a deployar hay que entrar a la carpeta de api_materiales(donde está el archivo fly.toml) y ejecutar flyctl deploy