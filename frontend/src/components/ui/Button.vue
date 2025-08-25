<template>
    <button
        :disabled="disabled"
        :type="type"
        class="btn"
        @click="handleClick"
    >
        <slot />
    </button>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, computed } from 'vue'

const props = defineProps({
    type: {
        type: String as () => 'button' | 'submit' | 'reset',
        default: 'button',
        validator: (value: string) => ['button', 'submit', 'reset'].includes(value)
    },
    disabled: {
        type: Boolean,
        default: false
    },
    confirmText: {
        type: String
    }
})

const emit = defineEmits(['click'])

function handleClick(event: MouseEvent) {
    if (props.confirmText) {
        const confirmed = window.confirm(props.confirmText)
        if (!confirmed) {
            return
        }
    }
    if (!props.disabled) {
        emit('click', event)
    }
}
</script>

<style scoped lang="scss">
@use '../../config.scss' as config;
@use 'sass:color';

.btn {
    padding: 8px;
    display: inline-block;
    background-color: config.$primary-color;
    color: config.$text-color;
    border: none;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
    min-width: 80px;

    &-primary {
        background-color: config.$primary-color;
        &:hover {
            background-color: color.adjust(config.$primary-color, $lightness: -10%);
        }
        &_outline {
            background-color: transparent;
            border: 1px solid config.$primary-color;
            &:hover {
                background-color: config.$primary-color;
                color: config.$surface-color;
            }
        }
    }

    &-warning {
        background-color: config.$warning-color;
        &:hover {
            background-color: color.adjust(config.$warning-color, $lightness: -10%);
        }
    }

    &-error {
        background-color: config.$error-color;
        &:hover {
            background-color: color.adjust(config.$error-color, $lightness: -10%);
        }
    }
}


</style>