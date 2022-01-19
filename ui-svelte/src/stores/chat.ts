import {writable} from 'svelte/store'
import type {ChatDetail} from '../types'

export const chatSelected = writable<ChatDetail>(null)