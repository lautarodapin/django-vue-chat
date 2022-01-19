<script lang="ts">
    import { onDestroy } from "svelte";
    import { chatSelected as chatStore } from "../stores/chat";

    import type { ChatDetail, ChatList } from "../types";

    const getChats = async () => {
        const response = await fetch("http://localhost:8000/chats/", {
            headers: {
                "Content-Type": "application/json",
                Authorization: `Token ${localStorage.getItem("token")}`,
            },
        });
        const data: ChatList = await response.json();
        chatStore.update(() => data.results[0]);
        return data.results;
    };

    const handleClick = (chat: ChatDetail) => {
        chatStore.update(() => chat);
    };

    let selectedChat: ChatDetail;
    let chatsPromise = getChats();
    const unSub = chatStore.subscribe((v) => (selectedChat = v));
    onDestroy(unSub);
</script>

{#await chatsPromise}
    Loading...
{:then chats}
    {#each chats as chat}
        <div
            on:click={() => handleClick(chat)}
            class="bg-slate-800 py-8 px-2 hover:bg-slate-300 hover:cursor-pointer"
            class:bg-slate-500={selectedChat.id === chat.id}
        >
            {chat.id}
            {#if chat.last_message && chat.last_message.created_by}
                {chat.last_message?.created_by?.username}: {chat.last_message
                    ?.text}
            {/if}
        </div>
    {/each}
{/await}
