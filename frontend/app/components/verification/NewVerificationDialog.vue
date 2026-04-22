<template>
  <Dialog v-model:open="isDialogOpen">
    <DialogTrigger as-child>
      <UButton
        label="New verification"
        :icon="Plus"
      />
    </DialogTrigger>
    <DialogContent class-name="sm:max-w-md">
      <DialogHeader>
        <DialogTitle>New verification</DialogTitle>
        <DialogDescription>Upload a vehicle video to start a new weight verification</DialogDescription>
      </DialogHeader>

      <UForm
        :schema="schema"
        :state="state"
        class="space-y-4"
        @submit="submit"
      >
        <UFormField
          label="Vehicle identifier"
          name="vehicle_identifier"
          class="w-full"
        >
          <UInput
            v-model="state.vehicle_identifier"
            class="w-full"
            placeholder="e.g. AA1234BB"
          />
        </UFormField>

        <UFormField
          label="Assigned result"
          name="assigned"
          class="w-full"
        >
          <USelect
            v-model="state.assigned"
            class="w-full"
            :items="assignedItems"
          />
        </UFormField>

        <UFormField
          label="Video"
          name="file"
          class="w-full"
        >
          <UInput
            type="file"
            accept="video/*"
            class="w-full"
            @change="onFileChange"
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
import {
  uploadFileToTemporaryFolderMutation,
  newWeightClassificationMutation
} from '~/client/@pinia/colada.gen'
import type { WeightClassResult } from '~/client'

const toast = useToast()
const { data: token } = useToken()

const assignedItems: WeightClassResult[] = ['EMPTY', 'LOADED']

const isDialogOpen = ref(false)

const schema = z.object({
  vehicle_identifier: z.string().min(1, 'Vehicle identifier is required'),
  assigned: z.enum(['EMPTY', 'LOADED']),
  file: z.instanceof(File, { message: 'Video file is required' })
})

type Schema = z.output<typeof schema>

const state = reactive<{
  vehicle_identifier: string
  assigned: WeightClassResult
  file: File | undefined
}>({
  vehicle_identifier: '',
  assigned: 'EMPTY',
  file: undefined
})

const { mutateAsync: uploadFile } = useMutation({
  ...uploadFileToTemporaryFolderMutation()
})

const { mutateAsync: createVerification } = useMutation({
  ...newWeightClassificationMutation()
})

const isSubmitting = ref(false)

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  state.file = input.files?.[0]
}

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
  if (!token.value?.id) return

  isSubmitting.value = true
  try {
    const upload = await uploadFile({
      body: { file: payload.data.file }
    })

    const verification = await createVerification({
      body: {
        customer_id: token.value.id,
        file_id: upload.file_id,
        vehicle_identifier: payload.data.vehicle_identifier,
        assigned: payload.data.assigned
      }
    })

    isDialogOpen.value = false
    await navigateTo(`/verifications/${verification.id}`)
  } catch (err) {
    reportError(err)
  } finally {
    isSubmitting.value = false
  }
}
</script>
