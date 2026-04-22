<template>
  <UCard>
    <template #header>
      <div
        v-if="data"
        class="flex items-center justify-between"
      >
        <div class="flex items-center gap-3">
          <p class="font-bold">
            {{ data.vehicle_identifier }}
          </p>
          <UBadge
            size="sm"
            variant="subtle"
            :color="badgeStatusColor[data.status]"
            :label="data.status"
          />
          <UBadge
            v-if="data.result"
            size="sm"
            variant="subtle"
            :color="badgeResultColor[data.result]"
            :label="data.result"
          />
        </div>
        <UButton
          size="sm"
          label="Back"
          :icon="ArrowLeft"
          variant="ghost"
          to="/verifications"
        />
      </div>
    </template>

    <div
      v-if="data"
      class="grid grid-cols-3 gap-3"
    >
      <Item variant="muted">
        <ItemHeader>
          Assigned
        </ItemHeader>
        <ItemContent>
          <ItemTitle>
            <UBadge
              size="sm"
              variant="subtle"
              :color="badgeResultColor[data.assigned]"
              :label="data.assigned"
            />
          </ItemTitle>
        </ItemContent>
      </Item>

      <Item variant="muted">
        <ItemHeader>
          Result
        </ItemHeader>
        <ItemContent>
          <ItemTitle>
            <UBadge
              v-if="data.result"
              size="sm"
              variant="subtle"
              :color="badgeResultColor[data.result]"
              :label="data.result"
            />
            <span v-else>—</span>
          </ItemTitle>
        </ItemContent>
      </Item>

      <Item variant="muted">
        <ItemHeader>
          Cost
        </ItemHeader>
        <ItemContent>
          <ItemTitle>
            {{ formatCost(data.processing_cost) }}
          </ItemTitle>
        </ItemContent>
      </Item>

      <Item variant="muted">
        <ItemHeader>
          Created
        </ItemHeader>
        <ItemContent>
          <ItemTitle>
            {{ formatDate(data.created_at) }}
          </ItemTitle>
        </ItemContent>
      </Item>

      <Item variant="muted">
        <ItemHeader>
          Updated
        </ItemHeader>
        <ItemContent>
          <ItemTitle>
            {{ formatDate(data.updated_at) }}
          </ItemTitle>
        </ItemContent>
      </Item>

      <Item variant="muted">
        <ItemHeader>
          Finished
        </ItemHeader>
        <ItemContent>
          <ItemTitle>
            {{ data.finished_at ? formatDate(data.finished_at) : '—' }}
          </ItemTitle>
        </ItemContent>
      </Item>
    </div>

    <template
      v-if="data?.video_url"
      #footer
    >
      <video
        :src="data.video_url"
        controls
        class="w-full rounded-md"
      />
    </template>
  </UCard>
</template>

<script setup lang="ts">
import { ArrowLeft } from '@lucide/vue'
import { getWeightClassificationDetailsQuery } from '~/client/@pinia/colada.gen'
import { badgeStatusColor, badgeResultColor } from '~/const/verificationBadge'

const props = defineProps<{
  verificationId: string
}>()

const { data } = useQuery({
  ...getWeightClassificationDetailsQuery({ path: { weight_class_id: props.verificationId } })
})

function formatDate(value: string) {
  return new Date(value).toLocaleString('en-US', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  })
}

function formatCost(cost: number | null) {
  if (cost == null) return '—'
  return new Intl.NumberFormat('en-UK', {
    style: 'currency',
    currency: 'UAH',
    minimumFractionDigits: 4
  }).format(cost)
}
</script>
