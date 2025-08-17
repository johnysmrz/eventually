<template>
    <DataTable :value="eventStore.getAll" selectionMode="single" dataKey="id_event" @row-select="onRowSelect">
        <Column field="name" header="Name"></Column>
        <Column field="start_date" header="Start Date">
            <template #body="slotProps">
                {{ new Date(slotProps.data.start_date).toLocaleDateString() }}
            </template>
        </Column>
        <Column field="end_date" header="End Date">
            <template #body="slotProps">
                {{ new Date(slotProps.data.end_date).toLocaleDateString() }}
            </template>
        </Column>
        <Column field="description" header="Description"></Column>
    </DataTable>
</template>

<script setup>
import DataTable from 'primevue/datatable'
import Column from 'primevue/column';
import { defineEmits } from 'vue'
import { useEventStore } from '@/stores/event'

const eventStore = useEventStore()

const promise = eventStore.fetchAll()
await promise

const emit = defineEmits(['eventSelect'])

const onRowSelect = (event) => {
    emit('eventSelect', event.data.id_event)
}
</script>
