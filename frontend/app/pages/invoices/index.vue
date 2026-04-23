<template>
  <UContainer class="pt-10">
    <UCard>
      <template #header>
        <div class="flex items-center justify-between gap-3">
          <h2 class="text-lg font-semibold">
            Invoices
          </h2>
          <div class="flex items-center gap-3">
            <span
              v-if="data"
              class="text-sm text-muted"
            >
              {{ data.total_count }} total
            </span>
            <NewInvoiceDialog
              :default-customer-id="userId"
              @created="refetch"
            />
          </div>
        </div>
      </template>

      <UFormField
        label="User id"
        class="sm:w-96"
      >
        <UInput
          v-model="userId"
          placeholder="Filter by user id"
          :icon="Search"
          class="w-full"
        />
      </UFormField>

      <UTable
        :data="data?.items ?? []"
        :columns="columns"
        :loading="isLoading"
        class="mt-4"
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
import { Search, ExternalLink } from '@lucide/vue'
import type { TableColumn } from '@nuxt/ui'
import type { Invoice } from '~/client'
import { getInvoicesListQuery } from '~/client/@pinia/colada.gen'
import { badgeInvoiceStatusColor } from '~/const/invoiceBadge'

definePageMeta({
  middleware: ['has-token']
})

const UBadge = resolveComponent('UBadge')
const UButton = resolveComponent('UButton')

const route = useRoute()
const router = useRouter()

const pageSize = 10
const page = ref(1)
const userId = ref((route.query.user_id as string | undefined) ?? '')

const debouncedUserId = refDebounced(userId, 300)

watch(debouncedUserId, (value) => {
  page.value = 1
  router.replace({ query: { ...route.query, user_id: value || undefined } })
})

const { data, isLoading, refetch } = useQuery(() => ({
  ...getInvoicesListQuery({
    query: {
      page: page.value,
      size: pageSize,
      customer_ids: debouncedUserId.value ? [debouncedUserId.value] : null
    }
  })
}))

const columns: TableColumn<Invoice>[] = [
  {
    accessorKey: 'id',
    header: 'Id',
    cell: ({ row }) => h('span', { class: 'font-mono text-xs' }, row.getValue('id'))
  },
  {
    accessorKey: 'customer_id',
    header: 'Customer',
    cell: ({ row }) => h('span', { class: 'font-mono text-xs' }, row.getValue('customer_id'))
  },
  {
    accessorKey: 'amount',
    header: 'Amount',
    meta: { class: { th: 'text-right', td: 'text-right font-medium' } },
    cell: ({ row }) => {
      const amount = row.getValue('amount') as number
      const currency = row.original.currency
      return `${amount.toFixed(2)} ${currency}`
    }
  },
  {
    accessorKey: 'status',
    header: 'Status',
    cell: ({ row }) => h(UBadge, {
      label: row.getValue('status'),
      color: badgeInvoiceStatusColor[row.getValue('status') as keyof typeof badgeInvoiceStatusColor],
      variant: 'subtle',
      size: 'sm'
    })
  },
  {
    accessorKey: 'reason',
    header: 'Reason',
    cell: ({ row }) => (row.getValue('reason') as string | null) ?? '—'
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
  },
  {
    accessorKey: 'finished_at',
    header: 'Finished',
    cell: ({ row }) => {
      const val = row.getValue('finished_at') as string | null
      if (!val) return '—'
      return new Date(val).toLocaleString('en-US', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      })
    }
  },
  {
    accessorKey: 'invoice_url',
    header: 'Link',
    cell: ({ row }) => h(UButton, {
      icon: ExternalLink,
      size: 'xs',
      variant: 'ghost',
      to: row.getValue('invoice_url'),
      target: '_blank'
    })
  }
]
</script>
