<script lang="ts">
    import { fade } from "svelte/transition";
    import type { MessageDetail } from "../../types/index";
    import { fromNow } from "../../utils/index";
    export let message: MessageDetail;

    // let { text, created_at, created_by: { username } = {} } = $message;
</script>

<div transition:fade>
    <!-- {fromNow(created_at)} - {username}: {text} -->
    {fromNow(message?.created_at)} - {message?.created_by?.username}: {message.text}
</div>
