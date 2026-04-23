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
      </template>

      <AppSidebar />

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

      <template #body>
        <AppSidebar
          orientation="vertical"
          class="-mx-2.5"
        />
      </template>
    </UHeader>

    <UMain>
      <NuxtLayout>
        <NuxtPage />
      </NuxtLayout>
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

const title = 'VizWeight — Visual Vehicle Weight Identification API'
const description = 'VizWeight is a SaaS platform providing API-driven vehicle weight identification from visual characteristics, with specialized tire-based analysis.'

useSeoMeta({
  title,
  description,
  ogTitle: title,
  ogDescription: description,
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
