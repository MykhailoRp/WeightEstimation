import type { CreateClientConfig } from '~/client/client.gen'

export const createClientConfig: CreateClientConfig = (config) => {
  return {
    ...config,
    auth: () => {
      const token = useJWTCookie().value
      return token ? `Bearer ${token}` : undefined
    },
    baseUrl: 'http://localhost:8000'
  }
}