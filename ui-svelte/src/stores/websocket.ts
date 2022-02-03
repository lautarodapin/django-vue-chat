import {writable} from 'svelte/store'
import {Token} from './token'

export const websocket = writable(new WebSocket(`ws://localhost:8000/ws/chats/?token=${localStorage.getItem('token')}`))

Token.subscribe(() => {
    const token = localStorage.getItem('token')
    if (token && token !== '') {
        websocket.update(() => new WebSocket(`ws://localhost:8000/ws/chats/?token=${token}`))
    }
})
