<template>
    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th v-for="column in columns" :key="column.id">{{ column.title }}</th>
                    <th v-if="hasControls">
                        <slot name="controlsHeader" />
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="row in data" :key="row.id_program_item">
                    <td v-for="column in columns" :key="column.id">
                        <slot :name="`cell[${column.id}]`" :cellContent="row[column.id]" :row="row">
                            {{ row[column.id] }}
                        </slot>
                    </td>
                    <td v-if="hasControls">
                        <slot name="controls" :row="row" />
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup lang="ts">
import type { TableColumn } from './Table.d.ts'
import { useSlots } from 'vue';

const props = defineProps({
    columns: {
        type: Array as () => TableColumn[],
        required: false,
        default: () => []
    },
    data: {
        type: Array as () => Array<Record<string, any>>,
        required: false,
        default: () => []
    }
})
const slots = useSlots()
const hasControls = !!slots.controls
defineEmits([])
</script>

<style scoped lang="scss">
@use '@/config.scss' as config;

$table-content-padding: 15px;

.table-container {
    width: 100%;
    overflow-x: auto;
    background-color: config.$surface-color;
    border-radius: config.$radius;
    border: 1px solid config.$surface-edge-color;
    table {
        width: 100%;
        border-collapse: collapse;
        border-spacing: 0;
    }
    thead {
        border-bottom: 1px solid config.$surface-edge-color;
    }
    thead th {
        color: config.$text-color;
        padding: $table-content-padding;
        text-align: left;
    }
    tbody {
        tr:not(:last-child) {
            border-bottom: 1px solid config.$surface-edge-color;
        }
        tr {
            td {
                padding: $table-content-padding;
            }
        }

    }
}

</style>