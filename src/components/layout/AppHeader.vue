<template>
  <header class="app-header">
    <MarqueeStrip />
    <div class="header-bar">
      <RouterLink to="/" class="header-logo text-label">рецепты</RouterLink>

      <nav class="header-nav text-label">
        <RouterLink to="/" class="nav-link">главная</RouterLink>
        <RouterLink
          to="/favorites"
          class="nav-link fav-link"
          :class="{ 'fav-active': isFavoritesRoute }"
          aria-label="избранное"
        >♥</RouterLink>
        <button class="nav-link cart-btn" @click="uiStore.toggleCart">
          список продуктов
          <span v-if="cartStore.totalItems > 0" class="cart-badge">
            {{ cartStore.totalItems }}
          </span>
        </button>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useCartStore } from '../../stores/cartStore'
import { useUiStore } from '../../stores/uiStore'
import MarqueeStrip from './MarqueeStrip.vue'

const cartStore = useCartStore()
const uiStore = useUiStore()
const route = useRoute()

const isFavoritesRoute = computed(() => route.name === 'favorites')
</script>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 90;
}

.header-bar {
  background: var(--bg-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px calc(var(--spacing) * 4);
  border-bottom: 1px solid var(--color-border);
  transition: background-color 0.8s ease;
}

.header-logo {
  font-size: 0.625rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  font-weight: 700;
  text-decoration: none;
  color: var(--color-ink);
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 28px;
}

.nav-link {
  font-size: 0.625rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--color-ink);
  text-decoration: none;
  transition: opacity 0.2s;
  background: none;
  border: none;
  cursor: pointer;
  font-family: var(--font-mono);
  padding: 0;
  position: relative;
}

.nav-link:hover {
  opacity: 0.55;
}

.fav-link {
  font-size: 1rem;
  letter-spacing: 0;
  line-height: 1;
  transition: color 0.25s, opacity 0.2s;
}

.fav-active {
  color: #c0392b;
  opacity: 1 !important;
}

.fav-active:hover {
  opacity: 0.75 !important;
}

.cart-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
  background: var(--color-ink);
  color: var(--bg-color);
  border-radius: 50%;
  font-size: 0.5rem;
  margin-left: 4px;
  transition: background 0.8s ease, color 0.8s ease;
}

@media (max-width: 480px) {
  .header-bar {
    padding: 14px calc(var(--spacing) * 2.5);
  }
}
</style>
