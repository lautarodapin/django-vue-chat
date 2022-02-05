<script lang="ts">
    import { chatSelected } from "../../stores/chat";

    let sendingMessage = false;
    let input: string = "";
    $: chat = $chatSelected;

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
    $: console.log("input", chat);
</script>

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
