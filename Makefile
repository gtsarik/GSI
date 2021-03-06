MANAGE=bin/django
LOCALE=ru_RU.UTF-8

# Targets
.PHONY: run dbshell shell mkmigr_gsi migrate migrate_gsi mkmigr_cards migrate_cards mkmigr_wiki migrate_wiki test_gsi test_cards deploy static restart

default: run

run:
	$(MANAGE) runserver

dbshell:
	$(MANAGE) dbshell

shell:
	$(MANAGE) shell

migrate:
	$(MANAGE) migrate

mkmigr_gsi:
	$(MANAGE) makemigrations gsi

migrate_gsi:
	$(MANAGE) migrate gsi

mkmigr_cards:
	$(MANAGE) makemigrations cards

migrate_cards:
	$(MANAGE) migrate cards

mkmigr_log:
	$(MANAGE) makemigrations log

migrate_log:
	$(MANAGE) migrate log

mkmigr_wiki:
	$(MANAGE) makemigrations wiki

migrate_wiki:
	$(MANAGE) migrate wiki

mkmigr_article:
	$(MANAGE) makemigrations articles

migrate_article:
	$(MANAGE) migrate articles

mkmigr_customers:
	$(MANAGE) makemigrations customers

migrate_customers:
	$(MANAGE) migrate customers

deploy:
	fab deploy

static:
	fab collectstatic

restart:
	fab restart

dep_migrate:
	fab migrate

update:
	fab update

nginx:
	fab nginx

fill_name:
	fab fill_name_carditem

copy_db:
	fab copy_db

update_dev_db:
	fab update_dev_db

docs:
	fab docs

test_gsi:
	fab test_gsi

test_cards:
	fab test_cards

req:
	fab requirements

set_local_user_token:
	fab lokal_set_user_token
	
set_dev_user_token:
	fab dev_set_user_token
	
lokal_set_url_kml:
	fab lokal_set_url_kml
	
dev_set_url_kml:
	fab dev_set_url_kml
