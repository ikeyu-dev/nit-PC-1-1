import { defineEventHandler, getQuery } from "h3";
import type { Questions } from "~/composables/questionInterface";

export default defineEventHandler(async (event) => {
    const uri = getQuery(event).uri as string;
    const BASE_API = useRuntimeConfig().public.BASE_API;
    try {
        const data = await $fetch<Questions>(`${BASE_API}${uri}`);
        console.log(new Date().toLocaleString(), data);
        return data;
    } catch (error) {
        throw createError({
            statusCode: 500,
            statusMessage: `問題の取得に失敗 : ${error}`,
        });
    }
});
