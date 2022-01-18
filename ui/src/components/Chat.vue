<script lang="ts" setup>
    import { ref, onMounted, watch } from "vue";
    import { MessageDetail, MessageList } from "../types";
    import { useWs } from "../hooks/use-ws";

    const props = defineProps<{ id?: number }>();
    const loading = ref(false);
    const messages = ref<MessageDetail[]>([]);
    const input = ref("");
    const next = ref("");
    const { ws } = useWs();

    watch(
        () => props.id,
        (newId, oldId) => {
            ws.value.onmessage = (event) => {
                console.log(event);
                const data: MessageDetail = JSON.parse(event.data);
                console.log(data);
                messages.value.push(data);
            };
            console.log("watch", oldId, newId);
            if (newId) {
                if (ws.value.readyState !== WebSocket.OPEN) {
                    ws.value.onopen = () => {
                        if (oldId) {
                            ws.value.send(
                                JSON.stringify({
                                    action: "unsubscribe_to_chat",
                                    id: oldId,
                                    request_id: Math.random(),
                                })
                            );
                        }
                        ws.value.send(
                            JSON.stringify({
                                action: "subscribe_to_chat",
                                id: newId,
                                request_id: Math.random(),
                            })
                        );
                    };
                } else {
                    if (oldId) {
                        ws.value.send(
                            JSON.stringify({
                                action: "unsubscribe_to_chat",
                                id: oldId,
                                request_id: Math.random(),
                            })
                        );
                    }
                    ws.value.send(
                        JSON.stringify({
                            action: "subscribe_to_chat",
                            id: newId,
                            request_id: Math.random(),
                        })
                    );
                }
            }
        },
        { immediate: true }
    );

    const getMessages = async () => {
        loading.value = true;
        try {
            const response = await fetch(
                `http://localhost:8000/messages/?chat=${props.id}`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Token ${localStorage.getItem("token")}`,
                    },
                }
            );
            const data: MessageList = await response.json();
            if (response.ok) {
                messages.value = [...data.results];
                next.value = data.next;
            }
        } finally {
            loading.value = false;
        }
    };

    getMessages();

    const createMessage = async () => {
        try {
            await fetch(`http://localhost:8000/messages/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Token ${localStorage.getItem("token")}`,
                },
                body: JSON.stringify({
                    text: input.value,
                    chat: props.id,
                }),
            });
        } finally {
        }
    };
</script>

<template>
    <div class="h-screen bg-stone-100">
        <div class="min-h-full flex flex-col-reverse">
            <form @submit.prevent="createMessage" class="flex flex-row">
                <input
                    v-model="input"
                    type="text"
                    class="bg-slate-200 rounded-md px-2 mr-2 grow"
                />
                <button
                    type="submit"
                    class="
                        px-10
                        rounded-md
                        bg-slate-700
                        text-white
                        hover:bg-slate-400 hover:text-black
                    "
                >
                    Send
                </button>
            </form>
            <div
                v-for="message in messages"
                :key="message.id"
                class="
                    transition-transform
                    duration-1000
                    delay-1000
                    ease-in-out
                "
            >
                {{ message.text }}
            </div>
        </div>
    </div>
</template>