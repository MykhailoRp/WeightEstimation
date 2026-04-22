<template>
  <UContainer class="pt-10">
    <UserCard :user-id="userId" />
  </UContainer>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: ['has-token']
})

const route = useRoute()
const userId = computed(() => route.params.user_id as string)
</script>
