<script lang="ts" setup>
import { defineProps, withDefaults, defineEmits } from "vue";
import { ChatDetail } from "../types";

const emit = defineEmits<{
  (e: "click", id: number): void;
}>();
const props = withDefaults(
  defineProps<{
    chat: ChatDetail;
    selected: boolean;
  }>(),
  {
    selected: false,
  }
);

const onClick = () => emit("click", props.chat.id);
</script>

<template>
  <div
    @click="onClick"
    class="bg-slate-800 py-8 px-2 hover:bg-slate-300 hover:cursor-pointer"
    :class="{ 'bg-slate-500': selected }"
  >
    {{ chat.id }}
  </div>
</template>

