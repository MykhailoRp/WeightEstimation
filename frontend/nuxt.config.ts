// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({

  compatibilityDate: '2025-01-15',

  modules: [
    '@nuxt/eslint',
    '@nuxt/ui',
    '@pinia/colada-nuxt',
    '@pinia/nuxt'
  ],

  devtools: {
    enabled: false
  },

  css: ['~/assets/css/main.css'],

  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000'
    }
  },

  routeRules: {
    '/': { prerender: true }
  },

  vite: {
    server: {
      hmr: true
    },
    optimizeDeps: {
      include: [
        'zod',
        '@lucide/vue'
      ]
    }
  },

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  }
})
