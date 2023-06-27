build-intermediary:
	docker build -t intermediary-image -f Docker/Dockerfile.intermediary .

build:
	docker-compose down
	docker-compose build --no-cache app
	docker-compose up -d

build-prod:
	mv Caddyfile_prod Caddyfile
	docker-compose down
	docker-compose build --no-cache app
	docker-compose up -d

up:
	docker-compose up -d

down:
	docker-compose down

test:
	docker exec -it app python manage.py test --verbosity=2

load-data:
	docker exec -it app python manage.py loaddata data/consumers.csv
