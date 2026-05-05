import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { SectionKey } from '../types'

export const SECTION_COLORS: Record<SectionKey, string> = {
  завтраки: '#F5ECD7',
  закуски: '#D4E6C3',
  основное: '#E8C4B0',
  десерты: '#F0D4D4',
}

export const useUiStore = defineStore('ui', () => {
  const activeSection = ref<SectionKey | null>(null)
  const cartOpen = ref(false)

  function setActiveSection(section: SectionKey | null) {
    activeSection.value = section
  }

  function openCart() {
    cartOpen.value = true
  }

  function closeCart() {
    cartOpen.value = false
  }

  function toggleCart() {
    cartOpen.value = !cartOpen.value
  }

  return { activeSection, cartOpen, setActiveSection, openCart, closeCart, toggleCart }
})
