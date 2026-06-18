import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { recipes } from '../data/recipes'
import { useRecipesStore } from './recipesStore'

export const useFavoritesStore = defineStore('favorites', () => {
  const seedCounts: Record<string, number> = {}
  recipes.forEach((r) => {
    seedCounts[r.id] = r.favoriteSeed
  })

  const savedFavorites = localStorage.getItem('userFavorites')
  const savedCounts = localStorage.getItem('globalCounts')

  const userFavorites = ref<Record<string, boolean>>(
    savedFavorites ? JSON.parse(savedFavorites) : {},
  )
  const globalCounts = ref<Record<string, number>>(
    savedCounts ? JSON.parse(savedCounts) : { ...seedCounts },
  )

  function isFavorited(recipeId: string): boolean {
    return !!userFavorites.value[recipeId]
  }

  function getCount(recipeId: string): number {
    return globalCounts.value[recipeId] ?? seedCounts[recipeId] ?? 0
  }

  function toggleFavorite(recipeId: string) {
    const nowFavoriting = !userFavorites.value[recipeId]
    userFavorites.value[recipeId] = nowFavoriting
    const current = globalCounts.value[recipeId] ?? seedCounts[recipeId] ?? 0
    globalCounts.value[recipeId] = current + (nowFavoriting ? 1 : -1)
    localStorage.setItem('userFavorites', JSON.stringify(userFavorites.value))
    localStorage.setItem('globalCounts', JSON.stringify(globalCounts.value))
  }

  const favoritedRecipes = computed(() => {
    const recipesStore = useRecipesStore()
    return recipesStore.recipes.filter((r) => userFavorites.value[r.id])
  })

  return { userFavorites, globalCounts, isFavorited, getCount, toggleFavorite, favoritedRecipes }
})
