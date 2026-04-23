<template>
  <UApp>
    <UHeader>
      <template #left>
        <NuxtLink
          to="/"
          :external="false"
        >
          <AppLogo class="w-auto h-6 shrink-0" />
        </NuxtLink>

        <TemplateMenu />
      </template>

      <template #right>
        <UButton
          v-if="!session"
          label="Sign In"
          to="sign-in"
          color="neutral"
          variant="outline"
          :external="false"
        />

        <UButton
          v-if="!session"
          label="Sign Up"
          to="sign-up"
          color="neutral"
          variant="solid"
          :external="false"
        />

        <UButton
          v-if="session"
          label="Sign Out"
          color="error"
          variant="outline"
          :loading="isLoggingout"
          @click="logoutClick"
        />

        <UColorModeButton />
      </template>
    </UHeader>

    <UMain>
      <div
        v-if="session"
        class="flex min-h-[calc(100vh-var(--ui-header-height,64px))]"
      >
        <AppSidebar />
        <div class="flex-1 min-w-0">
          <NuxtPage />
        </div>
      </div>
      <NuxtPage v-else />
    </UMain>

    <USeparator icon="i-simple-icons-nuxtdotjs" />

    <UFooter />
  </UApp>
</template>

<script setup>
import { logoutMutation } from './client/@pinia/colada.gen'

useHead({
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1' }
  ],
  link: [
    { rel: 'icon', href: '/favicon.ico' }
  ],
  htmlAttrs: {
    lang: 'en'
  }
})

const title = 'Nuxt Starter Template'
const description = 'A production-ready starter template powered by Nuxt UI. Build beautiful, accessible, and performant applications in minutes, not hours.'

useSeoMeta({
  title,
  description,
  ogTitle: title,
  ogDescription: description,
  ogImage: 'https://ui.nuxt.com/assets/templates/nuxt/starter-light.png',
  twitterCard: 'summary_large_image'
})

const session = useSessionCookie()

const { mutate: logout, isLoading: isLoggingout } = useMutation({
  ...logoutMutation(),
  onSuccess: () => {
    ClearAuth()
    navigateTo('/')
  },
  onError: () => {
    ClearAuth()
    navigateTo('/')
  }
})

function logoutClick() {
  if (session.value) {
    logout({ body: { session: session.value } })
  }
}
</script>
