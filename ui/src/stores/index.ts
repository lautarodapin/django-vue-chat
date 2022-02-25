import {ChatDetail, MessageDetail} from '@/types'
import {ref} from 'vue'
const chat = new URLSearchParams(window.location.search).get('chat')
export const token = ref<string | undefined | null>(localStorage.getItem('token') || null)
export const websocket = ref<WebSocket>(new WebSocket('ws://localhost:8000/ws/?token=' + token.value))
export const chatSelected = ref<number | null>(chat ? parseInt(chat) : null)
export const chats = ref<ChatDetail[]>([])
export const messages = ref<MessageDetail[]>([])