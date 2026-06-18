<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="uiStore.cartOpen" class="cart-overlay" @click="uiStore.closeCart" />
    </Transition>

    <Transition name="cart-slide">
      <aside v-if="uiStore.cartOpen" class="cart-drawer">
        <div class="drawer-header">
          <h2 class="drawer-title text-label">список продуктов</h2>
          <button class="close-btn text-label" @click="uiStore.closeCart">✕</button>
        </div>

        <div v-if="cartStore.entries.length === 0" class="drawer-empty">
          <p class="text-small text-muted">добавьте рецепты, чтобы сформировать список продуктов</p>
        </div>

        <div v-else class="drawer-body">
          <div class="recipes-in-cart">
            <h3 class="section-label text-label">рецепты</h3>
            <ul class="recipes-list">
              <li
                v-for="entry in cartStore.entries"
                :key="entry.recipeId"
                class="recipe-entry text-small"
              >
                <span class="recipe-entry-name">{{ getTitle(entry.recipeId) }}</span>
                <div class="recipe-entry-controls">
                  <span class="text-muted">{{ entry.servings }} порц.</span>
                  <button class="remove-btn text-label" @click="cartStore.removeRecipe(entry.recipeId)">✕</button>
                </div>
              </li>
            </ul>
          </div>

          <div class="ingredients-section">
            <h3 class="section-label text-label">список покупок</h3>
            <ul class="ingredients-list">
              <CartItem
                v-for="item in cartStore.mergedIngredients"
                :key="item.id"
                :item="item"
              />
            </ul>
          </div>
        </div>

        <div v-if="cartStore.entries.length > 0" class="drawer-footer">
          <button class="export-btn text-label" @click="exportList">
            {{ copied ? '✓ скопировано' : 'поделиться списком' }}
          </button>
          <button class="clear-btn text-label" @click="cartStore.clearCart">
            очистить список
          </button>
        </div>
      </aside>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useCartStore } from '../../stores/cartStore'
import { useUiStore } from '../../stores/uiStore'
import { useRecipesStore } from '../../stores/recipesStore'
import CartItem from './CartItem.vue'

const cartStore = useCartStore()
const uiStore = useUiStore()
const recipesStore = useRecipesStore()
const copied = ref(false)

function getTitle(id: string): string {
  return recipesStore.getById(id).value?.title ?? id
}

function buildText(): string {
  const recipes = cartStore.entries
    .map((e) => `${getTitle(e.recipeId)} (${e.servings} порц.)`)
    .join(', ')

  const ingredients = cartStore.mergedIngredients
    .map((i) => `• ${i.name} — ${Math.round(i.totalAmount * 10) / 10} ${i.baseUnit}`)
    .join('\n')

  return `список продуктов\n\nрецепты: ${recipes}\n\n${ingredients}`
}

async function exportList() {
  const text = buildText()
  if (navigator.share) {
    try {
      await navigator.share({ title: 'список продуктов', text })
      return
    } catch {}
  }
  await navigator.clipboard.writeText(text)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}
</script>

<style scoped>
.cart-overlay {
  position: fixed;
  inset: 0;
  background: rgba(26, 26, 26, 0.35);
  z-index: 200;
}

.cart-drawer {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: min(420px, 100vw);
  background: var(--bg-color);
  z-index: 201;
  display: flex;
  flex-direction: column;
  border-left: 1px solid var(--color-border);
}

.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
}

.drawer-title {
  font-size: 0.625rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
}

.close-btn {
  font-size: 0.75rem;
  letter-spacing: 0.1em;
  opacity: 0.55;
  transition: opacity 0.2s;
}

.close-btn:hover {
  opacity: 1;
}

.drawer-empty {
  padding: 40px 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.section-label {
  font-size: 0.6rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--color-ink-light);
  margin-bottom: 10px;
  display: block;
}

.recipes-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.recipe-entry {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid var(--color-border);
  font-size: 0.8rem;
  gap: 12px;
}

.recipe-entry-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recipe-entry-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.remove-btn {
  font-size: 0.6rem;
  opacity: 0.45;
  transition: opacity 0.2s;
}

.remove-btn:hover {
  opacity: 1;
}

.ingredients-list {
  display: flex;
  flex-direction: column;
}

.drawer-footer {
  padding: 16px 24px;
  border-top: 1px solid var(--color-border);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.export-btn {
  font-size: 0.6rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 7px 14px;
  border: 1px solid var(--color-ink);
  background: var(--color-ink);
  color: var(--bg-color);
  cursor: pointer;
  transition: opacity 0.2s;
}

.export-btn:hover {
  opacity: 0.75;
}

.clear-btn {
  font-size: 0.6rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  opacity: 0.55;
  transition: opacity 0.2s;
}

.clear-btn:hover {
  opacity: 1;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.cart-slide-enter-active,
.cart-slide-leave-active {
  transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.cart-slide-enter-from,
.cart-slide-leave-to {
  transform: translateX(100%);
}
</style>
