<script lang="ts" setup>
import { defineProps, withDefaults } from "vue";
import { ChatDetail } from "../types";

// withDefaults(defineProps<{
//   size?: number
//   labels?: string[]
// }>(), {
//   size: 3,
//   labels: () => ['default label']
// })

const { chat, selected } = withDefaults(
  defineProps<{
    chat: ChatDetail;
    selected: boolean;
  }>(),
  {
    selected: false,
  }
);
</script>

<template>
  <div
    class="bg-slate-800 py-8 px-2 hover:bg-slate-300 hover:cursor-pointer"
    :class="{ 'bg-slate-500': selected }"
  >
    {{ chat.id }}
  </div>
</template>

