DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker/app.yml
STORAGES_FILE= docker/storages.yml
APP_CONTAINER = django-backend-app

.PHONY: app
app:
	$(DC) -f $(APP_FILE) $(ENV) up --build -d

.PHONY: storages
storages:
	$(DC) -f $(STORAGES_FILE) $(ENV) up --build -d

.PHONY: all
all:
	$(DC) -f $(STORAGES_FILE) -f $(APP_FILE) $(ENV) up --build -d

.PHONY: app-down
app-down:
	$(DC) -f $(APP_FILE) ${ENV} down

.PHONY: storages-down
storages-down:
	$(DC) -f $(STORAGES_FILE) ${ENV} down

.PHONY: all-down
all-down:
	$(DC) -f $(STORAGES_FILE) -f $(APP_FILE) $(ENV) down

.PHONY: app-shell
app-shell:
	$(EXEC) $(APP_CONTAINER) bash

.PHONY: app-logs
app-logs:
	$(LOGS) $(APP_CONTAINER) -f