<script lang="ts">
    import { chatSelected } from "../../stores/chat";
    import { websocket } from "../../stores/websocket";
    import {
        Actions,
        MessageDetail,
        Streams,
        WebsocketData,
    } from "../../types";

    let sendingMessage = false;
    let input: string = "";
    let request_id: number = Math.random();
    $: chat = $chatSelected;

    $: {
        $websocket?.addEventListener("message", (e) => {
            const {
                stream,
                payload: { action, request_id: id },
            }: WebsocketData<MessageDetail> = JSON.parse(e.data);

            if (
                stream === Streams.Messages &&
                action === Actions.Create &&
                request_id === id
            ) {
                input = "";
                request_id = Math.random();
                sendingMessage = false;
            }
        });
    }

    const createMessage = async () => {
        sendingMessage = true;
        $websocket.send(
            JSON.stringify({
                stream: Streams.Messages,
                payload: {
                    action: Actions.Create,
                    request_id,
                    data: {
                        text: input,
                        chat: chat,
                    },
                },
            })
        );
    };
    $: console.log("input", chat);
</script>

<form class="flex" on:submit|preventDefault={(e) => createMessage()}>
    <input
        bind:value={input}
        type="text"
        class="bg-slate-200 border-slate-400 rounded-md mr-2 grow focus:border-slate-700 border-[.12rem] focus:border-[.2rem] px-2 py-1"
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
