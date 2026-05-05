<template>
  <span class="svg-illustration" v-html="svgContent" />
</template>

<script setup lang="ts">
import { computed } from 'vue'

import SprigSvg from '../../assets/illustrations/sprig.svg?raw'
import LeafSvg from '../../assets/illustrations/leaf.svg?raw'
import ForkSvg from '../../assets/illustrations/fork.svg?raw'
import BowlSvg from '../../assets/illustrations/bowl.svg?raw'

const SVG_MAP: Record<string, string> = {
  sprig: SprigSvg,
  leaf: LeafSvg,
  fork: ForkSvg,
  bowl: BowlSvg,
}

const props = defineProps<{ name: string }>()

const svgContent = computed(() => SVG_MAP[props.name] ?? '')
</script>

<style scoped>
.svg-illustration {
  display: inline-block;
  color: currentColor;
}

.svg-illustration :deep(svg) {
  width: 100%;
  height: 100%;
  stroke: currentColor;
}
</style>
