<script lang="ts">
    import Message from "./messages/Message.svelte";
    import Input from "./messages/Input.svelte";
    import { fade } from "svelte/transition";
    import type { MessageDetail } from "../types";
    import { useWebsocket } from "../composables/use-websocket";
    import { chatSelected } from "../stores/chat";
    import { loadMessages } from "../composables/load-messages";

    $: chat = chatSelected;
    let next: string;
    let messages: MessageDetail[] = [];
    let loading: boolean = false;
    let loadingMoreMessages: boolean = false;

    const load = async (
        url: string = `http://localhost:8000/messages/?chat=${chat}`
    ) => {
        await loadMessages(
            url,
            (load) => {
                console.log("loading", load);
                loading = load;
                loadingMoreMessages = load;
            },
            (data) => {
                console.log("data", data);
                console.log("old messages", messages);
                messages = [...messages, ...data.results];
                console.log("new messages", messages);
                next = data.next;
            }
        );
    };
    let { ws, onMessage, onOpen } = useWebsocket({
        callback: (message) => {
            if (message.chat !== parseInt($chat)) return;
            messages = [message, ...messages];
        },
        resetMessages: async (newChat) => {
            messages = [];
            await load(`http://localhost:8000/messages/?chat=${newChat}`);
        },
    });

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
                on:click={() => load(next)}
                disabled={loadingMoreMessages}
            >
                {#if !loadingMoreMessages}Load more{:else}Loading. . .{/if}
            </button>
        {/if}
    </div>
{:else}
    Loading...
{/if}
