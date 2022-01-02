<script setup lang="ts">
const onSubmit = async () => {};
</script>

<template>
  <div>
    <form @submit.prevent="onSubmit">
      <h3>Login</h3>
      <label>Username</label>
      <input type="text" v-model="form.username" />
      <label>Username</label>
      <input type="password" v-model="form.password" />
      <button type="submit">Login!</button>
    </form>
  </div>
</template>