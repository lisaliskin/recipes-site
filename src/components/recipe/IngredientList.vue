<template>
  <div class="ingredient-list">
    <h3 class="list-title text-label">ингредиенты</h3>
    <div v-for="g in groups" :key="g.title" class="group">
      <h4 v-if="g.title" class="group-title text-label">{{ g.title }}</h4>
      <ul class="list">
        <li
          v-for="ing in g.items"
          :key="ing.id"
          class="list-item"
        >
          <span class="ing-name text-body">{{ ing.name }}</span>
          <span class="ing-amount text-body">
            <template v-if="isToTaste(ing.baseUnit)">{{ ing.baseUnit }}</template>
            <template v-else>{{ formatAmount(ing.amount) }} {{ ing.baseUnit }}</template>
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Ingredient, Recipe } from '../../types'
import { isToTaste } from '../../utils/units'

const props = defineProps<{
  recipe: Recipe
  formatAmount: (amount: number) => string
}>()

// Группы в порядке первого появления; ингредиенты без группы — в общей группе без заголовка
const groups = computed(() => {
  const map = new Map<string, Ingredient[]>()
  for (const ing of props.recipe.ingredients) {
    const title = ing.group ?? ''
    if (!map.has(title)) map.set(title, [])
    map.get(title)!.push(ing)
  }
  return [...map].map(([title, items]) => ({ title, items }))
})
</script>

<style scoped>
.ingredient-list {
  display: flex;
  flex-direction: column;
  gap: calc(var(--spacing) * 2);
}

.list-title {
  font-size: 0.625rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--color-ink-light);
  padding-bottom: calc(var(--spacing) * 1.5);
  border-bottom: 1px solid var(--color-border);
}

.group-title {
  font-size: 0.75rem;
  font-style: italic;
  color: var(--color-ink);
  padding-top: calc(var(--spacing) * 1.5);
}

.list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.list-item {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: 10px 0;
  border-bottom: 1px solid var(--color-border);
  gap: 16px;
}

.ing-name {
  font-size: 0.875rem;
}

.ing-amount {
  font-size: 0.875rem;
  font-style: italic;
  color: var(--color-ink-light);
  white-space: nowrap;
  flex-shrink: 0;
}
</style>
