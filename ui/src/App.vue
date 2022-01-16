<script setup lang="ts">
import { ref } from "@vue/reactivity";
import Login from "../src/components/Login.vue";
import SideBar from "../src/components/SideBar.vue";
import SideChat from "../src/components/SideChat.vue";
import { useChats } from "../src/hooks/use-chats";
const { chats, loading } = useChats();
const selected = ref(4);
</script>

<template>
  <div>
    <side-bar>
      <side-chat
        v-for="chat in chats"
        :key="chat.id"
        :chat="chat"
        :selected="chat.id === selected"
      />
    </side-bar>
    <!-- <div v-if="!token">
      <login />
    </div>
    <div v-else>
    </div> -->
  </div>
</template>

