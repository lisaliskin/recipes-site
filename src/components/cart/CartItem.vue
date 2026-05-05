<template>
  <li class="cart-item" :class="{ checked: isChecked }">
    <button class="check-btn" @click="isChecked = !isChecked" :aria-label="isChecked ? 'снять отметку' : 'отметить'">
      <span class="check-box">{{ isChecked ? '✓' : '' }}</span>
    </button>
    <div class="item-info">
      <span class="item-name text-body" :class="{ 'item-done': isChecked }">{{ item.name }}</span>
      <span class="item-amount text-small text-muted">
        {{ formatAmount(item.totalAmount) }} {{ item.baseUnit }}
      </span>
    </div>
  </li>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { CartIngredient } from '../../types'

defineProps<{ item: CartIngredient }>()

const isChecked = ref(false)

function formatAmount(n: number): string {
  if (n < 10) return (Math.round(n * 10) / 10).toString()
  return Math.round(n).toString()
}
</script>

<style scoped>
.cart-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid var(--color-border);
  transition: opacity 0.2s;
}

.cart-item.checked {
  opacity: 0.45;
}

.check-btn {
  width: 20px;
  height: 20px;
  border: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 0.7rem;
  transition: background 0.15s, border-color 0.15s;
}

.check-btn:hover {
  border-color: var(--color-ink);
}

.cart-item.checked .check-btn {
  background: var(--color-ink);
  color: var(--bg-color);
  border-color: var(--color-ink);
}

.item-info {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  flex: 1;
  gap: 8px;
}

.item-name {
  font-size: 0.8rem;
}

.item-done {
  text-decoration: line-through;
}

.item-amount {
  font-style: italic;
  white-space: nowrap;
  flex-shrink: 0;
}
</style>
