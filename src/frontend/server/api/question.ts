import { defineEventHandler, getQuery } from "h3";
import type { Questions } from "~/types/question";

export default defineEventHandler(async (event) => {
    const uri = getQuery(event).uri as string;
    const BASE_API = useRuntimeConfig().public.BASE_API;
    try {
        const data = await $fetch<Questions>(`${BASE_API}${uri}`);
        console.log(
            `[${new Date().toLocaleString()}] questions: ${JSON.stringify(
                data
            )}`
        );
        return data;
    } catch (error) {
        console.error(`[${new Date().toLocaleString()}]: ${error}`);
        throw createError({
            statusCode: 500,
            message: `server: ${error}`,
        });
    }
});
