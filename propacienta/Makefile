.SILENT:

local:
	docker-compose -f local.yml up $(SERVICE) --remove-orphans

local_nginx:
	docker-compose -f local.yml up reverse_proxy

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
	sudo docker-compose -f production.yml up --build -d

down_prod:
	sudo docker-compose -f production.yml down

backup_db:
	./backup_db_production.sh

manage_local:
	docker-compose -f local.yml run --rm django ./manage.py $(NAME)

create_superuser_local:
	docker-compose -f local.yml run --rm django ./manage.py createsuperuser

startapp_local:
	docker-compose -f local.yml run --rm django ./manage.py startapp $(APP) && sudo chown ghost:ghost -R ./