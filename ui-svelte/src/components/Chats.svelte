<script lang="ts">
    import ChatSideBar from "./ChatSideBar.svelte";
    import { chats, chatSelected } from "../stores";
    import {
        Actions,
        ChatDetail,
        MessageDetail,
        Streams,
        WebsocketData,
    } from "../types";
    import { getContext, onMount } from "svelte";
    import type { Writable } from "svelte/store";
    import { fade } from "svelte/transition";
    import GrowingSpinner from "./GrowingSpinner.svelte";

    const ws = getContext<Writable<WebSocket> | undefined>("websocket");
    $: websocket = $ws;
    let timeout;
    let loading = false;
    onMount(() => {
        console.log("Mount chats");
        websocket.addEventListener("message", listenMessage);
        websocket.addEventListener("message", onChats);
        return () => {
            websocket.removeEventListener("message", listenMessage);
            websocket.removeEventListener("message", onChats);
        };
    });

    $: if (websocket) {
        if (websocket.readyState === WebSocket.OPEN) loadChats();
        else timeout = setTimeout(loadChats, 1000);
    }

    const listenMessage = (e: MessageEvent) => {
        const {
            stream,
            payload: { action, data },
        }: WebsocketData<MessageDetail> = JSON.parse(e.data);
        if (
            stream === Streams.Chats &&
            action === Actions.Create &&
            data.chat !== +$chatSelected
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

    const loadChats = () => {
        if (timeout) clearTimeout(timeout);
        console.log("loadChats");
        loading = true;
        websocket.send(
            JSON.stringify({
                stream: Streams.Chats,
                payload: {
                    action: Actions.List,
                    request_id: Date.now(),
                },
            })
        );
    };

    const subscribeToChats = (id: number) => {
        console.log("subscribeToChats");
        websocket.send(
            JSON.stringify({
                stream: Streams.Chats,
                payload: {
                    action: Actions.SubscribeToChat,
                    request_id: Date.now(),
                    id,
                },
            })
        );
    };

    const onChats = (e: MessageEvent) => {
        console.log("onChats");
        const {
            stream,
            payload: { action, data },
        }: WebsocketData<ChatDetail[]> = JSON.parse(e.data);
        if (stream === Streams.Chats && action === Actions.List) {
            chats.set(data);
            loading = false;
            data.forEach(({ id }) => subscribeToChats(id));
        }
    };
</script>

{#if loading}
    Loading...
{:else}
    {#each $chats as chat}
        <ChatSideBar {chat} />
    {/each}
{/if}
