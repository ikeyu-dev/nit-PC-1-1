import { defineEventHandler } from "h3";

export default defineEventHandler(async () => {
    const BASE_API = useRuntimeConfig().public.BASE_API;
    try {
        const data = (await $fetch(`${BASE_API}health`)) as {
            status: string;
            message: string;
        };
        const seconds = new Date().getSeconds();
        console.log(
            `[${new Date().toLocaleString()}] backend-api: ${
                data.status
            }\n${"-".repeat(seconds)}`
        );
    } catch (error) {
        console.error(`[${new Date().toLocaleString()}] backend-api: ${error}`);
        throw createError({
            statusCode: 500,
            message: `server: ${error}`,
        });
    }
    return;
});
