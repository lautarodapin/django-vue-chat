import {writable} from 'svelte/store'

const token = () => {
    const {subscribe, set} = writable(localStorage.getItem('token') || '')
    return {
        subscribe,
        signout: () => {
            localStorage.removeItem('token')
            set(null)
        },
        signin: () => {
            set(localStorage.getItem('token'))
        },
    }
}

export const Token = token()