SHELL := /usr/bin/env sh
TESTS := $(wildcard tests/*.sh)

INSTALL ?= install
PREFIX ?= /usr/local
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
	@printf "Installing loom man page to %s...\n" $(DESTDIR)$(MAN1DIR)
	@$(INSTALL) -Dm 644 docs/loom.1.gz $(DESTDIR)$(MAN1DIR)/loom.1.gz
	-@mandb > /dev/null 2>&1

uninstall:
	@printf "Uninstalling loom from %s/bin...\n" $(DESTDIR)$(PREFIX)
	@printf "Uninstalling loom documentation from %s...\n" $(DESTDIR)$(PREFIX)
	@$(RM) $(DESTDIR)$(PREFIX)/bin/loom
	@$(RM) $(DESTDIR)$(MAN1DIR)/loom.1.gz
	-@mandb > /dev/null 2>&1
