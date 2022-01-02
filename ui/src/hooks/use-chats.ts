import {ref} from 'vue'
import {ChatDetail, Pagination} from '../types'

type ChatList = Pagination<ChatDetail>

export const useChats = () => {
    const chats = ref<ChatDetail[]>([])
    const loading = ref(false)

    const fetchChats = async () => {
        loading.value = true
        const token = localStorage.getItem('token')
        const response = await fetch(
            'http://localhost:8000/chats/', {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
            },
        })
        const data: ChatList = await response.json()
        chats.value = data.results
        loading.value = false
    }
    fetchChats()

    return {chats, loading}
}