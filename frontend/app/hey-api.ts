import type { CreateClientConfig } from '~/client/client.gen'

export const createClientConfig: CreateClientConfig = (config) => {
  console.log(config)
  return {
    ...config,
    baseUrl: 'https://localhost:8000'
  }
}
