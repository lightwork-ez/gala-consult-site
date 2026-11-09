# GalA-Consult - сайт galaconsult.com

Статический сайт ТОО «ГалА-Консалт» (Алматы). Сделан студией WEBCRAFT.

## Как устроено
- Домен galaconsult.com: A @ → 75.2.60.5, CNAME www → gala-consult.netlify.app (проект Netlify gala-consult). Почта компании остаётся на galaconsult.kz.
- `site/` - готовый сайт. Netlify публикует эту папку без сборки (`netlify.toml`), деплой - любой push в `main`.
- `build/build.py` - генератор всех страниц: тексты главной, список проектов `P` (тексты, даты, 2 документа), шапка, подвал, форма запроса, 404. После правок: `python3 build/build.py` - пересобирает `site/`.
- Три языка, одинаковые имена файлов: русский `site/`, казахский `site/kz/`, немецкий `site/de/`. Переключатель KZ | RU | DE в шапке ведёт на ту же страницу другой версии (на главной - к тому же разделу), в `<head>` - hreflang kk/ru/de, в sitemap - все версии. 404 только русская.
- Тексты интерфейса и главной в `build.py` стоят парами `t('по-русски', 'auf Deutsch')`. Казахские - в `build/texts_kk.py`: `KK` по русскому тексту (сборка останавливается с «no Kazakh text for: ...», если перевода нет) и `P_KK` для проектов. Немецкие тексты проектов - `P_DE` в `build.py`. Новый проект = запись в `P`, `P_DE` и `P_KK`.
- В Spectral нет казахских букв (Ә Ғ Қ Ң Ө Ү Һ), поэтому заголовки казахской версии набраны Literata (`site/assets/fonts`, лицензия OFL), уменьшенной до размера Spectral (`size-adjust` в `site.css`).
- Форма на казахской и немецкой версиях: подписи на языке страницы, но темы (`value`) и тема письма уходят по-русски с пометкой (KZ) или (DE), плюс скрытое поле `lang` (ru/kk/de). Тексты ошибок формы - в `site.js` (`TXS`).
- Превью для соцсетей: `assets/img/og.jpg` (RU), `og-kz.jpg` (KZ), `og-de.jpg` (DE).
- `build/logos.py` + `build/applemark.py` - логотип (глобус-яблоко) и все SVG-версии; `python3 build/logos.py` перегенерирует файлы логотипов.
- `site/assets/css/site.css`, `site/assets/js/site.js` - стили и скрипты, правятся напрямую.
- `site/_redirects` - старые ссылки (например `/july2024`) ведут на новые страницы; задаются в `OLD_SLUGS` в `build.py`.
- Форма «Написать нам» - Netlify Forms (`name="request"`). На galaconsult.com (и .kz) и *.netlify.app отправляет по-настоящему, в остальных местах (превью, localhost) - демо-режим.

## Правила
- На странице каждого проекта всегда 2 ссылки на анкеты и документы - не убирать.
- Тексты проектов - по письмам-приглашениям компании (блоки `p`, `h3`, `ul`, `ol`, `callout`). У каждого проекта поле `end` - последний день; после него документ без ссылки помечается «expired» вместо «скоро».
- На главной только последние проекты (3), полный список - `/projects/`.
- Только обычный дефис "-", без длинного тире. Нумерация 1, 2, 3 без нулей.
- Палитра 60-30-10: светло-серый фон, navy, оранжевый акцент (`--accent`). Без ИИ-картинок.
- В подвале по центру «Made by WEBCRAFT» со ссылкой на wwwebcraft.com.
- Немецкие названия - как у AHK Zentralasien: Repräsentanz der Deutschen Wirtschaft in Kasachstan (с 1994), Delegation der Deutschen Wirtschaft für Zentralasien, Deutscher Wirtschaftsklub, затем Verband der Deutschen Wirtschaft in der Republik Kasachstan. Основатель по-немецки - Dr. Galia Shunussalieva. Обращение на «Sie». В казахской версии имя основателя - как в русской, форма организации - «ЖШС».
