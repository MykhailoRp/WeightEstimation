<template>
  <UContainer class="pt-10">
    <UCard>
      <template #header>
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-semibold">
            Weight Verifications
          </h2>
          <span
            v-if="data"
            class="text-sm text-muted"
          >
            {{ data.total_count }} total
          </span>
        </div>
      </template>

      <UTable
        :data="data?.items ?? []"
        :columns="columns"
        :loading="isLoading"
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
import type { TableColumn } from '@nuxt/ui'
import type { WeightClassificationItem } from '~/client'
import { getWeightClassificationListQuery } from '~/client/@pinia/colada.gen'
import { badgeStatusColor, badgeResultColor } from '~/const/verificationBadge'

definePageMeta({
  middleware: ['has-token']
})

const UBadge = resolveComponent('UBadge')

const pageSize = 10
const page = ref(1)

const { data, isLoading } = useQuery(() => ({
  ...getWeightClassificationListQuery({
    query: { page: page.value, size: pageSize }
  })
}))

const columns: TableColumn<WeightClassificationItem>[] = [
  {
    accessorKey: 'vehicle_identifier',
    header: 'Vehicle'
  },
  {
    accessorKey: 'status',
    header: 'Status',
    cell: ({ row }) => h(UBadge, {
      label: row.getValue('status'),
      color: badgeStatusColor[row.getValue('status') as keyof typeof badgeStatusColor],
      variant: 'subtle',
      size: 'sm'
    })
  },
  {
    accessorKey: 'result',
    header: 'Result',
    cell: ({ row }) => {
      const result = row.getValue('result') as string | null
      if (!result) return '—'
      return h(UBadge, {
        label: result,
        color: badgeResultColor[result as keyof typeof badgeResultColor],
        variant: 'subtle',
        size: 'sm'
      })
    }
  },
  {
    accessorKey: 'processing_cost',
    header: 'Cost',
    meta: { class: { th: 'text-right', td: 'text-right font-medium' } },
    cell: ({ row }) => {
      const cost = row.getValue('processing_cost') as number | null
      if (cost == null) return '—'
      return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 4 }).format(cost)
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
  }
]
</script>
