<script lang="ts" setup>
import {chatSelected, messages, websocket} from '../stores'
import {Actions, MessageDetail, Streams, WebsocketData} from '../types'
import {onMounted, ref, watchEffect} from 'vue'
import Message from './Message.vue'
import Input from './Input.vue'

let loading = ref(false)

let timeout = ref<number>()

const listenMessages = (e: MessageEvent) => {
    const {
        stream,
        payload: {action, request_id, data},
    }: WebsocketData<MessageDetail[]> = JSON.parse(e.data)
    if (stream === Streams.Messages && action === Actions.List) {
        messages.value = data
        loading.value = false
    }
}
const listenMessage = (e: MessageEvent) => {
    const {
        stream,
        payload: {action, data},
    }: WebsocketData<MessageDetail> = JSON.parse(e.data)
    if (
        stream === Streams.Chats &&
        action === Actions.Create &&
        data.chat === chatSelected.value
    ) {
        messages.value = [data, ...messages.value]
    }
}
const loadMessages = (chat: number | null) => {
    if (chat === null) return
    loading.value = true
    if (timeout) clearTimeout(timeout.value)
    websocket.value.send(
        JSON.stringify({
            stream: Streams.Messages,
            payload: {
                action: Actions.List,
                filters: {
                    chat__id: chat,
                },
                request_id: Date.now(),
            },
        })
    )
}

watchEffect(() => {
    if (!chatSelected.value) return
    if (websocket.value.readyState === WebSocket.OPEN) loadMessages(chatSelected.value)
    else timeout.value = setTimeout(() => loadMessages(chatSelected.value), 1000)
})

onMounted(() => {
    websocket.value.addEventListener("message", listenMessages)
    websocket.value.addEventListener("message", listenMessage)
    return () => {
        websocket.value.removeEventListener("message", listenMessages)
        websocket.value.removeEventListener("message", listenMessage)
    }
})

watchEffect(() => {
    if (websocket.value.readyState === WebSocket.OPEN)
        loadMessages(chatSelected.value)
    else setTimeout(() => loadMessages(chatSelected.value), 1000)
})
</script>

<template>
    <div v-if="!loading" class="h-[95vh] flex flex-col-reverse">
        <Input />
        <div class="overflow-y-scroll flex flex-col-reverse">
            <Message v-for="message in messages" :key="message.id" :message="message" />
        </div>
    </div>
    <div v-else class="h-[95vh] flex justify-center">
        <div class="flex self-center font-mono">Loading...</div>
    </div>
</template>