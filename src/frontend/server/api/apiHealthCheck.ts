import { defineEventHandler } from "h3";

export default defineEventHandler(async () => {
    const BASE_API = useRuntimeConfig().public.BASE_API;
    try {
        const data = (await $fetch(`${BASE_API}health`)) as {
            status: string;
            message: string;
        };
        console.log(new Date().toLocaleString(), data.status);
    } catch {
        throw createError({
            statusCode: 500,
        });
    }
});
