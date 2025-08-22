<script setup lang="ts">
// import { getCookie } from "~/composables/cookie";
import { useUserStore } from "~/composables/user";
import FaceMeshCanvas from "~/components/camera.vue";
import PcShow from "~/components/question.vue";

onMounted(() => {
    const userStore = useUserStore();
    if (userStore.user === null || userStore.user.nickname === "") {
        window.location.href = "/newGame";
    }
    const nickname = computed(() => userStore.user?.nickname);
    console.log(nickname.value);
});
</script>

<template>
    <div
        class="top-0 grid grid-cols-1 md:grid-cols-2 gap-4 justify-center items-center"
    >
        <div class="flex justify-center items-center">
            <FaceMeshCanvas />
        </div>

        <div class="flex justify-center items-center">
            <PcShow />
        </div>
    </div>
</template>
