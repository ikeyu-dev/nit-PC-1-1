<script setup lang="ts">
import { useRoute } from "vue-router";

const route = useRoute();
const currentPath = ref(route.path);

watch(route, (newRoute) => {
    currentPath.value = newRoute.path;
});

const mobile_nav_show = ref(false);
const pc_nav_show = ref(true);

const updateVisibility = () => {
    mobile_nav_show.value = window.innerWidth < 768;
    pc_nav_show.value = window.innerWidth >= 768;
};

onMounted(() => {
    window.addEventListener("resize", updateVisibility);
    updateVisibility();
});

onUnmounted(() => {
    window.removeEventListener("resize", updateVisibility);
});
</script>

<template>
    <header class="header text-gray-600 body-font sticky top-0">
        <div
            class="contaier mx-auto flex flex-wrap p-0 flex-col md:flex-row items-center"
        >
            <div class="flex">
                <img
                    class="h-40 w-40"
                    src="~/assets/img/logo.svg"
                    alt="logo"
                    id="logo"
                />
            </div>
            <nav
                v-if="pc_nav_show"
                class="md:ml-auto flex flex-wrap items-center text-base justify-center"
            >
                <nuxt-link
                    to="/"
                    class="p-4 hover:text-gray-900 hover:bg-slate-100"
                >
                    ホーム
                </nuxt-link>
                <nuxt-link
                    to="/events"
                    class="p-4 hover:text-gray-900 hover:bg-slate-100"
                >
                    開始
                </nuxt-link>
                <nuxt-link
                    to="/info"
                    class="p-4 hover:text-gray-900 hover:bg-slate-100"
                >
                    成績
                </nuxt-link>
                <!-- <nuxt-link
                    :to="sign_link"
                    class="p-4  hover:text-gray-900 hover:bg-slate-100"
                >
                    {{ log_in_out_msg }}
                </nuxt-link> -->
            </nav>
        </div>
    </header>

    <slot />

    <footer
        v-if="mobile_nav_show"
        class="flex mobile_navbar fixed bottom-0 left-0 w-full bg-white py-3 px-4"
    >
        <div class="container mx-auto flex justify-between items-center">
            <nuxt-link
                to="/"
                class="flex flex-col md:flex-row justify-center items-center"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 576 512"
                    class="w-5 h-5"
                    :class="{
                        'fill-black': currentPath === '/',
                        'fill-neutral-400': currentPath !== '/',
                    }"
                >
                    <path
                        d="M575.8 255.5c0 18-15 32.1-32 32.1h-32l.7 160.2c0 2.7-.2 5.4-.5 8.1V472c0 22.1-17.9 40-40 40H456c-1.1 0-2.2 0-3.3-.1c-1.4 .1-2.8 .1-4.2 .1H416 392c-22.1 0-40-17.9-40-40V448 384c0-17.7-14.3-32-32-32H256c-17.7 0-32 14.3-32 32v64 24c0 22.1-17.9 40-40 40H160 128.1c-1.5 0-3-.1-4.5-.2c-1.2 .1-2.4 .2-3.6 .2H104c-22.1 0-40-17.9-40-40V360c0-.9 0-1.9 .1-2.8V287.6H32c-18 0-32-14-32-32.1c0-9 3-17 10-24L266.4 8c7-7 15-8 22-8s15 2 21 7L564.8 231.5c8 7 12 15 11 24z"
                    />
                </svg>
                <span
                    class="font-bold"
                    :class="{
                        'text-black': currentPath === '/',
                        'text-slate-400': currentPath !== '/',
                    }"
                    >HOME</span
                >
            </nuxt-link>
            <nuxt-link
                to="/events"
                class="flex flex-col md:flex-row justify-center items-center"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 512 512"
                    class="w-5 h-5"
                    :class="{
                        'fill-black': currentPath === '/order',
                        'fill-neutral-400': currentPath !== '/order',
                    }"
                >
                    <path
                        d="M498.1 5.6c10.1 7 15.4 19.1 13.5 31.2l-64 416c-1.5 9.7-7.4 18.2-16 23s-18.9 5.4-28 1.6L284 427.7l-68.5 74.1c-8.9 9.7-22.9 12.9-35.2 8.1S160 493.2 160 480V396.4c0-4 1.5-7.8 4.2-10.7L331.8 202.8c5.8-6.3 5.6-16-.4-22s-15.7-6.4-22-.7L106 360.8 17.7 316.6C7.1 311.3 .3 300.7 0 288.9s5.9-22.8 16.1-28.7l448-256c10.7-6.1 23.9-5.5 34 1.4z"
                    />
                </svg>
                <span
                    class="font-bold"
                    :class="{
                        'text-black': currentPath === '#',
                        'text-slate-400': currentPath !== '#',
                    }"
                    >作成</span
                >
            </nuxt-link>
            <nuxt-link
                to="/info"
                class="flex flex-col md:flex-row justify-center items-center"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 512 512"
                    class="w-5 h-5"
                    :class="{
                        'fill-black': currentPath === '/info',
                        'fill-neutral-400': currentPath !== '/info',
                    }"
                >
                    <path
                        d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM216 336h24V272H216c-13.3 0-24-10.7-24-24s10.7-24 24-24h48c13.3 0 24 10.7 24 24v88h8c13.3 0 24 10.7 24 24s-10.7 24-24 24H216c-13.3 0-24-10.7-24-24s10.7-24 24-24zm40-208a32 32 0 1 1 0 64 32 32 0 1 1 0-64z"
                    />
                </svg>
                <span
                    class="font-bold"
                    :class="{
                        'text-black': currentPath === '/info',
                        'text-slate-400': currentPath !== '/info',
                    }"
                    >各情報</span
                >
            </nuxt-link>
        </div>
    </footer>
</template>
