<template>
    <Suspense>
        <template #default>
            <Main></Main>
        </template>
        <template #fallback>
            <StartupSplash />
        </template>
    </Suspense>
</template>

<script setup>
import Main from './Main.vue'
import StartupSplash from './components/StartupSplash.vue'


</script>

<style lang="scss">
@use './config.scss' as config;

body {
    margin: 0;
    font-family: Avenir, Helvetica, Arial, sans-serif;
    background-color: config.$background-color;
    color: config.$text-color;
}
</style>
