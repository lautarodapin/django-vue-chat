export enum Actions {
    SubscribeToChat = "subscribe_to_chat",
    UnsubscribeToChat = "unsubscribe_to_chat",
    Create = "create",
    List = "list"
}

export enum Streams {
    Chats = "chats",
    Messages = "messages",
    Users = "users",
}

export type WebsocketData<T> = {
    stream: Streams
    payload: {
        action: Actions
        request_id: number
        response_status: number
        errors: any[]
        data: T
    }
}

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
    last_message?: MessageDetail
    unread_count: number
}

export type ChatList = Pagination<ChatDetail>

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
    created_by?: UserDetail
    created_at: string
    mod_at: string
    read: boolean
}

export type MessageList = Pagination<MessageDetail>

export type Authtoken = {
    key: string
}