<template>
  <UContainer class="pt-10">
    <VerificationCard :verification-id="weightClassId" />
  </UContainer>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: ['has-token']
})

const _t = useToken()

const route = useRoute()
const weightClassId = computed(() => route.params.weight_class_id as string)
</script>
