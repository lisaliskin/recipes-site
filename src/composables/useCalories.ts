import { computed, isRef } from 'vue'
import type { Recipe } from '../types'
import type { ComputedRef, Ref } from 'vue'

export function useCalories(
  recipeOrRef: Recipe | Ref<Recipe> | ComputedRef<Recipe>,
  scaleFactor: ComputedRef<number>,
  scaledServings: ComputedRef<number>,
) {
  const kcalPerServing = computed(() => {
    const recipe = isRef(recipeOrRef) ? recipeOrRef.value : recipeOrRef
    const totalKcal = recipe.ingredients.reduce((sum, ing) => {
      return sum + (ing.amount * scaleFactor.value / 100) * ing.nutrition.kcal
    }, 0)
    return Math.round(totalKcal / (scaledServings.value || 1))
  })

  return { kcalPerServing }
}
