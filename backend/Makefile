restart: down up

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

migrate:
	docker-compose run server python manage.py migrate

user:
	docker-compose run server python manage.py createsuperuser