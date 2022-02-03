import {writable} from 'svelte/store'

const token = () => {
    const {subscribe, set} = writable(localStorage.getItem('token') || '')
    return {
        subscribe,
        signout: () => {
            localStorage.removeItem('token')
            set('')
        },
        signin: (token: string) => {
            localStorage.setItem('token', token)
            set(token)
        },
    }
}

export const Token = token()