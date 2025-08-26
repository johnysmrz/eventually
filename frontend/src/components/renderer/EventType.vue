<template>
    <span :class="classMap[value]">
        {{ nameMap[value] }}
    </span>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

const props = defineProps({
    value: {
        type: String,
        required: true
    }
})

const classMap: Record<string, string> = {
    workshop: 'event-type-workshop',
    lecture: 'event-type-lecture',
    unspecified: 'event-type-unspecified'
}

const nameMap: Record<string, string> = {
    workshop: 'Workshop',
    lecture: 'Přednáška',
    unspecified: 'Nespecifikováno'
}

</script>

<style scoped lang="scss">
.event-type-workshop {
    color: rgb(97, 97, 255);
    font-weight: bold;
}

.event-type-lecture {
    color: rgb(86, 255, 86);
    font-weight: bold;
}

.event-type-unspecified {
    color: rgb(134, 133, 133);
    font-style: italic;
}
</style>