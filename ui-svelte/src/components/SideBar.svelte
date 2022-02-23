<script lang="ts">
    import { fade } from "svelte/transition";
    import { chats, messages, Token, user } from "../stores";
    import LogoutIcon from "./icons/LogoutIcon.svelte";
    $: isAuth = !!$Token;

    export const title = "Svelte chat";

    const logout = () => {
        messages.set([]);
        chats.set([]);
        user.set(undefined);
        Token.signout();
    };
</script>

<nav class="fixed bg-slate-900 text-white top-0 left-0 h-screen w-64">
    <div>
        <h3 class="text-center my-8">{title}</h3>
    </div>
    {#if $user}
        <div>
            {$user?.username}
        </div>
    {/if}
    {#if isAuth}
        <slot><!-- optional fallback --></slot>
    {/if}
    {#if isAuth}
        <div
            transition:fade
            class="absolute bottom-4 flex w-60 h-12 justify-center"
        >
            <button
                class="rounded-md bg-slate-600 border-slate-600 text-white hover:bg-slate-400 hover:text-black w-40 hover:border-slate-400 grid-cols-2
                inline-flex justify-center items-center gap-3"
                on:click={logout}
            >
                Logout
                <LogoutIcon />
            </button>
        </div>
    {/if}
</nav>
