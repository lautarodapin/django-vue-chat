<script lang="ts" setup>


import {chatSelected, websocket} from '../stores'
import {
    Actions,
    MessageDetail,
    Streams,
    WebsocketData,
} from "../types"
import {onMounted, ref} from 'vue'

let sendingMessage = ref(false)
let input: string = ""
let request_id = ref(Date.now())

const listenMessage = (e: MessageEvent) => {
    const {
        stream,
        payload: {action, request_id: id},
    }: WebsocketData<MessageDetail> = JSON.parse(e.data)

    if (
        stream === Streams.Messages &&
        action === Actions.Create &&
        request_id.value === id
    ) {
        input = ""
        request_id.value = Date.now()
        sendingMessage.value = false
    }
}
onMounted(() => {
    websocket.value.addEventListener("message", listenMessage)
    return () => {
        websocket.value.removeEventListener("message", listenMessage)
    }
})

const createMessage = async () => {
    sendingMessage.value = true
    websocket.value.send(
        JSON.stringify({
            stream: Streams.Messages,
            payload: {
                action: Actions.Create,
                request_id,
                data: {
                    text: input,
                    chat: chatSelected.value,
                },
            },
        })
    )
}
</script>

<template>
    <form class="flex" @submit.prevent="(e) => {
        createMessage()
    }">
        <input
            bind:value="{input}"
            type="text"
            class="bg-slate-200 border-slate-400 rounded-md mr-2 grow focus:border-slate-700 border-[.12rem] focus:border-[.2rem] px-2 py-1"
        />
        <button
            type="submit"
            class="px-10 rounded-md bg-slate-700 text-white hover:bg-slate-400 hover:text-black"
            :disabled="sendingMessage"
        >
            <div v-if="!sendingMessage">Send</div>
            <div v-else>Sending . . .</div>
        </button>
    </form>
</template>