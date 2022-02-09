<script lang="ts">
  import dayjs from "dayjs";
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";
  import { chatSelected as chatStore } from "../stores/chat";
  import type { ChatDetail, ChatList } from "../types";
  import ChatSideBar from "./ChatSideBar.svelte";
  import GrowingSpinner from "./GrowingSpinner.svelte";
  let chats: ChatList["results"] = [];
  let loading = false;

  onMount(() => {
    getChats();
  });

  const getChats = async () => {
    loading = true;
    const response = await fetch("http://localhost:8000/chats/", {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${localStorage.getItem("token")}`,
      },
    });
    const data: ChatList = await response.json();
    chatStore.update((old) => {
      if (old) return old;
      return data.results[0].id.toString();
    });
    if (data.results)
      chats = data.results.sort((a, b) =>
        dayjs(a.last_message.created_at).isBefore(
          dayjs(b.last_message.created_at)
        )
          ? 1
          : -1
      );
  };

  const handleClick = (chat: ChatDetail) => {
    const searchParams = new URLSearchParams(window.location.search);
    searchParams.set("chat", chat.id.toString());
    history.pushState(
      null,
      "",
      window.location.pathname + "?" + searchParams.toString()
    );
    chatStore.update(() => chat.id.toString());
  };
</script>

{#if !loading}
  <div transition:fade>
    <GrowingSpinner size="16" />
  </div>
{:else}
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
{/if}
