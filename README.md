# 🎵 MuzzLow

[Русский](#русский) | [English](#english)

---

# Русский

## О проекте

**MuzzLow** — это веб-приложение для прослушивания музыки с умной системой рекомендаций на основе приоритетов. В отличие от обычных плееров, треки здесь играют не случайно, а с учётом их приоритета (1–5), текущего "шанса" выпадения и времени отдыха после проигрыша.

Проект состоит из двух частей:
- **Бэкенд** на FastAPI, который работает с Genius API для поиска песен и управляет логикой плейлиста
- **Фронтенд** на чистом HTML/CSS/JS с минималистичным дизайном, адаптированным для мобильных устройств

### Основные возможности

- 🔍 **Поиск музыки** через Genius API (песни и исполнители)
- 📋 **Умный плейлист** с приоритетами — песни с высоким приоритетом играют чаще
- 🎲 **Вероятностный алгоритм** — шанс выпадения трека динамически меняется в зависимости от того, как давно он играл
- 📥 **Импорт плейлистов** из Яндекс Музыки и ВК (в разработке)
- 🎨 **Минималистичный интерфейс** с тёмной темой
- 📱 **Адаптивный дизайн** — удобно пользоваться с телефона

### Как работает алгоритм плейлиста?

Каждый трек имеет следующие параметры:

| Параметр | Описание |
|----------|----------|
| `priority` | Базовый приоритет (1 — самый высокий, 5 — самый низкий) |
| `chance` | Текущий шанс выпадения (растёт со временем) |
| `cooldown` | Количество треков, которое должно сыграть после последнего проигрыша, прежде чем шанс начнёт расти |
| `up` | На сколько увеличивается `chance` после каждого пропуска (если `idle > cooldown`) |
| `idle` | Счётчик пропусков (сколько треков сыграло после последнего проигрыша) |

Приоритеты настраиваются в `backend/config/settings.json`:

```json
{
    "1": { "chance": 20, "up": 6, "cooldown": 0.4 },
    "2": { "chance": 16, "up": 4, "cooldown": 0.55 },
    "3": { "chance": 13, "up": 3, "cooldown": 0.6 },
    "4": { "chance": 10, "up": 2, "cooldown": 0.7 },
    "5": { "chance": 7,  "up": 1, "cooldown": 0.9 }
}
```

# English

## About

**MuzzLow** is a web-based music player with a smart, priority-based recommendation system. Unlike traditional random play, tracks are selected using a weighted algorithm that takes into account their priority level, current chance of playing, and a cooldown period after being played.

The project consists of two parts:
- **FastAPI backend** that communicates with the Genius API for music search and manages playlist logic
- **Pure HTML/CSS/JS frontend** with a clean, minimalist design optimized for mobile devices

## Features

- 🔍 **Music search** via Genius API (songs and artists)
- 📋 **Weighted playlist system** — high-priority tracks play more often
- 🎲 **Dynamic probability algorithm** — play chance increases over time when tracks are not selected
- 📥 **Playlist import** from Yandex Music and VK (in development)
- 🎨 **Minimalist dark-themed interface**
- 📱 **Fully responsive** — works great on phones and tablets

## How the Playlist Algorithm Works

Each track has the following parameters:

| Parameter | Description |
|-----------|-------------|
| `priority` | Base priority level (1 = highest, 5 = lowest) |
| `chance` | Current probability of being selected (increases when idle) |
| `cooldown` | Number of tracks that must play after last playback before chance starts increasing |
| `up` | Amount by which `chance` increases after each skip (when `idle > cooldown`) |
| `idle` | Counter of how many tracks have played since the last playback |

Priority settings are configured in `backend/config/settings.json`:

```json
{
    "1": { "chance": 20, "up": 6, "cooldown": 0.4 },
    "2": { "chance": 16, "up": 4, "cooldown": 0.55 },
    "3": { "chance": 13, "up": 3, "cooldown": 0.6 },
    "4": { "chance": 10, "up": 2, "cooldown": 0.7 },
    "5": { "chance": 7,  "up": 1, "cooldown": 0.9 }
}