export default defineNuxtRouteMiddleware(() => {
  const token = useTokenDataCookie()

  if (token.value !== null) {
    return navigateTo('/account')
  }
})
