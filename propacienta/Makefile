.SILENT:

local:
	docker-compose -f local.yml up $(SERVICE) --remove-orphans

local_django:
	docker-compose -f local.yml up django $(SERVICE) --remove-orphans

local_django_nginx:
	docker-compose -f local.yml up django reverse_proxy $(SERVICE) --remove-orphans

local_build:
	docker-compose -f local.yml up --build --remove-orphans

local_nginx:
	docker-compose -f local.yml up reverse_proxy

local_coturn:
	docker-compose -f local.yml up coturn

db:
	docker-compose -f local.yml up --remove-orphans -d postgres

pgadmin:
	docker-compose -f local.yml up --remove-orphans -d pgadmin

down:
	docker-compose -f local.yml down

make_migrations_local:
	docker-compose -f local.yml run --rm django python manage.py makemigrations && sudo chown ghost:ghost -R ./

migrate_production:
	sudo docker-compose -f production.yml run --rm django python manage.py migrate

production:
	sudo docker-compose -f production.yml up --build -d --remove-orphans

down_prod:
	sudo docker-compose -f production.yml down

backup_db:
	./backup_db_production.sh

manage_local:
	docker-compose -f local.yml run --rm django ./manage.py $(COMMAND)

local_shell:
	docker-compose -f local.yml run --rm django ./manage.py shell

create_superuser_local:
	docker-compose -f local.yml run --rm django ./manage.py createsuperuser

startapp_local:
	docker-compose -f local.yml run --rm django ./manage.py startapp $(APP) && sudo chown ghost:ghost -R ./

manage_production:
	sudo docker-compose -f production.yml run --rm django ./manage.py $(COMMAND)

production_shell:
	sudo docker-compose -f production.yml run --rm django ./manage.py shell

create_superuser_production:
	sudo docker-compose -f production.yml run --rm django ./manage.py createsuperuser

production_logs:
	sudo docker-compose -f production.yml logs -f