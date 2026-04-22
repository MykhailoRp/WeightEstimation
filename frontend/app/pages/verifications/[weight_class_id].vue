<template>
  <UContainer class="pt-10">
    <VerificationCard :verification-id="weightClassId" />
  </UContainer>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: ['has-token']
})

const route = useRoute()
const weightClassId = computed(() => route.params.weight_class_id as string)
</script>
