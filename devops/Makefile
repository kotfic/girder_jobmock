_initialize: 
	pip install -U -r requirements.txt
	ansible-galaxy install -r requirements.yml --roles-path=roles/

init: _initialize
	docker-compose up -d
	ansible-playbook -i localhost, -e ansible_python_interpreter=$(shell which python) playbook.yml

start:
	docker-compose up -d

stop:
	docker-compose down

kill: stop
	docker-compose kill

clean: kill
	pip uninstall -y -r requirements.txt
	rm -rf roles

.PHONY: init _initialize start stop kill clean
