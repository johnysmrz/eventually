<template>
    <div class="event-program-overview">
        <h1>Program Overview</h1>
        <Table :columns="columns" :data="programOverview">
            <template #cell[start_time]="{ cellContent, row }">
                {{ cellContent }}
            </template>
            <template #cell[type]="{ cellContent, row }">
                <Badge :text="cellContent" />
            </template>
            <template #cell[status]="{ cellContent, row }">
                <Badge :text="cellContent" />
            </template>
            <template #cell[date]="{ cellContent, row }">
                {{ row.start_time.format('HH:mm') }} - {{ row.end_time.format('HH:mm (D.M.YY)') }}
            </template>
            <template #cell[attendee]="{ cellContent, row }">
                <Progress :value="row.attendee_count" :max="row.attendee_limit"></Progress>
            </template>
        </Table>
    </div>
</template>

<script setup lang="ts">
import { ref, defineEmits } from 'vue'
import useProgramOverview from '../../api/EventProgramOverview.js'
import { useRoute } from 'vue-router'
import Table from '../../components/Table.vue'
import Badge from '../../components/Badge.vue'
import Progress from '../../components/Progress.vue'


const route = useRoute()

const { programOverview, fetchProgramOverview } = useProgramOverview()


const columns = ref([
    { id: 'name', title: 'Název' },
    { id: 'date', title: 'Datum' },
    { id: 'type', title: 'Typ' },
    { id: 'status', title: 'Stav' },
    { id: 'attendee', title: 'Účastníků' }
])

const eventId = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id
await fetchProgramOverview(eventId)
</script>

<style scoped lang="scss">
@use '../../config.scss' as config;
</style>