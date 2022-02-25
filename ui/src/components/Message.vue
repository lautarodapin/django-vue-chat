<script lang="ts" setup>
import {MessageDetail} from '../types'
import {fromNow} from '../utils'


const {message: {created_at, created_by: {username} = {}, text}} = defineProps<{message: MessageDetail}>()
</script>

<template>
    <div>{{fromNow(created_at)}} - {{username}}: {{message.text}}</div>
</template>