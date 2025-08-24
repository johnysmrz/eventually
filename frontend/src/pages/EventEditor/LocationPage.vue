<template>
    <div id="event-location-page">
        <Table :data="eventLocation" :columns="columns">
            <template #cell[color]="{ cellContent }">
                <span class="colorBox" :style="{ backgroundColor: cellContent }"></span>
            </template>
            <template #cell[gps]="{ row }">
                <span>{{ row.lat }}, {{ row.lon }}</span>
            </template>
            <template #controlsHeader>
                <Button @click="dialogVisible = true">Přidat lokaci</Button>
            </template>
            <template #controls="{ row }">
                <Button color="error" @click="handleDeleteLocation(row.id_location)" confirmText="Opravdu chcete smazat?">Smazat</Button>
            </template>
        </Table>
        <GoogleMap :api-key="googleMapsApiKey" style="width: 100%; height: 600px" :center="center"
            :zoom="17">
            <CustomMarker v-for="location in locationsWithGPS" :options="{ position: { lat: location.lat, lng: location.lon }, anchorPoint: 'TOP_CENTER' }">
                <div class="marker" :style="{'color': location.color}">{{ location.name }}</div>
            </CustomMarker>
        </GoogleMap>
        <Dialog :isOpen="dialogVisible">
            <AutoForm :config="fetchEventAutoFormOptions(eventId)" @cancel="dialogVisible = false" @submit="handleCreateSubmit"></AutoForm>
        </Dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, defineEmits, computed } from 'vue'
import useEventLocation from '../../api/EventLocation'
import { useRoute } from 'vue-router'
import Table from '../../components/ui/Table.vue'
import type { TableColumn } from '../../components/ui/Table'
// @ts-ignore
import { GoogleMap, CustomMarker } from 'vue3-google-map'
import Button from '@ui/Button.vue'
import Dialog from '@ui/Dialog.vue'
import AutoForm from '@ui/AutoForm.vue'

// @ts-ignore
const googleMapsApiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY 

const route = useRoute()

const { eventLocation, fetchEventLocation, fetchEventAutoFormOptions, createEventLocation, deleteEventLocation } = useEventLocation()

const columns: TableColumn[] = [
    { title: 'Název', id: 'name' },
    { title: 'Barva', id: 'color' },
    { title: 'GPS', id: 'gps' }
]

const locationsWithGPS = computed(() => {
    return eventLocation.value.filter(location => location.lat && location.lon)
})

let dialogVisible = ref(false)

const eventId = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id
const center = ref({ lat: 50.058956, lng: 14.010947 })

const handleCreateSubmit = async (data: any) => {
    await createEventLocation(eventId, data)
    dialogVisible.value = false
}
const handleDeleteLocation = async (locationId: string) => {
    await deleteEventLocation(eventId, locationId)
    await fetchEventLocation(eventId)
}

await fetchEventLocation(eventId)
</script>

<style scoped lang="scss">
@use '../../config.scss' as config;
@use 'sass:color';


.colorBox {
    width: 20px;
    height: 20px;
    display: inline-block;
    border: 1px solid config.$text-color;
}

#event-location-page {
    display: flex;
}

.marker {
    display: block;
    border: 1px solid config.$surface-edge-color;
    background-color: config.$surface-color;
    padding: 3px;
    border-radius: 5px;
}
</style>