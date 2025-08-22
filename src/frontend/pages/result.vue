<script setup lang="ts">
import { useScoreStore } from "~/composables/score";
import { useUserStore } from "~/composables/user";

const scoreStore = useScoreStore();
const userStore = useUserStore();

const score = computed(() => scoreStore.score) ? scoreStore.score : 0;
const nickname = computed(() => userStore.user?.nickname);

const resetGame = () => {
    scoreStore.clearScore();
    userStore.clearUser();
};

onMounted(() => {
    if (!userStore.user?.nickname) {
        window.location.href = "/newGame";
    }
});

definePageMeta({
    layout: false,
});
</script>

<template>
    <section class="bg-base-200">
        <div
            class="flex flex-col items-center justify-center px-4 py-8 mx-auto lg:py-0"
            style="height: 100svh"
        >
            <div
                class="w-full max-w-xs md:max-w-md bg-base-100 rounded-lg shadow-xl"
            >
                <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
                    <div class="flex flex-row items-center mb-6 space-x-4">
                        <img
                            class="w-16 h-16"
                            src="~/assets/img/logo.svg"
                            alt="Logo"
                        />
                        <p
                            class="text-2xl font-bold leading-tight tracking-tight text-neutral md:text-3xl"
                        >
                            ゲームリザルト
                        </p>
                    </div>
                    <form
                        class="space-y-4 md:space-y-6"
                        method="post"
                    >
                        <div class="form-control">
                            <label
                                for="nickname"
                                class="label"
                            >
                                <span class="label-text">ニックネーム</span>
                            </label>
                            <input
                                type="text"
                                name="nickname"
                                id="nickname"
                                class="input input-bordered w-full"
                                placeholder="ニックネームを入力"
                                autocomplete="nickname"
                                :value="nickname"
                                readonly
                            />
                        </div>
                        <div class="form-control">
                            <label
                                for="score"
                                class="label"
                            >
                                <span class="label-text">スコア</span>
                            </label>
                            <input
                                type="number"
                                name="score"
                                id="score"
                                class="input input-bordered w-full"
                                placeholder="スコアを表示"
                                autocomplete="score"
                                :value="score"
                                readonly
                            />
                        </div>
                        <button
                            @click="resetGame()"
                            type="submit"
                            class="btn btn-primary w-full"
                        >
                            終了
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </section>
</template>
