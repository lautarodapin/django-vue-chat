<script lang="ts">
  import { fade } from "svelte/transition";

  import { Token } from "../stores/token";
  import { formatDate } from "../utils/index";

  let username: string;
  let password: string;
  let loading: boolean;
  let errors: { username?: string; password?: string; formErrors?: string };
  const onSubmit = async () => {
    loading = true;
    const response = await fetch("http://localhost:8000/users/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    console.log(response.ok);

    if (response.ok) {
      const { token } = data;
      Token.signin(token);
    } else {
      errors = {
        formErrors: data.non_field_errors?.join(", "),
        password: data.password?.join(", "),
        username: data.username?.join(", "),
      };
    }
    loading = false;
  };

  $: console.log(errors);
</script>

<div transition:fade class="h-screen flex items-center justify-center">
  <form on:submit|preventDefault={onSubmit} class="grid grid-cols-1 gap-2">
    <div>
      <label for="username">Username</label>
      <input
        name="username"
        bind:value={username}
        type="text"
        class="w-full min-w-[300px] h-10 focus:border-slate-700 rounded-lg border-slate-400 border-[.12rem] focus:border-[.2rem] px-2 py-2"
      />
      {#if errors?.username}
        <div transition:fade class="text-red-600">{errors.username}</div>
      {/if}
    </div>
    <div>
      <label for="password">Password</label>
      <input
        name="password"
        bind:value={password}
        type="password"
        class="w-full min-w-[300px] h-10 focus:border-slate-700 rounded-lg border-slate-400 border-[.12rem] focus:border-[.2rem] px-2 py-2"
      />
      {#if errors?.password}
        <div transition:fade class="text-red-600">{errors.password}</div>
      {/if}
    </div>
    {#if errors?.formErrors}
      <div transition:fade class="text-red-600">{errors.formErrors}</div>
    {/if}
    <button
      type="submit"
      class="h-10 rounded-md bg-slate-700 text-white hover:bg-slate-400 hover:text-black"
    >
      {#if loading}
        Login...
      {:else}
        Login
      {/if}
    </button>
  </form>
</div>
