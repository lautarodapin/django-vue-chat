import {onBeforeUnmount, onMounted, ref} from 'vue'
const token = ref(localStorage.getItem('token'))
const ws = ref(new WebSocket(`ws://localhost:8000/ws/chats/?token=${token.value}`))

export const useWs = () => {

    const tokenListener = (e: StorageEvent) => {
        if (e.key === 'token' && e.newValue !== '' && e.newValue !== null) {
            token.value = e.newValue
            ws.value = new WebSocket(`ws://localhost:8000/ws/chats/?token=${token.value}`)
        }
    }
    onMounted(() => {
        addEventListener('storage', tokenListener)
    })

    onBeforeUnmount(() => {
        removeEventListener('storage', tokenListener)
    })
    return {ws}
}