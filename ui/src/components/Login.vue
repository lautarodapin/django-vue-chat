<script setup lang="ts">
import { reactive } from "vue";
const form = reactive({
  username: "",
  password: "",
});
const onSubmit = async () => {
  console.log(form);
};
</script>

<template>
  <div class="w-full justify-center">
    <form @submit.prevent="onSubmit" class="md:grid">
      <h3 class="col-span-1">Login</h3>
      <div class="col-span-1 justify-center">
        <label>Username</label>
        <input type="text" v-model="form.username" />
      </div>
      <div class="col-span-1">
        <label>Password</label>
        <input type="password" v-model="form.password" />
      </div>
      <button type="submit">Login!</button>
    </form>
  </div>
</template>