<script setup lang="ts">
import { useUserStore } from "~/composables/user";
import { getCookie } from "~/composables/cookie";
import type { User } from "~/types/user";
definePageMeta({
    layout: false,
});

const userStore = useUserStore();

onMounted(() => {
    if (userStore.user?.nickname !== "" && userStore.user !== null) {
        window.location.href = "/";
    }
});

const defineNewUser = () => {
    const newUserName = (
        document.getElementById("nickname") as HTMLInputElement
    ).value as string;
    const userStore = useUserStore();
    userStore.setUser({
        nickname: newUserName,
        score: 0,
    } as User);
};
const defineNewGuest = () => {
    const userStore = useUserStore();
    const randomId = Math.random().toString(36).substring(2, 10);
    userStore.setUser({
        nickname: `ゲスト-${randomId}`,
        score: 0,
    } as User);
};
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
                            新規ゲーム
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
                            />
                        </div>
                        <button
                            @click="defineNewUser()"
                            type="submit"
                            class="btn btn-primary w-full"
                        >
                            スタート
                        </button>
                        <button
                            @click="defineNewGuest()"
                            type="submit"
                            class="btn btn-link w-full"
                        >
                            ゲストとして開始
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </section>
</template>
