<template>
  <div class="flex flex-col items-center justify-center gap-4 p-4">
    <UPageCard class="w-full max-w-md">
      <UAuthForm
        :schema="schema"
        title="Sign Up"
        description="Create your account."
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
import { newUserMutation } from '~/client/@pinia/colada.gen'

const toast = useToast()
const router = useRouter()

const fields: AuthFormField[] = [
  {
    name: 'email',
    type: 'email',
    label: 'Email',
    placeholder: 'Enter your email',
    required: true
  },
  {
    name: 'password',
    label: 'Password',
    type: 'password',
    placeholder: 'Enter your password',
    required: true
  },
  {
    name: 'confirm_password',
    label: 'Comfirm Password',
    type: 'password',
    placeholder: 'Confirm your password',
    required: true
  }
]

const schema = z.object({
  email: z.email('Invalid email'),
  password: z.string('Password is required').min(8, 'Must be at least 8 characters'),
  confirm_password: z.string('Confirm is required')
}).refine(
  data => data.password === data.confirm_password,
  {
    message: 'Passwords must match',
    path: ['confirm_password']
  }
)

type Schema = z.output<typeof schema>

const { mutate: signUp, isLoading } = useMutation({
  ...newUserMutation(),
  onSuccess: async (data) => {
    console.log('Submitted', data)
    const userId = data?.user_id

    if (userId) {
      await router.push({
        name: 'sign-up-validate',
        query: { user_id: userId }
      })
    }
  },
  onError: (data) => {
    toast.add({
      description: data.detail?.map(item => item.msg).join(', ') || 'Request error'
    })
    console.log('Error', data)
  }
})

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  signUp({ body: payload.data })
}
</script>
