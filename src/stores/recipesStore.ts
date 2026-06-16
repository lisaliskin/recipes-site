import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { fetchRecipes } from '../api/directus'
import type { Recipe, SectionKey } from '../types'

export const useRecipesStore = defineStore('recipes', () => {
  const recipes = ref<Recipe[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const loaded = ref(false)

  async function load() {
    if (loaded.value) return
    loading.value = true
    error.value = null
    try {
      recipes.value = await fetchRecipes()
      loaded.value = true
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Ошибка загрузки'
    } finally {
      loading.value = false
    }
  }

  function getBySection(section: SectionKey) {
    return computed(() => recipes.value.filter((r) => r.section === section))
  }

  function getById(id: string) {
    return computed(() => recipes.value.find((r) => r.id === id) ?? null)
  }

  return { recipes, loading, error, loaded, load, getBySection, getById }
})
