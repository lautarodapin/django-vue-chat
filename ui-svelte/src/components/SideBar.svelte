<script lang="ts">
    import { Token } from "../stores/token";
</script>

<nav class="fixed bg-slate-900 text-white top-0 left-0 h-screen w-64">
    <div>
        <h3 class="text-center my-8">Svelte chat</h3>
        <button on:click={Token.signout}>Logout</button>
    </div>
    <slot><!-- optional fallback --></slot>
</nav>
