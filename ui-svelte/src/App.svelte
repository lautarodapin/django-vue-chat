<script lang="ts">
    import { onDestroy, onMount } from "svelte";
    import Chats from "./components/Chats.svelte";
    import Login from "./components/Login.svelte";
    import SideBar from "./components/SideBar.svelte";
    import { Token } from "./stores/token";

    let token: string;
    let ws: WebSocket;
    const unToken = Token.subscribe((t) => {
        token = t;
        console.log("token changed", t);
        if (t) {
            ws = new WebSocket(`ws://localhost:8000/ws/chats/?token=${t}`);
        } else if (ws) {
            ws.close();
        }
    });
    onDestroy(() => {
        unToken();
    });
    $: isAuth = !!token;
</script>

<main>
    {#if isAuth}
        <button on:click={() => Token.signout()}>Logout</button>
        <SideBar>
            <Chats />
        </SideBar>
    {:else}
        <Login />
    {/if}
</main>

<style lang="postcss" global>
    @tailwind base;
    @tailwind components;
    @tailwind utilities;
</style>
