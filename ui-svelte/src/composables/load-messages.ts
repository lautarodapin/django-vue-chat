import { chatSelected } from '../stores/chat';
import type { MessageList } from '../types/index';


export const loadMessages = async (
    url: string,
    loadingCallback: (loading: boolean) => void,
    callback: (data: MessageList, next?: string,) => void,
) => {
    loadingCallback(true)
    const response = await fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${localStorage.getItem("token")}`,
        },
    });
    const data: MessageList = await response.json();
    callback(data, data.next);
    // messages = [...messages, ...data.results];
    // next = data.next;
    loadingCallback(false)
};