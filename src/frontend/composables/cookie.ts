export function setCookie(name: string, value: string) {
    const date = new Date();
    date.setTime(date.getTime() + 3600 * 1000 * 3); //3600000[ms]
    const cookieExpires = "expires=" + date.toUTCString();
    document.cookie = `${name}=${value}; ${cookieExpires}; path=/`;
}

export function getCookie(name: string) {
    const cookie = document.cookie;
    const parts = cookie.split('; ');
    for (const part of parts) {
        if (part.startsWith(name + '=')) {
            return part.split('=')[1];
        }
    }
    return null;
}