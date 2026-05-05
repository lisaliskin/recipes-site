<template>
  <section class="author-bio">
    <div class="bio-grid">
      <div class="bio-label">
        <span class="text-label">обо мне</span>
        <SvgIllustration name="sprig" class="bio-illus" />
      </div>

      <div class="bio-content">
        <h2 class="bio-name text-display-md">{{ name }}</h2>
        <div class="bio-text">
          <p class="text-body">
            {{ bio }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import SvgIllustration from '../common/SvgIllustration.vue'

const name = 'lisa liskin'
const bio =
  'кулинарный дневник. здесь я собираю рецепты, которые люблю готовить — простые, сезонные, с хорошими продуктами. верю, что еда должна приносить радость, а не занимать весь день. все рецепты проверены на кухне не один раз.'
</script>

<style scoped>
.author-bio {
  padding: calc(var(--spacing) * 8) 0 calc(var(--spacing) * 6);
  border-top: 1px solid var(--color-border);
}

.bio-grid {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: calc(var(--spacing) * 4);
  align-items: start;
}

.bio-label {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding-top: 6px;
}

.bio-illus {
  width: 40px;
  height: 54px;
  opacity: 0.35;
}

.bio-name {
  margin-bottom: calc(var(--spacing) * 2);
}

.bio-text {
  max-width: 480px;
}

.bio-text p {
  color: var(--color-ink-light);
  font-size: 0.875rem;
  line-height: 1.7;
}

@media (max-width: 640px) {
  .bio-grid {
    grid-template-columns: 1fr;
  }
}
</style>
