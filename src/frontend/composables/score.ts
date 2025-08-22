import { ref } from "vue";
import { defineStore } from "pinia";

export const useScoreStore = defineStore(
    "score",
    () => {
        const score = ref<number | null>(null);
        function setScore(newscore: number) {
            score.value = newscore;
            console.log(score.value);
        }
        function clearScore() {
            score.value = null;
        }
        return { score, setScore, clearScore };
    },
    {
        persist: {
            storage: piniaPluginPersistedstate.cookies({
                sameSite: "strict",
                maxAge: 60 * 60 * 3,
            }),
        },
    }
);
