<script lang="ts">
    import { createEventDispatcher, getContext, onMount } from "svelte";
    import { fade } from "svelte/transition";
    import { chats, chatSelected, messages } from "../stores";
    import {
        Actions,
        ChatDetail,
        MessageDetail,
        Streams,
        WebsocketData,
    } from "../types";

    export let chat: ChatDetail;
    const websocket = getContext<WebSocket>("websocket");
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
        // TODO setear read count a cero para el nuevo chat
    };

    const listenMessage = (e: MessageEvent) => {
        // TODO mover este listener a un componente de más arriba, sino se repite dos veces 
        const {
            stream,
            payload: { action, data },
        }: WebsocketData<MessageDetail> = JSON.parse(e.data);
        if (
            stream === Streams.Chats &&
            action === Actions.Create &&
            data.chat === +$chatSelected
        ) {
            chats.update((prev) =>
                prev.reduce<typeof prev>((acc, curr) => {
                    if (!curr.hasOwnProperty("unread_count"))
                        curr.unread_count = 0;
                    if (curr.id === data.chat) {
                        curr.last_message = data;
                        curr.unread_count += 1;
                    }
                    acc.push(curr);
                    return acc;
                }, [])
            );
        }
    };
    onMount(() => {
        websocket.addEventListener("message", listenMessage);
        return () => {
            websocket.removeEventListener("message", listenMessage);
        };
    });
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
