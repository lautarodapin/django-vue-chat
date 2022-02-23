<script lang="ts">
    import { fade } from "svelte/transition";
    import type { MessageDetail } from "../../types/index";
    import { fromNow } from "../../utils/index";
    export let message: MessageDetail;
</script>

<div transition:fade>
    {fromNow(message?.created_at)} - {message?.created_by?.username}: {message.text}
</div>
