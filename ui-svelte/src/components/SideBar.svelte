<script lang="ts">
    import { Token } from "../stores/token";
    import { fade } from "svelte/transition";
    import LogoutIcon from "./icons/LogoutIcon.svelte";
    $: isAuth = !!$Token;
</script>

<nav class="fixed bg-slate-900 text-white top-0 left-0 h-screen w-64">
    <div>
        <h3 class="text-center my-8">Svelte chat</h3>
    </div>
    {#if isAuth}
        <slot><!-- optional fallback --></slot>
    {/if}
    {#if isAuth}
        <div
            transition:fade
            class="absolute bottom-4 flex w-60 h-12 justify-center"
        >
            <button
                class="rounded-md bg-slate-600 border-slate-600 text-white hover:bg-slate-400 hover:text-black w-40 hover:border-slate-400"
                on:click={Token.signout}
            >
                Logout
            </button>
            <LogoutIcon />
        </div>
    {/if}
</nav>
