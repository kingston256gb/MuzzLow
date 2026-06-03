# Audio Streaming Experiment

[[Русский](#русский) | [English](#english)]

---

# Русский

## Цель

Исследовать возможность бесплатного получения аудиопотока для MuzzLow без использования платных музыкальных API.

---

## Попытка 1 — YouTube Music API | ❌ Провал

### Идея

Использовать официальный API YouTube Music для получения прямой ссылки на аудиопоток и передачи её во frontend.

### Результат

Официального бесплатного API для получения аудиопотоков не существует.

### Проблемы

* Нет доступа к аудиофайлам через API.
* Требуется использование официального клиента YouTube Music.
* Решение не подходит для бесплатного пет-проекта.

### Вывод

Подход признан непригодным.

---

## Попытка 2 — Invidious API | ⚠️ Частичный успех

### Идея

Использовать Invidious как прокси-слой над YouTube:

1. Выполнить поиск трека.
2. Получить информацию о видео.
3. Извлечь ссылку на аудиопоток.
4. Передать ссылку во frontend.

### Что удалось

* Поиск треков работает.
* Получение metadata работает.
* Получение audio URL работает.
* Воспроизведение возможно.

### Обнаруженные проблемы

* Некоторые Invidious-инстансы блокируют автоматические запросы.
* Аудиопоток выдаётся через googlevideo.com.
* Без VPN соединение может зависать или завершаться по таймауту.

### Вывод

Технически решение работает, однако требует дополнительного исследования вариантов проксирования аудиопотока.

---

## Следующие шаги

* Исследовать Cloudflare Workers.
* Исследовать проксирование потока через backend.
* Проверить другие Invidious-инстансы.
* Найти способ обхода зависимости от прямых запросов к googlevideo.com.

---

# English

## Goal


Explore the possibility of getting audio stream URLs for free and using them in MuzzLow without commercial APIs.

---

## Try #1 — YouTube Music API | ❌ Fail

### Idea

Use the official YouTube Music API to fetch audio stream URL and send it to the frontend.

### Result

There is no free official API to get audio stream URLs.

### Issues


* There is no access to audio files via API.
* The use of the official YouTube Music client is required.
* This method is not suitable for a free project.


### Output

This method is not a viable option

---

## Try #2 — Invidious API | ⚠️ Partial success

### Idea

Use Invidious as a proxy layer over YouTube:

1. Search the track.
2. Get video info.
3. Get audio stream URL.
4. Send this URL to the frontend.

### What worked

* Track search works.
* Metadata retrieval works.
* Audio stream URLs can be obtained.
* Playback is possible

### Detected problems

* Some of Invidious instances are blocking automatic requests
* Audio stream URLs contain "googlevideo.com" `[countries where YouTube is blocked]`
* Connection without VPN can freeze or time out `[countries where YouTube is blocked]`

### Output

Technically, this method works, but requires additional research into audio proxying.

---

## Next steps

* Look into Cloudflare Workers.
* Explore backend-based audio stream proxying.
* Try other Invidious instances.
* Find a way to avoid direct requests to googlevideo.com.