<script lang="ts">
    import { fade } from "svelte/transition";
    import { useWebsocket } from "../composables/use-websocket";
    import { chatSelected as chatStore } from "../stores/chat";
    import type { ChatDetail, ChatList } from "../types";
    import ChatSideBar from "./ChatSideBar.svelte";
    import GrowingSpinner from "./GrowingSpinner.svelte";

    const getChats = async () => {
        const response = await fetch("http://localhost:8000/chats/", {
            headers: {
                "Content-Type": "application/json",
                Authorization: `Token ${localStorage.getItem("token")}`,
            },
        });
        const data: ChatList = await response.json();
        chatStore.update((old) => {
            if (old) return old;
            return data.results[0].id.toString();
        });
        return data.results;
    };

    const handleClick = (chat: ChatDetail) => {
        const searchParams = new URLSearchParams(window.location.search);
        searchParams.set("chat", chat.id.toString());
        history.pushState(
            null,
            "",
            window.location.pathname + "?" + searchParams.toString()
        );
        chatStore.update(() => chat.id.toString());
    };

    $: selectedChat = $chatStore;
    let chatsPromise = getChats();
</script>

{#await chatsPromise}
    <div transition:fade>
        <GrowingSpinner size="16" />
    </div>
{:then chats}
    {#each chats as chat}
        <ChatSideBar {chat} />
    {/each}
{/await}
