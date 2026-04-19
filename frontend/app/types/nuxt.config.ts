declare module 'nuxt/schema' {
  interface RuntimeConfig {
    apiSecret: string
  }

  interface PublicRuntimeConfig {
    apiBase: string
    jwtCookie: string
    sessionCookie: string
    tokenDataCookie: string
  }
}

export {}
