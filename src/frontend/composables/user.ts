import { ref } from "vue";
import { defineStore } from "pinia";
import type { User } from "../types/user";

export const useUserStore = defineStore(
    "nickname",
    () => {
        const user = ref<User | null>(null);
        function setUser(newuser: User) {
            user.value = newuser;
            console.log(user.value);
        }
        function clearUser() {
            user.value = null;
        }
        return { user, setUser, clearUser };
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
