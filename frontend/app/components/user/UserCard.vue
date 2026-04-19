<template>
  <UCard>
    <template #header>
      <div class="flex gap-3">
        <p class="font-bold">
          mail@mail.com
        </p>
        <UBadge
          size="sm"
          variant="soft"
          color="info"
          label="CUSTOMER"
        />
      </div>
    </template>
    <div class="grid grid-cols-3 gap-3">
      <template v-if="data?.user">
        <Item variant="muted">
          <ItemHeader>
            Email
          </ItemHeader>
          <ItemContent>
            <ItemTitle>
              {{ data.user.email }}
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
            </ItemTitle>
          </ItemContent>
          <ItemActions v-if="data.user.id === token?.id">
            <UButton
              size="sm"
              :icon="Edit"
              variant="ghost"
            />
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

      <template v-if="data?.admin">
        <Item variant="muted">
          <ItemHeader>
            Promoted By
          </ItemHeader>
          <ItemContent>
            <ItemTitle>
              mail@mail.com
            </ItemTitle>
          </ItemContent>
          <ItemActions>
            <UButton
              size="sm"
              label="Details"
              :trailing-icon="ArrowRight"
              variant="outline"
              color="primary"
            />
          </ItemActions>
        </Item>
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
import { CheckCircle, Edit, Plus, ArrowRight, UserKey, CircleX, UserX2 } from '@lucide/vue'
import { getAccountDetailsQuery } from '~/client/@pinia/colada.gen'

const { data: token, isLoading: _isLoadingToken } = useToken()

const props = defineProps<{
  userId: string
}>()

const { data, error: _error, isLoading: _isLoading } = useQuery({
  ...getAccountDetailsQuery({ path: { account_id: props.userId } })
})
</script>
