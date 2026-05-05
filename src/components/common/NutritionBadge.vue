<template>
  <span class="nutrition-badge text-label">
    {{ time }} мин&nbsp;·&nbsp;{{ kcal }} ккал
  </span>
</template>

<script setup lang="ts">
defineProps<{
  time: number
  kcal: number
}>()
</script>

<style scoped>
.nutrition-badge {
  display: inline-block;
  color: var(--color-ink-light);
  font-size: 0.625rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
}
</style>
