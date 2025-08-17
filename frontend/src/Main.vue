<template>
    <div id="layout">
        <div id="menubar">
            <TheMainMenu />
        </div>
        <div id="main">
            <RouterView />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import TheMainMenu from './components/TheMainMenu.vue';
import { useEventStore } from './stores/event.ts';
import type { EventType } from './stores/event.ts';
import { useRouter } from 'vue-router';
import eventBus from './eventBus.ts';

const eventStore = useEventStore()
const router = useRouter()

let currentEvent = ref(localStorage.getItem('selectedEventId'))

eventBus.on('eventSelected', (event: unknown) => {
    const typedEvent = event as EventType
    localStorage.setItem('selectedEventId', typedEvent.id_event)
    router.push({ name: 'EventEditorProgram', params: { id: typedEvent.id_event } })
})

await Promise.all([
    eventStore.fetchAll()
])

if (currentEvent.value === null) {
    router.push({ name: 'EventSelector' })
}
</script>

<style lang="scss">
@use './config.scss' as config;

#layout {
    display: flex;
    flex-direction: column;
    height: 100vh;

    #main {
        flex-grow: 1;
    }

    #menubar {
        background-color: config.$surface-color;
        border-bottom: 1px solid config.$surface-edge-color;
    }
}
</style>
