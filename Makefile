PYTHON = python3
MODULE = app.main
ENV_DIR = .env
ENV_PYTHON = $(ENV_DIR)/bin/python
ENV_PIP = $(ENV_DIR)/bin/pip
ZSHRC = $(HOME)/.zshrc
LOCK_CMD_DIR = $(HOME)/.local/bin
LOCK_CMD = $(LOCK_CMD_DIR)/lock
PIP_DEPS = pynput

LOCK_ALIAS = alias lock='cd $(CURDIR) && $(ENV_PYTHON) -m $(MODULE)'

run: pull setup-env check-tkinter setup-lock
	$(ENV_PYTHON) -m $(MODULE)

pull:
	git pull --ff-only

setup-env:
	@if [ ! -d "$(ENV_DIR)" ]; then \
		echo "Creation de $(ENV_DIR)"; \
		$(PYTHON) -m venv $(ENV_DIR); \
	fi
	@$(ENV_PIP) install --upgrade pip
	@$(ENV_PIP) install $(PIP_DEPS)

check-tkinter:
	@$(ENV_PYTHON) -c "import tkinter" >/dev/null 2>&1 || ( \
		echo "Erreur: tkinter n'est pas installe sur le systeme."; \
		echo "Installe le paquet systeme puis relance make run:"; \
		echo "  Debian/Ubuntu : sudo apt install python3-tk"; \
		echo "  Fedora       : sudo dnf install python3-tkinter"; \
		echo "  Arch         : sudo pacman -S tk"; \
		exit 1 \
	)

setup-lock:
	@if [ ! -f "$(ZSHRC)" ]; then \
		touch "$(ZSHRC)"; \
	fi
	@mkdir -p "$(LOCK_CMD_DIR)"
	@printf '%s\n' '#!/usr/bin/env sh' 'cd "$(CURDIR)" || exit 1' 'exec "$(CURDIR)/$(ENV_PYTHON)" -m $(MODULE) "$$@"' > "$(LOCK_CMD)"
	@chmod +x "$(LOCK_CMD)"
	@sed -i "/^alias lock=/d" "$(ZSHRC)"
	@echo "$(LOCK_ALIAS)" >> "$(ZSHRC)"
	@echo "Alias lock mis a jour dans $(ZSHRC)"
	@echo "Commande lock creee dans $(LOCK_CMD)"

clean:
	@rm -rf $(ENV_DIR)
	@find . -name "*.pyc" -delete
	@find . -name "*.pyo" -delete
	@find . -name "__pycache__" -delete
.PHONY: run pull setup-env check-tkinter setup-lock clean