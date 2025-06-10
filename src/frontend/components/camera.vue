<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from "vue";
import { get, useUserMedia } from "@vueuse/core";
import { Camera } from "@mediapipe/camera_utils";
import { FaceMesh } from "@mediapipe/face_mesh";
import type { Results } from "@mediapipe/face_mesh";
import { draw } from "~/composables/draw";

const mobile_nav_show = ref(false);
const pc_nav_show = ref(true);

const updateVisibility = () => {
    mobile_nav_show.value = window.innerWidth < 768;
    pc_nav_show.value = window.innerWidth >= 768;
};

const CANVAS_WIDTH = pc_nav_show.value ? 700 : window.innerWidth; // PCでは700px、モバイルでは画面幅に合わせる
const CANVAS_HEIGHT = pc_nav_show.value ? 700 : window.innerHeight; // PCでは500px、モバイルでは画面高さに合わせる

// DOM要素への参照
const videoRef = ref<HTMLVideoElement | null>(null);
const canvasRef = ref<HTMLCanvasElement | null>(null);

// @vueuse/coreでカメラアクセスを管理
const { stream, enabled } = useUserMedia({
    constraints: {
        video: {
            width: CANVAS_WIDTH,
            height: CANVAS_HEIGHT,
            facingMode: "user",
        },
        audio: false,
    },
});

// MediaPipe インスタンス 保持
let faceMesh: FaceMesh | null = null;
let camera: Camera | null = null;
let isComponentMounted = true;

// streamが取得できたらvideoに接続
watch(stream, (newStream) => {
    if (videoRef.value && newStream) {
        videoRef.value.srcObject = newStream;
        videoRef.value.play();
    }
});

// mediaPipe初期化
const initialize = () => {
    if (!isComponentMounted || !videoRef.value || !canvasRef.value) return;

    const videoElement = videoRef.value;
    const canvasElement = canvasRef.value;
    const ctx = canvasElement.getContext("2d")!;

    faceMesh = new FaceMesh({
        locateFile: (file) =>
            `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`,
    });
    faceMesh.setOptions({
        maxNumFaces: 10, // 最大10人
        refineLandmarks: true, // 顔のランドマークをより正確に検出
        minDetectionConfidence: 0.5, // 検出の信頼度の閾値
        minTrackingConfidence: 0.5, // トラッキングの信頼度の閾値
    });

    // 検出結果のコールバック関数
    faceMesh.onResults((results: Results) => {
        // コンポーネントがマウントされている場合のみ描画
        if (isComponentMounted && ctx) {
            draw(ctx, results, true, [13, 14, 61, 291]);
        }
    });

    // --- MediaPipe Camera セットアップ ---
    camera = new Camera(videoElement, {
        onFrame: async () => {
            // videoの準備ができていれば、FaceMeshに映像を送る
            if (videoElement.readyState >= 3) {
                // 1はHAVE_CURRENT_DATA、2はHAVE_ENOUGH_DATA、3はHAVE_FUTURE_DATA
                await faceMesh?.send({ image: videoElement });
            }
        },
        width: CANVAS_WIDTH,
        height: CANVAS_HEIGHT,
    });

    camera.start();
    console.log("✅ MediaPipe Initialized.");
};

onMounted(() => {
    isComponentMounted = true;
    // カメラへのアクセスを有効にする
    enabled.value = true;

    if (videoRef.value) {
        // video要素のメタデータが読み込まれたら初期化処理を開始
        videoRef.value.onloadedmetadata = initialize;
    }

    window.addEventListener("resize", updateVisibility);
    updateVisibility();
});

// コンポーネントがアンマウントされるときにリソースを解放
onUnmounted(() => {
    isComponentMounted = false;
    enabled.value = false; // カメラを停止
    camera?.stop();
    faceMesh?.close();

    window.removeEventListener("resize", updateVisibility);
});
</script>

<template>
    <!-- MediaPipe入力用 -->
    <video
        ref="videoRef"
        class="hidden"
        autoplay
        playsinline
        muted
    ></video>
    <div class="canvas-wrapper flex justify-center items-center">
        <canvas
            ref="canvasRef"
            :class="[
                'canvas shadow-lg rounded-lg border border-gray-300',
                mobile_nav_show ? 'mobile mx-auto' : 'pc',
            ]"
            :width="CANVAS_WIDTH"
            :height="CANVAS_HEIGHT"
        ></canvas>
    </div>
</template>

<style scoped>
.canvas {
    position: absolute;
    background-color: #1e1e1e;
    object-fit: contain;
}

.canvas.mobile {
    position: relative;
    width: 100%;
    object-fit: cover;
}

.canvas.pc {
    top: calc(160px);
    left: 30px;
    width: calc(50% - 30px);
    height: calc(100svh - 200px);
}
</style>
