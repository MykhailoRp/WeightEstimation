<template>
  <UContainer class="pt-10">
    <UCard>
      <template #header>
        <div class="flex items-center justify-between gap-3">
          <div class="flex items-center gap-3">
            <h2 class="text-lg font-semibold">
              API integration
            </h2>
            <span
              v-if="data"
              class="text-sm text-muted"
            >
              {{ data.total_count }} token{{ data.total_count === 1 ? '' : 's' }}
            </span>
          </div>
          <div class="flex items-center gap-2">
            <UButton
              label="Swagger docs"
              :trailing-icon="ExternalLink"
              variant="outline"
              :to="docsUrl"
              target="_blank"
            />
            <UButton
              label="New token"
              :icon="Plus"
              :loading="isCreating"
              :disabled="(data?.total_count ?? 0) >= MAX_TOKENS"
              @click="createToken"
            />
          </div>
        </div>
      </template>

      <ItemGroup
        v-if="data?.items.length"
        class="gap-3"
      >
        <Item
          v-for="item in data.items"
          :key="item.token"
          variant="muted"
        >
          <ItemContent>
            <ItemTitle class="font-mono text-xs break-all">
              {{ item.token }}
            </ItemTitle>
            <ItemDescription>
              Created {{ formatDate(item.created_at) }}
            </ItemDescription>
          </ItemContent>
          <ItemActions>
            <UButton
              size="sm"
              :icon="Copy"
              variant="ghost"
              :aria-label="`Copy token ${item.token}`"
              @click="copyToken(item.token)"
            />
            <UButton
              size="sm"
              :icon="Trash2"
              variant="ghost"
              color="error"
              :loading="deletingToken === item.token"
              :aria-label="`Delete token ${item.token}`"
              @click="deleteToken(item.token)"
            />
          </ItemActions>
        </Item>
      </ItemGroup>

      <div
        v-else-if="!isLoading"
        class="py-8 text-center text-sm text-muted"
      >
        No API tokens yet. Create one to get started.
      </div>
    </UCard>
  </UContainer>
</template>

<script setup lang="ts">
import { Plus, Copy, Trash2, ExternalLink } from '@lucide/vue'
import { useClipboard } from '@vueuse/core'
import {
  getApiTokenListQuery,
  createNewApiTokenMutation,
  deleteApiTokenMutation
} from '~/client/@pinia/colada.gen'

definePageMeta({
  middleware: ['has-token']
})

const _t = useToken()

const route = useRoute()
const toast = useToast()
const { copy } = useClipboard()

const userId = computed(() => route.params.user_id as string)

const docsUrl = computed(() => `${useRuntimeConfig().public.apiBase}/docs`)

const MAX_TOKENS = 5

const { data, isLoading, refetch } = useQuery(() => ({
  ...getApiTokenListQuery({
    query: {
      size: MAX_TOKENS,
      customer_ids: [userId.value]
    }
  }),
  staleTime: 0
}))

function reportError(err: unknown) {
  const detail = (err as { detail?: Array<{ msg: string }> | string }).detail
  toast.add({
    color: 'error',
    description: Array.isArray(detail)
      ? detail.map(item => item.msg).join(', ')
      : detail || 'Request error'
  })
}

const { mutateAsync: createTokenMutation, isLoading: isCreating } = useMutation({
  ...createNewApiTokenMutation()
})

async function createToken() {
  try {
    await createTokenMutation({ body: { customer_id: userId.value } })
    toast.add({ color: 'success', description: 'Token created' })
    await refetch()
  } catch (err) {
    reportError(err)
  }
}

const deletingToken = ref<string | null>(null)
const { mutateAsync: deleteTokenMutation } = useMutation({
  ...deleteApiTokenMutation()
})

async function deleteToken(token: string) {
  deletingToken.value = token
  try {
    await deleteTokenMutation({ path: { api_token: token } })
    toast.add({ color: 'success', description: 'Token deleted' })
    await refetch()
  } catch (err) {
    reportError(err)
  } finally {
    deletingToken.value = null
  }
}

async function copyToken(token: string) {
  try {
    await copy(token)
    toast.add({ color: 'success', description: 'Token copied to clipboard' })
  } catch {
    toast.add({ color: 'error', description: 'Failed to copy token' })
  }
}

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
</script>
