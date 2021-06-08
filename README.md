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

Available routes:

**GET**
- / - Home page (table with albums)
- /login - Login page
- /logout
- /albums/:id/photos/ - Page with photos table for concrete album
- /albums/ - Get all albums in format
```json
[
  {
    "id": 1,
    "title": "Lorem ipsum"
  },
  ...
]
```
- /albums/:id/ - Get album by id with all the photos belong to him
```json
{
  "id": 1,
  "title": "Lorem ipsum",
  "photos": [
    {
      "id": 1,
      "title": "Some image title",
      "url": "https://some.link",
      "thumbnail_url": "https://some.link/thumbnail"
    },
    ...
  ]
}
```

**PATCH**
- /albums/:id/ - Update album by ID (accepted JSON only with title parameter)

**DELETE**
- /albums/:id/ - Delete album by ID

