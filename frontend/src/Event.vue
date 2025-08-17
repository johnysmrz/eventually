<template>
    <div id="layout">
        <div id="menubar">
            <TheMenuBar :menu-items="menuItems" />
        </div>
        <div id="main">
            <RouterView />
        </div>
        <div id="footer">Footer</div>
    </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import { useEventStore } from '@/stores/event'
import { computed } from 'vue'
import { RouterView } from "vue-router"
import TheMenuBar from './components/TheMenuBar.vue'
import { MenuItem } from './defs/menuItem.ts'


const eventStore = useEventStore()

await eventStore.fetchAll()

const props = defineProps({
    eventId: {
        type: String,
        required: true
    }
})

const currentEvent = computed(() => eventStore.getById(props.eventId) || {})
const allEvents = computed(() => eventStore.getAll())

const menuItems: MenuItem[] = [
    new MenuItem({
        id: 'home',
        label: 'Home',
        icon: 'pi pi-home',
        route: '/'
    }),
    new MenuItem({
        id: 'events',
        label: 'Events',
        icon: 'pi pi-calendar',
        route: '/events'
    }),
    new MenuItem({
        id: 'logout',
        label: 'Logout',
        icon: 'pi pi-sign-out',
        route: '/logout'
    })
]

</script>

<style scoped>
#layout {
    display: grid;
    grid-template-columns: 200px 1fr;
    grid-template-rows: 50px 1fr 30px;
    grid-column-gap: 0px;
    grid-row-gap: 0px;
    height: 100vh;
    width: 100vw;
    background-color: #262626;
    grid-template-areas: 
        "menubar menubar"
        "main main"
        "footer footer";
    }

#layout > #menubar {
    grid-area: menubar;
}

#layout > #main {
    grid-area: main;
}

#layout > #footer {
    grid-area: footer;
}
</style>