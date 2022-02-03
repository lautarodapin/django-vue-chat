<script lang="ts">
  import { fade } from "svelte/transition";
  import { onDestroy } from "svelte";

  import { chatSelected } from "../stores/chat";
  import { Token } from "../stores/token";
  import { websocket } from "../stores/websocket";
  import type { ChatDetail, MessageDetail, MessageList } from "../types";
  import { formatDate, fromNow } from "../utils";

  let input: string;
  let chat: string;
  let next: string;
  let messages: MessageDetail[] = [];
  let loading: boolean = false;
  let ws: WebSocket | undefined;

  const loadMessages = async (
    url: string = `http://localhost:8000/messages/?chat=${chat}`
  ) => {
    loading = true;
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${localStorage.getItem("token")}`,
      },
    });
    const data: MessageList = await response.json();
    messages = [...messages, ...data.results];
    next = data.next;
    loading = false;
  };
  const unChatSelected = chatSelected.subscribe(async (newChat) => {
    if (ws?.readyState === WebSocket.OPEN) unsubscribe();
    chat = newChat;
    if (!chat) return;
    messages.splice(0, messages.length);
    messages = messages;
    await loadMessages(`http://localhost:8000/messages/?chat=${newChat}`);
    if (ws?.readyState === WebSocket.OPEN) onOpen();
  });

  const createMessage = async () => {
    await fetch(`http://localhost:8000/messages/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({
        text: input,
        chat: chat,
      }),
    });
    input = "";
  };

  const onOpen = () => {
    console.log("ws opened");
    if (!chat) setTimeout(onOpen, 2000);
    ws?.send(
      JSON.stringify({
        action: "subscribe_to_chat",
        id: chat,
        request_id: Math.random(),
      })
    );
    console.log(chat);
  };

  const unsubscribe = () => {
    console.log("unsubscribe", chat);
    ws?.send(
      JSON.stringify({
        action: "unsubscribe_to_chat",
        id: chat,
        request_id: Math.random(),
      })
    );
  };

  const onMessage = (e: MessageEvent<any>) => {
    const data: MessageDetail = JSON.parse(e.data);
    console.log("ws message", data);
    console.log("old messages", messages);
    messages = [data, ...messages];
  };

  websocket.subscribe((newWs) => {
    ws = newWs;
    ws?.addEventListener("open", onOpen);
    ws?.addEventListener("message", onMessage);
  });

  onDestroy(() => {
    // unToken();
    unChatSelected();
  });
  $: console.log(messages);
</script>

{#if !loading}
  <div transition:fade class="h-[95vh] flex flex-col-reverse">
    <form class="flex" on:submit|preventDefault={(e) => createMessage()}>
      <input
        bind:value={input}
        type="text"
        class="bg-slate-200 rounded-md px-2 mr-2 grow"
      />
      <button
        type="submit"
        class="
                    px-10
                    rounded-md
                    bg-slate-700
                    text-white
                    hover:bg-slate-400 hover:text-black
                "
      >
        Send
      </button>
    </form>
    <div class="overflow-y-scroll flex flex-col-reverse">
      {#each messages as { id, created_at, text, created_by: { first_name, last_name, username, email } }}
        <div transition:fade>
          {fromNow(created_at)} - {username}: {text}
        </div>
      {:else}
        No messages
      {/each}
    </div>
    {#if next}
      <button
        class="
                    px-10
                    rounded-md
                    bg-slate-700
                    text-white
                    hover:bg-slate-400 hover:text-black
                "
        on:click={() => loadMessages(next)}
      >
        Load more
      </button>
    {/if}
  </div>
{:else}
  Loading...
{/if}
