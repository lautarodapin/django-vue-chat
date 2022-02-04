<script lang="ts">
  import { fade } from "svelte/transition";
  import type { MessageDetail, MessageList } from "../types";
  import { fromNow } from "../utils";
  import { useWebsocket } from "../composables/use-websocket";

  let input: string;
  let chat: string;
  let next: string;
  let messages: MessageDetail[] = [];
  let loading: boolean = false;
  let sendingMessage: boolean = false;
  let { ws, onMessage, onOpen } = useWebsocket({
    callback: (message) => {
      messages = [message, ...messages];
    },
    resetMessages: async (newChat) => {
      messages = [];
      await loadMessages(`http://localhost:8000/messages/?chat=${newChat}`);
    },
  });

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

  const createMessage = async () => {
    sendingMessage = true;
    try {
      const response = await fetch(`http://localhost:8000/messages/`, {
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
      if (response.ok) {
        input = "";
      }
    } finally {
      sendingMessage = false;
    }
  };

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
        disabled={sendingMessage}
      >
        {#if !sendingMessage}
          Send
        {:else}
          Sending . . .
        {/if}
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
