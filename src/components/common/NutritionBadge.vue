<template>
  <div class="nutrition-wrap">
    <span class="nutrition-badge text-label">
      {{ time }} мин&nbsp;·&nbsp;{{ kcal }} ккал
    </span>
    <div v-if="macros" class="macros-row text-label">
      <span class="macro"><span class="macro-label">Б</span> {{ macros.protein }}г</span>
      <span class="macro-sep">·</span>
      <span class="macro"><span class="macro-label">Ж</span> {{ macros.fat }}г</span>
      <span class="macro-sep">·</span>
      <span class="macro"><span class="macro-label">У</span> {{ macros.carbs }}г</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  time: number
  kcal: number
  macros?: { protein: number; fat: number; carbs: number }
}>()
</script>

<style scoped>
.nutrition-wrap {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.nutrition-badge {
  display: inline-block;
  color: var(--color-ink-light);
  font-size: 0.625rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
}

.macros-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.6rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-ink-light);
}

.macro {
  display: flex;
  align-items: baseline;
  gap: 3px;
}

.macro-label {
  font-weight: 600;
  color: var(--color-ink);
  opacity: 0.5;
}

.macro-sep {
  opacity: 0.3;
}
</style>
