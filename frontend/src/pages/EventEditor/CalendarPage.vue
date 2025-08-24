<template>
    <div class="event-program-overview">
        <h1>Kalendář</h1>
        <Calendar :program="programOverview" />
    </div>
</template>

<script setup lang="ts">
import { ref, defineEmits } from 'vue'
import useProgramOverview from '../../api/EventProgramOverview.js'
import { useRoute } from 'vue-router'
import Calendar from '../../components/Calendar.vue'

const route = useRoute()

const { programOverview, fetchProgramOverview } = useProgramOverview()


const eventId = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id
await fetchProgramOverview(eventId)
</script>

<style scoped lang="scss">
@use '../../config.scss' as config;

</style>