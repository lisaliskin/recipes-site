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
  favorite_seed: number
  photo: string | null
}

interface DirectusProduct {
  id: number
  name: string
  kcal_per_100g: number
  proteins: number
  fats: number
  carbs: number
}

interface DirectusRecipeIngredient {
  id: number
  recipe_id: number
  product_id: number
  amount: number
  base_unit: string
  sort: number
  product?: DirectusProduct
}

interface DirectusStep {
  id: number
  recipe_id: number
  text: string
  sort: number
}

function calcKcalPerServing(
  recipeIngredients: DirectusRecipeIngredient[],
  servings: number,
): number {
  const total = recipeIngredients.reduce((sum, ri) => {
    const kcal = ri.product?.kcal_per_100g ?? 0
    return sum + (ri.amount * kcal) / 100
  }, 0)
  return servings > 0 ? Math.round(total / servings) : 0
}

function toRecipe(
  d: DirectusRecipe,
  recipeIngredients: DirectusRecipeIngredient[],
  steps: DirectusStep[],
): Recipe {
  const sortedIng = [...recipeIngredients].sort((a, b) => a.sort - b.sort)
  const sortedSteps = [...steps].sort((a, b) => a.sort - b.sort)

  return {
    id: d.slug || String(d.id),
    title: d.title,
    section: d.section,
    servings: d.servings,
    cookingTimeMinutes: d.cooking_time_minutes,
    photoUrl: d.photo ? `${BASE_URL}/assets/${d.photo}` : '',
    description: d.description,
    totalKcalPerServing: calcKcalPerServing(sortedIng, d.servings),
    favoriteSeed: d.favorite_seed,
    ingredients: sortedIng.map((ri) => ({
      id: String(ri.product_id),
      name: ri.product?.name ?? '',
      amount: ri.amount,
      baseUnit: ri.base_unit,
      nutrition: {
        kcal: ri.product?.kcal_per_100g ?? 0,
        protein: ri.product?.proteins ?? 0,
        fat: ri.product?.fats ?? 0,
        carbs: ri.product?.carbs ?? 0,
      },
    })),
    steps: sortedSteps.map((s, i) => ({ step: i + 1, text: s.text })),
  }
}

export async function fetchRecipes(): Promise<Recipe[]> {
  const [recipesRes, riRes, productsRes, stepsRes] = await Promise.all([
    fetch(`${BASE_URL}/items/recipes?limit=100&sort=id`),
    fetch(`${BASE_URL}/items/recipe_ingredients?limit=2000&sort=sort`),
    fetch(`${BASE_URL}/items/products?limit=500`),
    fetch(`${BASE_URL}/items/steps?limit=2000&sort=sort`),
  ])

  if (!recipesRes.ok) throw new Error(`Directus error: ${recipesRes.status}`)

  const [recipesJson, riJson, productsJson, stepsJson] = await Promise.all([
    recipesRes.json(),
    riRes.json(),
    productsRes.json(),
    stepsRes.json(),
  ])

  const productsById: Record<number, DirectusProduct> = {}
  for (const p of productsJson.data ?? []) productsById[p.id] = p

  const allRI: DirectusRecipeIngredient[] = (riJson.data ?? []).map(
    (ri: DirectusRecipeIngredient) => ({ ...ri, product: productsById[ri.product_id] }),
  )
  const allSteps: DirectusStep[] = stepsJson.data ?? []

  return (recipesJson.data as DirectusRecipe[]).map((r) =>
    toRecipe(
      r,
      allRI.filter((ri) => ri.recipe_id === r.id),
      allSteps.filter((s) => s.recipe_id === r.id),
    ),
  )
}

export async function fetchRecipeById(id: string): Promise<Recipe | null> {
  const res = await fetch(`${BASE_URL}/items/recipes?filter[slug][_eq]=${id}`)
  if (!res.ok) return null
  const recipe: DirectusRecipe | undefined = (await res.json()).data?.[0]
  if (!recipe) return null

  const [riRes, productsRes, stepsRes] = await Promise.all([
    fetch(`${BASE_URL}/items/recipe_ingredients?filter[recipe_id][_eq]=${recipe.id}&sort=sort&limit=100`),
    fetch(`${BASE_URL}/items/products?limit=500`),
    fetch(`${BASE_URL}/items/steps?filter[recipe_id][_eq]=${recipe.id}&sort=sort&limit=100`),
  ])

  const productsById: Record<number, DirectusProduct> = {}
  for (const p of (await productsRes.json()).data ?? []) productsById[p.id] = p

  const ri: DirectusRecipeIngredient[] = ((await riRes.json()).data ?? []).map(
    (r: DirectusRecipeIngredient) => ({ ...r, product: productsById[r.product_id] }),
  )
  const steps: DirectusStep[] = (await stepsRes.json()).data ?? []

  return toRecipe(recipe, ri, steps)
}
