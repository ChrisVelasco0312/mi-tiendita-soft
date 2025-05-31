ed:
	AUTO_NVIM=1 nix develop
nix:
	nix develop
dev:
	textual run --dev main.py
serve:
	textual serve main.py
console:
	textual console -x SYSTEM -x EVENT -x DEBUG
pinstall:
	poetry install --no-root
start:
	START=1 nix develop
run:
	poetry run python main.py

