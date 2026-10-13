<template>
  <section class="dinner-picker">
    <div class="picker-row">
      <button class="picker-btn text-label" :disabled="!recipesStore.loaded" @click="pick">
        {{ picked ? 'ещё вариант' : 'что приготовить на ужин?' }}
      </button>

      <div class="picker-options" role="radiogroup" aria-label="главный ингредиент">
        <span class="options-label text-label text-muted">главный ингредиент:</span>
        <button
          v-for="opt in OPTIONS"
          :key="opt.key"
          class="option text-label"
          :class="{ active: mainIngredient === opt.key }"
          role="radio"
          :aria-checked="mainIngredient === opt.key"
          @click="selectOption(opt.key)"
        >{{ opt.label }}</button>
      </div>
    </div>

    <Transition name="page" mode="out-in">
      <div v-if="picked" :key="picked.id" class="picker-result">
        <RecipeCard :recipe="picked" />
      </div>
      <p v-else-if="noMatch" class="picker-empty text-body text-muted">
        пока нет подходящих рецептов — попробуйте другой ингредиент
      </p>
    </Transition>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Recipe } from '../../types'
import { useRecipesStore } from '../../stores/recipesStore'
import RecipeCard from './RecipeCard.vue'

type MainIngredient = 'любой' | 'курица' | 'говядина' | 'без мяса'

const OPTIONS: { key: MainIngredient; label: string }[] = [
  { key: 'любой', label: 'любой' },
  { key: 'курица', label: 'курица' },
  { key: 'говядина', label: 'говядина' },
  { key: 'без мяса', label: 'без мяса' },
]

// Определяем по названиям ингредиентов (основы слов, чтобы ловить «куриные бёдра», «говяжий фарш» и т.п.)
const CHICKEN = /кур(ин|иц)|цыпл/
const BEEF = /говя[дж]|телят/
const MEAT = /кур(ин|иц)|цыпл|говя[дж]|телят|свин|фарш|бекон|ветчин|панчетт|гуанчал|индей|баран|колбас|сосис|утк|утин|кроли|прошутто|салями|хамон|чоризо/

const recipesStore = useRecipesStore()
const mainIngredient = ref<MainIngredient>('любой')
const picked = ref<Recipe | null>(null)
const noMatch = ref(false)

function hasIngredient(r: Recipe, re: RegExp) {
  return r.ingredients.some((i) => re.test(i.name.toLowerCase()))
}

function matches(r: Recipe): boolean {
  switch (mainIngredient.value) {
    case 'курица':
      return hasIngredient(r, CHICKEN)
    case 'говядина':
      return hasIngredient(r, BEEF)
    case 'без мяса':
      return !hasIngredient(r, MEAT)
    default:
      return true
  }
}

function candidates(): Recipe[] {
  const all = recipesStore.recipes.filter((r) => r.section !== 'десерты' && matches(r))
  // на ужин в первую очередь основные блюда и закуски, завтраки — если больше ничего нет
  const dinner = all.filter((r) => r.section === 'основное' || r.section === 'закуски')
  return dinner.length ? dinner : all
}

function pick() {
  const list = candidates()
  noMatch.value = list.length === 0
  if (!list.length) {
    picked.value = null
    return
  }
  // не показываем то же блюдо два раза подряд, если есть выбор
  const pool = list.length > 1 ? list.filter((r) => r.id !== picked.value?.id) : list
  picked.value = pool[Math.floor(Math.random() * pool.length)]
}

function selectOption(key: MainIngredient) {
  mainIngredient.value = key
  if (picked.value || noMatch.value) {
    picked.value = null
    pick()
  }
}
</script>

<style scoped>
.dinner-picker {
  padding: calc(var(--spacing) * 3) 0 calc(var(--spacing) * 4);
  border-top: 1px solid var(--color-border);
  margin-bottom: calc(var(--spacing) * 2);
}

.picker-row {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}

.picker-btn {
  font-size: 0.7rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 12px 18px;
  background: var(--color-ink);
  color: var(--bg-color);
  border: 1px solid var(--color-ink);
  transition: opacity 0.2s;
}

.picker-btn:hover {
  opacity: 0.8;
}

.picker-btn:disabled {
  opacity: 0.4;
  cursor: default;
}

.picker-options {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.options-label {
  margin-right: 4px;
}

.option {
  font-size: 0.6rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 5px 10px;
  border: 1px solid var(--color-border);
  transition: background 0.2s, color 0.2s, border-color 0.2s;
}

.option:hover,
.option.active {
  background: var(--color-ink);
  color: var(--bg-color);
  border-color: var(--color-ink);
}

.picker-result {
  margin-top: calc(var(--spacing) * 3);
  max-width: 420px;
}

.picker-empty {
  margin-top: calc(var(--spacing) * 3);
  font-size: 0.85rem;
}

@media (max-width: 640px) {
  .picker-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .picker-result {
    max-width: none;
  }
}
</style>
