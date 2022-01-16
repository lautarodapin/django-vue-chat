<script setup lang="ts">
import { ref } from "@vue/reactivity";
import Login from "../src/components/Login.vue";
import SideBar from "../src/components/SideBar.vue";
import SideChat from "../src/components/SideChat.vue";
import Chat from "../src/components/Chat.vue";
import { useChats } from "../src/hooks/use-chats";
const { chats, loading } = useChats();
const selected = ref(4);
const token = localStorage.getItem("token");

const handleSelected = (id: number) => {
  selected.value = id;
  console.log(id);
};
</script>

<template>
  <div>
    <side-bar>
      <side-chat
        v-for="chat in chats"
        :key="chat.id"
        :chat="chat"
        :selected="chat.id === selected"
        @click="handleSelected"
      />
    </side-bar>
    <div class="pl-64">
      <chat :id="selected" />
    </div>
    <!-- <div v-if="!token">
      <login />
    </div>
    <div v-else>
    </div> -->
  </div>
</template>

