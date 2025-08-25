<template>
    <div id="event-editor-page">
        <div class="menu">
            <nav>
                <RouterLink :to="{ name: 'EventEditorProgram' }">Program</RouterLink>
                <span class="right-arrow"></span>
                <RouterLink :to="{ name: 'EventEditorCalendar' }">Kalendář</RouterLink>
                <span class="right-arrow"></span>
                <RouterLink :to="{ name: 'EventEditorLocations' }">Lokace</RouterLink>
                <span class="right-arrow"></span>
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
            display: grid;
            grid-template-columns: 1fr 10px;

            // padding: 10px;
            &>a {
                // margin-bottom: 10px;
                padding: 5px 10px;
                text-decoration: none;
                display: block;
                color: config.$text-color;

                &:hover {
                    color: config.$text-color-hover;
                }

                &.router-link-exact-active {
                    font-weight: bold;
                    padding: 5px 10px;
                    background-color: config.$primary-color;

                    &+span {
                        background-color: config.$primary-color;

                        &::after {
                            content: '';
                            border: solid config.$primary-color;
                            border-width: 0 6px 6px 0;
                            display: inline-block;
                            padding: 4px;
                            margin-top: 7px;
                            transform: rotate(-45deg);
                        }

                    }
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