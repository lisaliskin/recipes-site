#!/usr/bin/env python3
"""
Доработки ингредиентов в Directus:

1. Каталог products: все названия с маленькой буквы, без дублей
   (дубли сливаются, ссылки из рецептов переносятся на оставшийся продукт),
   недостающие продукты и пустые КБЖУ дополняются из scripts/data/products.json.
   Новые поля: grams_per_piece (вес 1 шт, г) и density (г в 1 мл) —
   по ним сайт пересчитывает шт / ложки / мл в граммы для КБЖУ.
2. recipe_ingredients.group_name — подзаголовок группы («для бисквита», «для сиропа»).
3. recipe_ingredients.base_unit — выпадающий список единиц, старые варианты
   написания приводятся к списку (гр → г, ч.л. → ч. л. и т.д.).

По умолчанию ничего не меняет, только печатает план (dry run).
Чтобы применить:  python3 scripts/ingredients-v2.py --apply
Перед применением сохраняет резервную копию products и recipe_ingredients в JSON.

Доступ берётся из переменных окружения, в коде пароля нет:
  DIRECTUS_URL   (по умолчанию https://157-180-79-150.sslip.io)
  DIRECTUS_TOKEN  или  DIRECTUS_EMAIL + DIRECTUS_PASSWORD
"""
import json
import os
import sys
import time
from pathlib import Path

import requests

APPLY = "--apply" in sys.argv
BASE_URL = os.environ.get("DIRECTUS_URL", "https://157-180-79-150.sslip.io").rstrip("/")
SEED = json.loads((Path(__file__).parent / "data" / "products.json").read_text("utf-8"))

# Синонимы → каноническое название (+ группа, если часть названия на самом деле группа)
ALIASES = {
    "мёд цветочный": ("мёд", None),
    "оливковое масло extra virgin": ("оливковое масло", None),
    "тимьян свежий": ("тимьян", None),
    "филе лосося (свежий)": ("филе лосося", None),
    "яйцо": ("яйца", None),
    "бурратa": ("буррата", None),  # в старом названии латинская «a»
    "варенье для подачи": ("варенье", "для подачи"),
}

# Должно совпадать с UNITS в src/utils/units.ts
UNITS = ["г", "кг", "мл", "л", "шт", "ст. л.", "ч. л.", "стакан", "щепотка", "по вкусу"]
UNIT_ALIASES = {
    "гр": "г", "гр.": "г", "г.": "г", "грамм": "г",
    "кг.": "кг",
    "мл.": "мл",
    "л.": "л",
    "шт.": "шт", "штука": "шт", "штуки": "шт",
    "ст.л.": "ст. л.", "ст.л": "ст. л.", "ст л": "ст. л.", "стл": "ст. л.", "ст. л": "ст. л.",
    "ч.л.": "ч. л.", "ч.л": "ч. л.", "ч л": "ч. л.", "чл": "ч. л.", "ч. л": "ч. л.",
    "стак.": "стакан", "ст.": "стакан",
    "щеп.": "щепотка",
}

LATIN_LOOKALIKES = str.maketrans("aceopxyAEKMHOPCTXB", "асеорхуаекмнорстхв")


def norm_name(name: str) -> str:
    n = " ".join((name or "").split()).lower()
    # латиница внутри кириллического слова — почти всегда опечатка раскладки
    words = []
    for w in n.split(" "):
        if any("а" <= ch <= "я" or ch == "ё" for ch in w):
            w = w.translate(LATIN_LOOKALIKES)
        words.append(w)
    return " ".join(words)


def canonical(name: str):
    n = norm_name(name)
    return ALIASES.get(n, (n, None))


def norm_unit(u: str):
    u0 = " ".join((u or "").split()).lower()
    if u0 in UNITS:
        return u0
    return UNIT_ALIASES.get(u0)


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


def call(method, path, **kw):
    if method != "GET" and not APPLY:
        return None
    r = S.request(method, f"{BASE_URL}{path}", **kw)
    if r.status_code >= 400:
        sys.exit(f"{method} {path} → {r.status_code}: {r.text[:300]}")
    return r.json().get("data") if r.content else None


def fields_of(collection):
    return {f["field"]: f for f in call("GET", f"/fields/{collection}")}


def log(msg):
    print(("" if APPLY else "[план] ") + msg)


# ── 1. схема ─────────────────────────────────────────────────────────────────
print(f"Directus: {BASE_URL}   режим: {'ПРИМЕНЕНИЕ' if APPLY else 'dry run (без изменений)'}\n")
print("── Схема")

pf = fields_of("products")
if "grams_per_piece" not in pf:
    log("products: добавить поле grams_per_piece (вес 1 шт, г)")
    call("POST", "/fields/products", json={
        "field": "grams_per_piece", "type": "float",
        "schema": {"is_nullable": True},
        "meta": {"interface": "input", "width": "half",
                 "note": "сколько граммов весит 1 шт — нужно для КБЖУ, если в рецепте указаны штуки",
                 "translations": [{"language": "ru-RU", "translation": "Вес 1 шт, г"}]},
    })
if "density" not in pf:
    log("products: добавить поле density (г в 1 мл)")
    call("POST", "/fields/products", json={
        "field": "density", "type": "float",
        "schema": {"is_nullable": True},
        "meta": {"interface": "input", "width": "half",
                 "note": "сколько граммов в 1 мл (вода = 1, мёд ≈ 1.4, мука ≈ 0.55); пусто = 1. "
                         "Нужно для мл, ложек и стаканов",
                 "translations": [{"language": "ru-RU", "translation": "Плотность, г/мл"}]},
    })
log("products.name: проверка «только строчные буквы»")
call("PATCH", "/fields/products/name", json={"meta": {
    "validation": {"_and": [{"name": {"_regex": "^[^A-ZА-ЯЁ]+$"}}]},
    "validation_message": "название с маленькой буквы",
}})

rf = fields_of("recipe_ingredients")
if "group_name" not in rf:
    log("recipe_ingredients: добавить поле group_name (группа)")
    call("POST", "/fields/recipe_ingredients", json={
        "field": "group_name", "type": "string",
        "schema": {"is_nullable": True},
        "meta": {"interface": "input", "width": "full",
                 "options": {"placeholder": "например: для бисквита"},
                 "note": "у ингредиентов одной группы пишите одинаковый текст; пусто — без группы",
                 "translations": [{"language": "ru-RU", "translation": "Группа"}]},
    })
log("recipe_ingredients.base_unit: выпадающий список " + ", ".join(UNITS))
call("PATCH", "/fields/recipe_ingredients/base_unit", json={"meta": {
    "interface": "select-dropdown",
    "options": {"choices": [{"text": u, "value": u} for u in UNITS], "allowOther": False},
    "display": "raw",
}, "schema": {"default_value": "г"}})

if "recipe_ingredients" in fields_of("recipes"):
    log("recipes.recipe_ingredients: показывать группу в списке")
    opts = (fields_of("recipes")["recipe_ingredients"]["meta"] or {}).get("options") or {}
    opts["template"] = "{{group_name}} {{product_id.name}} — {{amount}} {{base_unit}}"
    call("PATCH", "/fields/recipes/recipe_ingredients", json={"meta": {"options": opts}})

# ── 2. данные ────────────────────────────────────────────────────────────────
products = call("GET", "/items/products", params={"limit": -1, "sort": "id"})
ris = call("GET", "/items/recipe_ingredients", params={"limit": -1, "sort": "id"})

if APPLY:
    backup = Path(f"directus-backup-{time.strftime('%Y%m%d-%H%M%S')}.json")
    backup.write_text(json.dumps({"products": products, "recipe_ingredients": ris},
                                 ensure_ascii=False, indent=1), "utf-8")
    print(f"\nРезервная копия: {backup.resolve()}")

print(f"\n── Каталог продуктов ({len(products)} шт.)")
seed_by_name = {p["name"]: p for p in SEED}

groups = {}       # каноническое название → [products]
group_hint = {}   # product_id → группа из названия (варенье для подачи)
for p in products:
    name, grp = canonical(p["name"])
    groups.setdefault(name, []).append(p)
    if grp:
        group_hint[p["id"]] = grp

redirect = {}  # id удаляемого дубля → id оставшегося
for name, items in sorted(groups.items()):
    keep = next((p for p in items if p["name"] == name), items[0])
    patch = {}
    if keep["name"] != name:
        patch["name"] = name
    seed = seed_by_name.get(name, {})
    for f in ("kcal_per_100g", "proteins", "fats", "carbs"):
        # дополняем только пустое; берём значение у дубля или из справочника
        if not keep.get(f):
            val = next((p[f] for p in items if p.get(f)), None) or seed.get(f)
            if val:
                patch[f] = val
    for f in ("grams_per_piece", "density"):
        if keep.get(f) is None:
            val = next((p.get(f) for p in items if p.get(f) is not None), None) or seed.get(f)
            if val:
                patch[f] = val
    dups = [p for p in items if p["id"] != keep["id"]]
    if dups:
        log(f"слить: {', '.join(repr(p['name']) for p in dups)} → {name!r}")
        for d in dups:
            redirect[d["id"]] = keep["id"]
    if patch:
        log(f"обновить #{keep['id']} {keep['name']!r}: {patch}")
        if not dups:  # при дублях — после их удаления, чтобы не упереться в уникальность имени
            call("PATCH", f"/items/products/{keep['id']}", json=patch)
    keep["_patch"] = patch

missing = [s for s in SEED if s["name"] not in groups]
for s in missing:
    log(f"добавить продукт {s['name']!r}")
    call("POST", "/items/products", json=s)

print(f"\n── Ингредиенты рецептов ({len(ris)} шт.)")
bad_units = []
for ri in ris:
    patch = {}
    pid = ri.get("product_id")
    if pid in redirect:
        patch["product_id"] = redirect[pid]
    if pid in group_hint and group_hint[pid] and not ri.get("group_name"):
        patch["group_name"] = group_hint[pid]
    u = norm_unit(ri.get("base_unit"))
    if u is None:
        bad_units.append(ri)
    elif u != ri.get("base_unit"):
        patch["base_unit"] = u
    if patch:
        log(f"#{ri['id']} (рецепт {ri.get('recipe_id')}): {patch}")
        call("PATCH", f"/items/recipe_ingredients/{ri['id']}", json=patch)

# дубли удаляем после переноса ссылок, затем применяем отложенные правки
for name, items in groups.items():
    keep = next((p for p in items if p["name"] == name), items[0])
    dups = [p for p in items if p["id"] != keep["id"]]
    for d in dups:
        log(f"удалить дубль #{d['id']} {d['name']!r}")
        call("DELETE", f"/items/products/{d['id']}")
    if dups and keep["_patch"]:
        call("PATCH", f"/items/products/{keep['id']}", json=keep["_patch"])

# ── 3. что осталось сделать руками ───────────────────────────────────────────
print("\n── Проверить вручную")
final = {}
for name, items in groups.items():
    keep = next((p for p in items if p["name"] == name), items[0])
    final[keep["id"]] = {**keep, **keep["_patch"]}
for p in final.values():
    if not any(p.get(f) for f in ("kcal_per_100g", "proteins", "fats", "carbs")) \
            and p["name"] not in ("вода", "морская соль", "флёр де сель"):
        print(f"  нет КБЖУ: {p['name']}")
for ri in ris:
    pid = redirect.get(ri.get("product_id"), ri.get("product_id"))
    p = final.get(pid)
    if p and norm_unit(ri.get("base_unit")) == "шт" and not p.get("grams_per_piece"):
        print(f"  нет веса 1 шт: {p['name']} (рецепт {ri.get('recipe_id')})")
for ri in bad_units:
    print(f"  неизвестная единица {ri.get('base_unit')!r} у ингредиента #{ri['id']} — "
          f"выберите из списка в Directus")

print("\nГотово." if APPLY else "\nЭто был план. Запустите с --apply, чтобы применить.")
