<template>
  <div class="flex flex-col items-center justify-center gap-4 p-4">
    <UPageCard class="w-full max-w-md">
      <UAuthForm
        :schema="schema"
        title="Sign In"
        description="Enter your credentials to access your account."
        :icon="DoorOpen"
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
import { DoorOpen } from '@lucide/vue'
import { loginMutation } from '~/client/@pinia/colada.gen'

const fields: AuthFormField[] = [
  {
    name: 'username',
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
  }
]

const schema = z.object({
  username: z.email('Invalid email'),
  password: z.string('Password is required').min(8, 'Must be at least 8 characters')
})

type Schema = z.output<typeof schema>

const {mutate: login, isLoading} = useMutation({
  ...loginMutation(),
  onSuccess: (data) => {
    SetAuth(data.access_token, data.session, data.token_type)
  }
})

function onSubmit(payload: FormSubmitEvent<Schema>) {
  console.log('Submitted', payload)
  login({body: payload.data})
}
</script>
