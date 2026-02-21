pre-commit :
	cd backend && make pre-commit
	git add --update

install : 
	cd backend && make install

setup : 
	cd backend && make setup

dev :
	cd backend && make dev