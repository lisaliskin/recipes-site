<template>
  <div class="recipe-hero">
    <div class="hero-photo">
      <img
        v-if="recipe.photoUrl && !imgMissing"
        :src="recipe.photoUrl"
        :alt="recipe.title"
        class="hero-img"
        @error="imgMissing = true"
      />
      <div v-else class="photo-placeholder hero-img">фото скоро</div>
    </div>

    <div class="hero-info">
      <RouterLink to="/" class="back-link text-label">← назад</RouterLink>
      <span class="section-tag text-label">{{ recipe.section }}</span>
      <h1 class="hero-title text-display">{{ recipe.title }}</h1>
      <p class="hero-desc text-body text-muted">{{ recipe.description }}</p>
      <NutritionBadge :time="recipe.cookingTimeMinutes" :kcal="kcal" />
      <div class="hero-actions">
        <button
          class="btn-add-cart text-label"
          :class="{ 'in-cart': inCart }"
          @click="toggleCart"
        >
          {{ inCart ? '✓ в корзине' : '+ добавить в корзину' }}
        </button>
        <HeartButton :recipe-id="recipe.id" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Recipe } from '../../types'
import { useCartStore } from '../../stores/cartStore'
import { useUiStore } from '../../stores/uiStore'
import NutritionBadge from '../common/NutritionBadge.vue'
import HeartButton from '../common/HeartButton.vue'

const props = defineProps<{ recipe: Recipe; kcal: number }>()

const cartStore = useCartStore()
const uiStore = useUiStore()
const imgMissing = ref(false)

const inCart = computed(() => cartStore.isInCart(props.recipe.id))

function toggleCart() {
  if (inCart.value) {
    cartStore.removeRecipe(props.recipe.id)
  } else {
    cartStore.addRecipe(props.recipe.id, props.recipe.servings)
    uiStore.openCart()
  }
}
</script>

<style scoped>
.recipe-hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: calc(var(--spacing) * 5);
  align-items: start;
  padding: calc(var(--spacing) * 5) 0 calc(var(--spacing) * 6);
}

.hero-photo {
  position: relative;
  overflow: hidden;
  max-height: 600px;
}

.hero-img {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
  object-position: center;
}

.hero-info {
  display: flex;
  flex-direction: column;
  gap: calc(var(--spacing) * 2.5);
  padding-top: calc(var(--spacing) * 2);
}

.back-link {
  display: inline-block;
  opacity: 0.55;
  transition: opacity 0.2s;
}

.back-link:hover {
  opacity: 1;
}

.section-tag {
  color: var(--color-ink-light);
}

.hero-title {
  font-size: clamp(2.5rem, 6vw, 5.5rem);
  line-height: 0.92;
  letter-spacing: -0.03em;
  font-weight: 700;
  text-transform: lowercase;
}

.hero-desc {
  max-width: 380px;
}

.hero-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: calc(var(--spacing) * 1);
  flex-wrap: wrap;
}

.btn-add-cart {
  font-size: 0.6rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 10px 18px;
  border: 1px solid var(--color-ink);
  transition: background 0.2s, color 0.2s;
}

.btn-add-cart:hover,
.btn-add-cart.in-cart {
  background: var(--color-ink);
  color: var(--bg-color);
}

@media (max-width: 768px) {
  .recipe-hero {
    grid-template-columns: 1fr;
  }

  .hero-photo {
    aspect-ratio: 4 / 3;
  }
}
</style>
