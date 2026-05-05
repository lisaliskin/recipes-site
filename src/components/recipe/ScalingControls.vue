<template>
  <div class="scaling-controls">
    <div class="mode-tabs">
      <button
        class="mode-tab text-label"
        :class="{ active: mode === 'servings' }"
        @click="setMode('servings')"
      >
        по порциям
      </button>
      <button
        class="mode-tab text-label"
        :class="{ active: mode === 'ingredient' }"
        @click="setMode('ingredient')"
      >
        по ингредиенту
      </button>
    </div>

    <div v-if="mode === 'servings'" class="servings-control">
      <span class="text-label">порций:</span>
      <div class="stepper">
        <button class="stepper-btn" @click="decrement" :disabled="desiredServings <= 1">−</button>
        <span class="stepper-val text-body">{{ desiredServings }}</span>
        <button class="stepper-btn" @click="increment">+</button>
      </div>
    </div>

    <div v-else class="ingredient-control">
      <div class="ingredient-select-row">
        <span class="text-label">ингредиент:</span>
        <select v-model="anchorIngredientId" class="ing-select text-small">
          <option
            v-for="ing in recipe.ingredients"
            :key="ing.id"
            :value="ing.id"
          >
            {{ ing.name }}
          </option>
        </select>
      </div>

      <div class="ingredient-input-row">
        <span class="text-label">количество:</span>
        <div class="input-unit">
          <input
            v-model.number="anchorQuantity"
            type="number"
            min="0"
            step="10"
            class="qty-input text-body"
          />
          <span class="unit-label text-label">{{ selectedUnit }}</span>
        </div>
      </div>
    </div>

    <div class="scale-result text-label" v-if="scaleFactor !== 1">
      коэффициент: ×{{ scaleFactor.toFixed(2) }} · {{ scaledServings }} порц.
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Recipe } from '../../types'
import type { ScalingMode } from '../../composables/useIngredientScaling'

const props = defineProps<{
  recipe: Recipe
  mode: ScalingMode
  desiredServings: number
  anchorIngredientId: string | null
  anchorQuantity: number
  scaleFactor: number
  scaledServings: number
}>()

const emit = defineEmits<{
  'update:mode': [v: ScalingMode]
  'update:desiredServings': [v: number]
  'update:anchorIngredientId': [v: string | null]
  'update:anchorQuantity': [v: number]
  'set-mode': [v: ScalingMode]
}>()

const mode = computed({
  get: () => props.mode,
  set: (v) => emit('update:mode', v),
})

const desiredServings = computed({
  get: () => props.desiredServings,
  set: (v) => emit('update:desiredServings', v),
})

const anchorIngredientId = computed({
  get: () => props.anchorIngredientId,
  set: (v) => emit('update:anchorIngredientId', v),
})

const anchorQuantity = computed({
  get: () => props.anchorQuantity,
  set: (v) => emit('update:anchorQuantity', v),
})

const selectedUnit = computed(() => {
  const ing = props.recipe.ingredients.find((i) => i.id === props.anchorIngredientId)
  return ing?.baseUnit ?? ''
})

function increment() {
  emit('update:desiredServings', props.desiredServings + 1)
}

function decrement() {
  if (props.desiredServings > 1) emit('update:desiredServings', props.desiredServings - 1)
}

function setMode(m: ScalingMode) {
  emit('set-mode', m)
}
</script>

<style scoped>
.scaling-controls {
  background: rgba(26, 26, 26, 0.04);
  padding: calc(var(--spacing) * 3);
  display: flex;
  flex-direction: column;
  gap: calc(var(--spacing) * 2);
}

.mode-tabs {
  display: flex;
  gap: 0;
  border: 1px solid var(--color-border);
  align-self: flex-start;
}

.mode-tab {
  font-size: 0.6rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 7px 14px;
  transition: background 0.2s, color 0.2s;
  border: none;
  background: transparent;
  color: var(--color-ink-light);
}

.mode-tab.active {
  background: var(--color-ink);
  color: var(--bg-color);
}

.servings-control,
.ingredient-control {
  display: flex;
  flex-direction: column;
  gap: calc(var(--spacing) * 1.5);
}

.ingredient-select-row,
.ingredient-input-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.stepper {
  display: flex;
  align-items: center;
  gap: 0;
  border: 1px solid var(--color-border);
  align-self: flex-start;
  margin-top: 4px;
}

.stepper-btn {
  width: 32px;
  height: 32px;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s;
  border: none;
  background: transparent;
  cursor: pointer;
}

.stepper-btn:hover:not(:disabled) {
  background: rgba(26, 26, 26, 0.08);
}

.stepper-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.stepper-val {
  min-width: 36px;
  text-align: center;
  border-left: 1px solid var(--color-border);
  border-right: 1px solid var(--color-border);
  padding: 4px 8px;
  font-size: 0.875rem;
}

.ing-select {
  font-size: 0.75rem;
  padding: 5px 8px;
  border: 1px solid var(--color-border);
  background: transparent;
  color: var(--color-ink);
  min-width: 160px;
  max-width: 220px;
}

.input-unit {
  display: flex;
  align-items: center;
  gap: 6px;
}

.qty-input {
  width: 80px;
  font-size: 0.875rem;
  padding: 5px 8px;
  border: 1px solid var(--color-border);
  background: transparent;
  color: var(--color-ink);
}

.unit-label {
  font-size: 0.6rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--color-ink-light);
}

.scale-result {
  font-size: 0.6rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--color-ink-light);
  padding-top: 4px;
  border-top: 1px solid var(--color-border);
}
</style>
