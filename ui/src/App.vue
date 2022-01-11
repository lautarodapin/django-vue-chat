<script setup lang="ts">
import Login from "../src/components/Login.vue";
import { useChats } from "../src/hooks/use-chats";
const { chats, loading } = useChats();
const token = localStorage.getItem("token");
</script>

<template>
  <div>
    <div v-if="!token">
      <Login />
    </div>
    <div v-else>
      <div v-if="loading">Loading...</div>
      <div v-if="!loading">
        <h1 class="text-3xl font-bold first-letter:capitalize">
          ahasello world!
        </h1>
        <div v-for="chat in chats" :key="chat.id">
          {{ chat }}
          <br />
        </div>
      </div>
    </div>
  </div>
</template>

