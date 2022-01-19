<script lang="ts">
    import { onDestroy } from "svelte";

    import { chatSelected } from "../stores/chat";
    import { Token } from "../stores/token";
    import type { ChatDetail, MessageDetail, MessageList } from "../types";

    let input: string;
    let chat: ChatDetail;
    let next: string;
    let messages: MessageDetail[];
    let loading: boolean = false;
    const unChatSelected = chatSelected.subscribe(async (c) => {
        chat = c;
        loading = true;
        const response = await fetch(
            `http://localhost:8000/messages/?chat=${c.id}`,
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Token ${localStorage.getItem("token")}`,
                },
            }
        );
        const data: MessageList = await response.json();
        messages = [...data.results];
        next = data.next;
        loading = false;
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
                chat: chat.id,
            }),
        });
    };

    let ws: WebSocket;

    const unToken = Token.subscribe((t) => {
        console.log("token changed", t);
        const token = localStorage.getItem("token");
        if (token) {
            ws = new WebSocket(`ws://localhost:8000/ws/chats/?token=${token}`);
            ws.onopen = () => {
                console.log("ws opened");
                ws.send(
                    JSON.stringify({
                        action: "subscribe_to_chat",
                        id: chat.id,
                        request_id: Math.random(),
                    })
                );
                console.log(chat.id);
            };
            ws.onmessage = (e) => {
                const data: MessageDetail = JSON.parse(e.data);
                console.log("ws message", data);
                messages = [...messages, data];
            };
        } else if (ws) {
            ws.close();
        }
    });

    onDestroy(() => {
        unToken();
        unChatSelected();
    });
    $: console.log(messages);
</script>

{#if !loading}
    <div class="h-[95vh] flex flex-col-reverse">
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
        {#each messages as { id, created_at, text, created_by: { first_name, last_name, username, email } }}
            <div>
                {created_at} - {username}: {text}
            </div>
        {:else}
            No messages
        {/each}
    </div>
{:else}
    Loading...
{/if}
