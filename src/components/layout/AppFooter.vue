<template>
  <footer class="app-footer">
    <div class="footer-bar">
      <span class="footer-copy text-label text-muted">© {{ year }} lisa liskin · домашняя кухня</span>
      <button class="footer-cta text-label" @click="open = true">заказать план питания</button>
    </div>

    <Transition name="page">
      <div v-if="open" class="plan-overlay" @click.self="close">
        <form class="plan-form" @submit.prevent="submit">
          <button type="button" class="plan-close" aria-label="закрыть" @click="close">✕</button>
          <h2 class="plan-title text-display-sm">план питания</h2>

          <template v-if="sent">
            <p class="text-body">спасибо! я свяжусь с вами в ближайшее время.</p>
            <button type="button" class="plan-submit text-label" @click="close">закрыть</button>
          </template>

          <template v-else>
            <p class="plan-intro text-small text-muted">
              составлю меню на неделю под ваши вкусы и цели. оставьте контакт — я напишу.
            </p>

            <label class="plan-field">
              <span class="text-label">имя</span>
              <input v-model.trim="form.name" required maxlength="100" autocomplete="name" />
            </label>
            <label class="plan-field">
              <span class="text-label">телефон, telegram или email</span>
              <input v-model.trim="form.contact" required maxlength="200" />
            </label>
            <label class="plan-field">
              <span class="text-label">пожелания</span>
              <textarea
                v-model.trim="form.wishes"
                rows="4"
                maxlength="2000"
                placeholder="цель, ограничения, сколько человек, бюджет..."
              />
            </label>

            <p v-if="error" class="plan-error text-small">не получилось отправить, попробуйте ещё раз</p>
            <button type="submit" class="plan-submit text-label" :disabled="sending">
              {{ sending ? 'отправляем...' : 'отправить заявку' }}
            </button>
          </template>
        </form>
      </div>
    </Transition>
  </footer>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { submitMealPlanRequest } from '../../api/directus'

const year = new Date().getFullYear()
const open = ref(false)
const sending = ref(false)
const sent = ref(false)
const error = ref(false)
const form = reactive({ name: '', contact: '', wishes: '' })

async function submit() {
  sending.value = true
  error.value = false
  try {
    await submitMealPlanRequest({ ...form })
    sent.value = true
    Object.assign(form, { name: '', contact: '', wishes: '' })
  } catch {
    error.value = true
  } finally {
    sending.value = false
  }
}

function close() {
  open.value = false
  sent.value = false
  error.value = false
}
</script>

<style scoped>
.app-footer {
  border-top: 1px solid var(--color-border);
}

.footer-bar {
  max-width: var(--max-width);
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  padding: 24px calc(var(--spacing) * 4);
}

.footer-cta {
  font-size: 0.65rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 10px 16px;
  border: 1px solid var(--color-ink);
  transition: background 0.2s, color 0.2s;
}

.footer-cta:hover {
  background: var(--color-ink);
  color: var(--bg-color);
}

.plan-overlay {
  position: fixed;
  inset: 0;
  z-index: 200;
  background: rgba(26, 26, 26, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.plan-form {
  position: relative;
  width: 100%;
  max-width: 440px;
  max-height: 100%;
  overflow-y: auto;
  background: var(--bg-color);
  padding: calc(var(--spacing) * 4);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.plan-close {
  position: absolute;
  top: 12px;
  right: 14px;
  font-size: 0.75rem;
  opacity: 0.6;
}

.plan-close:hover {
  opacity: 1;
}

.plan-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.plan-field input,
.plan-field textarea {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--color-ink);
  background: transparent;
  border: 1px solid var(--color-border);
  padding: 8px 10px;
  outline: none;
  resize: vertical;
}

.plan-field input:focus,
.plan-field textarea:focus {
  border-color: var(--color-ink);
}

.plan-error {
  color: #c0392b;
}

.plan-submit {
  align-self: flex-start;
  font-size: 0.65rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 12px 18px;
  background: var(--color-ink);
  color: var(--bg-color);
}

.plan-submit:disabled {
  opacity: 0.5;
  cursor: default;
}

@media (max-width: 480px) {
  .footer-bar {
    padding: 20px calc(var(--spacing) * 2.5);
  }
}
</style>
