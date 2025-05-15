dev:
	AUTO_NVIM=1 nix develop
install:
	poetry install --no-root
start:
	START=1 nix develop
run:
	poetry run python main.py

