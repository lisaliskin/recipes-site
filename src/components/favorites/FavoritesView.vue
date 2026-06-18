<template>
  <main class="favorites">
    <div class="fav-hero">
      <h1 class="fav-title text-display">избранное</h1>
      <p class="fav-sub text-small text-muted">
        <span v-if="favStore.favoritedRecipes.length">
          {{ favStore.favoritedRecipes.length }} {{ pluralize(favStore.favoritedRecipes.length) }}
        </span>
        <span v-else>пока пусто</span>
      </p>
    </div>

    <div v-if="favStore.favoritedRecipes.length" class="fav-grid">
      <RecipeCard v-for="r in favStore.favoritedRecipes" :key="r.id" :recipe="r" />
    </div>

    <div v-else class="fav-empty">
      <span class="fav-empty-icon">♡</span>
      <p class="text-body text-muted">добавляй рецепты в избранное — они появятся здесь</p>
    </div>
  </main>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useFavoritesStore } from '../../stores/favoritesStore'
import { useRecipesStore } from '../../stores/recipesStore'
import { useUiStore } from '../../stores/uiStore'
import RecipeCard from '../home/RecipeCard.vue'

const favStore = useFavoritesStore()
const recipesStore = useRecipesStore()
const uiStore = useUiStore()

onMounted(async () => {
  uiStore.setActiveSection(null)
  await recipesStore.load()
})

function pluralize(n: number): string {
  const mod10 = n % 10
  const mod100 = n % 100
  if (mod100 >= 11 && mod100 <= 19) return 'рецептов'
  if (mod10 === 1) return 'рецепт'
  if (mod10 >= 2 && mod10 <= 4) return 'рецепта'
  return 'рецептов'
}
</script>

<style scoped>
.favorites {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 calc(var(--spacing) * 4) calc(var(--spacing) * 8);
}

.fav-hero {
  padding: calc(var(--spacing) * 8) 0 calc(var(--spacing) * 4);
  display: flex;
  align-items: baseline;
  gap: 32px;
  flex-wrap: wrap;
}

.fav-title {
  font-size: clamp(4rem, 10vw, 8rem);
  line-height: 0.88;
  letter-spacing: -0.04em;
  font-weight: 700;
  text-transform: lowercase;
}

.fav-sub {
  font-size: 0.7rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding-bottom: 4px;
}

.fav-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: calc(var(--spacing) * 3);
}

.fav-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: calc(var(--spacing) * 8) 0;
  text-align: center;
}

.fav-empty-icon {
  font-size: 3rem;
  opacity: 0.2;
}

@media (max-width: 480px) {
  .favorites {
    padding: 0 calc(var(--spacing) * 2.5) calc(var(--spacing) * 6);
  }

  .fav-hero {
    padding: calc(var(--spacing) * 5) 0 calc(var(--spacing) * 3);
  }
}
</style>
