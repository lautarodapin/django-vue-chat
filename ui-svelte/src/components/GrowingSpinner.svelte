<script lang="ts">
    export let size: "8" | "16" | "32" | "64" = "32";
</script>

<div class="flex justify-center items-center">
    <div
        class={`animate-spin rounded-full h-${size} w-${size} border-b-2 border-slate-200`}
    />
</div>
