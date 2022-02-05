<script lang="ts">
    import { fade } from "svelte/transition";
    import { onDestroy } from "svelte";
    import { chatSelected as chatStore } from "../stores/chat";

    import type { ChatDetail, ChatList } from "../types";
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

    let selectedChat: string;
    let chatsPromise = getChats();
    const unSub = chatStore.subscribe((v) => (selectedChat = v));
    onDestroy(unSub);
</script>

{#await chatsPromise}
    <div transition:fade>
        <GrowingSpinner size="16" />
    </div>
{:then chats}
    {#each chats as chat}
        <div
            transition:fade
            on:click={() => handleClick(chat)}
            class="bg-slate-800 py-8 px-2 hover:bg-slate-300 hover:cursor-pointer"
            class:bg-slate-500={Number(selectedChat) === chat.id}
        >
            {chat.id}
            {#if chat.last_message && chat.last_message.created_by}
                {chat.last_message?.created_by?.username}: {chat.last_message
                    ?.text}
            {/if}
        </div>
    {/each}
{/await}
