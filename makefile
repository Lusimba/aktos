build:
	docker compose down
	docker compose build --no-cache app
	docker compose up -d

up:
	docker compose up -d

down:
	docker compose down

test:
	docker exec -it aktos_app python manage.py test

