<template>
    <div v-if="currentLocation" :style="{ color: currentLocation.color, fontWeight: 'bold' }">
        {{ currentLocation.name }}
    </div>
    <div v-else>
        Neznámá lokalita ({{ value }})
    </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import type { EventLocationEntity } from '@/api/EventLocation'

const props = defineProps({
    value: {
        type: String,
        required: true
    },
    locations: {
        type: Array as () => Array<EventLocationEntity>,
        required: true
    }
})

const currentLocation: EventLocationEntity | undefined = props.locations.find(location => location.id_location === props.value)

</script>
