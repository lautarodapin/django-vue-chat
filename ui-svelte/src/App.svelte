<script lang="ts">
    import { onDestroy, onMount } from "svelte";
    import Chat from "./components/Chat.svelte";
    import Chats from "./components/Chats.svelte";
    import Login from "./components/Login.svelte";
    import SideBar from "./components/SideBar.svelte";
    import { Token } from "./stores/token";

    $: token = $Token;
    $: isAuth = !!token;
</script>

<main>
    {#if isAuth}
        <button on:click={() => Token.signout()}>Logout</button>
        <SideBar>
            <Chats />
        </SideBar>
        <div class="pl-64">
            <Chat />
        </div>
    {:else}
        <Login />
    {/if}
</main>

<style lang="postcss" global>
    @tailwind base;
    @tailwind components;
    @tailwind utilities;
</style>
