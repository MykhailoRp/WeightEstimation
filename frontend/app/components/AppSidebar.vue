<template>
  <UNavigationMenu
    orientation="vertical"
    :items="sections"
    variant="pill"
    :ui="{ link: 'text-sm' }"
  />
</template>

<script setup lang="ts">
import { User, ShieldCheck, KeyRound, FileText, Users } from '@lucide/vue'
import type { NavigationMenuItem } from '@nuxt/ui'

const { data: token } = useToken()

const sections = computed<NavigationMenuItem[]>(() => {
  const out: NavigationMenuItem[] = []

  if (!token.value) return out

  const userId = token.value.id
  const isCustomer = hasRole(token.value, 'CUSTOMER')
  const isAdmin = hasRole(token.value, 'ADMIN')

  out.push({ label: 'My account', icon: User, to: '/account' })

  if (isCustomer) {
    out.push({ label: 'Verifications', icon: ShieldCheck, to: '/verifications' })
    out.push({ label: 'API integrations', icon: KeyRound, to: `/integrations/${userId}` })
    out.push({ label: 'Invoices', icon: FileText, to: '/invoices' })
  }

  if (isAdmin) {
    out.push({ label: 'User list', icon: Users, to: '/users' })
  }

  return out
})
</script>
