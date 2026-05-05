export type SectionKey = 'завтраки' | 'закуски' | 'основное' | 'десерты'

export interface NutritionPer100g {
  kcal: number
  protein: number
  fat: number
  carbs: number
}

export interface Ingredient {
  id: string
  name: string
  amount: number
  baseUnit: string
  nutrition: NutritionPer100g
}

export interface InstructionStep {
  step: number
  text: string
}

export interface Recipe {
  id: string
  title: string
  section: SectionKey
  servings: number
  cookingTimeMinutes: number
  photoUrl: string
  description: string
  ingredients: Ingredient[]
  steps: InstructionStep[]
  totalKcalPerServing: number
  favoriteSeed: number
}

export interface CartRecipe {
  recipeId: string
  servings: number
}

export interface CartIngredient {
  id: string
  name: string
  totalAmount: number
  baseUnit: string
}
