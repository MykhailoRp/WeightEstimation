import { getMe, refreshToken, type TokenData, type UserRole } from '~/client'

export const useJWTCookie = () => useCookie(useRuntimeConfig().public.jwtCookie)
export const useSessionCookie = () => useCookie(useRuntimeConfig().public.sessionCookie)
export const useTokenDataCookie = () => useCookie<TokenData | null>(useRuntimeConfig().public.tokenDataCookie, { default: () => null })

export function SetAuth(jwt_token: string, session_token: string, token_data: TokenData) {
  useJWTCookie().value = `${jwt_token}`
  useSessionCookie().value = session_token
  useTokenDataCookie().value = token_data
}

export const useToken = () => {
  const sessionCookie = useSessionCookie()
  const tokenDataCookie = useTokenDataCookie()

  return useQuery({
    key: ['me'],
    staleTime: 60_000,
    query: async () => {
      const meResult = await getMe()

      if (meResult.response.status !== 401) {
        tokenDataCookie.value = meResult.data!
        return meResult.data!
      }

      const session = sessionCookie.value
      const userId = tokenDataCookie.value?.id

      if (!userId || !session) {
        await navigateTo('/sign-in')
        throw new Error('Unauthenticated')
      }

      const refreshResult = await refreshToken({
        body: { user_id: userId, session }
      })

      if (refreshResult.response.status !== 200 || !refreshResult.data) {
        await navigateTo('/sign-in')
        throw new Error('Unauthenticated')
      }

      SetAuth(refreshResult.data.access_token, session, refreshResult.data.data)

      let i = 0
      let retryResult = await getMe()
      while (!retryResult.data && i < 3) {
        retryResult = await getMe()
        i++
      };
      tokenDataCookie.value = retryResult.data!
      return retryResult.data!
    }
  })
}

export function hasRole(token: TokenData | undefined, r: UserRole) {
  if (token) return token.role.includes(r)
  return false
}
