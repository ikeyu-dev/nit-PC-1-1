import type { Questions } from "~/composables/questionInterface";

export async function manageQuestion(type: string) {
    const CREATE_QUESTION = useRuntimeConfig().public.CREATE_QUESTION;
    const DELETE_QUESTION = useRuntimeConfig().public.DELETE_QUESTION;
    const GET_ALL_QUESTION = useRuntimeConfig().public.GET_ALL_QUESTION;

    const uri =
        type === "get"
            ? GET_ALL_QUESTION
            : type === "create"
            ? CREATE_QUESTION
            : DELETE_QUESTION;

    const { data } = await useFetch<Questions>(`/api/question?uri=${uri}`);

    return data.value;
}
