<template>
    <p>Program</p>
</template>

<script setup>
import { ref, defineEmits } from 'vue'
import { useEventStore } from '../../stores/event.js'
import { RouterLink } from 'vue-router'

const eventStore = useEventStore()


function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

await delay(2000)
</script>

<style scoped lang="scss">
@use '../../config.scss' as config;


</style>