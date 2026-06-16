<template>
  <main class="home">
    <div class="home-hero">
      <h1 class="hero-title text-display">рецепты</h1>
      <p class="hero-sub text-small text-muted">
        <span v-if="recipesStore.loading">загружаем...</span>
        <span v-else>{{ recipesStore.recipes.length }} {{ pluralize(recipesStore.recipes.length) }} · домашняя кухня</span>
      </p>
    </div>

    <div v-if="recipesStore.error" class="load-error text-body">
      не удалось загрузить рецепты: {{ recipesStore.error }}
    </div>

    <div class="home-sections" v-else>
      <RecipeSection
        v-for="(section, idx) in SECTIONS"
        :key="section.key"
        :section="section"
        :recipes="recipesStore.getBySection(section.key).value"
        :default-open="idx === 0"
      />
    </div>

    <AuthorBio />
  </main>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { SECTIONS } from '../../data/recipes'
import RecipeSection from './RecipeSection.vue'
import AuthorBio from './AuthorBio.vue'
import { useUiStore } from '../../stores/uiStore'
import { useRecipesStore } from '../../stores/recipesStore'

const uiStore = useUiStore()
const recipesStore = useRecipesStore()

onMounted(() => {
  uiStore.setActiveSection(null)
  recipesStore.load()
})

function pluralize(n: number): string {
  const mod10 = n % 10
  const mod100 = n % 100
  if (mod100 >= 11 && mod100 <= 19) return 'блюд'
  if (mod10 === 1) return 'блюдо'
  if (mod10 >= 2 && mod10 <= 4) return 'блюда'
  return 'блюд'
}

</script>

<style scoped>
.home {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 calc(var(--spacing) * 4) calc(var(--spacing) * 8);
}

.home-hero {
  padding: calc(var(--spacing) * 8) 0 calc(var(--spacing) * 4);
  display: flex;
  align-items: baseline;
  gap: 32px;
  flex-wrap: wrap;
}

.hero-title {
  font-size: clamp(4rem, 10vw, 8rem);
  line-height: 0.88;
  letter-spacing: -0.04em;
  font-weight: 700;
  text-transform: lowercase;
}

.hero-sub {
  font-size: 0.7rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding-bottom: 4px;
}

.home-sections {
  display: flex;
  flex-direction: column;
  gap: calc(var(--spacing) * 2);
}

.load-error {
  padding: calc(var(--spacing) * 4) 0;
  color: var(--color-ink-light);
}

@media (max-width: 480px) {
  .home {
    padding: 0 calc(var(--spacing) * 2.5) calc(var(--spacing) * 6);
  }

  .home-hero {
    padding: calc(var(--spacing) * 5) 0 calc(var(--spacing) * 3);
  }
}
</style>
