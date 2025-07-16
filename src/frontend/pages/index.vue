<script setup lang="ts">
import FaceMeshCanvas from "~/components/camera.vue";
import PcShow from "~/components/question.vue";
const username = ref<string>("");
onMounted(() => {});
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
