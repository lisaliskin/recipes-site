<template>
  <section class="recipe-section">
    <div class="section-header" @click="toggle">
      <div class="section-header-left">
        <SvgIllustration :name="illustrationName" class="section-illus" />
        <h2 class="section-title text-display-md">{{ section.label }}</h2>
      </div>
      <div class="section-header-right">
        <span class="section-count text-label">{{ recipes.length }} {{ pluralizeRecipe(recipes.length) }}</span>
        <span class="section-toggle text-label">{{ isOpen ? '−' : '+' }}</span>
      </div>
    </div>

    <div class="section-divider" />

    <transition name="section-collapse">
      <div v-show="isOpen" class="section-content" :style="{ maxHeight: isOpen ? '9999px' : '0' }">
        <div class="recipe-grid">
          <RecipeCard v-for="r in recipes" :key="r.id" :recipe="r" />
        </div>
      </div>
    </transition>
  </section>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Recipe } from '../../types'
import type { SectionKey } from '../../types'
import RecipeCard from './RecipeCard.vue'
import SvgIllustration from '../common/SvgIllustration.vue'

const props = defineProps<{
  section: { key: SectionKey; label: string }
  recipes: Recipe[]
  defaultOpen?: boolean
}>()

const isOpen = ref(props.defaultOpen ?? false)

function pluralizeRecipe(n: number): string {
  const mod10 = n % 10
  const mod100 = n % 100
  if (mod100 >= 11 && mod100 <= 19) return 'рецептов'
  if (mod10 === 1) return 'рецепт'
  if (mod10 >= 2 && mod10 <= 4) return 'рецепта'
  return 'рецептов'
}

const ILLUS_MAP: Record<SectionKey, string> = {
  завтраки: 'sprig',
  закуски: 'leaf',
  основное: 'fork',
  десерты: 'bowl',
}

const illustrationName = computed(() => ILLUS_MAP[props.section.key])

function toggle() {
  isOpen.value = !isOpen.value
}
</script>

<style scoped>
.recipe-section {
  padding: calc(var(--spacing) * 4) 0;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  padding: calc(var(--spacing) * 2) 0;
  gap: 16px;
  user-select: none;
}

.section-header:hover .section-title {
  opacity: 0.6;
}

.section-header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.section-illus {
  width: 36px;
  height: 48px;
  opacity: 0.5;
  flex-shrink: 0;
}

.section-title {
  font-size: clamp(2rem, 5vw, 4rem);
  line-height: 1;
  transition: opacity 0.2s;
}

.section-header-right {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-shrink: 0;
}

.section-count,
.section-toggle {
  font-size: 0.625rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--color-ink-light);
}

.section-toggle {
  font-size: 1.25rem;
  letter-spacing: 0;
  color: var(--color-ink);
  font-weight: 400;
  min-width: 20px;
  text-align: center;
}

.section-divider {
  height: 1px;
  background: var(--color-border);
}

.section-content {
  padding-top: calc(var(--spacing) * 3);
}

.recipe-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: calc(var(--spacing) * 3);
}

/* Transition */
.section-collapse-enter-active {
  transition: opacity 0.4s ease 0.05s;
  overflow: hidden;
}
.section-collapse-leave-active {
  transition: opacity 0.25s ease;
  overflow: hidden;
}
.section-collapse-enter-from,
.section-collapse-leave-to {
  opacity: 0;
}
</style>
