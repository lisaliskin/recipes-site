import { ref, computed } from 'vue'
import type { Recipe } from '../types'

export type ScalingMode = 'servings' | 'ingredient'

export function useIngredientScaling(recipe: Recipe) {
  const mode = ref<ScalingMode>('servings')
  const desiredServings = ref(recipe.servings)
  const anchorIngredientId = ref<string | null>(null)
  const anchorQuantity = ref<number>(0)

  const scaleFactor = computed(() => {
    if (mode.value === 'servings') {
      return desiredServings.value / recipe.servings
    }
    if (!anchorIngredientId.value || anchorQuantity.value === 0) return 1
    const anchor = recipe.ingredients.find((i) => i.id === anchorIngredientId.value)
    if (!anchor) return 1
    return anchorQuantity.value / anchor.amount
  })

  const scaledServings = computed(() => {
    if (mode.value === 'servings') return desiredServings.value
    return Math.round(recipe.servings * scaleFactor.value * 10) / 10
  })

  function formatAmount(amount: number): string {
    const scaled = amount * scaleFactor.value
    if (scaled < 10) return (Math.round(scaled * 10) / 10).toString()
    return Math.round(scaled).toString()
  }

  function setMode(m: ScalingMode) {
    mode.value = m
    if (m === 'ingredient' && !anchorIngredientId.value && recipe.ingredients.length > 0) {
      anchorIngredientId.value = recipe.ingredients[0].id
      anchorQuantity.value = recipe.ingredients[0].amount
    }
  }

  return {
    mode,
    desiredServings,
    anchorIngredientId,
    anchorQuantity,
    scaleFactor,
    scaledServings,
    formatAmount,
    setMode,
  }
}
