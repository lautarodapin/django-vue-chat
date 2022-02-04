<script lang="ts">
  import type { MessageDetail } from "../../types/index";
  import { fromNow } from "../../utils/index";
  export let { text, created_at, created_by: { username } = {} }: MessageDetail;
</script>

<div transition:fade>
  {fromNow(created_at)} - {username}: {text}
</div>
