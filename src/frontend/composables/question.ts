export async function getAllQuestion() {
    const GET_ALL_QUESTION = useRuntimeConfig().public.GET_ALL_QUESTION;
    const allQuestion = await useFetch(`/api/${GET_ALL_QUESTION}`);
    return allQuestion.data.value;
}
