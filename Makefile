.PHONY: frontend/% backend/%

frontend/%:
	$(MAKE) -C frontend $*

backend/%:
	$(MAKE) -C backend $*

pre-commit :
	$(MAKE) -C backend pre-commit
	git add --update

install : 
	cd backend && make install

setup : 
	cd backend && make setup

dev :
	cd backend && make dev

lint : backend/lint

client:
	$(MAKE) -C backend openapi
	mv backend/openapi.json frontend/openapi.json
	$(MAKE) -C frontend client
