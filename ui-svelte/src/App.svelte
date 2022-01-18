<script lang="ts">
	export let count: number = 0;
</script>

<main>
    <button on:click={() => count++}>+1</button>
    {count}
</main>

<style lang="postcss" global>
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
</style>