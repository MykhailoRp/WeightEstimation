<template>
  <aside class="w-60 shrink-0 border-r border-default bg-elevated/30">
    <nav class="sticky top-[var(--ui-header-height,64px)] p-4 flex flex-col gap-6">
      <div
        v-for="section in sections"
        :key="section.label"
        class="flex flex-col gap-1"
      >
        <div class="px-2 text-xs font-semibold uppercase tracking-wider text-muted">
          {{ section.label }}
        </div>
        <UNavigationMenu
          orientation="vertical"
          :items="section.items"
          variant="pill"
          :ui="{ link: 'text-sm' }"
        />
      </div>
    </nav>
  </aside>
</template>

<script setup lang="ts">
import { User, ShieldCheck, KeyRound, FileText, Users } from '@lucide/vue'
import type { NavigationMenuItem } from '@nuxt/ui'

type Section = { label: string, items: NavigationMenuItem[] }

const { data: token } = useToken()

const sections = computed<Section[]>(() => {
  const out: Section[] = []

  if (!token.value) return out

  const userId = token.value.id
  const isCustomer = hasRole(token.value, 'CUSTOMER')
  const isAdmin = hasRole(token.value, 'ADMIN')

  out.push({
    label: 'Account',
    items: [
      { label: 'My account', icon: User, to: '/account' }
    ]
  })

  if (isCustomer) {
    out.push({
      label: 'Customer',
      items: [
        { label: 'Verifications', icon: ShieldCheck, to: '/verifications' },
        { label: 'API integrations', icon: KeyRound, to: `/integrations/${userId}` },
        { label: 'Invoices', icon: FileText, to: '/invoices' }
      ]
    })
  }

  if (isAdmin) {
    out.push({
      label: 'Admin',
      items: [
        { label: 'User list', icon: Users, to: '/users' }
      ]
    })
  }

  return out
})
</script>
