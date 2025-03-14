import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
    state: () => ({
        name: "",
        email: "",
    }),
    actions: {
        setEmail(email) {
            this.email = email;
        },
        setName(name) {
            this.name = name;
        },
    },
});
