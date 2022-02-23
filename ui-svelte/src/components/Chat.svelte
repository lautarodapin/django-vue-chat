<script lang="ts">
    import Message from "./messages/Message.svelte";
    import Input from "./messages/Input.svelte";
    import { fade } from "svelte/transition";
    import { chatSelected, messages } from "../stores";
    import { Actions, MessageDetail, Streams, WebsocketData } from "../types";
    import { getContext, onDestroy, onMount } from "svelte";
    import type { Writable } from "svelte/store";

    let loading = true;
    const ws = getContext<Writable<WebSocket>>("websocket");
    $: websocket = $ws;
    let timeout;

    const listenMessages = (e: MessageEvent) => {
        const {
            stream,
            payload: { action, request_id, data },
        }: WebsocketData<MessageDetail[]> = JSON.parse(e.data);
        if (stream === Streams.Messages && action === Actions.List) {
            messages.set(data);
            loading = false;
        }
    };
    const listenMessage = (e: MessageEvent) => {
        const {
            stream,
            payload: { action, data },
        }: WebsocketData<MessageDetail> = JSON.parse(e.data);
        if (
            stream === Streams.Chats &&
            action === Actions.Create &&
            data.chat === +$chatSelected
        ) {
            messages.update((prev) => [data, ...prev]);
        }
    };
    const loadMessages = (chat: string) => {
        loading = true;
        if (timeout) clearTimeout(timeout);
        websocket.send(
            JSON.stringify({
                stream: Streams.Messages,
                payload: {
                    action: Actions.List,
                    filters: {
                        chat__id: chat,
                    },
                    request_id: Date.now(),
                },
            })
        );
    };

    const unSubChat = chatSelected.subscribe((newChat) => {
        if (!newChat) return;
        if (websocket?.readyState === WebSocket.OPEN) loadMessages(newChat);
        else setTimeout(() => loadMessages(newChat), 1000);
    });

    onMount(() => {
        websocket.addEventListener("message", listenMessages);
        websocket.addEventListener("message", listenMessage);
        return () => {
            websocket.removeEventListener("message", listenMessages);
            websocket.removeEventListener("message", listenMessage);
        };
    });

    $: if (websocket) {
        if (websocket.readyState === WebSocket.OPEN)
            loadMessages($chatSelected);
        else setTimeout(() => loadMessages($chatSelected), 1000);
    }

    onDestroy(() => {
        unSubChat();
    });
    $: console.log("Chat", $messages);
</script>

{#if !loading}
    <div transition:fade class="h-[95vh] flex flex-col-reverse">
        <Input />
        <div class="overflow-y-scroll flex flex-col-reverse">
            {#each $messages as message}
                <Message {message} />
            {:else}
                No messages
            {/each}
        </div>
    </div>
{:else}
    <div transition:fade class="h-[95vh] flex justify-center">
        <div class="flex self-center font-mono">Loading...</div>
    </div>
{/if}
