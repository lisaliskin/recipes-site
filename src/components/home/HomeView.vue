<template>
  <main class="home">
    <div class="home-hero">
      <div class="hero-top">
        <h1 class="hero-title text-display">рецепты</h1>
        <p class="hero-sub text-small text-muted">
          <span v-if="recipesStore.loading">загружаем...</span>
          <span v-else>{{ recipesStore.recipes.length }} {{ pluralize(recipesStore.recipes.length) }} · домашняя кухня</span>
        </p>
      </div>
      <div class="search-wrap">
        <input
          v-model="query"
          class="search-input text-label"
          type="search"
          placeholder="поиск рецептов..."
          autocomplete="off"
        />
        <button v-if="query" class="search-clear" @click="query = ''" aria-label="очистить">✕</button>
      </div>
    </div>

    <div v-if="recipesStore.error" class="load-error text-body">
      не удалось загрузить рецепты: {{ recipesStore.error }}
    </div>

    <template v-else-if="query.trim()">
      <div v-if="searchResults.length" class="search-grid">
        <RecipeCard v-for="r in searchResults" :key="r.id" :recipe="r" />
      </div>
      <div v-else class="search-empty text-body text-muted">
        по запросу «{{ query.trim() }}» ничего не найдено
      </div>
    </template>

    <div v-else class="home-sections">
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
import { ref, computed, onMounted } from 'vue'
import { SECTIONS } from '../../data/recipes'
import RecipeSection from './RecipeSection.vue'
import RecipeCard from './RecipeCard.vue'
import AuthorBio from './AuthorBio.vue'
import { useUiStore } from '../../stores/uiStore'
import { useRecipesStore } from '../../stores/recipesStore'

const uiStore = useUiStore()
const recipesStore = useRecipesStore()
const query = ref('')

const searchResults = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return []
  return recipesStore.recipes.filter(
    (r) =>
      r.title.toLowerCase().includes(q) ||
      r.description.toLowerCase().includes(q),
  )
})

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
  align-items: flex-end;
  justify-content: space-between;
  gap: 32px;
  flex-wrap: wrap;
}

.hero-top {
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

.search-wrap {
  position: relative;
  flex-shrink: 0;
}

.search-input {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--color-ink);
  background: transparent;
  border: none;
  border-bottom: 1px solid var(--color-border);
  padding: 6px 28px 6px 0;
  width: 200px;
  outline: none;
  transition: border-color 0.2s;
}

.search-input::placeholder {
  color: var(--color-ink-light);
  opacity: 0.6;
}

.search-input:focus {
  border-color: var(--color-ink);
}

.search-input::-webkit-search-cancel-button {
  display: none;
}

.search-clear {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.55rem;
  color: var(--color-ink-light);
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.search-clear:hover {
  opacity: 1;
}

.search-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: calc(var(--spacing) * 3);
  padding-top: calc(var(--spacing) * 2);
}

.search-empty {
  padding: calc(var(--spacing) * 6) 0;
  font-size: 0.85rem;
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

@media (max-width: 640px) {
  .home {
    padding: 0 calc(var(--spacing) * 2.5) calc(var(--spacing) * 6);
  }

  .home-hero {
    padding: calc(var(--spacing) * 5) 0 calc(var(--spacing) * 3);
    flex-direction: column;
    align-items: flex-start;
  }

  .search-input {
    width: 100%;
  }

  .search-wrap {
    width: 100%;
  }
}
</style>
