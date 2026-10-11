// Единицы из выпадающего списка в Directus (recipe_ingredients.base_unit).
// Должно совпадать с UNITS в scripts/ingredients-v2.py
export const UNITS = ['г', 'кг', 'мл', 'л', 'шт', 'ст. л.', 'ч. л.', 'стакан', 'щепотка', 'по вкусу'] as const

// Объём в мл для единиц, которые пересчитываются через плотность продукта
const ML: Record<string, number> = {
  'мл': 1,
  'л': 1000,
  'ст. л.': 15,
  'ч. л.': 5,
  'стакан': 250,
}

// Старые варианты написания, которые ещё могут прийти из базы
const ALIASES: Record<string, string> = {
  'гр': 'г',
  'ч.л.': 'ч. л.',
  'ст.л.': 'ст. л.',
  'шт.': 'шт',
}

export function normalizeUnit(unit: string): string {
  const u = (unit ?? '').trim().toLowerCase()
  return ALIASES[u] ?? u
}

export interface UnitWeights {
  gramsPerPiece?: number | null
  density?: number | null
}

// Сколько граммов в одной единице. 0 — пересчитать нельзя (нет веса 1 шт, «по вкусу»)
export function gramsPerUnit(unit: string, w: UnitWeights): number {
  const u = normalizeUnit(unit)
  if (u === 'г') return 1
  if (u === 'кг') return 1000
  if (u === 'шт') return w.gramsPerPiece ?? 0
  if (u === 'щепотка') return 0.5
  if (u in ML) return ML[u] * (w.density || 1)
  return 0
}

export function isToTaste(unit: string): boolean {
  return normalizeUnit(unit) === 'по вкусу'
}
