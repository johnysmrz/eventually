<template>
    <nav class="the-menu-bar">
        <RouterLink :to="{ name: 'EventSelector' }">
            Vybrat událost
        </RouterLink>
    </nav>
</template>

<script setup lang="ts">

import { RouterView, RouterLink } from 'vue-router';


</script>

<style scoped lang="scss">
$yellow: #fecd40;
$red: #c42737;
$teal: #2f7979;
$blue: #10273a;
$surface: #262626;

    // --color-background: $background;
    // --color-surface: $surface;

.the-menu-bar {
    padding: 10px;
    display: flex;

    a {
        color: $surface;
        text-decoration: none;
        padding: 5px 12px;
        background-color: $teal;
        margin-right: 5px;
        border-radius: 6px;
        font-weight: bold;

        &:hover {
            background-color: $yellow;
            color: $red;
        }
    }
}
</style>