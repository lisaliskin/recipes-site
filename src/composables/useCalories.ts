import { computed, isRef } from 'vue'
import type { Recipe } from '../types'
import type { ComputedRef, Ref } from 'vue'

export function useCalories(
  recipeOrRef: Recipe | Ref<Recipe> | ComputedRef<Recipe>,
  scaleFactor: ComputedRef<number>,
  scaledServings: ComputedRef<number>,
) {
  const macros = computed(() => {
    const recipe = isRef(recipeOrRef) ? recipeOrRef.value : recipeOrRef
    const servings = scaledServings.value || 1
    let kcal = 0, protein = 0, fat = 0, carbs = 0
    for (const ing of recipe.ingredients) {
      const a = (ing.amount * scaleFactor.value) / 100
      kcal    += a * ing.nutrition.kcal
      protein += a * ing.nutrition.protein
      fat     += a * ing.nutrition.fat
      carbs   += a * ing.nutrition.carbs
    }
    return {
      kcal:    Math.round(kcal / servings),
      protein: Math.round((protein / servings) * 10) / 10,
      fat:     Math.round((fat / servings) * 10) / 10,
      carbs:   Math.round((carbs / servings) * 10) / 10,
    }
  })

  const kcalPerServing = computed(() => macros.value.kcal)

  return { kcalPerServing, macros }
}
