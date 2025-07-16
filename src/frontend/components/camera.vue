<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from "vue";
import { useUserMedia } from "@vueuse/core";
import { Camera } from "@mediapipe/camera_utils";
import { FaceMesh } from "@mediapipe/face_mesh";
import type { Results } from "@mediapipe/face_mesh";
import * as faceapi from "face-api.js";
import { Landmarks } from "~/composables/landmarks";
import { draw } from "~/composables/draw";

const faceAPI_uri = "/models";

const mobile_nav_show = ref(false);
const pc_nav_show = ref(true);

const updateVisibility = () => {
    mobile_nav_show.value = window.innerWidth < 768;
    pc_nav_show.value = window.innerWidth >= 768;
};

const CANVAS_WIDTH = pc_nav_show.value ? 700 : window.innerWidth;
const CANVAS_HEIGHT = pc_nav_show.value ? 700 : window.innerHeight;

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

// 初期化
const initialize = () => {
    if (!isComponentMounted || !videoRef.value || !canvasRef.value) return;

    const videoElement = videoRef.value;
    const canvasElement = canvasRef.value;
    const ctx = canvasElement.getContext("2d", { willReadFrequently: true });

    faceMesh = new FaceMesh({
        locateFile: (file) =>
            `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`,
    });
    faceMesh.setOptions({
        maxNumFaces: 1, // 最大10人
        refineLandmarks: true, // 顔のランドマークをより正確に検出
        minDetectionConfidence: 0.5, // 検出の信頼度の閾値
        minTrackingConfidence: 0.5, // トラッキングの信頼度の閾値
    });

    // モデルをロード
    Promise.all([
        faceapi.nets.ssdMobilenetv1.loadFromUri(faceAPI_uri),
        faceapi.nets.faceLandmark68Net.loadFromUri(faceAPI_uri),
        faceapi.nets.faceExpressionNet.loadFromUri(faceAPI_uri),
    ]).then(() => {
        console.log("✅ face-api models loaded.");
    });

    // 検出結果のコールバック関数
    faceMesh.onResults(async (results: Results) => {
        // コンポーネントがマウントされている場合のみ描画
        if (isComponentMounted && ctx) {
            const landmarks = new Landmarks();
            const detections = await faceapi
                .detectAllFaces(videoRef.value!)
                .withFaceExpressions();

            const faceapi_detection = !detections
                ? []
                : detections.map((detection) => ({
                      expressions: detection.expressions, // 表情データ
                      box: detection.detection.box, // 顔の位置情報
                  }));
            draw(
                ctx,
                results,
                true,
                [
                    landmarks.upper_lip_bottom,
                    landmarks.lower_lip_top,
                    landmarks.lip_center_point,
                    landmarks.lip_corner_left,
                    landmarks.lip_corner_right,
                    landmarks.left_eye_top,
                    landmarks.left_eye_bottom,
                    landmarks.right_eye_top,
                    landmarks.right_eye_bottom,
                ],
                JSON.stringify(faceapi_detection)
            ).then((emotionJudgeResult) => {
                const event = new CustomEvent("emotionResult", {
                    detail: emotionJudgeResult,
                });
                window.dispatchEvent(event);
            });
        }
    });

    // --- MediaPipe Camera セットアップ ---
    camera = new Camera(videoElement, {
        onFrame: async () => {
            // videoの準備ができていれば、FaceMeshに映像を送る
            if (videoElement.readyState >= 3) {
                // 0はHAVE_NOTHING -> 1はHAVE_METADATA -> 2はHAVE_CURRENT_DATA -> 3はHAVE_FUTURE_DATA
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
    height: calc(100svh - 233px);
}

.canvas.pc {
    top: calc(160px);
    left: 30px;
    width: calc(50% - 30px);
    height: calc(100svh - 200px);
}
</style>
