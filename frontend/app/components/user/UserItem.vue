<template>
  <Item variant="muted">
    <ItemHeader v-if="header">
      {{ header }}
    </ItemHeader>
    <ItemContent>
      <ItemTitle>
        <template v-if="data?.user">
          {{ data.user.email }}
        </template>
        <template v-else>
          —
        </template>
      </ItemTitle>
    </ItemContent>
    <ItemActions v-if="data?.user">
      <UButton
        size="sm"
        label="Details"
        :trailing-icon="ArrowRight"
        variant="outline"
        color="primary"
        :to="`/account/${data.user.id}`"
      />
    </ItemActions>
  </Item>
</template>

<script setup lang="ts">
import { ArrowRight } from '@lucide/vue'
import { getAccountDetailsQuery } from '~/client/@pinia/colada.gen'

const props = defineProps<{
  userId: string
  header?: string
}>()

const { data } = useQuery({
  ...getAccountDetailsQuery({ path: { account_id: props.userId } })
})
</script>
