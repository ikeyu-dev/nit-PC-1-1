<script setup lang="ts">
const error = useError();
</script>

<template>
    <div
        class="flex flex-col flex-wrap items-center justify-center min-h-screen"
    >
        <section>
            <div class="p-5">
                <h1 class="text-6xl font-bold text-blue-500 text-center">
                    {{ error?.statusCode }}
                </h1>
                <p class="text-gray-500 text-center mt-4">
                    {{
                        error?.statusCode === 404
                            ? "お探しのページは見つかりませんでした。"
                            : "エラーが発生しました。"
                    }}
                </p>
            </div>
            <section class="flex flex-col text-center items-center">
                <nuxt-link
                    to="/"
                    class="w-1/2 py-3 m-3 px-5 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
                >
                    ホーム画面へ
                </nuxt-link>
            </section>
        </section>
    </div>
</template>
