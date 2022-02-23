<script lang="ts">
    import { fade } from "svelte/transition";
    import { chats, chatSelected, messages } from "../stores";
    import type { ChatDetail } from "../types";

    export let chat: ChatDetail;
    $: console.log("chat side bar log ", chat);
    $: ({
        id,
        unread_count,
        last_message: {
            text,
            created_by: { username },
        },
    } = chat);

    const handleClick = (chat: ChatDetail) => {
        const searchParams = new URLSearchParams(window.location.search);
        searchParams.set("chat", chat.id.toString());
        history.pushState(
            null,
            "",
            window.location.pathname + "?" + searchParams.toString()
        );
        chatSelected.set(chat.id.toString());
        messages.set([]);
        chats.update((prev) => {
            return prev.map((c) => {
                if (c.id === chat.id) {
                    c.unread_count = 0;
                }
                return c;
            });
        });
    };
</script>

<div
    transition:fade
    on:click={() => handleClick(chat)}
    class="bg-slate-800 py-8 px-2 hover:bg-slate-300 hover:cursor-pointer"
    class:bg-slate-500={Number($chatSelected) === id}
>
    <span class="">
        ({id})
        {#if username}
            {username}: {text}
        {/if}
    </span>
    {#if unread_count && unread_count > 0}
        <span
            class="inline-flex items-center p-1 mr-2 text-[0.625rem] font-semibold text-white bg-red-500 rounded-full"
        >
            {unread_count}
        </span>
    {/if}
</div>
