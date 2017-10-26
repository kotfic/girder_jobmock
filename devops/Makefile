COMPOSE_FILE=docker-compose.yml
PLAYBOOK_EXTRA_ARGS=""
_initialize: 
	pip install -U -r requirements.txt
	ansible-galaxy install -r requirements.yml --roles-path=roles/

check-env:
ifndef GIRDER_PATH
    $(error GIRDER_PATH is undefined)
endif

dev: check-env
	$(eval COMPOSE_FILE=docker-compose-dev.yml)
	$(eval PLAYBOOK_EXTRA_ARGS="-e development=1")
	@echo "Mounting Girder from $$GIRDER_PATH"


init: _initialize
	docker-compose -f $(COMPOSE_FILE) up -d
	ansible-playbook -i localhost, -e ansible_python_interpreter=$(shell which python) playbook.yml

start:
	docker-compose -f $(COMPOSE_FILE) up -d

stop:
	docker-compose -f $(COMPOSE_FILE) down

kill: stop
	docker-compose -f $(COMPOSE_FILE) kill


clean: kill
	pip uninstall -y -r requirements.txt
	rm -rf roles

.PHONY: init _initialize start stop kill clean
