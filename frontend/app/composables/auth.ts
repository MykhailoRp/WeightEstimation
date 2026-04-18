
export const useJWTCookie = () => useCookie(useRuntimeConfig().public.jwtCookie)
export const useSessionCookie = () => useCookie(useRuntimeConfig().public.sessionCookie)

export function SetAuth(jwt_token: string, session_token: string, token_type?: string) {
    useJWTCookie().value = `${token_type ?? 'Bearer'} ${jwt_token}`;
    useSessionCookie().value = session_token;
}