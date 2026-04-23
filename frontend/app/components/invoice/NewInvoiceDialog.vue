<template>
  <Dialog v-model:open="isDialogOpen">
    <DialogTrigger as-child>
      <UButton
        label="New invoice"
        :icon="Plus"
      />
    </DialogTrigger>
    <DialogContent class-name="sm:max-w-md">
      <DialogHeader>
        <DialogTitle>New invoice</DialogTitle>
        <DialogDescription>Request a new invoice for the specified amount</DialogDescription>
      </DialogHeader>

      <UForm
        :schema="schema"
        :state="state"
        class="space-y-4"
        @submit="submit"
      >
        <UFormField
          label="Amount"
          name="amount"
          class="w-full"
        >
          <UInput
            v-model.number="state.amount"
            type="number"
            step="0.01"
            min="0"
            class="w-full"
            placeholder="0.00"
          />
        </UFormField>

        <DialogFooter>
          <DialogClose as-child>
            <UButton
              variant="outline"
              label="Cancel"
            />
          </DialogClose>
          <UButton
            type="submit"
            label="Create"
            :loading="isSubmitting"
          />
        </DialogFooter>
      </UForm>
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import * as z from 'zod'
import { Plus } from '@lucide/vue'
import type { FormSubmitEvent } from '@nuxt/ui'
import { createNewInvoiceMutation } from '~/client/@pinia/colada.gen'

const { data: token, isLoading: _isLoadingToken } = useToken()

const emit = defineEmits<{
  created: []
}>()

const toast = useToast()

const isDialogOpen = ref(false)

const schema = z.object({
  amount: z.number().positive('Amount must be greater than 0')
})

type Schema = z.output<typeof schema>

const state = reactive<{
  amount: number | undefined
}>({
  amount: undefined
})

const { mutateAsync: createInvoice, isLoading: isSubmitting } = useMutation({
  ...createNewInvoiceMutation()
})

function reportError(err: unknown) {
  const detail = (err as { detail?: Array<{ msg: string }> | string }).detail
  toast.add({
    color: 'error',
    description: Array.isArray(detail)
      ? detail.map(item => item.msg).join(', ')
      : detail || 'Request error'
  })
}

async function submit(payload: FormSubmitEvent<Schema>) {
  try {
    if (token.value) {
      await createInvoice({
        body: {
          customer_id: token.value?.id,
          amount: payload.data.amount
        }
      })
      toast.add({ color: 'success', description: 'Invoice created' })
      emit('created')
      isDialogOpen.value = false
      state.amount = undefined
    }
  } catch (err) {
    reportError(err)
  }
}
</script>
