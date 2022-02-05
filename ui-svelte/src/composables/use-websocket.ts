import { chatSelected } from "../stores/chat";
import type { MessageDetail } from "../types/index";
import { websocket } from '../stores/websocket';

type Props = {
    callback: (data: MessageDetail) => void
    resetMessages: (chat: string) => void
}

export const useWebsocket = ({ callback, resetMessages }: Props) => {
    let chat: string;
    let ws: WebSocket | undefined;

    chatSelected.subscribe((newChat) => {
        if (ws?.readyState === WebSocket.OPEN) unsubscribe(chat)
        chat = newChat
        if (!chat) return
        resetMessages(newChat)
        if (ws?.readyState === WebSocket.OPEN) onOpen()
    })


    const unsubscribe = (chat: string) => {
        console.log("unsubscribe", chat);
        ws?.send(
            JSON.stringify({
                action: "unsubscribe_to_chat",
                id: chat,
                request_id: Math.random(),
            })
        );
    };


    const onMessage = (e: MessageEvent<any>) => {
        const data: MessageDetail = JSON.parse(e.data);
        console.log("ws message", data);
        callback(data);

    };

    const onOpen = () => {
        console.log("ws opened");
        if (!chat) setTimeout(onOpen, 2000);
        ws?.send(
            JSON.stringify({
                action: "subscribe_to_chat",
                id: chat,
                request_id: Math.random(),
            })
        );
        console.log(chat);
    };


    websocket.subscribe((newWs) => {
        ws = newWs;
        ws?.addEventListener("open", onOpen);
        ws?.addEventListener("message", onMessage);
    });

    return { ws, onOpen, onMessage }
}