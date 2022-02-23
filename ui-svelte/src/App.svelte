<script lang="ts">
    import { onDestroy, onMount, setContext } from "svelte";
    import { writable } from "svelte/store";
    import Chat from "./components/Chat.svelte";
    import Chats from "./components/Chats.svelte";
    import Login from "./components/Login.svelte";
    import SideBar from "./components/SideBar.svelte";
    import { Token } from "./stores";

    $: token = $Token;
    $: isAuth = !!token;

    let websocket = writable(
        new WebSocket(
            `ws://localhost:8000/ws/?token=${
                localStorage.getItem("token") || ""
            }`
        )
    );

    const unSubToken = Token.subscribe((token) => {
        console.log("App sub token", token, $websocket.readyState);
        if ($websocket.readyState === WebSocket.OPEN) $websocket.close();
        websocket.set(
            new WebSocket(`ws://localhost:8000/ws/?token=${token || ""}`)
        );
    });

    setContext("websocket", websocket);
    onDestroy(() => unSubToken());
</script>

<main>
    <button on:click={() => Token.signout()}>Logout</button>
    <SideBar>
        <Chats />
    </SideBar>
    <div class="pl-64">
        {#if isAuth}
            <Chat />
        {:else}
            <Login />
        {/if}
    </div>
</main>

<style lang="postcss" global>
    @tailwind base;
    @tailwind components;
    @tailwind utilities;
</style>
