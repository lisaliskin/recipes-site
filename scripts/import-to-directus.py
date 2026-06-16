#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://157.180.79.150:8055"
EMAIL = "lisaliskin@gmail.com"
PASSWORD = "recipes2024!"

# Авторизация
r = requests.post(f"{BASE_URL}/auth/login", json={"email": EMAIL, "password": PASSWORD})
token = r.json()["data"]["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

recipes = [
  {
    "id": "ovsyanaya-kasha", "title": "овсяная каша с ягодами", "section": "завтраки",
    "servings": 2, "cooking_time_minutes": 15, "total_kcal_per_serving": 387, "favorite_seed": 34,
    "description": "сливочная каша с черникой и кленовым сиропом",
    "ingredients": [
      {"ingredient_key": "oat-flakes", "name": "овсяные хлопья", "amount": 160, "base_unit": "г", "kcal_per_100g": 389, "proteins": 17, "fats": 7, "carbs": 66},
      {"ingredient_key": "milk", "name": "молоко 3.2%", "amount": 400, "base_unit": "мл", "kcal_per_100g": 60, "proteins": 3.2, "fats": 3.2, "carbs": 4.7},
      {"ingredient_key": "blueberry", "name": "черника", "amount": 100, "base_unit": "г", "kcal_per_100g": 44, "proteins": 0.7, "fats": 0.4, "carbs": 10},
      {"ingredient_key": "maple-syrup", "name": "кленовый сироп", "amount": 30, "base_unit": "мл", "kcal_per_100g": 260, "proteins": 0, "fats": 0.1, "carbs": 67},
      {"ingredient_key": "butter", "name": "сливочное масло", "amount": 20, "base_unit": "г", "kcal_per_100g": 748, "proteins": 0.5, "fats": 82, "carbs": 0.5},
    ],
    "steps": ["довести молоко до кипения на среднем огне", "добавить овсяные хлопья, варить 5 минут, помешивая", "снять с огня, добавить сливочное масло, накрыть крышкой на 2 минуты", "разложить по тарелкам, сверху выложить чернику и полить кленовым сиропом"],
  },
  {
    "id": "yaichniza-s-avokado", "title": "яичница с авокадо и фетой", "section": "завтраки",
    "servings": 1, "cooking_time_minutes": 10, "total_kcal_per_serving": 512, "favorite_seed": 47,
    "description": "быстрый и сытный завтрак с кремовым авокадо",
    "ingredients": [
      {"ingredient_key": "eggs", "name": "яйца", "amount": 2, "base_unit": "шт", "kcal_per_100g": 157, "proteins": 13, "fats": 11, "carbs": 1.1},
      {"ingredient_key": "avocado", "name": "авокадо", "amount": 100, "base_unit": "г", "kcal_per_100g": 160, "proteins": 2, "fats": 15, "carbs": 9},
      {"ingredient_key": "feta", "name": "сыр фета", "amount": 40, "base_unit": "г", "kcal_per_100g": 264, "proteins": 14, "fats": 21, "carbs": 4},
      {"ingredient_key": "olive-oil", "name": "оливковое масло", "amount": 10, "base_unit": "мл", "kcal_per_100g": 899, "proteins": 0, "fats": 100, "carbs": 0},
      {"ingredient_key": "chili-flakes", "name": "хлопья чили", "amount": 1, "base_unit": "ч.л.", "kcal_per_100g": 314, "proteins": 12, "fats": 17, "carbs": 56},
    ],
    "steps": ["разрезать авокадо пополам, удалить косточку, нарезать ломтиками", "разогреть оливковое масло на сковороде на среднем огне", "разбить яйца и жарить до нужной степени готовности", "переложить на тарелку, добавить авокадо, раскрошить фету", "посыпать хлопьями чили и подавать сразу"],
  },
  {
    "id": "bliny-s-medom", "title": "блинчики с мёдом и сметаной", "section": "завтраки",
    "servings": 2, "cooking_time_minutes": 30, "total_kcal_per_serving": 498, "favorite_seed": 52,
    "description": "тонкие ажурные блинчики с цветочным мёдом",
    "ingredients": [
      {"ingredient_key": "flour", "name": "пшеничная мука", "amount": 150, "base_unit": "г", "kcal_per_100g": 364, "proteins": 10, "fats": 1, "carbs": 76},
      {"ingredient_key": "milk", "name": "молоко 3.2%", "amount": 400, "base_unit": "мл", "kcal_per_100g": 60, "proteins": 3.2, "fats": 3.2, "carbs": 4.7},
      {"ingredient_key": "eggs", "name": "яйца", "amount": 2, "base_unit": "шт", "kcal_per_100g": 157, "proteins": 13, "fats": 11, "carbs": 1.1},
      {"ingredient_key": "butter", "name": "сливочное масло", "amount": 40, "base_unit": "г", "kcal_per_100g": 748, "proteins": 0.5, "fats": 82, "carbs": 0.5},
      {"ingredient_key": "honey", "name": "мёд цветочный", "amount": 60, "base_unit": "г", "kcal_per_100g": 304, "proteins": 0.8, "fats": 0, "carbs": 82},
      {"ingredient_key": "sour-cream", "name": "сметана 20%", "amount": 80, "base_unit": "г", "kcal_per_100g": 204, "proteins": 2.8, "fats": 20, "carbs": 3.7},
    ],
    "steps": ["взбить яйца с щепоткой соли, добавить молоко", "всыпать просеянную муку, перемешать до однородности, дать постоять 15 минут", "растопить ложку масла и добавить в тесто", "жарить тонкие блинчики на слегка смазанной сковороде по 1–2 минуты с каждой стороны", "подавать со сметаной и щедрым количеством мёда"],
  },
  {
    "id": "granola-s-jogurtom", "title": "домашняя гранола с йогуртом", "section": "завтраки",
    "servings": 4, "cooking_time_minutes": 35, "total_kcal_per_serving": 487, "favorite_seed": 39,
    "description": "хрустящая гранола с орехами, запечённая с мёдом",
    "ingredients": [
      {"ingredient_key": "oat-flakes", "name": "овсяные хлопья", "amount": 200, "base_unit": "г", "kcal_per_100g": 389, "proteins": 17, "fats": 7, "carbs": 66},
      {"ingredient_key": "mixed-nuts", "name": "смесь орехов", "amount": 100, "base_unit": "г", "kcal_per_100g": 650, "proteins": 16, "fats": 60, "carbs": 15},
      {"ingredient_key": "honey", "name": "мёд", "amount": 60, "base_unit": "г", "kcal_per_100g": 304, "proteins": 0.8, "fats": 0, "carbs": 82},
      {"ingredient_key": "coconut-oil", "name": "кокосовое масло", "amount": 30, "base_unit": "г", "kcal_per_100g": 862, "proteins": 0, "fats": 100, "carbs": 0},
      {"ingredient_key": "greek-yogurt", "name": "греческий йогурт", "amount": 300, "base_unit": "г", "kcal_per_100g": 66, "proteins": 10, "fats": 2, "carbs": 4},
      {"ingredient_key": "dried-cranberry", "name": "сушёная клюква", "amount": 40, "base_unit": "г", "kcal_per_100g": 308, "proteins": 0.1, "fats": 1, "carbs": 82},
    ],
    "steps": ["разогреть духовку до 160°C", "смешать хлопья с орехами, растопленным кокосовым маслом и мёдом", "распределить на противне в один слой", "запекать 25–30 минут, помешивая каждые 10 минут, до золотистого цвета", "остудить, добавить клюкву", "подавать с греческим йогуртом"],
  },
  {
    "id": "syrniki", "title": "творожные сырники с вареньем", "section": "завтраки",
    "servings": 2, "cooking_time_minutes": 25, "total_kcal_per_serving": 412, "favorite_seed": 44,
    "description": "воздушные творожники, поджаренные до золотистой корочки",
    "ingredients": [
      {"ingredient_key": "cottage-cheese", "name": "творог 9%", "amount": 300, "base_unit": "г", "kcal_per_100g": 159, "proteins": 18, "fats": 9, "carbs": 3},
      {"ingredient_key": "flour", "name": "пшеничная мука", "amount": 60, "base_unit": "г", "kcal_per_100g": 364, "proteins": 10, "fats": 1, "carbs": 76},
      {"ingredient_key": "eggs", "name": "яйцо", "amount": 1, "base_unit": "шт", "kcal_per_100g": 157, "proteins": 13, "fats": 11, "carbs": 1.1},
      {"ingredient_key": "sugar", "name": "сахар", "amount": 40, "base_unit": "г", "kcal_per_100g": 399, "proteins": 0, "fats": 0, "carbs": 100},
      {"ingredient_key": "vanilla-extract", "name": "ванильный экстракт", "amount": 5, "base_unit": "мл", "kcal_per_100g": 288, "proteins": 0, "fats": 0.1, "carbs": 13},
      {"ingredient_key": "jam", "name": "варенье для подачи", "amount": 60, "base_unit": "г", "kcal_per_100g": 238, "proteins": 0.3, "fats": 0, "carbs": 60},
    ],
    "steps": ["тщательно размять творог вилкой, если крупинистый — протереть через сито", "смешать творог, яйцо, сахар, ванильный экстракт и половину муки", "сформировать сырники, обвалять в оставшейся муке", "жарить на среднем огне по 3–4 минуты с каждой стороны до золотистой корочки", "подавать горячими с вареньем или сметаной"],
  },
  {
    "id": "bruschetta-s-tomatami", "title": "брускетта с томатами и базиликом", "section": "закуски",
    "servings": 4, "cooking_time_minutes": 15, "total_kcal_per_serving": 198, "favorite_seed": 29,
    "description": "хрустящий хлеб с сочными томатами и свежим базиликом",
    "ingredients": [
      {"ingredient_key": "baguette", "name": "багет", "amount": 200, "base_unit": "г", "kcal_per_100g": 262, "proteins": 9, "fats": 2, "carbs": 53},
      {"ingredient_key": "tomatoes", "name": "помидоры черри", "amount": 300, "base_unit": "г", "kcal_per_100g": 18, "proteins": 0.9, "fats": 0.2, "carbs": 3.9},
      {"ingredient_key": "garlic", "name": "чеснок", "amount": 15, "base_unit": "г", "kcal_per_100g": 149, "proteins": 6.4, "fats": 0.5, "carbs": 33},
      {"ingredient_key": "fresh-basil", "name": "базилик свежий", "amount": 20, "base_unit": "г", "kcal_per_100g": 23, "proteins": 3.2, "fats": 0.6, "carbs": 2.7},
      {"ingredient_key": "olive-oil", "name": "оливковое масло", "amount": 30, "base_unit": "мл", "kcal_per_100g": 899, "proteins": 0, "fats": 100, "carbs": 0},
      {"ingredient_key": "sea-salt", "name": "морская соль", "amount": 3, "base_unit": "г", "kcal_per_100g": 0, "proteins": 0, "fats": 0, "carbs": 0},
    ],
    "steps": ["нарезать багет диагональными ломтиками толщиной 1.5 см", "обжарить ломтики на сухой сковороде или запечь в духовке при 200°C 5 минут", "натереть горячий хлеб разрезанным зубчиком чеснока", "нарезать помидоры черри, смешать с оливковым маслом, солью и рваным базиликом", "выложить томатную смесь на хлеб и подавать сразу"],
  },
  {
    "id": "hummus-domashny", "title": "домашний хумус с питой", "section": "закуски",
    "servings": 6, "cooking_time_minutes": 20, "total_kcal_per_serving": 241, "favorite_seed": 22,
    "description": "кремовый нутовый дип с тахини и лимоном",
    "ingredients": [
      {"ingredient_key": "chickpeas", "name": "нут консервированный", "amount": 400, "base_unit": "г", "kcal_per_100g": 164, "proteins": 9, "fats": 3, "carbs": 27},
      {"ingredient_key": "tahini", "name": "тахини", "amount": 60, "base_unit": "г", "kcal_per_100g": 595, "proteins": 17, "fats": 53, "carbs": 21},
      {"ingredient_key": "lemon-juice", "name": "сок лимона", "amount": 40, "base_unit": "мл", "kcal_per_100g": 25, "proteins": 0.4, "fats": 0.2, "carbs": 8},
      {"ingredient_key": "garlic", "name": "чеснок", "amount": 10, "base_unit": "г", "kcal_per_100g": 149, "proteins": 6.4, "fats": 0.5, "carbs": 33},
      {"ingredient_key": "olive-oil", "name": "оливковое масло", "amount": 30, "base_unit": "мл", "kcal_per_100g": 899, "proteins": 0, "fats": 100, "carbs": 0},
      {"ingredient_key": "paprika", "name": "паприка копчёная", "amount": 2, "base_unit": "ч.л.", "kcal_per_100g": 282, "proteins": 14, "fats": 13, "carbs": 54},
    ],
    "steps": ["слить жидкость с нута, оставив 50 мл", "смешать в блендере нут, тахини, лимонный сок, чеснок, оставленную жидкость", "пробить до однородной кремовой консистенции 2–3 минуты", "выложить на тарелку, сделать углубление, налить оливковое масло", "посыпать паприкой, подавать с питой или овощами"],
  },
  {
    "id": "kaprese-s-burratoj", "title": "капрезе с бурратой", "section": "закуски",
    "servings": 2, "cooking_time_minutes": 10, "total_kcal_per_serving": 328, "favorite_seed": 31,
    "description": "классический итальянский салат с кремовой бурратой",
    "ingredients": [
      {"ingredient_key": "burrata", "name": "бурратa", "amount": 200, "base_unit": "г", "kcal_per_100g": 280, "proteins": 12, "fats": 24, "carbs": 2},
      {"ingredient_key": "tomatoes", "name": "томаты разных сортов", "amount": 300, "base_unit": "г", "kcal_per_100g": 18, "proteins": 0.9, "fats": 0.2, "carbs": 3.9},
      {"ingredient_key": "fresh-basil", "name": "базилик свежий", "amount": 15, "base_unit": "г", "kcal_per_100g": 23, "proteins": 3.2, "fats": 0.6, "carbs": 2.7},
      {"ingredient_key": "olive-oil", "name": "оливковое масло extra virgin", "amount": 20, "base_unit": "мл", "kcal_per_100g": 899, "proteins": 0, "fats": 100, "carbs": 0},
      {"ingredient_key": "balsamic-glaze", "name": "бальзамический крем", "amount": 15, "base_unit": "мл", "kcal_per_100g": 260, "proteins": 0.5, "fats": 0, "carbs": 65},
      {"ingredient_key": "sea-salt", "name": "морская соль", "amount": 3, "base_unit": "г", "kcal_per_100g": 0, "proteins": 0, "fats": 0, "carbs": 0},
    ],
    "steps": ["нарезать томаты кружками или половинками, разложить на тарелке", "выложить бурратy в центр", "разорвать бурратy руками — из неё вытечет кремовая начинка", "полить оливковым маслом и бальзамическим кремом", "посыпать крупной солью и листьями базилика"],
  },
  {
    "id": "gazpacho", "title": "испанский гаспачо", "section": "закуски",
    "servings": 4, "cooking_time_minutes": 15, "total_kcal_per_serving": 118, "favorite_seed": 17,
    "description": "освежающий холодный суп из свежих томатов",
    "ingredients": [
      {"ingredient_key": "ripe-tomatoes", "name": "спелые помидоры", "amount": 700, "base_unit": "г", "kcal_per_100g": 18, "proteins": 0.9, "fats": 0.2, "carbs": 3.9},
      {"ingredient_key": "cucumber", "name": "огурец", "amount": 200, "base_unit": "г", "kcal_per_100g": 15, "proteins": 0.7, "fats": 0.1, "carbs": 3.6},
      {"ingredient_key": "red-pepper", "name": "красный перец", "amount": 150, "base_unit": "г", "kcal_per_100g": 31, "proteins": 1, "fats": 0.3, "carbs": 7.2},
      {"ingredient_key": "garlic", "name": "чеснок", "amount": 10, "base_unit": "г", "kcal_per_100g": 149, "proteins": 6.4, "fats": 0.5, "carbs": 33},
      {"ingredient_key": "olive-oil", "name": "оливковое масло", "amount": 40, "base_unit": "мл", "kcal_per_100g": 899, "proteins": 0, "fats": 100, "carbs": 0},
      {"ingredient_key": "sherry-vinegar", "name": "хересный уксус", "amount": 20, "base_unit": "мл", "kcal_per_100g": 19, "proteins": 0, "fats": 0, "carbs": 4},
    ],
    "steps": ["крупно нарезать помидоры, огурец и перец, сложить в блендер", "добавить чеснок, оливковое масло, уксус, соль", "пробить до однородной консистенции 2–3 минуты", "попробовать на соль и кислоту, при необходимости скорректировать", "охладить минимум 2 часа в холодильнике", "подавать очень холодным с кусочками льда и мелко нарезанными овощами"],
  },
  {
    "id": "salmon-tartar", "title": "тартар из лосося", "section": "закуски",
    "servings": 2, "cooking_time_minutes": 15, "total_kcal_per_serving": 314, "favorite_seed": 26,
    "description": "свежий лосось с авокадо, каперсами и лимонной заправкой",
    "ingredients": [
      {"ingredient_key": "salmon-fillet", "name": "филе лосося (свежий)", "amount": 250, "base_unit": "г", "kcal_per_100g": 208, "proteins": 20, "fats": 13, "carbs": 0},
      {"ingredient_key": "avocado", "name": "авокадо", "amount": 100, "base_unit": "г", "kcal_per_100g": 160, "proteins": 2, "fats": 15, "carbs": 9},
      {"ingredient_key": "capers", "name": "каперсы", "amount": 20, "base_unit": "г", "kcal_per_100g": 23, "proteins": 2.4, "fats": 0.9, "carbs": 4.9},
      {"ingredient_key": "shallot", "name": "шалот", "amount": 30, "base_unit": "г", "kcal_per_100g": 72, "proteins": 2.5, "fats": 0.1, "carbs": 17},
      {"ingredient_key": "lemon-juice", "name": "сок лимона", "amount": 20, "base_unit": "мл", "kcal_per_100g": 25, "proteins": 0.4, "fats": 0.2, "carbs": 8},
      {"ingredient_key": "olive-oil", "name": "оливковое масло", "amount": 15, "base_unit": "мл", "kcal_per_100g": 899, "proteins": 0, "fats": 100, "carbs": 0},
    ],
    "steps": ["убедиться, что лосось свежайший. нарезать мелким кубиком 5 мм", "авокадо нарезать таким же кубиком, сразу сбрызнуть лимонным соком", "шалот мелко порубить, каперсы — нарезать", "смешать всё с оливковым маслом, солью, щепоткой перца", "формировать с помощью кулинарного кольца. подавать немедленно"],
  },
  {
    "id": "kuritsa-s-ovoshchami", "title": "запечённая курица с корнеплодами", "section": "основное",
    "servings": 4, "cooking_time_minutes": 75, "total_kcal_per_serving": 423, "favorite_seed": 41,
    "description": "сочная курица с карамелизованными овощами из духовки",
    "ingredients": [
      {"ingredient_key": "chicken-thighs", "name": "куриные бёдра", "amount": 800, "base_unit": "г", "kcal_per_100g": 215, "proteins": 16, "fats": 17, "carbs": 0},
      {"ingredient_key": "carrots", "name": "морковь", "amount": 200, "base_unit": "г", "kcal_per_100g": 41, "proteins": 0.9, "fats": 0.2, "carbs": 10},
      {"ingredient_key": "parsnip", "name": "пастернак", "amount": 200, "base_unit": "г", "kcal_per_100g": 75, "proteins": 1.2, "fats": 0.3, "carbs": 18},
      {"ingredient_key": "red-onion", "name": "красный лук", "amount": 150, "base_unit": "г", "kcal_per_100g": 42, "proteins": 1, "fats": 0.1, "carbs": 10},
      {"ingredient_key": "thyme", "name": "тимьян свежий", "amount": 10, "base_unit": "г", "kcal_per_100g": 101, "proteins": 6, "fats": 2, "carbs": 24},
      {"ingredient_key": "olive-oil", "name": "оливковое масло", "amount": 40, "base_unit": "мл", "kcal_per_100g": 899, "proteins": 0, "fats": 100, "carbs": 0},
    ],
    "steps": ["разогреть духовку до 200°C", "нарезать корнеплоды крупными кусками, лук — четвертинками", "смешать овощи с оливковым маслом, солью и перцем в форме для запекания", "выложить курицу поверх овощей, натереть маслом и тимьяном", "запекать 50–60 минут до золотистой корочки", "дать постоять 10 минут перед подачей"],
  },
  {
    "id": "pasta-karbonara", "title": "паста карбонара", "section": "основное",
    "servings": 2, "cooking_time_minutes": 25, "total_kcal_per_serving": 678, "favorite_seed": 56,
    "description": "классическая итальянская паста с яичным кремом и панчеттой",
    "ingredients": [
      {"ingredient_key": "spaghetti", "name": "спагетти", "amount": 200, "base_unit": "г", "kcal_per_100g": 371, "proteins": 13, "fats": 1.5, "carbs": 75},
      {"ingredient_key": "pancetta", "name": "панчетта", "amount": 120, "base_unit": "г", "kcal_per_100g": 443, "proteins": 14, "fats": 42, "carbs": 1},
      {"ingredient_key": "eggs", "name": "яйца", "amount": 2, "base_unit": "шт", "kcal_per_100g": 157, "proteins": 13, "fats": 11, "carbs": 1.1},
      {"ingredient_key": "pecorino", "name": "пекорино романо", "amount": 60, "base_unit": "г", "kcal_per_100g": 387, "proteins": 26, "fats": 31, "carbs": 0},
      {"ingredient_key": "black-pepper", "name": "чёрный перец", "amount": 3, "base_unit": "г", "kcal_per_100g": 251, "proteins": 10, "fats": 3, "carbs": 64},
    ],
    "steps": ["взбить яйца с тёртым пекорино, добавить щедро чёрного перца", "обжарить панчетту на среднем огне до хрустящего состояния, снять с огня", "отварить спагетти в солёной воде до al dente, оставить стакан воды от варки", "переложить горячие спагетти к панчетте, снять с плиты", "добавить яичную смесь, быстро перемешивая и добавляя воду от пасты по ложке", "подавать немедленно с дополнительным пекорино и перцем"],
  },
  {
    "id": "pelmeni-sibirskie", "title": "сибирские пельмени в бульоне", "section": "основное",
    "servings": 4, "cooking_time_minutes": 90, "total_kcal_per_serving": 445, "favorite_seed": 18,
    "description": "домашние пельмени с говядиной и свининой, поданные в наваристом бульоне",
    "ingredients": [
      {"ingredient_key": "flour", "name": "пшеничная мука", "amount": 400, "base_unit": "г", "kcal_per_100g": 364, "proteins": 10, "fats": 1, "carbs": 76},
      {"ingredient_key": "beef-mince", "name": "говяжий фарш", "amount": 250, "base_unit": "г", "kcal_per_100g": 254, "proteins": 17, "fats": 20, "carbs": 0},
      {"ingredient_key": "pork-mince", "name": "свиной фарш", "amount": 250, "base_unit": "г", "kcal_per_100g": 263, "proteins": 16, "fats": 22, "carbs": 0},
      {"ingredient_key": "onion", "name": "репчатый лук", "amount": 150, "base_unit": "г", "kcal_per_100g": 41, "proteins": 1.1, "fats": 0.1, "carbs": 10},
      {"ingredient_key": "eggs", "name": "яйца", "amount": 1, "base_unit": "шт", "kcal_per_100g": 157, "proteins": 13, "fats": 11, "carbs": 1.1},
      {"ingredient_key": "butter", "name": "сливочное масло", "amount": 30, "base_unit": "г", "kcal_per_100g": 748, "proteins": 0.5, "fats": 82, "carbs": 0.5},
    ],
    "steps": ["замесить тесто из муки, яйца, воды и щепотки соли, завернуть в плёнку на 30 минут", "смешать фарш с мелко порубленным луком, солью и перцем", "раскатать тесто тонко, вырезать кружки стаканом диаметром 7 см", "выложить начинку, слепить пельмени, соединив края и загнув хвостики", "варить в подсолённом бульоне 8–10 минут после всплытия", "подавать в бульоне со сливочным маслом и укропом"],
  },
  {
    "id": "rizotto-s-gribami", "title": "ризотто с лесными грибами", "section": "основное",
    "servings": 2, "cooking_time_minutes": 40, "total_kcal_per_serving": 512, "favorite_seed": 48,
    "description": "сливочное ризотто с ароматными лесными грибами и пармезаном",
    "ingredients": [
      {"ingredient_key": "arborio", "name": "рис арборио", "amount": 180, "base_unit": "г", "kcal_per_100g": 351, "proteins": 7, "fats": 0.5, "carbs": 78},
      {"ingredient_key": "forest-mushrooms", "name": "лесные грибы", "amount": 200, "base_unit": "г", "kcal_per_100g": 25, "proteins": 3.1, "fats": 0.3, "carbs": 3.3},
      {"ingredient_key": "white-wine", "name": "белое сухое вино", "amount": 100, "base_unit": "мл", "kcal_per_100g": 66, "proteins": 0.1, "fats": 0, "carbs": 1.4},
      {"ingredient_key": "parmesan", "name": "пармезан", "amount": 50, "base_unit": "г", "kcal_per_100g": 431, "proteins": 38, "fats": 29, "carbs": 3.2},
      {"ingredient_key": "butter", "name": "сливочное масло", "amount": 40, "base_unit": "г", "kcal_per_100g": 748, "proteins": 0.5, "fats": 82, "carbs": 0.5},
      {"ingredient_key": "onion", "name": "репчатый лук", "amount": 80, "base_unit": "г", "kcal_per_100g": 41, "proteins": 1.1, "fats": 0.1, "carbs": 10},
    ],
    "steps": ["разогреть бульон (грибной или куриный) в отдельной кастрюле", "обжарить грибы до румяности, отложить", "в той же кастрюле обжарить мелко нарезанный лук на масле 3–4 минуты", "добавить рис, перемешать с луком 1 минуту, влить вино", "добавлять горячий бульон по половнику, постоянно помешивая, пока каждая порция не впитается", "добавить грибы, снять с огня, вмешать холодное масло и пармезан. дать настояться 2 минуты"],
  },
  {
    "id": "losos-v-duhovke", "title": "лосось с лимоном и травами", "section": "основное",
    "servings": 2, "cooking_time_minutes": 20, "total_kcal_per_serving": 387, "favorite_seed": 35,
    "description": "нежный запечённый лосось с зеленью и лимоном",
    "ingredients": [
      {"ingredient_key": "salmon-fillet", "name": "филе лосося", "amount": 400, "base_unit": "г", "kcal_per_100g": 208, "proteins": 20, "fats": 13, "carbs": 0},
      {"ingredient_key": "lemon", "name": "лимон", "amount": 80, "base_unit": "г", "kcal_per_100g": 34, "proteins": 1.3, "fats": 0.3, "carbs": 9},
      {"ingredient_key": "fresh-dill", "name": "укроп свежий", "amount": 15, "base_unit": "г", "kcal_per_100g": 43, "proteins": 3.5, "fats": 1.1, "carbs": 7},
      {"ingredient_key": "olive-oil", "name": "оливковое масло", "amount": 20, "base_unit": "мл", "kcal_per_100g": 899, "proteins": 0, "fats": 100, "carbs": 0},
      {"ingredient_key": "garlic", "name": "чеснок", "amount": 10, "base_unit": "г", "kcal_per_100g": 149, "proteins": 6.4, "fats": 0.5, "carbs": 33},
      {"ingredient_key": "dijon-mustard", "name": "дижонская горчица", "amount": 15, "base_unit": "г", "kcal_per_100g": 66, "proteins": 3.8, "fats": 4, "carbs": 6},
    ],
    "steps": ["разогреть духовку до 200°C", "смешать горчицу, оливковое масло, измельчённый чеснок и укроп", "выложить лосось на фольгу, смазать горчичной смесью", "разложить сверху кружочки лимона", "запекать 12–15 минут — рыба должна легко расслаиваться вилкой"],
  },
  {
    "id": "govyadina-v-vine", "title": "говядина, тушёная в вине", "section": "основное",
    "servings": 4, "cooking_time_minutes": 150, "total_kcal_per_serving": 467, "favorite_seed": 23,
    "description": "нежная говядина в насыщенном соусе из красного вина",
    "ingredients": [
      {"ingredient_key": "beef-chuck", "name": "говядина (лопатка)", "amount": 800, "base_unit": "г", "kcal_per_100g": 187, "proteins": 18, "fats": 12, "carbs": 0},
      {"ingredient_key": "red-wine", "name": "красное вино", "amount": 300, "base_unit": "мл", "kcal_per_100g": 85, "proteins": 0.1, "fats": 0, "carbs": 2.6},
      {"ingredient_key": "carrots", "name": "морковь", "amount": 150, "base_unit": "г", "kcal_per_100g": 41, "proteins": 0.9, "fats": 0.2, "carbs": 10},
      {"ingredient_key": "celery", "name": "черешковый сельдерей", "amount": 100, "base_unit": "г", "kcal_per_100g": 16, "proteins": 0.7, "fats": 0.2, "carbs": 3.5},
      {"ingredient_key": "onion", "name": "репчатый лук", "amount": 150, "base_unit": "г", "kcal_per_100g": 41, "proteins": 1.1, "fats": 0.1, "carbs": 10},
      {"ingredient_key": "thyme", "name": "тимьян", "amount": 5, "base_unit": "г", "kcal_per_100g": 101, "proteins": 6, "fats": 2, "carbs": 24},
    ],
    "steps": ["нарезать говядину крупными кубиками 4–5 см, обсушить бумажным полотенцем", "обжарить мясо партиями на сильном огне до тёмной корочки со всех сторон", "обжарить крупно нарезанные лук, морковь и сельдерей 5 минут", "вернуть мясо, влить вино, добавить тимьян", "тушить на минимальном огне под крышкой 2–2.5 часа до мягкости", "при необходимости уварить соус и подавать с хлебом или картофельным пюре"],
  },
  {
    "id": "shokoladny-mousse", "title": "шоколадный мусс", "section": "десерты",
    "servings": 4, "cooking_time_minutes": 20, "total_kcal_per_serving": 334, "favorite_seed": 63,
    "description": "воздушный тёмный мусс с хрустящей морской солью",
    "ingredients": [
      {"ingredient_key": "dark-chocolate", "name": "тёмный шоколад 70%", "amount": 150, "base_unit": "г", "kcal_per_100g": 598, "proteins": 8, "fats": 43, "carbs": 46},
      {"ingredient_key": "heavy-cream", "name": "сливки 33%", "amount": 200, "base_unit": "мл", "kcal_per_100g": 322, "proteins": 2.5, "fats": 33, "carbs": 4},
      {"ingredient_key": "eggs", "name": "яйца", "amount": 3, "base_unit": "шт", "kcal_per_100g": 157, "proteins": 13, "fats": 11, "carbs": 1.1},
      {"ingredient_key": "sugar", "name": "сахар", "amount": 40, "base_unit": "г", "kcal_per_100g": 399, "proteins": 0, "fats": 0, "carbs": 100},
      {"ingredient_key": "fleur-de-sel", "name": "флёр де сель", "amount": 2, "base_unit": "г", "kcal_per_100g": 0, "proteins": 0, "fats": 0, "carbs": 0},
    ],
    "steps": ["растопить шоколад на водяной бане, слегка остудить", "отделить желтки от белков. желтки взбить с сахаром до светлой пены", "ввести желтки в шоколад, перемешать", "взбить белки до устойчивых пиков, аккуратно вмешать в шоколадную массу", "взбить сливки до мягких пиков, сложить в мусс", "разлить по бокалам, охладить минимум 2 часа. подавать с флёр де сель"],
  },
  {
    "id": "panna-cotta", "title": "ванильная панна котта", "section": "десерты",
    "servings": 6, "cooking_time_minutes": 25, "total_kcal_per_serving": 287, "favorite_seed": 38,
    "description": "нежный итальянский десерт с соусом из лесных ягод",
    "ingredients": [
      {"ingredient_key": "heavy-cream", "name": "сливки 33%", "amount": 500, "base_unit": "мл", "kcal_per_100g": 322, "proteins": 2.5, "fats": 33, "carbs": 4},
      {"ingredient_key": "milk", "name": "молоко 3.2%", "amount": 200, "base_unit": "мл", "kcal_per_100g": 60, "proteins": 3.2, "fats": 3.2, "carbs": 4.7},
      {"ingredient_key": "gelatin", "name": "желатин листовой", "amount": 12, "base_unit": "г", "kcal_per_100g": 355, "proteins": 87, "fats": 0, "carbs": 0},
      {"ingredient_key": "sugar", "name": "сахар", "amount": 80, "base_unit": "г", "kcal_per_100g": 399, "proteins": 0, "fats": 0, "carbs": 100},
      {"ingredient_key": "vanilla-pod", "name": "стручок ванили", "amount": 1, "base_unit": "шт", "kcal_per_100g": 288, "proteins": 0, "fats": 0.1, "carbs": 13},
      {"ingredient_key": "mixed-berries", "name": "смесь лесных ягод", "amount": 200, "base_unit": "г", "kcal_per_100g": 50, "proteins": 1, "fats": 0.5, "carbs": 12},
    ],
    "steps": ["замочить желатин в холодной воде на 5 минут", "нагреть сливки, молоко и сахар с семенами ванили, не доводя до кипения", "отжать желатин, растворить в горячей смеси", "процедить, разлить по формочкам, охладить минимум 4 часа", "прогреть ягоды с ложкой сахара для соуса", "перевернуть панна котту на тарелку, полить ягодным соусом"],
  },
  {
    "id": "yablochny-pirog", "title": "яблочный пирог с корицей", "section": "десерты",
    "servings": 8, "cooking_time_minutes": 60, "total_kcal_per_serving": 312, "favorite_seed": 27,
    "description": "домашний пирог с мягкими яблоками и хрустящей корочкой",
    "ingredients": [
      {"ingredient_key": "flour", "name": "пшеничная мука", "amount": 300, "base_unit": "г", "kcal_per_100g": 364, "proteins": 10, "fats": 1, "carbs": 76},
      {"ingredient_key": "butter", "name": "сливочное масло", "amount": 150, "base_unit": "г", "kcal_per_100g": 748, "proteins": 0.5, "fats": 82, "carbs": 0.5},
      {"ingredient_key": "apples", "name": "яблоки", "amount": 600, "base_unit": "г", "kcal_per_100g": 52, "proteins": 0.3, "fats": 0.2, "carbs": 14},
      {"ingredient_key": "sugar", "name": "сахар", "amount": 150, "base_unit": "г", "kcal_per_100g": 399, "proteins": 0, "fats": 0, "carbs": 100},
      {"ingredient_key": "cinnamon", "name": "корица молотая", "amount": 5, "base_unit": "г", "kcal_per_100g": 247, "proteins": 4, "fats": 1, "carbs": 81},
      {"ingredient_key": "eggs", "name": "яйца", "amount": 2, "base_unit": "шт", "kcal_per_100g": 157, "proteins": 13, "fats": 11, "carbs": 1.1},
    ],
    "steps": ["нагреть духовку до 180°C. натереть холодное масло в муку, перемешать в крошку", "добавить яйца и 2 ст.л. сахара, быстро замесить тесто, убрать в холодильник на 20 минут", "почистить и тонко нарезать яблоки, смешать с оставшимся сахаром и корицей", "раскатать 2/3 теста, выложить в форму, сформировать бортики", "выложить яблочную начинку, накрыть оставшимся тестом, защипнуть края", "смазать верх яйцом, запекать 40–45 минут до золотистого цвета"],
  },
  {
    "id": "tiramisu", "title": "тирамису", "section": "десерты",
    "servings": 6, "cooking_time_minutes": 30, "total_kcal_per_serving": 423, "favorite_seed": 71,
    "description": "классический итальянский десерт с маскарпоне и эспрессо",
    "ingredients": [
      {"ingredient_key": "mascarpone", "name": "маскарпоне", "amount": 400, "base_unit": "г", "kcal_per_100g": 410, "proteins": 7, "fats": 42, "carbs": 4},
      {"ingredient_key": "savoiardi", "name": "печенье савоярди", "amount": 200, "base_unit": "г", "kcal_per_100g": 372, "proteins": 8, "fats": 7, "carbs": 70},
      {"ingredient_key": "eggs", "name": "яйца", "amount": 3, "base_unit": "шт", "kcal_per_100g": 157, "proteins": 13, "fats": 11, "carbs": 1.1},
      {"ingredient_key": "sugar", "name": "сахар", "amount": 80, "base_unit": "г", "kcal_per_100g": 399, "proteins": 0, "fats": 0, "carbs": 100},
      {"ingredient_key": "espresso", "name": "эспрессо", "amount": 200, "base_unit": "мл", "kcal_per_100g": 2, "proteins": 0.2, "fats": 0, "carbs": 0},
      {"ingredient_key": "cocoa-powder", "name": "какао-порошок", "amount": 20, "base_unit": "г", "kcal_per_100g": 228, "proteins": 20, "fats": 11, "carbs": 35},
    ],
    "steps": ["сварить эспрессо, охладить, добавить по желанию 2 ст.л. амаретто", "отделить желтки, взбить с сахаром до белой пышной массы", "добавить маскарпоне, аккуратно перемешать", "взбить белки до устойчивых пиков, вмешать в кремовую массу", "быстро обмакнуть каждое печенье в кофе (не замачивать!), выложить слоем в форму", "покрыть кремом, повторить слои. убрать в холодильник минимум на 6 часов. перед подачей посыпать какао"],
  },
  {
    "id": "klubnichnyi-sorbet", "title": "клубничный сорбет", "section": "десерты",
    "servings": 4, "cooking_time_minutes": 20, "total_kcal_per_serving": 142, "favorite_seed": 29,
    "description": "освежающий сорбет из спелой клубники — без сливок и яиц",
    "ingredients": [
      {"ingredient_key": "strawberries", "name": "клубника", "amount": 600, "base_unit": "г", "kcal_per_100g": 33, "proteins": 0.7, "fats": 0.3, "carbs": 8},
      {"ingredient_key": "sugar", "name": "сахар", "amount": 120, "base_unit": "г", "kcal_per_100g": 399, "proteins": 0, "fats": 0, "carbs": 100},
      {"ingredient_key": "lemon-juice", "name": "сок лимона", "amount": 30, "base_unit": "мл", "kcal_per_100g": 25, "proteins": 0.4, "fats": 0.2, "carbs": 8},
      {"ingredient_key": "water", "name": "вода", "amount": 100, "base_unit": "мл", "kcal_per_100g": 0, "proteins": 0, "fats": 0, "carbs": 0},
    ],
    "steps": ["сварить сироп из воды и сахара, остудить", "пробить клубнику блендером, процедить через сито от косточек", "смешать клубничное пюре с сиропом и лимонным соком", "вылить в плоский контейнер и заморозить на 1 час", "взбить вилкой, разбив кристаллы льда. повторить ещё 2–3 раза каждые 40 минут", "или использовать мороженицу согласно инструкции"],
  },
]

print(f"Импортируем {len(recipes)} рецептов...")

for recipe in recipes:
    # Создаём рецепт
    recipe_data = {
        "title": recipe["title"],
        "section": recipe["section"],
        "servings": recipe["servings"],
        "cooking_time_minutes": recipe["cooking_time_minutes"],
        "description": recipe["description"],
        "total_kcal_per_serving": recipe["total_kcal_per_serving"],
        "favorite_seed": recipe["favorite_seed"],
    }
    r = requests.post(f"{BASE_URL}/items/recipes", headers=headers, json=recipe_data)
    if r.status_code not in (200, 201):
        print(f"  ОШИБКА рецепт {recipe['title']}: {r.text[:200]}")
        continue
    recipe_id = r.json()["data"]["id"]

    # Создаём ингредиенты
    for i, ing in enumerate(recipe["ingredients"]):
        ing_data = {
            "recipe_id": recipe_id,
            "sort": i,
            "ingredient_key": ing["ingredient_key"],
            "name": ing["name"],
            "amount": ing["amount"],
            "base_unit": ing["base_unit"],
            "kcal_per_100g": ing["kcal_per_100g"],
            "proteins": ing["proteins"],
            "fats": ing["fats"],
            "carbs": ing["carbs"],
        }
        requests.post(f"{BASE_URL}/items/ingredients", headers=headers, json=ing_data)

    # Создаём шаги
    for i, step_text in enumerate(recipe["steps"]):
        step_data = {"recipe_id": recipe_id, "sort": i, "text": step_text}
        requests.post(f"{BASE_URL}/items/steps", headers=headers, json=step_data)

    print(f"  ✓ {recipe['title']}")

print("\nГотово!")
