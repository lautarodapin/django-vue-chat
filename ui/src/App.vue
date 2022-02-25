<script setup lang="ts">
import {token, chatSelected} from "./stores"
import Login from "./components/Login.vue"
import SideBar from "./components/SideBar.vue"
import Chats from "./components/Chats.vue"
import Chat from './components/Chat.vue'

</script>

<template>
    <div>
        <side-bar>
            <chats />
        </side-bar>
        <div class="pl-64" v-if="token">
            <chat v-if="chatSelected" />
            <div
                v-else
                class="h-[95vh] flex justify-center text-4xl text-slate-600"
            >Seleccione un chat</div>
            <Login />
        </div>
        <div v-else class="pl-64">
            <login />
        </div>
    </div>
</template>

