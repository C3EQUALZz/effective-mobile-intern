STORAGES_FILE= docker/storages.yml
ENV = --env-file .env

.PHONY: storages
storages:
	$(DC) -f $(STORAGES_FILE) $(ENV) up --build -d

.PHONY: storages-down
storages-down:
	$(DC) -f $(STORAGES_FILE) ${ENV} down