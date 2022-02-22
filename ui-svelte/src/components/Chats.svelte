<script lang="ts">
    import ChatSideBar from "./ChatSideBar.svelte";
    import { chats } from "../stores";
    import { Actions, ChatDetail, Streams, WebsocketData } from "../types";
    import { getContext, onMount } from "svelte";

    const websocket = getContext<WebSocket>("websocket");
    let timeout;
    onMount(() => {
        console.log("Mount chats");
        websocket.addEventListener("message", onChats);
        if (websocket.readyState === WebSocket.OPEN) loadChats();
        else timeout = setTimeout(loadChats, 1000);
        return () => {
            websocket.removeEventListener("message", onChats);
        };
    });

    const loadChats = () => {
        if (timeout) clearTimeout(timeout);
        console.log("loadChats");
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
            data.forEach(({ id }) => subscribeToChats(id));
        }
    };
</script>

<!-- svelte-ignore missing-declaration -->
<!-- {#if !loading}
  Loading...
  <div transition:fade>
    <GrowingSpinner size="16" />
  </div>
{:else} -->
{#each $chats as chat}
    <ChatSideBar {chat} />
{/each}
<!-- {/if} -->
<!-- on:newMessage={({ detail: chat }) => {
            chats = chats
                .map((c) => (c.id === chat.id ? { ...chat } : c))
                .sort((a, b) =>
                    dayjs(a.last_message.created_at).isBefore(
                        dayjs(b.last_message.created_at)
                    )
                        ? 1
                        : -1
                );
        }} -->
