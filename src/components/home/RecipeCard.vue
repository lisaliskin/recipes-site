<template>
  <article class="recipe-card" @click="navigate">
    <div class="card-photo">
      <img
        v-if="recipe.photoUrl"
        :src="recipe.photoUrl"
        :alt="recipe.title"
        class="card-img"
        loading="lazy"
        @error="onImgError"
      />
      <div v-if="imgMissing || !recipe.photoUrl" class="photo-placeholder card-img">
        фото
      </div>
    </div>

    <div class="card-body">
      <h3 class="card-title text-display-sm">{{ recipe.title }}</h3>
      <p class="card-desc text-small text-muted">{{ recipe.description }}</p>

      <div class="card-meta">
        <NutritionBadge :time="recipe.cookingTimeMinutes" :kcal="recipe.totalKcalPerServing" />
        <div class="card-actions">
          <button
            class="btn-cart text-label"
            :class="{ 'in-cart': inCart }"
            @click.stop="toggleCart"
          >
            {{ inCart ? '✓ в корзине' : '+ корзина' }}
          </button>
          <HeartButton :recipe-id="recipe.id" />
        </div>
      </div>
    </div>
  </article>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import type { Recipe } from '../../types'
import { useCartStore } from '../../stores/cartStore'
import { useUiStore } from '../../stores/uiStore'
import NutritionBadge from '../common/NutritionBadge.vue'
import HeartButton from '../common/HeartButton.vue'

const props = defineProps<{ recipe: Recipe }>()

const router = useRouter()
const cartStore = useCartStore()
const uiStore = useUiStore()
const imgMissing = ref(false)

const inCart = computed(() => cartStore.isInCart(props.recipe.id))

function navigate() {
  router.push({ name: 'recipe', params: { id: props.recipe.id } })
}

function toggleCart() {
  if (inCart.value) {
    cartStore.removeRecipe(props.recipe.id)
  } else {
    cartStore.addRecipe(props.recipe.id, props.recipe.servings)
    uiStore.openCart()
  }
}

function onImgError() {
  imgMissing.value = true
}
</script>

<style scoped>
.recipe-card {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--color-border);
  transition: border-color 0.2s, transform 0.2s;
  overflow: hidden;
}

.recipe-card:hover {
  border-color: var(--color-ink);
  transform: translateY(-2px);
}

.card-photo {
  position: relative;
  aspect-ratio: 4 / 3;
  overflow: hidden;
  background: rgba(26, 26, 26, 0.06);
}

.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.recipe-card:hover .card-img {
  transform: scale(1.04);
}

.card-body {
  padding: calc(var(--spacing) * 2.5);
  display: flex;
  flex-direction: column;
  gap: calc(var(--spacing) * 1.5);
  flex: 1;
}

.card-title {
  font-size: clamp(1rem, 2.5vw, 1.35rem);
  line-height: 1.05;
  letter-spacing: -0.02em;
  font-weight: 700;
  text-transform: lowercase;
}

.card-desc {
  font-size: 0.75rem;
  color: var(--color-ink-light);
  line-height: 1.5;
}

.card-meta {
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-cart {
  font-size: 0.6rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 5px 8px;
  border: 1px solid var(--color-border);
  transition: background 0.2s, color 0.2s, border-color 0.2s;
  white-space: nowrap;
}

.btn-cart:hover,
.btn-cart.in-cart {
  background: var(--color-ink);
  color: var(--bg-color);
  border-color: var(--color-ink);
}
</style>
