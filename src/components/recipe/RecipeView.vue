<template>
  <main v-if="recipe" class="recipe-view">
    <RecipeHero :recipe="recipe" :kcal="kcalPerServing" />

    <div class="recipe-body">
      <div class="recipe-left">
        <ScalingControls
          :recipe="recipe"
          :mode="mode"
          :desired-servings="desiredServings"
          :anchor-ingredient-id="anchorIngredientId"
          :anchor-quantity="anchorQuantity"
          :scale-factor="scaleFactor"
          :scaled-servings="scaledServings"
          @update:mode="mode = $event"
          @update:desired-servings="desiredServings = $event"
          @update:anchor-ingredient-id="anchorIngredientId = $event"
          @update:anchor-quantity="anchorQuantity = $event"
          @set-mode="setModeHandler"
        />
        <IngredientList :recipe="recipe" :format-amount="formatAmount" />
      </div>

      <div class="recipe-right">
        <InstructionSteps :recipe="recipe" />
      </div>
    </div>
  </main>

  <div v-else class="not-found">
    <p class="text-body">рецепт не найден.</p>
    <RouterLink to="/" class="text-label">← на главную</RouterLink>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, watch } from 'vue'
import { getRecipeById } from '../../data/recipes'
import { useIngredientScaling } from '../../composables/useIngredientScaling'
import { useCalories } from '../../composables/useCalories'
import { useUiStore } from '../../stores/uiStore'
import type { ScalingMode } from '../../composables/useIngredientScaling'
import RecipeHero from './RecipeHero.vue'
import ScalingControls from './ScalingControls.vue'
import IngredientList from './IngredientList.vue'
import InstructionSteps from './InstructionSteps.vue'

const props = defineProps<{ id: string }>()
const uiStore = useUiStore()

const recipe = computed(() => getRecipeById(props.id))

const fallbackRecipe = {
  id: '',
  title: '',
  section: 'основное' as const,
  servings: 2,
  cookingTimeMinutes: 0,
  photoUrl: '',
  description: '',
  ingredients: [],
  steps: [],
  totalKcalPerServing: 0,
  favoriteSeed: 0,
}

const activeRecipe = computed(() => recipe.value ?? fallbackRecipe)

const {
  mode,
  desiredServings,
  anchorIngredientId,
  anchorQuantity,
  scaleFactor,
  scaledServings,
  formatAmount,
  setMode,
} = useIngredientScaling(activeRecipe.value)

watch(
  () => props.id,
  () => {
    const r = getRecipeById(props.id)
    if (r) {
      desiredServings.value = r.servings
      mode.value = 'servings'
    }
  },
)

const { kcalPerServing } = useCalories(activeRecipe.value, scaleFactor, scaledServings)

function setModeHandler(m: ScalingMode) {
  setMode(m)
}

onMounted(() => {
  if (recipe.value) {
    uiStore.setActiveSection(recipe.value.section)
  }
})
</script>

<style scoped>
.recipe-view {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 calc(var(--spacing) * 4) calc(var(--spacing) * 10);
}

.recipe-body {
  display: grid;
  grid-template-columns: 1fr 1.4fr;
  gap: calc(var(--spacing) * 6);
  align-items: start;
  padding-top: calc(var(--spacing) * 2);
}

.recipe-left {
  display: flex;
  flex-direction: column;
  gap: calc(var(--spacing) * 4);
  position: sticky;
  top: 160px;
}

.not-found {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: calc(var(--spacing) * 8) calc(var(--spacing) * 4);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

@media (max-width: 900px) {
  .recipe-body {
    grid-template-columns: 1fr;
  }

  .recipe-left {
    position: static;
  }
}

@media (max-width: 480px) {
  .recipe-view {
    padding: 0 calc(var(--spacing) * 2.5) calc(var(--spacing) * 8);
  }
}
</style>
