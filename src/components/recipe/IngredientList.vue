<template>
  <div class="ingredient-list">
    <h3 class="list-title text-label">ингредиенты</h3>
    <ul class="list">
      <li
        v-for="ing in recipe.ingredients"
        :key="ing.id"
        class="list-item"
      >
        <span class="ing-name text-body">{{ ing.name }}</span>
        <span class="ing-amount text-body">
          {{ formatAmount(ing.amount) }} {{ ing.baseUnit }}
        </span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import type { Recipe } from '../../types'

defineProps<{
  recipe: Recipe
  formatAmount: (amount: number) => string
}>()
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
