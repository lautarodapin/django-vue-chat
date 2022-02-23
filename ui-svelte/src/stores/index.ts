
import {writable} from 'svelte/store'
import type {ChatDetail, MessageDetail, UserDetail} from '../types'

const search = new URLSearchParams(window.location.search)
export const chatSelected = writable<string>(search.get('chat') || null)
export const Token = (() => {
    const {subscribe, set} = writable(localStorage.getItem('token') || '')
    return {
        subscribe,
        signout: () => {
            localStorage.removeItem('token')
            history.pushState(null, "", window.location.pathname)
            set('')
        },
        signin: (token: string) => {
            localStorage.setItem('token', token)
            set(token)
        },
    }
})()
export const messages = writable<MessageDetail[]>([])
export const chats = writable<ChatDetail[]>([])
export const user = writable<Omit<UserDetail, 'auth_token'> | undefined>()