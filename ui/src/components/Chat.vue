<script lang="ts" setup>
import { ref } from "@vue/reactivity";
import { MessageDetail, MessageList } from "../types";

const props = defineProps<{ id?: number }>();
const loading = ref(false);
const messages = ref<MessageDetail[]>([]);
const next = ref("");

const getMessages = async () => {
  loading.value = true;
  try {
    const response = await fetch(
      `http://localhost:8000/messages/?chat=${props.id}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      }
    );
    const data: MessageList = await response.json();
    if (response.ok) {
      messages.value = [...data.results];
      next.value = data.next;
    }
  } finally {
    loading.value = false;
  }
};

getMessages();
</script>

<template>
  <div class="h-screen bg-stone-100">
    <div class="min-h-full flex flex-col-reverse">
      <div class="grid grid-cols-12 gap-1">
        <input type="text" class="bg-slate-200 rounded-md px-2 col-span-10" />
        <button
          class="
            px-10
            rounded-md
            bg-slate-700
            text-white
            hover:bg-slate-400 hover:text-black
            col-span-2
          "
        >
          Send
        </button>
      </div>
      <div v-for="message in messages" :key="message.id">
        {{ message.text }}
      </div>
    </div>
  </div>
</template>