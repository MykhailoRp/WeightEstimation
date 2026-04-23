<template>
  <UCard>
    <template #header>
      <div
        v-if="data?.user"
        class="flex gap-3"
      >
        <p class="font-bold">
          {{ data.user.email }}
        </p>
        <UBadge
          v-for="role in data?.user.role"
          :key="role"
          size="sm"
          variant="soft"
          :color="userRoleBadge[role].color"
          :label="role"
        />
      </div>
    </template>
    <div class="grid grid-cols-3 gap-3">
      <template v-if="data?.user">
        <Item variant="muted">
          <ItemHeader>
            Email

            <UBadge
              v-if="data.user.email_verified"
              :leading-icon="CheckCircle"
              size="sm"
              label="Verified"
              variant="soft"
              color="success"
            />
            <UBadge
              v-else
              :leading-icon="CircleX"
              size="sm"
              label="Unverified"
              variant="soft"
              color="error"
            />
          </ItemHeader>
          <ItemContent>
            <ItemTitle>
              {{ data.user.email }}
            </ItemTitle>
          </ItemContent>
          <ItemActions v-if="data.user.id === token?.id">
            <Dialog v-model:open="isDialogOpen">
              <DialogTrigger as-child>
                <UButton
                  size="sm"
                  :icon="Edit"
                  variant="ghost"
                />
              </DialogTrigger>
              <DialogContent class-name="sm:max-w-sm">
                <DialogHeader>
                  <DialogTitle>Change your email</DialogTitle>
                  <DialogDescription>We will send you a code to validate your new email</DialogDescription>
                </DialogHeader>

                <UForm
                  :schema="editEmailSchema"
                  :state="editEmailState"
                  class="space-y-4"
                  @submit="editEmail"
                >
                  <UFormField
                    label="New email"
                    name="new_email"
                    class="w-full"
                  >
                    <UInput
                      v-model="editEmailState.new_email"
                      class="w-full"
                      placeholder="your.email@mail.com"
                    />
                  </UFormField>

                  <DialogFooter>
                    <UButton
                      label="Send code"
                      type="submit"
                      :loading="isRequestingEmailReset"
                    />
                  </DialogFooter>
                </UForm>

                <UForm
                  :schema="validateEmailSchema"
                  :state="validateEmailState"
                  class="space-y-4"
                  @submit="validateEmail"
                >
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
          </ItemActions>
        </Item>
      </template>

      <template v-if="data?.customer">
        <Item variant="muted">
          <ItemHeader>
            Funds
          </ItemHeader>
          <ItemContent>
            <ItemTitle>
              {{ data.customer.funds }}
            </ItemTitle>
          </ItemContent>
          <ItemActions v-if="data.customer.id === token?.id">
            <UButton
              size="sm"
              label="Deposit"
              :trailing-icon="Plus"
              variant="ghost"
              color="success"
            />
          </ItemActions>
        </Item>
      </template>

      <template v-if="data?.admin?.promoted_by_id">
        <UserItem
          :user-id="data.admin.promoted_by_id"
          header="Promoted By"
        />
      </template>
    </div>

    <template #footer>
      <div class="grid grid-cols-3 gap-3">
        <template v-if="data?.customer">
          <NuxtLink to="account">
            <Item
              variant="outline"
              as="a"
            >
              <ItemContent>
                <ItemTitle>
                  Go to Verifications
                </ItemTitle>
              </ItemContent>
              <ItemActions>
                <UBadge
                  size="md"
                  :icon="ArrowRight"
                  variant="soft"
                />
              </ItemActions>
            </Item>
          </NuxtLink>

          <NuxtLink :to="`/invoices?user_id=${data.customer.id}`">
            <Item
              variant="outline"
              as="a"
            >
              <ItemContent>
                <ItemTitle>
                  Go to Invoices
                </ItemTitle>
              </ItemContent>
              <ItemActions>
                <UBadge
                  size="md"
                  :icon="ArrowRight"
                  variant="soft"
                />
              </ItemActions>
            </Item>
          </NuxtLink>

          <NuxtLink to="account">
            <Item
              variant="outline"
              as="a"
            >
              <ItemContent>
                <ItemTitle>
                  Go to API integration
                </ItemTitle>
              </ItemContent>
              <ItemActions>
                <UBadge
                  size="md"
                  :icon="ArrowRight"
                  variant="soft"
                />
              </ItemActions>
            </Item>
          </NuxtLink>
        </template>

        <template v-if="hasRole(token, 'ADMIN')">
          <Item
            v-if="data?.admin"
            variant="outline"
          >
            <ItemContent>
              <ItemTitle>
                Remove Admin role
              </ItemTitle>
            </ItemContent>
            <ItemActions>
              <UButton
                size="md"
                :trailing-icon="UserX2"
                variant="ghost"
              />
            </ItemActions>
          </Item>
          <Item
            v-else
            variant="outline"
          >
            <ItemContent>
              <ItemTitle>
                Promote to Admin
              </ItemTitle>
            </ItemContent>
            <ItemActions>
              <UButton
                size="md"
                :trailing-icon="UserKey"
                variant="ghost"
              />
            </ItemActions>
          </Item>
        </template>
      </div>
    </template>
  </UCard>
</template>

<script setup lang="ts">
import * as z from 'zod'
import { CheckCircle, Edit, Plus, ArrowRight, UserKey, CircleX, UserX2 } from '@lucide/vue'
import { getAccountDetailsQuery, requestEmailResetMutation, validateEmailResetMutation } from '~/client/@pinia/colada.gen'
import type { FormSubmitEvent } from '@nuxt/ui'
import { userRoleBadge } from '~/const/userRole'

const { data: token, isLoading: _isLoadingToken } = useToken()
const toast = useToast()

const props = defineProps<{
  userId: string
}>()

const { data, refresh, error: _error, isLoading: _isLoading } = useQuery({
  ...getAccountDetailsQuery({ path: { account_id: props.userId } })
})

const { mutate: requestEmailReset, isLoading: isRequestingEmailReset } = useMutation({
  ...requestEmailResetMutation(),
  onError: (data) => {
    toast.add({
      color: 'error',
      description: data.detail?.map(item => item.msg).join(', ') || 'Request error'
    })
    console.log('Error', data)
  }
})

const isDialogOpen = ref(false)
const { mutate: validateEmailReset, isLoading: isValidatingEmailReset } = useMutation({
  ...validateEmailResetMutation(),
  onSuccess: () => {
    refresh()
    isDialogOpen.value = false
  },
  onError: (data) => {
    toast.add({
      color: 'error',
      description: data.detail?.map(item => item.msg).join(', ') || 'Request error'
    })
    console.log('Error', data)
  }
})

const editEmailSchema = z.object({
  new_email: z.email('Invalid email')
})

const editEmailState = reactive({
  new_email: ''
})

type EditEmailSchema = z.output<typeof editEmailSchema>

function editEmail(payload: FormSubmitEvent<EditEmailSchema>) {
  requestEmailReset({ body: payload.data, path: { user_id: props.userId } })
}

const validateEmailSchema = z.object({
  code: z
    .string()
    .min(6, 'Code must be 6 characters')
    .max(6, 'Code must be 6 characters')
})

const validateEmailState = reactive({
  code: ''
})

type ValidateEmailSchema = z.output<typeof validateEmailSchema>

function validateEmail(payload: FormSubmitEvent<ValidateEmailSchema>) {
  validateEmailReset({ body: payload.data, path: { user_id: props.userId } })
}
</script>
