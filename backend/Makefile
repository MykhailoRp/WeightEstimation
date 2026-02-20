setup :
	uv sync --group dev
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