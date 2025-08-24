<template>
    <div id="event-editor-page">
        <div class="menu">
            <nav>
                <RouterLink :to="{ name: 'EventEditorProgram' }">Program</RouterLink>
                <RouterLink :to="{ name: 'EventEditorCalendar' }">Kalendář</RouterLink>
                <RouterLink :to="{ name: 'EventEditorLocations' }">Lokace</RouterLink>
            </nav>
        </div>
        <div class="editor">
            <Suspense>
                <RouterView #default />
                <template #fallback>
                    <p>Loading...</p>
                </template>
            </Suspense>
        </div>
    </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue'
import { useEventStore } from '../stores/event.ts';
import { RouterLink, RouterView } from 'vue-router';

const eventStore = useEventStore()

</script>

<style scoped lang="scss">
@use '../config.scss' as config;


#event-editor-page {
    display: grid;
    grid-template-columns: 200px 1fr;
    grid-template-rows: 1fr;
    grid-row-gap: 0px;
    height: 100%;

    .menu {
        background-color: config.$surface-color;
        border-right: 1px solid config.$surface-edge-color;
        nav {
            display: flex;
            flex-direction: column;
            padding: 10px;
            & > a {
                margin-bottom: 10px;
                text-decoration: none;
                display: block;
                color: config.$text-color;
                &:hover {
                    color: config.$text-color-hover;
                }
            }
        }
    }

    .editor {
        background-color: config.$background-color;
        color: config.$text-color;
    }
}
</style>