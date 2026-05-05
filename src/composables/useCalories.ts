import { computed } from 'vue'
import type { Recipe } from '../types'
import type { ComputedRef } from 'vue'

export function useCalories(recipe: Recipe, scaleFactor: ComputedRef<number>, scaledServings: ComputedRef<number>) {
  const kcalPerServing = computed(() => {
    const totalKcal = recipe.ingredients.reduce((sum, ing) => {
      const scaledAmount = ing.amount * scaleFactor.value
      return sum + (scaledAmount / 100) * ing.nutrition.kcal
    }, 0)
    const servings = scaledServings.value || 1
    return Math.round(totalKcal / servings)
  })

  return { kcalPerServing }
}
