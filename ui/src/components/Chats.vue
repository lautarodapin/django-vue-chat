<script lang="ts" setup>
import {onMounted, ref} from "@vue/runtime-core"
import {chats, chatSelected, websocket} from "../stores"
import ChatSideBar from "./ChatSideBar.vue"
import {
    Actions,
    ChatDetail,
    MessageDetail,
    Streams,
    WebsocketData,
} from "../types"

let timeout = ref<number>()
let loading = ref(false)
onMounted(() => {
    console.log("Mount chats")
    websocket.value.addEventListener("message", listenMessage)
    websocket.value.addEventListener("message", onChats)
    return () => {
        websocket.value.removeEventListener("message", listenMessage)
        websocket.value.removeEventListener("message", onChats)
    }
})

const loadChats = () => {
    if (timeout) clearTimeout(timeout.value)
    console.log("loadChats")
    loading.value = true
    websocket.value.send(
        JSON.stringify({
            stream: Streams.Chats,
            payload: {
                action: Actions.List,
                request_id: Date.now(),
            },
        })
    )
}
$: if (websocket) {
    if (websocket.value.readyState === WebSocket.OPEN) loadChats()
    else timeout.value = setTimeout(loadChats, 1000)
}

const listenMessage = (e: MessageEvent) => {
    const {
        stream,
        payload: {action, data},
    }: WebsocketData<MessageDetail> = JSON.parse(e.data)
    if (
        stream === Streams.Chats &&
        action === Actions.Create &&
        data.chat !== chatSelected.value
    ) {
        chats.value = chats.value.reduce<typeof chats.value>((acc, curr) => {
            if (!('unread_count' in curr)) curr.unread_count = 0
            else if (curr.id === data.chat) {
                curr.last_message = data
                curr.unread_count += 1
            }
            acc.push(curr)
            return acc
        }, [])
    }
}

const subscribeToChats = (id: number) => {
    console.log("subscribeToChats")
    websocket.value.send(
        JSON.stringify({
            stream: Streams.Chats,
            payload: {
                action: Actions.SubscribeToChat,
                request_id: Date.now(),
                id,
            },
        })
    )
}

const onChats = (e: MessageEvent) => {
    console.log("onChats")
    const {
        stream,
        payload: {action, data},
    }: WebsocketData<ChatDetail[]> = JSON.parse(e.data)
    if (stream === Streams.Chats && action === Actions.List) {
        chats.value = data
        loading.value = false
        data.forEach(({id}) => subscribeToChats(id))
    }
}
</script>

<template>
    <div v-if="loading">Loading...</div>
    <div v-else>
        <chat-side-bar v-for="chat in chats" :key="chat.id" :chat="chat" />
    </div>
</template>