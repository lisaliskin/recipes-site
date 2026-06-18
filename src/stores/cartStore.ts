import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { CartRecipe, CartIngredient } from '../types'
import { useRecipesStore } from './recipesStore'

export const useCartStore = defineStore('cart', () => {
  const entries = ref<CartRecipe[]>([])

  function addRecipe(recipeId: string, servings: number) {
    const existing = entries.value.find((e) => e.recipeId === recipeId)
    if (existing) {
      existing.servings = servings
    } else {
      entries.value.push({ recipeId, servings })
    }
  }

  function removeRecipe(recipeId: string) {
    entries.value = entries.value.filter((e) => e.recipeId !== recipeId)
  }

  function clearCart() {
    entries.value = []
  }

  function isInCart(recipeId: string): boolean {
    return entries.value.some((e) => e.recipeId === recipeId)
  }

  const totalItems = computed(() => entries.value.length)

  const mergedIngredients = computed((): CartIngredient[] => {
    const recipesStore = useRecipesStore()
    const map = new Map<string, CartIngredient>()

    for (const entry of entries.value) {
      const recipe = recipesStore.getById(entry.recipeId).value
      if (!recipe) continue
      const factor = entry.servings / recipe.servings

      for (const ing of recipe.ingredients) {
        if (map.has(ing.id)) {
          map.get(ing.id)!.totalAmount += ing.amount * factor
        } else {
          map.set(ing.id, {
            id: ing.id,
            name: ing.name,
            totalAmount: ing.amount * factor,
            baseUnit: ing.baseUnit,
          })
        }
      }
    }

    return Array.from(map.values())
  })

  return { entries, addRecipe, removeRecipe, clearCart, isInCart, totalItems, mergedIngredients }
})
