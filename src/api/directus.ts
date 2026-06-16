import type { Recipe, SectionKey } from '../types'

const BASE_URL = 'https://157-180-79-150.sslip.io'

interface DirectusRecipe {
  id: number
  slug: string
  title: string
  section: SectionKey
  servings: number
  cooking_time_minutes: number
  description: string
  total_kcal_per_serving: number
  favorite_seed: number
  photo: string | null
  ingredients: DirectusIngredient[]
  steps: DirectusStep[]
}

interface DirectusIngredient {
  id: number
  ingredient_key: string
  name: string
  amount: number
  base_unit: string
  kcal_per_100g: number
  proteins: number
  fats: number
  carbs: number
  sort: number
}

interface DirectusStep {
  id: number
  text: string
  sort: number
}

function toRecipe(d: DirectusRecipe): Recipe {
  const ingredients = [...(d.ingredients ?? [])].sort((a, b) => a.sort - b.sort)
  const steps = [...(d.steps ?? [])].sort((a, b) => a.sort - b.sort)

  return {
    id: d.slug || String(d.id),
    title: d.title,
    section: d.section,
    servings: d.servings,
    cookingTimeMinutes: d.cooking_time_minutes,
    photoUrl: d.photo ? `${BASE_URL}/assets/${d.photo}` : `/photos/${d.title}.jpg`,
    description: d.description,
    totalKcalPerServing: d.total_kcal_per_serving,
    favoriteSeed: d.favorite_seed,
    ingredients: ingredients.map((ing) => ({
      id: ing.ingredient_key,
      name: ing.name,
      amount: ing.amount,
      baseUnit: ing.base_unit,
      nutrition: {
        kcal: ing.kcal_per_100g,
        protein: ing.proteins,
        fat: ing.fats,
        carbs: ing.carbs,
      },
    })),
    steps: steps.map((s, i) => ({ step: i + 1, text: s.text })),
  }
}

export async function fetchRecipes(): Promise<Recipe[]> {
  const res = await fetch(
    `${BASE_URL}/items/recipes?fields=*,ingredients.*,steps.*&limit=100&sort=id`,
  )
  if (!res.ok) throw new Error(`Directus error: ${res.status}`)
  const json = await res.json()
  return (json.data as DirectusRecipe[]).map(toRecipe)
}

export async function fetchRecipeById(id: string): Promise<Recipe | null> {
  const res = await fetch(
    `${BASE_URL}/items/recipes/${id}?fields=*,ingredients.*,steps.*`,
  )
  if (!res.ok) return null
  const json = await res.json()
  return toRecipe(json.data as DirectusRecipe)
}
