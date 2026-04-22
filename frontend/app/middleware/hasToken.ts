export default defineNuxtRouteMiddleware(() => {
  const token = useTokenDataCookie()

  console.log(token.value)

  if (token.value === null) {
    return navigateTo('/sign-in')
  }
})
