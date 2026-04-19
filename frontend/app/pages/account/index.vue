<template>
  <UContainer class="pt-10">
    <UserCard
      v-if="token?.id"
      :user-id="token.id"
    />
  </UContainer>
</template>

<script setup lang="ts">
const { data: token } = useToken()
</script>
