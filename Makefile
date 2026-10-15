.DEFAULT_GOAL := help

QUARTO ?= quarto
PYTHON ?= $(shell pyenv which python 2>/dev/null || command -v python3)
QUARTO_PYTHON ?= $(PYTHON)

-include Makefile.local

export QUARTO_PYTHON

BOOK_RU_DIR := ru/book
BOOK_EN_DIR := en/book
SLIDES_RU_DIR := ru/slides
SLIDES_EN_DIR := en/slides

.PHONY: help check-env ci-setup sync-shared site home slides ru-slides en-slides books ru en ru-html en-html ru-pdf en-pdf ru-preview clean

help: ## Показать цели сборки
	@printf '%s\n' 'Доступные цели:'
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_.-]+:.*## / {printf "  %-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check-env: ## Проверить Quarto и Python
	@command -v "$(QUARTO)" >/dev/null 2>&1 || { echo "Не найден quarto: $(QUARTO)"; exit 1; }
	@if ! command -v "$(PYTHON)" >/dev/null 2>&1 && [ ! -x "$(PYTHON)" ]; then \
	  echo "Не найден Python: $(PYTHON)"; exit 1; \
	fi

ci-setup: ## Установить зависимости для CI
	$(PYTHON) -m pip install -r requirements.txt

site: check-env ## Собрать полный сайт в _site (страница курса, книги и слайды RU и EN)
	rm -rf _site $(BOOK_RU_DIR)/_book $(BOOK_EN_DIR)/_book $(SLIDES_RU_DIR)/_site $(SLIDES_EN_DIR)/_site
	$(QUARTO) render
	$(QUARTO) render $(BOOK_RU_DIR) --to html
	$(QUARTO) render $(BOOK_EN_DIR) --to html
	$(QUARTO) render $(SLIDES_RU_DIR)
	$(QUARTO) render $(SLIDES_EN_DIR)
	find _site -type f -name '*.qmd' -delete
	test -s _site/index.html
	test -s _site/ru/slides/index.html
	test -s _site/en/slides/index.html
	test -s _site/ru/book/index.html
	test -s _site/en/book/index.html

sync-shared: check-env ## Обновить общие RevealJS- и книжные ресурсы из ../neutrinohit-map
	$(PYTHON) scripts/sync_shared_assets.py

home:check-env ## Собрать только страницу курса (_site/index.html)
	$(QUARTO) render

slides: ru-slides en-slides ## Собрать слайды RU и EN

ru-slides: check-env ## Собрать русские слайды
	$(QUARTO) render $(SLIDES_RU_DIR)

en-slides: check-env ## Собрать английские слайды
	$(QUARTO) render $(SLIDES_EN_DIR)

books: ru en ## Собрать обе книги

ru: check-env ## Собрать русскую книгу целиком
	$(QUARTO) render $(BOOK_RU_DIR)

en: check-env ## Собрать английскую книгу целиком
	$(QUARTO) render $(BOOK_EN_DIR)

ru-html: check-env ## Собрать HTML русской книги
	$(QUARTO) render $(BOOK_RU_DIR) --to html

en-html: check-env ## Собрать HTML английской книги
	$(QUARTO) render $(BOOK_EN_DIR) --to html

ru-pdf: check-env ## Собрать PDF русской книги
	$(QUARTO) render $(BOOK_RU_DIR) --to pdf

en-pdf: check-env ## Собрать PDF английской книги
	$(QUARTO) render $(BOOK_EN_DIR) --to pdf

ru-preview: check-env ## Локальный предпросмотр русской книги
	$(QUARTO) preview $(BOOK_RU_DIR) --to html

clean: ## Очистить артефакты сборки
	rm -rf _site .quarto .make-tmp
	rm -rf $(BOOK_RU_DIR)/_book $(BOOK_RU_DIR)/.quarto $(BOOK_EN_DIR)/_book $(BOOK_EN_DIR)/.quarto
	rm -rf $(SLIDES_RU_DIR)/.quarto $(SLIDES_EN_DIR)/.quarto
