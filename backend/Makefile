# TODO: add test logging
test :
	docker compose -f docker-compose.test.yml down -v --remove-orphans
	docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from test_result --remove-orphans
	docker compose -f docker-compose.test.yml down -v --remove-orphans

dev : 
	docker compose up --build --remove-orphans

api : 
	uv run uvicorn api.main:app --host localhost --port 8000 --reload

install : 
	uv sync --all-packages --group dev

setup : install
	uv run pre-commit install

style : 
	@echo "Stylechecking..."
	@uv run ruff check --fix

format :
	@echo "Formatting..."
	@uv run ruff format

type : 
	@echo "Typechecking..."
	@uv run mypy .

lint : style format type

pre-commit : lint

NAME ?=
migrate : 
	docker compose run --rm db_setup uv run alembic upgrade head

migration : migrate
	@test -n "$(NAME)" || { echo "NAME is required! Usage: make migration NAME=value"; exit 1; }
	docker compose run --rm db_setup uv run alembic revision --autogenerate -m "$(NAME)"
