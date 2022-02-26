<script lang="ts" setup>
import {MessageDetail} from '../types'
import {fromNow} from '../utils'


const props = defineProps<{message: MessageDetail}>()
</script>

<template>
    <div>{{fromNow(props.message.created_at)}} - {{props.message.created_by?.username}}: {{props.message.text}}</div>
</template>