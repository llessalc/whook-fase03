THISDIR := $(notdir $(CURDIR))
PROJECT := $(THISDIR)

api_up:
	docker compose -f docker-compose-app.yml up --force-recreate --build -d

db_up:
	docker compose -f docker-compose-db.yml up --force-recreate -d

api_down:
	docker compose -f docker-compose-app.yml down --remove-orphans

db_down:
	docker compose -f docker-compose-db.yml down --remove-orphans

prune-system:
	docker system prune --force

api_logs:
	docker compose -f docker-compose-app.yml logs -f

db_logs:
	docker compose -f docker-compose-db.yml logs -f

down-clean-vols:
	docker compose -f docker-compose-db.yml down --remove-orphans -v && \
	docker compose -f docker-compose-app.yml down --remove-orphans -v
