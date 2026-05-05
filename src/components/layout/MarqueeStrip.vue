<template>
  <div class="marquee-bar">
    <div class="marquee-wrapper">
      <div class="marquee-track" aria-hidden="true">
        <span v-for="n in 4" :key="n" class="marquee-text text-label">
          {{ text }}&nbsp;&nbsp;&nbsp;
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const text =
  '· домашние рецепты · перерасчёт ингредиентов · продуктовая корзина · сезонные блюда · без лишних шагов ·'
</script>

<style scoped>
.marquee-bar {
  background: var(--color-ink);
  color: var(--bg-color);
  overflow: hidden;
  padding: 9px 0;
  position: sticky;
  top: 0;
  z-index: 100;
  transition: color 0.8s ease;
}

.marquee-wrapper {
  overflow: hidden;
  white-space: nowrap;
}

.marquee-track {
  display: inline-block;
  animation: marquee 30s linear infinite;
}

.marquee-text {
  font-size: 0.6rem;
  letter-spacing: 0.2em;
}

@keyframes marquee {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}
</style>
