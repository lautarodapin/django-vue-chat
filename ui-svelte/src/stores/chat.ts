import {writable} from 'svelte/store'
import type {ChatDetail} from '../types'

const search = new URLSearchParams(window.location.search)

export const chatSelected = writable<string>(search.get('chat') || null)