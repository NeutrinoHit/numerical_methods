# Численные методы для физиков

Часть NeutrinoHit. Двуязычный Quarto-проект: курс из 17 лекций (по 1.5 часа,
для бакалавров, один семестр), общие задачи и книга (книга собирается локально и на сайте не публикуется). Авторы — Кирилл
Базаров и Дмитрий Наумов. Лекция — одна физическая задача;
вычислительные методы вводятся тогда, когда задача их требует. Язык — Python с
Numba. Пакет LightHit используется как пример в нескольких лекциях. Статус:
содержание готовится. Предлагаемый план курса — на странице курса
([`_includes/course-plan-ru.qmd`](_includes/course-plan-ru.qmd)).

## Структура

- `index.qmd`, `_quarto.yml`, `styles.css` — страница курса (корень сайта) с
  планом курса и инструкциями для авторов;
- `ru/slides/`, `en/slides/` — слайды (RevealJS) и программа курса;
  `exercises/` — страницы задач; `notebooks/` — ноутбуки лекций;
- `ru/book/`, `en/book/` — книга (`make ru`, `make en`; в `make site` не входит);
- `_includes/course-plan-ru.qmd` — предлагаемый план курса;
- `_includes/exercises/` — общие задачи: один файл на лекцию и язык, подключается
  и в страницу задач слайдов, и в главу книги;
- `shared/` — общие стили, библиография, рисунки, общий код и ноутбуки,
  файлы для Reveal и PDF (`ru/slides/shared` и `en/slides/shared` — ссылки на него);
- `docs/` — инструкции для авторов: `git-guide.md`, `quarto-guide.md`,
  `authoring-guide.md` (публикуются на сайте курса);
- `scripts/` — служебные скрипты (`sync_shared_assets.py`, `export_notebooks.py`).

Лекции, которые ещё не вошли в курс, хранятся без номера в `planned/`
(`ru|en/slides/planned/`, `ru|en/book/planned/`, `_includes/exercises/planned/`)
и не входят в публикацию. Номер присваивается вместе с публикацией; при этом
файл лекции, ноутбук, глава и файл задач переносятся одновременно (подробности —
в `docs/quarto-guide.md`).

## Сборка

```bash
python -m pip install -r requirements.txt
make help
make site
```

`make site` собирает страницу курса, HTML-книги и слайды RU и EN в `_site/`.
Пока в списках публикации только главные страницы.

## Общие файлы из neutrinohit-map

`ru|en/book/assets/styles/neutrinohit-book.css`, `ru|en/book/assets/filters/neutrinohit-book.lua`,
`shared/latex/neutrinohit-book.tex`, `shared/reveal/*`, `shared/styles/neutrinohit-reveal.scss`
и `shared/html/cloudflare-web-analytics.html` — копии канонических файлов из
`neutrinohit-map`. Правятся там, затем обновляются командой `make sync-shared`.

Слайды используют тему `black` с общим `neutrinohit-reveal.scss` и общий footer;
кнопка footer ведёт на страницу курса `https://neutrinohit.github.io/numerical_methods/`.

## Что нужно сделать для включения в NeutrinoHit

Эти шаги затрагивают другие репозитории и пока не выполнены:

- добавить проект в `scripts/sync_book_assets.py` и `scripts/sync_reveal_assets.py`
  репозитория neutrinohit-map;
- зарегистрировать адрес страницы курса `https://neutrinohit.github.io/numerical_methods/`
  в `scripts/reveal_context_targets.json` (footer слайдов уже подключён);
- добавить карточку курса с якорем `#numerical-methods` в `ru/education.qmd`
  и `en/education.qmd` и проект в `make local-aggregate`;
- завести GitHub-репозиторий и workflow публикации
  (`.github/workflows/publish-site.yml`, вызывающий общий reusable workflow);
- добавить обложку книги.
