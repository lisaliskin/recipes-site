#!/usr/bin/env python3
"""
Migrates Directus to new structure:
- products: unique catalog (name, kcal/100g, proteins, fats, carbs)
- recipe_ingredients: recipe_id, product_id, amount, base_unit, sort
- recipes: remove total_kcal_per_serving
- steps: keep O2M but make visible in recipe form
"""
import requests
import json

BASE_URL = "https://157-180-79-150.sslip.io"
EMAIL = "lisaliskin@gmail.com"
PASSWORD = "recipes2024!"

r = requests.post(f"{BASE_URL}/auth/login", json={"email": EMAIL, "password": PASSWORD})
token = r.json()["data"]["access_token"]
H = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# ── 1. Получаем все текущие ингредиенты ──────────────────────────────────────
print("Загружаем ингредиенты...")
ings = requests.get(f"{BASE_URL}/items/ingredients?limit=1000&sort=sort", headers=H).json()["data"]
print(f"  {len(ings)} записей")

# ── 2. Создаём каталог продуктов (дедупликация по имени) ─────────────────────
print("\nСоздаём коллекцию products...")
resp = requests.post(f"{BASE_URL}/collections", headers=H, json={
    "collection": "products",
    "meta": {"icon": "local_grocery_store", "translations": [{"language": "ru-RU", "translation": "Продукты"}]},
    "schema": {},
    "fields": [
        {"field": "id", "type": "integer", "meta": {"hidden": True, "readonly": True}, "schema": {"is_primary_key": True, "has_auto_increment": True}},
        {"field": "name", "type": "string", "meta": {"required": True, "translations": [{"language": "ru-RU", "translation": "Название"}]}, "schema": {"is_nullable": False, "is_unique": True}},
        {"field": "kcal_per_100g", "type": "float", "meta": {"translations": [{"language": "ru-RU", "translation": "Ккал / 100г"}]}, "schema": {"default_value": 0}},
        {"field": "proteins", "type": "float", "meta": {"translations": [{"language": "ru-RU", "translation": "Белки / 100г"}]}, "schema": {"default_value": 0}},
        {"field": "fats", "type": "float", "meta": {"translations": [{"language": "ru-RU", "translation": "Жиры / 100г"}]}, "schema": {"default_value": 0}},
        {"field": "carbs", "type": "float", "meta": {"translations": [{"language": "ru-RU", "translation": "Углеводы / 100г"}]}, "schema": {"default_value": 0}},
    ]
})
if resp.json().get("data"):
    print("  OK: products создана")
else:
    print("  Уже существует или ошибка:", resp.json().get("errors", ""))

# ── 3. Заполняем products уникальными продуктами ──────────────────────────────
print("\nЗаполняем каталог продуктов...")
seen = {}
for ing in ings:
    name = ing["name"]
    if name not in seen:
        seen[name] = ing
    # если дубль — берём запись с большей граммовкой (более точные данные)
    elif ing["amount"] > seen[name]["amount"]:
        seen[name] = ing

products_map = {}  # name → product_id
for name, ing in seen.items():
    r = requests.post(f"{BASE_URL}/items/products", headers=H, json={
        "name": name,
        "kcal_per_100g": ing["kcal_per_100g"],
        "proteins": ing["proteins"],
        "fats": ing["fats"],
        "carbs": ing["carbs"],
    })
    if r.status_code in (200, 201):
        pid = r.json()["data"]["id"]
        products_map[name] = pid
    else:
        print(f"  ОШИБКА {name}: {r.text[:100]}")

print(f"  Создано {len(products_map)} уникальных продуктов")

# ── 4. Создаём recipe_ingredients ────────────────────────────────────────────
print("\nСоздаём коллекцию recipe_ingredients...")
resp = requests.post(f"{BASE_URL}/collections", headers=H, json={
    "collection": "recipe_ingredients",
    "meta": {"icon": "grocery", "hidden": True, "translations": [{"language": "ru-RU", "translation": "Ингредиенты рецепта"}]},
    "schema": {},
    "fields": [
        {"field": "id", "type": "integer", "meta": {"hidden": True, "readonly": True}, "schema": {"is_primary_key": True, "has_auto_increment": True}},
        {"field": "recipe_id", "type": "integer", "meta": {"hidden": True}, "schema": {}},
        {"field": "product_id", "type": "integer", "meta": {"hidden": True}, "schema": {}},
        {"field": "amount", "type": "float", "meta": {"required": True, "translations": [{"language": "ru-RU", "translation": "Количество"}]}, "schema": {}},
        {"field": "base_unit", "type": "string", "meta": {"translations": [{"language": "ru-RU", "translation": "Единица"}]}, "schema": {"default_value": "г"}},
        {"field": "sort", "type": "integer", "meta": {"hidden": True}, "schema": {}},
    ]
})
if resp.json().get("data"):
    print("  OK: recipe_ingredients создана")
else:
    print("  Уже существует или ошибка:", resp.json().get("errors", ""))

# Связь recipe_ingredients.recipe_id → recipes
requests.post(f"{BASE_URL}/relations", headers=H, json={
    "collection": "recipe_ingredients",
    "field": "recipe_id",
    "related_collection": "recipes",
    "meta": {"one_field": "recipe_ingredients", "sort_field": "sort", "one_deselect_action": "delete"}
})

# Связь recipe_ingredients.product_id → products
requests.post(f"{BASE_URL}/relations", headers=H, json={
    "collection": "recipe_ingredients",
    "field": "product_id",
    "related_collection": "products",
    "meta": {"one_field": None}
})

print("  Связи созданы")

# ── 5. Заполняем recipe_ingredients ──────────────────────────────────────────
print("\nМигрируем данные в recipe_ingredients...")
migrated = 0
for ing in ings:
    pid = products_map.get(ing["name"])
    if not pid:
        print(f"  НЕ НАЙДЕН продукт: {ing['name']}")
        continue
    r = requests.post(f"{BASE_URL}/items/recipe_ingredients", headers=H, json={
        "recipe_id": ing["recipe_id"],
        "product_id": pid,
        "amount": ing["amount"],
        "base_unit": ing["base_unit"],
        "sort": ing["sort"],
    })
    if r.status_code in (200, 201):
        migrated += 1
    else:
        print(f"  ОШИБКА: {r.text[:100]}")

print(f"  Перенесено {migrated} записей")

# ── 6. Убираем total_kcal_per_serving из recipes ─────────────────────────────
print("\nУдаляем поле total_kcal_per_serving из recipes...")
resp = requests.delete(f"{BASE_URL}/fields/recipes/total_kcal_per_serving", headers=H)
print(f"  {'OK' if resp.status_code in (200, 204) else resp.text[:100]}")

# ── 7. Делаем steps видимыми в форме рецепта ──────────────────────────────────
print("\nНастраиваем отображение шагов в форме рецепта...")
# Проверяем есть ли виртуальное поле steps в recipes
resp = requests.get(f"{BASE_URL}/fields/recipes", headers=H)
fields = [f["field"] for f in resp.json().get("data", [])]
print(f"  Поля recipes: {fields}")

if "steps" not in fields:
    # Создаём alias-поле для O2M steps
    resp = requests.post(f"{BASE_URL}/fields/recipes", headers=H, json={
        "field": "steps",
        "type": "alias",
        "meta": {
            "interface": "list-o2m",
            "special": ["o2m"],
            "hidden": False,
            "options": {
                "template": "{{text}}",
                "fields": ["text"],
                "enableCreate": True,
                "enableSelect": False,
            },
            "translations": [{"language": "ru-RU", "translation": "Шаги приготовления"}]
        }
    })
    print(f"  {'OK: поле steps добавлено' if resp.status_code in (200, 201) else resp.text[:200]}")
else:
    # Обновляем meta чтобы сделать видимым
    resp = requests.patch(f"{BASE_URL}/fields/recipes/steps", headers=H, json={
        "meta": {
            "interface": "list-o2m",
            "special": ["o2m"],
            "hidden": False,
            "options": {
                "template": "{{text}}",
                "fields": ["text"],
                "enableCreate": True,
                "enableSelect": False,
            },
            "translations": [{"language": "ru-RU", "translation": "Шаги приготовления"}]
        }
    })
    print(f"  {'OK: поле steps обновлено' if resp.status_code in (200, 201) else resp.text[:200]}")

# ── 8. Добавляем recipe_ingredients в форму рецепта ──────────────────────────
print("\nНастраиваем отображение ингредиентов в форме рецепта...")
if "recipe_ingredients" not in fields:
    resp = requests.post(f"{BASE_URL}/fields/recipes", headers=H, json={
        "field": "recipe_ingredients",
        "type": "alias",
        "meta": {
            "interface": "list-o2m",
            "special": ["o2m"],
            "hidden": False,
            "options": {
                "template": "{{product_id.name}} — {{amount}} {{base_unit}}",
                "enableCreate": True,
                "enableSelect": False,
            },
            "translations": [{"language": "ru-RU", "translation": "Ингредиенты"}]
        }
    })
    print(f"  {'OK' if resp.status_code in (200, 201) else resp.text[:200]}")

# ── 9. Публичные права на products и recipe_ingredients ──────────────────────
print("\nНастраиваем публичные права...")
PUBLIC_POLICY = "abf8a154-5b1c-4a46-ac9c-7300570f4f17"
for col in ["products", "recipe_ingredients"]:
    r = requests.post(f"{BASE_URL}/permissions", headers=H, json={
        "policy": PUBLIC_POLICY, "collection": col, "action": "read", "fields": ["*"]
    })
    print(f"  {col}: {'OK' if r.status_code in (200, 201) else r.json().get('errors','')}")

print("\n✓ Миграция завершена!")
print("\nСтарая коллекция 'ingredients' оставлена — удали вручную после проверки")
