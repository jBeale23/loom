SHELL := /usr/bin/env sh
TESTS := $(wildcard tests/*.sh)

INSTALL ?= install
PREFIX ?= /usr/local
BASH_COMP_DIR := $(shell pkg-config --variable=completionsdir bash-completion 2>/dev/null)
ifeq ($(BASH_COMP_DIR),)
    BASH_COMP_DIR = /usr/share/bash-completion/completions
endif
ZSH_COMP_DIR ?= $(PREFIX)/share/zsh/site-functions
MANDIR ?= $(PREFIX)/share/man
MAN1DIR = $(MANDIR)/man1

.PHONY: all default info install install-loom install-loom-info uninstall

default: all

all: info

info:
	@help2man ./loom -o docs/loom.1
	@gzip docs/loom.1

install: install-loom install-loom-info

install-loom:
	@printf "Installing loom to %s/bin...\n" $(DESTDIR)$(PREFIX)
	@$(INSTALL) -Dm 755 loom $(DESTDIR)$(PREFIX)/bin/loom

install-loom-info: docs/loom.1.gz
	@printf "Installing loom bash completion to %s...\n" $(DESTDIR)$(BASH_COMP_DIR)
	@$(INSTALL) -Dm 644 docs/loom-completion $(DESTDIR)$(BASH_COMP_DIR)/loom
	@printf "Installing loom zsh completion to %s...\n" $(DESTDIR)$(ZSH_COMP_DIR)
	@$(INSTALL) -Dm 644 docs/loom-completion $(DESTDIR)$(ZSH_COMP_DIR)/_loom
	@printf "Installing loom man page to %s...\n" $(DESTDIR)$(MAN1DIR)
	@$(INSTALL) -Dm 644 docs/loom.1.gz $(DESTDIR)$(MAN1DIR)/loom.1.gz
	-@mandb > /dev/null 2>&1

uninstall:
	@printf "Uninstalling loom from %s/bin...\n" $(DESTDIR)$(PREFIX)
	@printf "Uninstalling loom documentation from %s...\n" $(DESTDIR)$(PREFIX)
	@$(RM) $(DESTDIR)$(PREFIX)/bin/loom
	@$(RM) $(DESTDIR)$(BASH_COMP_DIR)/loom
	@$(RM) $(DESTDIR)$(ZSH_COMP_DIR)/_loom
	@$(RM) $(DESTDIR)$(MAN1DIR)/loom.1.gz
	-@mandb > /dev/null 2>&1
