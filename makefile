make build:
	docker compose down
	docker compose build --no-cache app
	docker compose up -d

make up:
	docker compose up -d

make down:
	docker compose down

make test:
	docker exec -it aktos_app python manage.py test

