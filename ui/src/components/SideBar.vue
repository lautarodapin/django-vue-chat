<script setup lang="ts">
import {token} from "../stores"
import {withDefaults, defineProps, toRef, toRefs} from "vue"

const props = withDefaults(
    defineProps<{
        title?: string
    }>(),
    {
        title: "Vue chat",
    }
)
const logout = () => {
    localStorage.removeItem("token")
    token.value = null
}
</script>

<template>
    <nav class="fixed bg-slate-900 text-white top-0 left-0 h-screen w-64">
        <div>
            <h3 class="font-mono text-center my-8">{{props.title}}</h3>
        </div>

        <slot v-if="token">
            <!-- optional fallback -->
        </slot>
        <div class="absolute bottom-4 flex w-60 h-12 justify-center">
            <button
                class="rounded-md bg-slate-600 border-slate-600 text-white hover:bg-slate-400 hover:text-black w-40 hover:border-slate-400 grid-cols-2 inline-flex justify-center items-center gap-3"
                @click.prevent="logout"
            >
                Logout
                <LogoutIcon />
            </button>
        </div>
    </nav>
</template>