.PHONY: init
init:
	./manage.py makemigrations
	./manage.py migrate
	./manage.py loaddata 000_users
#	./manage.py loaddata 000_project
#	./manage.py loaddata 001_entity
#	./manage.py loaddata 002_entity_field
#	./manage.py loaddata 002_collection_endpoint
#	./manage.py loaddata 002_item_endpoint
#	./manage.py loaddata 002_generic_endpoint

.PHONY: down
down: del-dev-migrations
	rm -f db.sqlite3

.PHONY: sync
sync:
	./manage.py sync_all

.PHONY: scores
scores:
	./manage.py list_scores

# Remove migrations que não foram adicionados.
.PHONY: del-dev-migrations
del-dev-migrations:
	git status --porcelain | grep "^?? "  | sed -e 's/^[?]* //' | \egrep "\migrations/00*"  | xargs -n1 rm -f
