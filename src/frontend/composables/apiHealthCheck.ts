export async function apiHealthCheck() {
    await $fetch(`/api/apiHealthCheck`);
    return;
}
