<template>
  <Dialog v-model:open="isDialogOpen">
    <DialogTrigger as-child>
      <UButton
        class="justify-center"
        label="Restore password"
        variant="outline"
      />
    </DialogTrigger>
    <DialogContent class-name="sm:max-w-sm">
      <DialogHeader>
        <DialogTitle>Restore your password</DialogTitle>
        <DialogDescription>We will send you a code to validate its you</DialogDescription>
      </DialogHeader>

      <UForm
        :schema="requestSchema"
        :state="requestState"
        class="space-y-4"
        @submit="request"
      >
        <UFormField
          label="Your email"
          name="email"
          class="w-full"
        >
          <UInput
            v-model="requestState.email"
            type="email"
            class="w-full"
            placeholder="your.email@mail.com"
          />
        </UFormField>

        <DialogFooter>
          <UButton
            label="Send code"
            type="submit"
            :loading="isRequesting"
          />
        </DialogFooter>
      </UForm>

      <UForm
        :schema="validateEmailSchema"
        :state="validateEmailState"
        class="space-y-4"
        @submit="set"
      >
        <UFormField
          label="New password"
          name="password"
        >
          <UInput
            v-model="validateEmailState.new_password"
            placeholder="Password"
            class="w-full"
            :type="show ? 'text' : 'password'"
            :ui="{ trailing: 'pe-1' }"
          >
            <template #trailing>
              <UButton
                color="neutral"
                variant="link"
                size="sm"
                :icon="show ? 'i-lucide-eye-off' : 'i-lucide-eye'"
                :aria-label="show ? 'Hide password' : 'Show password'"
                :aria-pressed="show"
                aria-controls="password"
                @click="show = !show"
              />
            </template>
          </UInput>
        </UFormField>
        <UFormField
          label="Validation code"
          name="code"
        >
          <UInput
            v-model="validateEmailState.code"
            class="w-full"
            placeholder="******"
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
            label="Save changes"
            :loading="isValidatingEmailReset"
          />
        </DialogFooter>
      </UForm>
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import * as z from 'zod'
import { requestPasswordResetMutation, setNewPasswordMutation } from '~/client/@pinia/colada.gen'
import type { FormSubmitEvent } from '@nuxt/ui'

const toast = useToast()

const show = ref(false)

const { mutate: requestPasswordReset, isLoading: isRequesting } = useMutation({
  ...requestPasswordResetMutation(),
  onError: (data) => {
    toast.add({
      color: 'error',
      description: Array.isArray(data.detail) ? data.detail?.map(item => item.msg).join(', ') : data.detail || 'Request error'
    })
    console.log('Error', data)
  }
})

const isDialogOpen = ref(false)
const { mutate: setNewPassword, isLoading: isValidatingEmailReset } = useMutation({
  ...setNewPasswordMutation(),
  onSuccess: () => {
    isDialogOpen.value = false
  },
  onError: (data) => {
    console.log('Error', data)
    toast.add({
      color: 'error',
      description: data.detail?.map(item => item.msg).join(', ') || 'Request error'
    })
    console.log('Error', data)
  }
})

const requestSchema = z.object({
  email: z.email('Invalid email')
})

const requestState = reactive({
  email: ''
})

type RequstSchema = z.output<typeof requestSchema>

function request(payload: FormSubmitEvent<RequstSchema>) {
  requestPasswordReset({ body: payload.data })
}

const validateEmailSchema = z.object({
  code: z
    .string()
    .min(12, 'Code must be 12 characters')
    .max(12, 'Code must be 12 characters'),

  new_password: z.string('New password is required').min(8, 'Must be at least 8 characters')
})

const validateEmailState = reactive({
  code: '',
  new_password: ''
})

type ValidateEmailSchema = z.output<typeof validateEmailSchema>

function set(payload: FormSubmitEvent<ValidateEmailSchema>) {
  setNewPassword({ body: payload.data })
}
</script>
