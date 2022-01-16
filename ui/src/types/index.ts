export type Pagination<T> = {
    count: number
    next?: string | null
    previous?: string | null
    results: T[]
}

export type ChatDetail = {
    id: number
    name?: string | null
    created_at: string
    mod_at: string
    created_by?: number
    mod_by: number
    users: number[]
    active_users: UserDetail[]
}

export type UserDetail = {
    id: number
    username: string
    first_name: string
    last_name: string
    email: string
    auth_token: Authtoken
}

export type MessageDetail = {
    id: number
    text: string
    chat: number
    created_by?: UserDetail | null
    created_at: string
    mod_at: string
}

export type MessageList = Pagination<MessageDetail>

export type Authtoken = {
    key: string
}