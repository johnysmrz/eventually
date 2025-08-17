<template>
    <DataView :value="events">
        <template #list="slotProps">
            <div v-for="e in slotProps.value" :key="e.id_event">
                <strong>{{ e.name }}</strong> — {{ e.start_date }} to {{ e.end_date }}
            </div>
        </template>
    </DataView>
</template>

<script setup>
import { onMounted } from 'vue'
import { useEventStore } from '@/stores/event'
import DataView from 'primevue/dataview'

const store = useEventStore()

// Suspense will wait for this promise to resolve if we return it from setup
const promise = store.fetchAll()
await promise

const events = store.events
</script>

<style scoped>
h2 { margin-top: 1rem }
</style>
