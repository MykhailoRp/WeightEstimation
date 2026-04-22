// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({

  modules: [
    'shadcn-nuxt',
    '@nuxt/eslint',
    '@nuxt/ui',
    '@pinia/colada-nuxt',
    '@pinia/nuxt'
  ],
  ssr: false,

  components: [
    {
      path: '~/components',
      pathPrefix: false
    }
  ],

  devtools: {
    enabled: false
  },

  css: ['~/assets/css/main.css'],

  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000',
      jwtCookie: 'jwt_token',
      sessionCookie: 'session_token',
      tokenDataCookie: 'token_data'
    }
  },

  routeRules: {
    '/': { prerender: true }
  },
  compatibilityDate: '2025-01-15',

  vite: {
    server: {
      hmr: true
    },
    optimizeDeps: {
      include: [
        'zod',
        '@lucide/vue',
        'clsx',
        'tailwind-merge',
        'class-variance-authority',
        '@vueuse/core',
        'lucide-vue-next'
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
  },

  shadcn: {
    prefix: '',
    componentDir: './components/ui'
  }
})
