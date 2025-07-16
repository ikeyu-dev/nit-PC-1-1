<script setup lang="ts">
import { manageQuestion } from "~/composables/question";
import type { Question } from "~/composables/questionInterface";
import correctSound from "~/assets/music/correct.mp3";
import resultSound from "~/assets/music/result.mp3";

const allQuestions = ref<Question[]>([]);
const currentQuestion = ref<Question | null>(null);
const score = ref<number>(0);
const maxScore: number = 300;
const emotion = ref<{ show: string; judge: string }>({
    show: "",
    judge: "",
});
const emotionCount = ref<{
    happy: number;
    sad: number;
    angry: number;
    surprised: number;
}>({
    happy: 0,
    sad: 0,
    angry: 0,
    surprised: 0,
});

try {
    const question = await manageQuestion("get");
    if (question) {
        allQuestions.value = question;
        currentQuestion.value = question[0] || null;
    }
} catch (error) {
    alert(`エラー : ${error}`);
}

const usePlaySound = () => {
    const correct = () => {
        if (score.value != null && score.value < maxScore) {
            const audio = new Audio(correctSound);
            audio.volume = 1;
            audio.play();
            score.value = (score.value || 0) + 25;
        }
    };
    const result = () => {
        const audio = new Audio(resultSound);
        audio.volume = 1;
        audio.play();
    };
    return { correct, result };
};

const mobile_nav_show = ref(false);
const pc_nav_show = ref(true);

const updateVisibility = () => {
    mobile_nav_show.value = window.innerWidth < 768;
    pc_nav_show.value = window.innerWidth >= 768;
};

onMounted(() => {
    window.addEventListener("resize", updateVisibility);
    updateVisibility();
    window.addEventListener("emotionResult", (event) => {
        emotion.value = (event as CustomEvent).detail || {
            show: "表情読み取り中...",
            judge: "none",
        };
        if (
            emotion.value.judge === currentQuestion.value?.tag &&
            emotionCount.value[
                emotion.value.judge as keyof typeof emotionCount.value
            ] < 1
        ) {
            emotionCount.value[
                emotion.value.judge as keyof typeof emotionCount.value
            ] += 1;
            usePlaySound().correct();
            currentQuestion.value =
                allQuestions.value.find(
                    (q) =>
                        q.tag !== currentQuestion.value?.tag &&
                        emotionCount.value[
                            q.tag as keyof typeof emotionCount.value
                        ] < 1
                ) || null;
        }
    });
});

onUnmounted(() => {
    window.removeEventListener("resize", updateVisibility);
});
</script>

<template>
    <section
        v-if="pc_nav_show"
        class="flex justify-center items-center text-gray-600 body-font"
    >
        <div class="container px-5 mx-auto">
            <div class="flex flex-col items-center m-2">
                <div
                    class="card w-full max-w-lg bg-base-100 shadow-xl rounded-lg border border-gray-200 m-5"
                >
                    <div class="button card-body text-center p-6">
                        <h2
                            class="card-title text-xl font-bold text-primary mb-4"
                        >
                            問題:
                        </h2>
                        <div
                            class="stats shadow bg-primary text-primary-content mb-6 w-full"
                        >
                            <div class="stat">
                                <div class="stat-value">
                                    <ClientOnly>
                                        {{
                                            currentQuestion?.question ||
                                            "問題を取得中です..."
                                        }}
                                    </ClientOnly>
                                </div>
                            </div>
                        </div>
                        <h2
                            class="card-title text-xl font-bold text-secondary mb-4"
                        >
                            スコア:
                        </h2>
                        <div
                            class="stats shadow bg-secondary text-secondary-content mb-6 w-full"
                        >
                            <div class="stat">
                                <div class="stat-value">
                                    <ClientOnly>
                                        {{ score }}
                                    </ClientOnly>
                                </div>
                            </div>
                        </div>
                        <h2
                            class="card-title text-xl font-bold text-accent mb-4"
                        >
                            現在の表情:
                        </h2>
                        <div
                            class="stats shadow bg-accent text-accent-content mb-6 w-full"
                        >
                            <div class="stat">
                                <div class="stat-value">
                                    <ClientOnly>
                                        {{
                                            emotion.show || "表情読み取り中..."
                                        }}
                                    </ClientOnly>
                                </div>
                            </div>
                        </div>
                        <p
                            class="text-sm text-gray-500"
                            style="font-family: Noto Sans JP"
                        >
                            お題をクリアすると、自動的に次の問題へ進みます。
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <footer
        v-if="mobile_nav_show"
        class="flex mobile_navbar fixed bottom-0 left-0 w-full bg-base-100 py-3 px-4 shadow-lg border-t border-gray-200"
    >
        <div class="container mx-auto text-center">
            <div class="mb-4">
                <h2 class="text-lg font-bold text-primary">問題:</h2>
                <div
                    class="stats shadow bg-primary text-primary-content w-full"
                >
                    <div class="stat">
                        <div class="stat-value text-xl">
                            {{
                                currentQuestion?.question ||
                                "問題を取得中です..."
                            }}
                        </div>
                    </div>
                </div>
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <h2 class="text-lg font-bold text-secondary">スコア:</h2>
                    <div
                        class="stats shadow bg-secondary text-secondary-content w-full"
                    >
                        <div class="stat">
                            <div class="stat-value text-xl">
                                {{ score }}
                            </div>
                        </div>
                    </div>
                </div>
                <div>
                    <h2 class="text-lg font-bold text-accent">現在の表情:</h2>
                    <div
                        class="stats shadow bg-accent text-accent-content w-full"
                    >
                        <div class="stat">
                            <div class="stat-value text-xl">
                                {{ emotion.show || "表情読み取り中..." }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </footer>
</template>
