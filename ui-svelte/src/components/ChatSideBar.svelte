<script lang="ts">
    import { fade } from "svelte/transition";
    import { useWebsocket } from "../composables/use-websocket";
    import { chatSelected } from "../stores/chat";
    import { websocket } from "../stores/websocket";
    import { Actions, ChatDetail, MessageDetail } from "../types";

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
    $: {
        $websocket?.addEventListener("open", () => {
            console.log("chat side bar open", chat.id);
            $websocket?.send(
                JSON.stringify({
                    action: Actions.SubscribeToChat,
                    id: chat.id,
                    request_id: Math.random(),
                })
            );
        });
        $websocket?.addEventListener("message", (e) => {
            const data: MessageDetail = JSON.parse(e.data);
            if (data.chat !== chat.id) return;
            chat.last_message = data;
        });
    }
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
