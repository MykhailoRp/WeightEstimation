import { defineConfig } from '@hey-api/openapi-ts'

export default defineConfig({
  input: 'openapi.json',
  output: {
    path: 'app/client',
    postProcess: ['prettier', 'eslint']
  },
  plugins: [
    {
      name: '@pinia/colada',
      mutationOptions: true
    },
    {
      name: '@hey-api/client-fetch',
      runtimeConfigPath: '~/hey-api'
    }
  ]
})
