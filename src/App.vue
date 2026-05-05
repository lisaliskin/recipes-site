<template>
  <div id="app-root">
    <AppHeader />

    <RouterView v-slot="{ Component }">
      <Transition name="page" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>

    <CartDrawer />
  </div>
</template>

<script setup lang="ts">
import { watch } from 'vue'
import { useUiStore, SECTION_COLORS } from './stores/uiStore'
import AppHeader from './components/layout/AppHeader.vue'
import CartDrawer from './components/cart/CartDrawer.vue'

const uiStore = useUiStore()

watch(
  () => uiStore.activeSection,
  (section) => {
    const color = section ? SECTION_COLORS[section] : '#f5ecd7'
    document.body.style.setProperty('--bg-color', color)
  },
  { immediate: true },
)
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
