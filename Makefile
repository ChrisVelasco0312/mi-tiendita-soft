ed:
	AUTO_NVIM=1 nix develop
nix:
	nix develop
dev:
	textual run --dev main.py
serve:
	textual serve main.py
install:
	poetry install --no-root
start:
	START=1 nix develop
run:
	poetry run python main.py

