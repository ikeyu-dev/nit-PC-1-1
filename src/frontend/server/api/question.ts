import { defineEventHandler, getQuery } from "h3";
import type { Questions } from "~/composables/questionInterface";

export default defineEventHandler(async (event) => {
    const uri = getQuery(event).uri as string;
    const BASE_API = useRuntimeConfig().public.BASE_API;
    const data = await $fetch<Questions>(`${BASE_API}${uri}`);
    return data;
});
