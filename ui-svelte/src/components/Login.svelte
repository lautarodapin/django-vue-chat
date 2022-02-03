<script lang="ts">
    import { Token } from "../stores/token";

    let username: string;
    let password: string;
    let loading: boolean;

    const onSubmit = async () => {
        loading = true;
        const response = await fetch("http://localhost:8000/users/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });
        const data = await response.json();
        const { token } = data;
        Token.signin(token);
        loading = false;
    };
</script>

<form on:submit|preventDefault={onSubmit}>
    <label for="username">Username</label>
    <input id="username" bind:value={username} type="text" />
    <label for="password">Password</label>
    <input id="password" bind:value={password} type="password" />
    <button type="submit">
        {#if loading}
            Login...
        {:else}
            Login
        {/if}
    </button>
</form>
