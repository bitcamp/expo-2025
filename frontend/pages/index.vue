<template>
    <div class="app-container">
        <Background />
    </div>
</template>

<script setup lang="ts">
useHead({
    title: 'Bitcamp - Expo',
    meta: [
        {
        name: 'description',
        content:
            "Bitcamp's Expo is the finale to your 36-hour adventure of exploration and creation. Surrounded by mentors and fellow campers, it's your moment to showcase your creativity and passion. Join us by the fire and share your journey!",
        },
        {
        property: 'og:title',
        content: 'Bitcamp - Expo',
        },
        {
        property: 'og:site_name',
        content: 'Bitcamp',
        },
        {
        property: 'og:url',
        content: 'https://expo.bit.camp/',
        },
        {
        property: 'og:description',
        content:
            "Bitcamp's Expo is the finale to your 36-hour adventure of exploration and creation. Surrounded by mentors and fellow campers, it's your moment to showcase your creativity and passion. Join us by the fire and share your journey!",
        },
        {
        property: 'og:type',
        content: 'website',
        },
        {
        property: 'twitter:card',
        content: 'summary',
        },
        {
        property: 'twitter:url',
        content: 'https://expo.bit.camp/',
        },
        {
        property: 'twitter:title',
        content: 'Bitcamp - Expo',
        },
        {
        property: 'twitter:description',
        content:
            "Bitcamp's Expo is the finale to your 36-hour adventure of exploration and creation. Surrounded by mentors and fellow campers, it's your moment to showcase your creativity and passion. Join us by the fire and share your journey!",
        },
        {
        name: 'msapplication-TileColor',
        content: '#ff6f3f',
        },
        {
        name: 'msapplication-config',
        content: '/bitcamp-brand/favicons/browserconfig.xml',
        },
        {
        name: 'theme-color',
        content: '#ffffff',
        },
    ],
    link: [
        {
        rel: 'icon',
        type: 'image/png',
        sizes: '32x32',
        href: '/bitcamp-brand/favicons/favicon-32x32.png',
        },
        {
        rel: 'icon',
        type: 'image/png',
        sizes: '16x16',
        href: '/bitcamp-brand/favicons/favicon-16x16.png',
        },
        {
        rel: 'manifest',
        href: '/bitcamp-brand/favicons/site.webmanifest',
        },
        {
        rel: 'mask-icon',
        href: '/bitcamp-brand/favicons/safari-pinned-tab.svg',
        color: '#ff6f3f',
        },
        {
        rel: 'shortcut icon',
        href: '/bitcamp-brand/favicons/favicon.ico',
        },
    ],
    });
</script>

<script lang="ts">
export default {
    name: 'Background',
};


</script>

<style scoped lang="scss"></style>