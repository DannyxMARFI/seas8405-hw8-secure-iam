reset:
	docker-compose down -v --remove-orphans
	rm -rf keycloak/realm-export.json
	docker-compose up --build

up:
	docker-compose up

down:
	docker-compose down

keycloak-export:
	docker exec -it keycloak /opt/keycloak/bin/kc.sh export \
		--dir /opt/keycloak/data/import \
		--realm demo-realm \
		--users realm_file
