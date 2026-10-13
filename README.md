# рецепты

Домашний сайт с рецептами: https://recipes-site-ashen.vercel.app

Разделы, поиск, перерасчёт ингредиентов и КБЖУ по числу порций, избранное, список продуктов с экспортом, «что приготовить на ужин?» и заявка на план питания. Сайт ставится на телефон как приложение и открывает уже просмотренные рецепты без интернета.

## Как устроено

- Vue 3 + TypeScript + Vite, Pinia, vue-router, PWA (`vite-plugin-pwa`).
- Рецепты, продукты, шаги и настройки сайта (цвета) хранятся в Directus CMS; адрес задан в `src/api/directus.ts`.
- Деплой — Vercel из ветки `main`, Node 22 (`.nvmrc`).

## Запуск

```sh
npm install
npm run dev      # локальный сервер
npm run build    # проверка типов и сборка в dist/
```

## Скрипты для Directus

Скрипты в `scripts/` меняют данные в Directus. Логин и пароль в коде не хранятся — их берут из окружения:

```sh
export DIRECTUS_TOKEN=...            # или DIRECTUS_EMAIL + DIRECTUS_PASSWORD
python3 scripts/site-settings.py     # пример
```

`DIRECTUS_URL` можно задать, если адрес CMS изменится.
