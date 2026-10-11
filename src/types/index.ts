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
  // id продукта из каталога (id строки уникален, продукт может повторяться в разных группах)
  productId?: string
  // граммов в одной единице baseUnit (для КБЖУ); нет — считаем как граммы
  gramsPerUnit?: number
  // подзаголовок группы: «для бисквита», «для сиропа»
  group?: string
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
