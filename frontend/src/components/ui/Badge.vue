<template>
    <span class="badge">
        <span v-if="icon" class="badge__icon">
            <component :is="icon" />
        </span>
        <span class="badge__text">{{ text }}</span>
    </span>
</template>

<script lang="ts" setup>
import { defineProps, type Component } from 'vue';

const props = defineProps<{
    text: string
    icon?: Component | string
}>();
</script>

<style lang="scss" scoped>
@use '../../config.scss' as config;

.badge {
    display: inline-flex;
    align-items: center;
    padding: 0.25em 0.75em;
    border-radius: 1em;
    background: #f0f0f0;
    color: #333;
    font-size: 0.95em;

    &__icon {
        margin-right: 0.5em;
        display: flex;
        align-items: center;
    }

    &__text {
        white-space: nowrap;
    }
}
</style>