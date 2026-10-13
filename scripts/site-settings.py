#!/usr/bin/env python3
"""
Настройки сайта и заявки на план питания в Directus:

1. site_settings — синглтон (одна запись) с полем title_color:
   цвет больших заголовков сайта, выбирается пипеткой в Directus.
   Публичный доступ: только чтение.
2. meal_plan_requests — заявки из футера «заказать план питания»:
   name, contact, wishes, status (новая / в работе / готово), date_created.
   Публичный доступ: только создание (читать заявки может только админ).

По умолчанию ничего не меняет, только печатает план (dry run).
Чтобы применить:  python3 scripts/site-settings.py --apply
Скрипт повторно запускать безопасно: уже созданное пропускается.

Доступ берётся из переменных окружения, в коде пароля нет:
  DIRECTUS_URL   (по умолчанию https://157-180-79-150.sslip.io)
  DIRECTUS_TOKEN  или  DIRECTUS_EMAIL + DIRECTUS_PASSWORD
"""
import os
import sys

import requests

APPLY = "--apply" in sys.argv
BASE_URL = os.environ.get("DIRECTUS_URL", "https://157-180-79-150.sslip.io").rstrip("/")
DEFAULT_TITLE_COLOR = "#1a1a1a"  # = --color-ink, как сейчас на сайте


# ── доступ ───────────────────────────────────────────────────────────────────
def session() -> requests.Session:
    s = requests.Session()
    token = os.environ.get("DIRECTUS_TOKEN")
    if not token:
        email, pwd = os.environ.get("DIRECTUS_EMAIL"), os.environ.get("DIRECTUS_PASSWORD")
        if not (email and pwd):
            sys.exit("Нужен DIRECTUS_TOKEN или DIRECTUS_EMAIL + DIRECTUS_PASSWORD")
        r = s.post(f"{BASE_URL}/auth/login", json={"email": email, "password": pwd})
        r.raise_for_status()
        token = r.json()["data"]["access_token"]
    s.headers["Authorization"] = f"Bearer {token}"
    return s


S = session()


def call(method, path, ok404=False, **kw):
    if method != "GET" and not APPLY:
        return None
    r = S.request(method, f"{BASE_URL}{path}", **kw)
    if ok404 and r.status_code in (403, 404):
        return None
    if r.status_code >= 400:
        sys.exit(f"{method} {path} → {r.status_code}: {r.text[:300]}")
    return r.json().get("data") if r.content else None


def log(msg):
    print(("" if APPLY else "[план] ") + msg)


def collection_exists(name):
    return call("GET", f"/collections/{name}", ok404=True) is not None


def public_policy_id():
    found = call("GET", "/policies", params={"filter[name][_eq]": "$t:public_label", "fields": "id"})
    if not found:
        sys.exit("Не нашёл публичную политику ($t:public_label) в Directus")
    return found[0]["id"]


def ensure_permission(policy, collection, action, fields):
    existing = call("GET", "/permissions", params={
        "filter[policy][_eq]": policy,
        "filter[collection][_eq]": collection,
        "filter[action][_eq]": action,
    }) or []
    if existing:
        print(f"  публичное право {action} на {collection} уже есть")
        return
    log(f"публичное право {action} на {collection}")
    call("POST", "/permissions", json={
        "policy": policy, "collection": collection, "action": action, "fields": fields,
    })


print(f"Directus: {BASE_URL}   режим: {'ПРИМЕНЕНИЕ' if APPLY else 'dry run (без изменений)'}\n")
policy = public_policy_id()

# ── 1. site_settings ─────────────────────────────────────────────────────────
print("── Настройки сайта (site_settings)")
if collection_exists("site_settings"):
    print("  коллекция уже есть")
else:
    log("создать синглтон site_settings с полем title_color (цвет заголовков)")
    call("POST", "/collections", json={
        "collection": "site_settings",
        "meta": {"singleton": True, "icon": "palette", "note": "Настройки сайта", "translations": [
            {"language": "ru-RU", "translation": "Настройки сайта"}]},
        "schema": {},
        "fields": [
            {"field": "id", "type": "integer", "meta": {"hidden": True},
             "schema": {"is_primary_key": True, "has_auto_increment": True}},
            {"field": "title_color", "type": "string",
             "meta": {"interface": "select-color", "display": "color", "width": "half",
                      "note": "Цвет больших заголовков сайта"},
             "schema": {"default_value": DEFAULT_TITLE_COLOR}},
        ],
    })
    log(f"записать цвет по умолчанию {DEFAULT_TITLE_COLOR}")
    call("PATCH", "/items/site_settings", json={"title_color": DEFAULT_TITLE_COLOR})
ensure_permission(policy, "site_settings", "read", ["*"])

# ── 2. meal_plan_requests ────────────────────────────────────────────────────
print("\n── Заявки на план питания (meal_plan_requests)")
if collection_exists("meal_plan_requests"):
    print("  коллекция уже есть")
else:
    log("создать коллекцию meal_plan_requests")
    call("POST", "/collections", json={
        "collection": "meal_plan_requests",
        "meta": {"icon": "restaurant_menu", "note": "Заявки с сайта: заказать план питания",
                 "sort_field": None, "archive_field": None, "translations": [
                     {"language": "ru-RU", "translation": "Заявки на план питания"}]},
        "schema": {},
        "fields": [
            {"field": "id", "type": "integer", "meta": {"hidden": True},
             "schema": {"is_primary_key": True, "has_auto_increment": True}},
            {"field": "date_created", "type": "timestamp",
             "meta": {"special": ["date-created"], "interface": "datetime", "readonly": True,
                      "display": "datetime", "width": "half", "note": "Когда пришла заявка"}},
            {"field": "status", "type": "string",
             "meta": {"interface": "select-dropdown", "display": "labels", "width": "half",
                      "options": {"choices": [
                          {"text": "новая", "value": "new"},
                          {"text": "в работе", "value": "in_progress"},
                          {"text": "готово", "value": "done"}]}},
             "schema": {"default_value": "new"}},
            {"field": "name", "type": "string",
             "meta": {"interface": "input", "width": "half", "required": True, "note": "Имя"}},
            {"field": "contact", "type": "string",
             "meta": {"interface": "input", "width": "half", "required": True,
                      "note": "Телефон, Telegram или email"}},
            {"field": "wishes", "type": "text",
             "meta": {"interface": "input-multiline", "note": "Пожелания"}},
        ],
    })
# сайт может только создавать заявки и только с этими полями; читать их публично нельзя
ensure_permission(policy, "meal_plan_requests", "create", ["name", "contact", "wishes"])

print("\nГотово." if APPLY else "\nЭто был план. Запустите с --apply, чтобы применить.")
