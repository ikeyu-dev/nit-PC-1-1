<script setup lang="ts">
import { apiHealthCheck } from "~/composables/apiHealthCheck";

const mobile_nav_show = ref(false);
const pc_nav_show = ref(true);

const updateVisibility = () => {
    mobile_nav_show.value = window.innerWidth < 768;
    pc_nav_show.value = window.innerWidth >= 768;
};

const nowDate = ref(new Date());

onMounted(() => {
    window.addEventListener("resize", updateVisibility);
    updateVisibility();
    setInterval(() => {
        apiHealthCheck();
        nowDate.value = new Date();
    }, 800);
});
onUnmounted(() => {
    window.removeEventListener("resize", updateVisibility);
});
</script>

<template>
    <header
        v-if="pc_nav_show"
        class="header text-gray-600 body-font sticky top-0"
    >
        <div
            class="contaier mx-auto flex flex-wrap p-0 flex-col md:flex-row items-center"
        >
            <div class="flex">
                <img
                    class="w-40 h-40"
                    src="~/assets/img/logo.svg"
                    alt="logo"
                    id="logo"
                />
            </div>
            <nav
                v-if="pc_nav_show"
                class="md:ml-auto flex flex-wrap items-center text-base justify-center"
            >
                <section class="p-4 m-4">
                    <ClientOnly>
                        {{ nowDate.toLocaleString() }}
                    </ClientOnly>
                </section>
            </nav>
        </div>
    </header>
    <slot />
</template>
