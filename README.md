### Setup project
1. Rename .env.example to .env
2. [Generate](https://djecrety.ir/) secret key for Django
3. Set up secret key, **host, username, password, db name** for database and **user/pass and host** for rabbitmq
4. Install [docker](https://docs.docker.com/get-docker/) and docker-compose (if not installed yet)
5. Run this commands one by one (all commands are executed with **sudo** permissions):
```bash
$ docker-compose build
$ docker-compose up -d
```
6. Apply migrations:
```bash
$ docker-compose exec app python manage.py makemigrations
$ docker-compose exec app python manage.py migrate
```
7. Create superuser (if need access to home page with tables)
```bash
$ docker-compose exec app python manage.py createsuperuser
```

Run management script with command:
```bash
$ docker-compose exec app python manage.py fetch_albums [--threads THREADS (int)] [--chunk_size CHUNK_SIZE (int)]
```