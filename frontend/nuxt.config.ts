// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({

  compatibilityDate: '2025-01-15',
  
  components: [
    {
      path: '~/components',
      pathPrefix: false
    }
  ],

  modules: [
    'shadcn-nuxt',
    '@nuxt/eslint',
    '@nuxt/ui',
    '@pinia/colada-nuxt',
    '@pinia/nuxt'
  ],

  routeRules: {
    '/': { prerender: true }
  },

  devtools: {
    enabled: false
  },

  css: ['~/assets/css/main.css'],

  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000',
      jwtCookie: 'jwt_token',
      sessionCookie: 'session_token',
    }
  },

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
