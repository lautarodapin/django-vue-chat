<script lang="ts" setup>
import {chatSelected, messages, chats} from '../stores'
import {ChatDetail} from "../types"

const props = defineProps<{
    chat: ChatDetail
}>()

const {
    chat: {
        id,
        last_message: {
            created_by,
            text,
        } = {},
        unread_count,
    },
} = props

const handleClick = (chat: ChatDetail) => {
    const searchParams = new URLSearchParams(window.location.search)
    searchParams.set("chat", chat.id.toString())
    history.pushState(
        null,
        "",
        window.location.pathname + "?" + searchParams.toString()
    )
    chatSelected.value = chat.id
    messages.value = []
    chats.value = chats.value.map(c => {
        if (c.id === chat.id) {
            c.unread_count = 0
        }
        return c
    })
}
</script>
<template>
    <div
        @click.prevent="() => handleClick(chat)"
        class="bg-slate-800 py-8 px-2 hover:bg-slate-300 hover:cursor-pointer"
        :class="{'bg-slate-500': chatSelected === id}"
    >
        <span class>({{id}}) {{created_by?.username}}: {{text}}</span>
        <span
            v-if="unread_count > 0"
            class="inline-flex items-center p-1 mr-2 text-[0.625rem] font-semibold text-white bg-red-500 rounded-full"
        >{{unread_count}}</span>
    </div>
</template>