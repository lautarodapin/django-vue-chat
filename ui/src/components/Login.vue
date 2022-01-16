<script setup lang="ts">
import { reactive, ref } from "vue";

const form = reactive({
  username: "",
  password: "",
});
const loading = ref(false);
const error = ref("");

const onSubmit = async () => {
  loading.value = true;
  try {
    const response = await fetch("http://localhost:8000/users/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form),
    });
    const data = await response.json();
    if (response.ok) {
      const { token } = data;
      localStorage.setItem("token", token);
    } else {
      console.error(data);
      throw new Error("Login failed");
    }
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="flex justify-center h-screen align-middle">
    {{ error }}
    <form @submit.prevent="onSubmit" class="max-w-md flex-row">
      <h3 class="p-2 text-center">Login</h3>
      <div class="p-2">
        <label class="p-1">Username</label>
        <input
          class="bg-slate-200 rounded-md p-2 w-full"
          type="text"
          v-model="form.username"
        />
      </div>
      <div class="p-2">
        <label class="p-1">Password</label>
        <input
          class="bg-slate-200 rounded-md p-2 w-full"
          type="password"
          v-model="form.password"
        />
      </div>
      <div class="p-2">
        <button
          class="
            p-2
            w-full
            rounded-lg
            bg-slate-700
            text-white
            hover:bg-slate-400 hover:text-black
          "
          type="submit"
        >
          Login!
        </button>
      </div>
    </form>
  </div>
</template>