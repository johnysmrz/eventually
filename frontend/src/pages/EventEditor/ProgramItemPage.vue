<template>
    <div class="program-item-page">
        <h1>Program Item</h1>
        <Table :columns="columns" :data="programItems">
            <template #cell[required_time]="{ cellContent }">
                {{ formatIntToTime(cellContent) }}
            </template>
            <template #cell[before_time_buffer]="{ cellContent }">
                {{ formatIntToTime(cellContent) }}
            </template>
            <template #cell[after_time_buffer]="{ cellContent }">
                {{ formatIntToTime(cellContent) }}
            </template>
            <template #cell[created_at]="{ cellContent }">
                {{ cellContent.fromNow() }}
            </template>
            <template #cell[type]="{ cellContent }">
                <EventTypeRenderer :value="cellContent" />
            </template>
            <template #cell[id_location]="{ cellContent }">
                <LocationRenderer :value="cellContent" :locations="eventLocation" />
            </template>
        </Table>
    </div>
</template>

<script setup lang="ts">
import useProgramItem from '@/api/EventProgramItem'
import { useRoute } from 'vue-router'
import Table from '@ui/Table.vue'
import type { TableColumn } from '@ui/Table.d.ts'
import LocationRenderer from '@/components/renderer/Location.vue'
import EventTypeRenderer from '@/components/renderer/EventType.vue'
import useEventLocation from '@/api/EventLocation'

const { programItems, fetchProgramItems } = useProgramItem()
const { eventLocation, fetchEventLocation } = useEventLocation()

const route = useRoute()
const eventId = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id

const columns: TableColumn[] = [
    { id: 'name', title: 'Název' },
    { id: 'description', title: 'Popis' },
    { id: 'type', title: 'Typ' },
    { id: 'id_location', title: 'Místo konání' },
    { id: 'attendee_limit', title: 'Limit účastníků' },
    { id: 'required_time', title: 'Požadovaný čas' },
    { id: 'before_time_buffer', title: 'Časový buffer před' },
    { id: 'after_time_buffer', title: 'Časový buffer po' },
    { id: 'created_at', title: 'Vytvořeno' },
]

const formatIntToTime = (value: number) => {
    const hours = Math.floor(value / 60)
    const minutes = value % 60
    if (hours > 0) {
        return `${hours}h ${minutes}min`
    }
    return `${minutes}min`
}

await Promise.all([
    fetchProgramItems(eventId),
    fetchEventLocation(eventId)
])
</script>

<style scoped>
.program-item-page {
    padding: 10px;
}

</style>