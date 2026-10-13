<template>
  <div id="app-root">
    <AppHeader />

    <RouterView v-slot="{ Component }">
      <Transition name="page" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>

    <AppFooter />
    <CartDrawer />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { fetchSiteSettings } from './api/directus'
import AppHeader from './components/layout/AppHeader.vue'
import AppFooter from './components/layout/AppFooter.vue'
import CartDrawer from './components/cart/CartDrawer.vue'

onMounted(async () => {
  const settings = await fetchSiteSettings()
  if (!settings) return
  const root = document.documentElement.style
  // пустое значение в Directus — возвращаемся к цветам из main.css
  if (settings.titleColor) root.setProperty('--title-color', settings.titleColor)
  else root.removeProperty('--title-color')
  if (settings.bgColor) {
    root.setProperty('--bg-color', settings.bgColor)
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', settings.bgColor)
  } else {
    root.removeProperty('--bg-color')
  }
  try {
    localStorage.setItem('siteColors', JSON.stringify(settings))
  } catch {
    // приватный режим — просто без кэша
  }
})
</script>

<style>
/* Page transition */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.2s ease;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
}
</style>
