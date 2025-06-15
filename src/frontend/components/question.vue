<script setup lang="ts">
import { manageQuestion } from "~/composables/question";
import { judge } from "~/composables/judge";
import type { Question } from "~/composables/questionInterface";
import correctSound from "~/assets/music/correct.mp3";
import resultSound from "~/assets/music/result.mp3";
import { now } from "@vueuse/core";

const allQuestions = ref<Question[]>([]);
const currentQuestion = ref<Question | null>(null);
const score = ref<number | null>(20);

try {
    const question = await manageQuestion("get");
    if (question) {
        allQuestions.value = question;
        currentQuestion.value =
            question[Math.floor(Math.random() * question.length)] || null;
    }
} catch (error) {
    alert(`エラー : ${error}`);
}

const usePlaySound = () => {
    const correct = () => {
        const audio = new Audio(correctSound);
        audio.volume = 1;
        audio.play();
        score.value = (score.value || 0) + 10; // スコアを更新
    };
    const result = () => {
        const audio = new Audio(resultSound);
        audio.volume = 1;
        audio.play();
    };
    return { correct, result };
};

const jedgement = () => {};

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
    updateVisibility();
});
</script>

<template>
    <section
        v-if="pc_nav_show"
        class="flex justify-center items-center text-gray-600 body-font"
    >
        <div class="container px-5 pb-20 mx-auto">
            <div class="flex flex-col items-center m-2">
                <div
                    class="card w-full max-w-lg bg-base-100 shadow-xl rounded-lg border border-gray-200 m-5"
                >
                    <div
                        class="button card-body text-center p-6"
                        @click="usePlaySound().correct()"
                    >
                        <!-- <div class="card-body text-center p-6"> -->
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
                                    {{
                                        currentQuestion?.question ||
                                        "問題を取得中です..."
                                    }}
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
                                    {{ score || "スコアを取得中です..." }}
                                </div>
                            </div>
                        </div>
                        <p class="text-sm text-gray-500">
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
        <div class="container mx-auto flex flex-col items-center">
            <div class="text-center w-full">
                <h2 class="text-lg font-bold text-primary mb-2">問題:</h2>
                <div
                    class="stats shadow bg-primary text-primary-content mb-4 w-full"
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
                <h2 class="text-lg font-bold text-secondary mb-2">スコア:</h2>
                <div
                    class="stats shadow bg-secondary text-secondary-content w-full"
                >
                    <div class="stat">
                        <div class="stat-value text-xl">
                            {{ score || "スコアを取得中です..." }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </footer>
</template>
