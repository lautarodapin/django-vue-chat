<script lang="ts">
  import Message from "./messages/Message.svelte";
  import Input from "./messages/Input.svelte";
  import { fade } from "svelte/transition";
  import type { MessageDetail, MessageList } from "../types";
  import { useWebsocket } from "../composables/use-websocket";
  import { chatSelected } from "../stores/chat";
  import { loadMessages } from "../composables/load-messages";

  $: chat = chatSelected;
  let next: string;
  let messages: MessageDetail[] = [];
  let loading: boolean = false;
  let loadingMoreMessages: boolean = false;
  let { ws, onMessage, onOpen } = useWebsocket({
    callback: (message) => {
      messages = [message, ...messages];
    },
    resetMessages: async (newChat) => {
      messages = [];
      await loadMessages(
        `http://localhost:8000/messages/?chat=${newChat}`,
        load
      );
      //   await loadMessages(`http://localhost:8000/messages/?chat=${newChat}`);
    },
  });

  //   const loadMessages = async (
  //     url: string = `http://localhost:8000/messages/?chat=${chat}`
  //   ) => {
  //     loading = true;
  //     loadingMoreMessages = true;
  //     const response = await fetch(url, {
  //       method: "GET",
  //       headers: {
  //         "Content-Type": "application/json",
  //         Authorization: `Token ${localStorage.getItem("token")}`,
  //       },
  //     });
  //     const data: MessageList = await response.json();
  //     messages = [...messages, ...data.results];
  //     next = data.next;
  //     loading = false;
  //     loadingMoreMessages = false;
  //   };
  $: console.log(messages);
</script>

{#if !loading}
  <div transition:fade class="h-[95vh] flex flex-col-reverse">
    <Input />
    <div class="overflow-y-scroll flex flex-col-reverse">
      {#each messages as message}
        <Message {message} />
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
        disabled={loadingMoreMessages}
      >
        {#if !loadingMoreMessages}Load more{:else}Loading. . .{/if}
      </button>
    {/if}
  </div>
{:else}
  Loading...
{/if}
