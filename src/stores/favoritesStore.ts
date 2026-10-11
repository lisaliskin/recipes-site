import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRecipesStore } from './recipesStore'

export const useFavoritesStore = defineStore('favorites', () => {
  const recipesStore = useRecipesStore()

  const savedFavorites = localStorage.getItem('userFavorites')
  const userFavorites = ref<Record<string, boolean>>(
    savedFavorites ? JSON.parse(savedFavorites) : {},
  )

  // Old builds cached whole counts here; they would hide seed changes made in Directus.
  localStorage.removeItem('globalCounts')

  function isFavorited(recipeId: string): boolean {
    return !!userFavorites.value[recipeId]
  }

  function getCount(recipeId: string): number {
    const seed = recipesStore.recipes.find((r) => r.id === recipeId)?.favoriteSeed ?? 0
    return seed + (userFavorites.value[recipeId] ? 1 : 0)
  }

  function toggleFavorite(recipeId: string) {
    userFavorites.value[recipeId] = !userFavorites.value[recipeId]
    localStorage.setItem('userFavorites', JSON.stringify(userFavorites.value))
  }

  const favoritedRecipes = computed(() =>
    recipesStore.recipes.filter((r) => userFavorites.value[r.id]),
  )

  return { userFavorites, isFavorited, getCount, toggleFavorite, favoritedRecipes }
})
