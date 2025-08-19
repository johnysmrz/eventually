<template>
    <div class="progress">
        <!-- {{ props.value }} / {{ props.max }} -->
        <div class="progress-bar" :style="{ width: progressBarWidth, backgroundColor: props.color }"></div>
    </div>
</template>

<script lang="ts" setup>
import { defineProps, computed } from 'vue';

const props = defineProps({
    value: {
        type: Number,
        required: true
    },
    max: {
        type: [Number, null],
        required: false,
        default: null
    },
    color: {
        type: String,
        required: false
    }
})

const progressBarWidth = computed(() => {
    if (props.max === null) return '0%'
    const percent = (props.value / props.max) * 100
    return `${Math.min(percent, 100)}%`
})
</script>

<style lang="scss" scoped>
@use '../config.scss' as config;

.progress {
    border: 1px solid config.$text-color;
    height: 20px;
    border-radius: 10px;
    .progress-bar {
        height: 16px;
        margin: 2px;
        background-color: config.$text-color;
        border-radius: 10px;
    }
}
</style>