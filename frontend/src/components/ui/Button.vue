<template>
    <button
        :disabled="disabled"
        :type="type"
        @click="handleClick"
        :class="`btn btn__${color}`"
    >
        <slot />
    </button>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
    color: {
        type: String,
        default: 'primary',
        validator: (value) => ['primary', 'secondary', 'success', 'info', 'warning', 'error'].includes(value)
    },
    type: {
        type: String,
        default: 'button',
        validator: (value) => ['button', 'submit', 'reset'].includes(value)
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

function handleClick(event) {
    if (props.confirmText) {
        const confirmed = confirm(props.confirmText)
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
    color: config.$text-color;
    background-color: config.$surface-color;
    border: none;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
    & > i {
        margin-right: 4px;
        transform: translateY(1px);
    }
    &:not(:last-of-type) {
        margin-right: 4px;
    }
    &__primary {
        background-color: config.$primary-color;
        &:hover {
            background-color: color.adjust(config.$primary-color, $lightness: -10%);
        }
    }
    &__secondary {
        background-color: config.$secondary-color;
        &:hover {
            background-color: color.adjust(config.$secondary-color, $lightness: -10%);
        }
    }
    &__success {
        background-color: config.$success-color;
        &:hover {
            background-color: color.adjust(config.$success-color, $lightness: -10%);
        }
    }
    &__info {
        background-color: config.$info-color;
        &:hover {
            background-color: color.adjust(config.$info-color, $lightness: -10%);
        }
    }
    &__warning {
        background-color: config.$warning-color;
        &:hover {
            background-color: color.adjust(config.$warning-color, $lightness: -10%);
        }
    }
    &__error {
        background-color: config.$error-color;
        &:hover {
            background-color: color.adjust(config.$error-color, $lightness: -10%);
        }
    }
}
</style>