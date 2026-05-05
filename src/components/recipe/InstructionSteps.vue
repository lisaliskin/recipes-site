<template>
  <div class="instruction-steps">
    <h3 class="steps-title text-label">приготовление</h3>
    <ol class="steps-list">
      <li
        v-for="step in recipe.steps"
        :key="step.step"
        class="step-item"
      >
        <span class="step-num">{{ String(step.step).padStart(2, '0') }}</span>
        <p class="step-text text-body">{{ step.text }}</p>
      </li>
    </ol>
  </div>
</template>

<script setup lang="ts">
import type { Recipe } from '../../types'

defineProps<{ recipe: Recipe }>()
</script>

<style scoped>
.instruction-steps {
  display: flex;
  flex-direction: column;
  gap: calc(var(--spacing) * 2);
}

.steps-title {
  font-size: 0.625rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--color-ink-light);
  padding-bottom: calc(var(--spacing) * 1.5);
  border-bottom: 1px solid var(--color-border);
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.step-item {
  display: grid;
  grid-template-columns: 36px 1fr;
  gap: 16px;
  align-items: start;
  padding: 18px 0;
  border-bottom: 1px solid var(--color-border);
}

.step-num {
  font-size: 0.625rem;
  letter-spacing: 0.1em;
  color: var(--color-ink-light);
  padding-top: 3px;
  font-style: italic;
}

.step-text {
  font-size: 0.875rem;
  line-height: 1.65;
}
</style>
