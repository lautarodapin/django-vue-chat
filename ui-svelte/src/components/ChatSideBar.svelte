<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { fade } from "svelte/transition";
  import { chatSelected } from "../stores/chat";
  import { websocket } from "../stores/websocket";
  import {
    Actions,
    ChatDetail,
    MessageDetail,
    Streams,
    WebsocketData,
  } from "../types";

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

  const dispatch = createEventDispatcher<{ newMessage: ChatDetail }>();
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
          stream: Streams.Chats,
          payload: {
            action: Actions.SubscribeToChat,
            id: chat.id,
            request_id: Math.random(),
          },
        })
      );
    });
    $websocket?.addEventListener("message", (e) => {
      const response: WebsocketData<MessageDetail> = JSON.parse(e.data);
      console.log("chat side bar message listener", response);
      const {
        stream,
        payload: { action, data },
      } = response;
      if (stream === Streams.Chats && action === Actions.Create) {
        if (data.chat !== chat.id) return;
        chat.last_message = data;
        dispatch("newMessage", chat);
      }
    });
  }
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
