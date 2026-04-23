<template>
  <UContainer class="pt-10">
    <UCard>
      <template #header>
        <div class="flex items-center justify-between gap-3">
          <h2 class="text-lg font-semibold">
            Users
          </h2>
          <span
            v-if="data"
            class="text-sm text-muted"
          >
            {{ data.total_count }} total
          </span>
        </div>
      </template>

      <div class="flex flex-col gap-3 sm:flex-row sm:items-end">
        <UFormField
          label="Email"
          class="flex-1"
        >
          <UInput
            v-model="emailLike"
            placeholder="Search by email"
            :icon="Search"
            class="w-full"
          />
        </UFormField>

        <UFormField
          label="Roles"
          class="sm:w-64"
        >
          <USelectMenu
            v-model="selectedRoles"
            :items="roleItems"
            multiple
            placeholder="All roles"
            class="w-full"
          />
        </UFormField>
      </div>

      <UTable
        :data="data?.items ?? []"
        :columns="columns"
        :loading="isLoading"
        class="mt-4 cursor-pointer"
        @select="(_e, row) => navigateTo(`/account/${row.original.id}`)"
      />

      <template #footer>
        <div class="flex justify-center">
          <UPagination
            v-model:page="page"
            :total="data?.total_count ?? 0"
            :items-per-page="pageSize"
          />
        </div>
      </template>
    </UCard>
  </UContainer>
</template>

<script setup lang="ts">
import { h, resolveComponent } from 'vue'
import { refDebounced } from '@vueuse/core'
import { Search } from '@lucide/vue'
import type { TableColumn } from '@nuxt/ui'
import type { UserDetailsResponse, UserRole } from '~/client'
import { getUsersListQuery } from '~/client/@pinia/colada.gen'
import { userRoleBadge } from '~/const/userRole'

definePageMeta({
  middleware: ['has-token']
})

const UBadge = resolveComponent('UBadge')

const pageSize = 10
const page = ref(1)
const emailLike = ref('')
const selectedRoles = ref<UserRole[]>([])

const roleItems: UserRole[] = ['CUSTOMER', 'ADMIN']

const debouncedEmailLike = refDebounced(emailLike, 300)

watch([debouncedEmailLike, selectedRoles], () => {
  page.value = 1
})

const { data, isLoading } = useQuery(() => ({
  ...getUsersListQuery({
    query: {
      page: page.value,
      size: pageSize,
      email_like: debouncedEmailLike.value || null,
      roles: selectedRoles.value.length ? selectedRoles.value : null
    }
  })
}))

const columns: TableColumn<UserDetailsResponse>[] = [
  {
    accessorKey: 'email',
    header: 'Email'
  },
  {
    accessorKey: 'email_verified',
    header: 'Verified',
    cell: ({ row }) => h(UBadge, {
      label: row.getValue('email_verified') ? 'Verified' : 'Unverified',
      color: row.getValue('email_verified') ? 'success' : 'error',
      variant: 'subtle',
      size: 'sm'
    })
  },
  {
    accessorKey: 'role',
    header: 'Roles',
    cell: ({ row }) => {
      const roles = row.getValue('role') as UserRole[]
      if (!roles.length) return '—'
      return h('div', { class: 'flex flex-wrap gap-1' }, roles.map(role =>
        h(UBadge, {
          label: role,
          color: userRoleBadge[role].color,
          variant: 'subtle',
          size: 'sm'
        })
      ))
    }
  },
  {
    accessorKey: 'created_at',
    header: 'Created',
    cell: ({ row }) => new Date(row.getValue('created_at')).toLocaleString('en-US', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    })
  }
]
</script>
