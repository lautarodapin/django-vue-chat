import {writable} from 'svelte/store'
import type {ChatDetail} from '../types'

export const chat = writable<ChatDetail>(null)