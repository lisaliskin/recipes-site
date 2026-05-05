<template>
  <button
    class="heart-btn"
    :class="{ active: isFavorited }"
    :aria-label="isFavorited ? 'убрать из избранного' : 'добавить в избранное'"
    @click.stop.prevent="handleToggle"
  >
    <span class="heart-icon" :class="{ 'heart-pop': justToggled }">
      {{ isFavorited ? '♥' : '♡' }}
    </span>
    <span class="heart-count text-label">{{ count }}</span>
  </button>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useFavoritesStore } from '../../stores/favoritesStore'

const props = defineProps<{ recipeId: string }>()
const favStore = useFavoritesStore()
const justToggled = ref(false)

const isFavorited = computed(() => favStore.isFavorited(props.recipeId))
const count = computed(() => favStore.getCount(props.recipeId))

function handleToggle() {
  favStore.toggleFavorite(props.recipeId)
  justToggled.value = true
  setTimeout(() => { justToggled.value = false }, 300)
}

import { computed } from 'vue'
</script>

<style scoped>
.heart-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 6px;
  border-radius: 2px;
  transition: opacity 0.2s;
  line-height: 1;
}

.heart-btn:hover {
  opacity: 0.7;
}

.heart-icon {
  display: inline-block;
  font-size: 1rem;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), color 0.2s;
}

.heart-btn.active .heart-icon {
  color: #b84040;
  transform: scale(1.15);
}

.heart-pop {
  animation: heart-pop 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes heart-pop {
  0% { transform: scale(1); }
  50% { transform: scale(1.45); }
  100% { transform: scale(1.15); }
}

.heart-count {
  font-size: 0.6rem;
  letter-spacing: 0.1em;
  color: var(--color-ink-light);
}
</style>
