<template>
    <div class="calendar">
        <svg width="800px" height="auto" viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
            <rect fill="#555555" stroke="#000" x="0" y="0" width="800" height="800"/>
        </svg>
    </div>
</template>

<script lang="ts" setup>
import { ref, defineProps } from 'vue'
import type { EventProgramOverviewEntity } from '../api/EventProgramOverview.js'

const props = defineProps<{
    program: Array<EventProgramOverviewEntity>
}>()

</script>

<style lang="scss" scoped>
.calendar {
    // Calendar styles go here
}
</style>