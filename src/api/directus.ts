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
  recipe_id: number
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
  recipe_id: number
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
  const [recipesRes, ingredientsRes, stepsRes] = await Promise.all([
    fetch(`${BASE_URL}/items/recipes?limit=100&sort=id`),
    fetch(`${BASE_URL}/items/ingredients?limit=1000&sort=sort`),
    fetch(`${BASE_URL}/items/steps?limit=1000&sort=sort`),
  ])

  if (!recipesRes.ok) throw new Error(`Directus error: ${recipesRes.status}`)

  const [recipesJson, ingredientsJson, stepsJson] = await Promise.all([
    recipesRes.json(),
    ingredientsRes.json(),
    stepsRes.json(),
  ])

  const ingredients: DirectusIngredient[] = ingredientsJson.data ?? []
  const steps: DirectusStep[] = stepsJson.data ?? []

  return (recipesJson.data as DirectusRecipe[]).map((r) => {
    r.ingredients = ingredients.filter((i) => i.recipe_id === r.id)
    r.steps = steps.filter((s) => s.recipe_id === r.id)
    return toRecipe(r)
  })
}

export async function fetchRecipeById(id: string): Promise<Recipe | null> {
  const res = await fetch(`${BASE_URL}/items/recipes?filter[slug][_eq]=${id}`)
  if (!res.ok) return null
  const json = await res.json()
  const recipe = json.data?.[0] as DirectusRecipe | undefined
  if (!recipe) return null

  const [ingRes, stepsRes] = await Promise.all([
    fetch(`${BASE_URL}/items/ingredients?filter[recipe_id][_eq]=${recipe.id}&sort=sort`),
    fetch(`${BASE_URL}/items/steps?filter[recipe_id][_eq]=${recipe.id}&sort=sort`),
  ])

  recipe.ingredients = ingRes.ok ? (await ingRes.json()).data ?? [] : []
  recipe.steps = stepsRes.ok ? (await stepsRes.json()).data ?? [] : []
  return toRecipe(recipe)
}
