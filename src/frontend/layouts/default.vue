<template>
    <header class="header text-gray-600 body-font sticky top-0">
        <div
            class="contaier mx-auto flex flex-wrap p-0 flex-col md:flex-row items-center"
        >
            <div class="flex">
                <img
                    class="h-40 w-40"
                    src="~/assets/img/logo.svg"
                    alt="logo"
                    id="logo"
                />
            </div>
        </div>
    </header>
    <slot />
</template>
