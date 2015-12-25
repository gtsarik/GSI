MANAGE=bin/django
LOCALE=ru_RU.UTF-8

# Targets
.PHONY: run dbshell shell mkmigr_gsi migrate_gsi mkmigr_cards migrate_cards test_gsi test_cards

default: run

run:
	$(MANAGE) runserver

dbshell:
	$(MANAGE) dbshell

shell:
	$(MANAGE) shell

mkmigr_gsi:
	$(MANAGE) makemigrations gsi

migrate_gsi:
	$(MANAGE) migrate gsi

mkmigr_cards:
	$(MANAGE) makemigrations cards

migrate_cards:
	$(MANAGE) migrate cards

test_gsi:
	$(MANAGE) test gsi

test_cards:
	$(MANAGE) test cards
