<script lang="ts">
  import { fade } from "svelte/transition";
  import dayjs from "dayjs";
  import { websocket } from "../stores/websocket";
  import { ChatList, Streams } from "../types/index";
  import GrowingSpinner from "./GrowingSpinner.svelte";
  import ChatSideBar from "./ChatSideBar.svelte";
  import { chatSelected as chatStore } from "../stores/chat";
  let chats: ChatList["results"] = [];
  let loading = false;
  $: {
    $websocket?.addEventListener("open", () => {
      loading = true;
      $websocket.send(
        JSON.stringify({
          stream: Streams.Chats,
          payload: {
            action: "list",
            request_id: Math.random(),
          },
        })
      );
    });

    $websocket?.addEventListener("message", (e) => {
      const data = JSON.parse(e.data);
      console.log("chats event listener", data);
      if (data.stream === Streams.Chats) {
        if (data.payload.action === "list") {
          chats = data.payload.data.sort((a, b) =>
            dayjs(a.last_message.created_at).isBefore(
              dayjs(b.last_message.created_at)
            )
              ? 1
              : -1
          );
          loading = false;
          chatStore.update((old) => {
            if (old) return old;
            return chats[0].id.toString();
          });
        }
      }
    });
  }

  $: console.log("chats log", chats, loading);
</script>

<!-- {#if !loading}
  Loading...
  <div transition:fade>
    <GrowingSpinner size="16" />
  </div>
{:else} -->
{#each chats as chat}
  <ChatSideBar
    {chat}
    on:newMessage={({ detail: chat }) => {
      chats = chats
        .map((c) => (c.id === chat.id ? { ...chat } : c))
        .sort((a, b) =>
          dayjs(a.last_message.created_at).isBefore(
            dayjs(b.last_message.created_at)
          )
            ? 1
            : -1
        );
    }}
  />
{/each}
<!-- {/if} -->
