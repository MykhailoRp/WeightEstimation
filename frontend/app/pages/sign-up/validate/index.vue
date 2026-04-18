<template>
  <div class="flex flex-col items-center justify-center gap-4 p-4">
    <UPageCard class="w-full max-w-md">
      <UAuthForm
        :schema="schema"
        title="Verify OTP"
        description="Enter the 6-digit code sent to your email."
        :icon="Clipboard"
        :fields="fields"
        :loading="isLoading"
        @submit="onSubmit"
      />
    </UPageCard>
  </div>
</template>

<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent, AuthFormField } from '@nuxt/ui'
import { Clipboard } from '@lucide/vue'
import { validateNewUserMutation } from '~/client/@pinia/colada.gen'

const toast = useToast()
const route = useRoute()
const router = useRouter()

const user_id = route.query.user_id as string

const fields: AuthFormField[] = [
  {
    name: 'code',
    type: 'string',
    label: 'Verification code',
    placeholder: '******',
    required: true
  }
]

const schema = z.object({
  code: z
    .string()
    .min(6, 'Code must be 6 characters')
    .max(6, 'Code must be 6 characters')
})

type Schema = z.output<typeof schema>

const { mutate: validateNewUser, isLoading } = useMutation({
  ...validateNewUserMutation(),
  onSuccess: async (data) => {
    console.log('Submitted', data)

    toast.add({
      title: 'Verified',
      description: 'Your account has been created.'
    })

    await router.push('/sign-in')
  },
  onError: (data) => {
    toast.add({
      title: 'Verification failed',
      description: data.detail?.map(item => item.msg).join(', ') || 'Request error'
    })
    console.log('Error', data)
  }
})

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  if (!user_id) {
    toast.add({
      title: 'Error',
      description: 'Missing user session. Please sign up again.'
    })
    return
  }
  validateNewUser({ body: { user_id: user_id, code: payload.data.code } })
}
</script>
