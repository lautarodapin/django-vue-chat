<script lang="ts">
    import { fade } from "svelte/transition";
    import { useWebsocket } from "../composables/use-websocket";
    import { chatSelected } from "../stores/chat";
    import type { ChatDetail } from "../types";

    export let chat: ChatDetail;

    const handleClick = (chat: ChatDetail) => {
        const searchParams = new URLSearchParams(window.location.search);
        searchParams.set("chat", chat.id.toString());
        history.pushState(
            null,
            "",
            window.location.pathname + "?" + searchParams.toString()
        );
        chatSelected.update(() => chat.id.toString());
    };

    let { ws, onMessage, onOpen } = useWebsocket({
        callback: (message) => {
            if (message.chat !== chat.id) return;
            chat.last_message = message;
            chat = chat;
        },
    });
</script>

<div
    transition:fade
    on:click={() => handleClick(chat)}
    class="bg-slate-800 py-8 px-2 hover:bg-slate-300 hover:cursor-pointer"
    class:bg-slate-500={Number($chatSelected) === chat.id}
>
    {chat.id}
    {#if chat.last_message && chat.last_message.created_by}
        {chat.last_message?.created_by?.username}: {chat.last_message?.text}
    {/if}
</div>
