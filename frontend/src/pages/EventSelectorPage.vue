<template>
    <div class="event-selector-page">
        <table>
            <thead>
                <tr>
                    <th>Event Name</th>
                    <th>Event Date</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="event in eventStore.getAll" :key="event.id_event">
                    <td>{{ event.name }}</td>
                    <td>{{ event.start_date.format('DD.MM.YYYY') }} ({{ event.start_date.fromNow() }}) - {{ event.end_date.format('DD.MM.YYYY') }}</td>
                    <td>
                        <button @click="handleEventClick(event)">Select</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup lang="ts">
import { ref, defineEmits } from 'vue'
import { useEventStore } from '../stores/event.js';
import eventBus from '@/eventBus.js';


const eventStore = useEventStore()

const emit = defineEmits(['eventSelected'])

const handleEventClick = (event) => {
    eventBus.emit('eventSelected', event)
}
</script>

<style scoped>
.event-selector-page {
    padding: 2rem;
}
</style>