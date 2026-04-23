<template>
  <div>
    <UPageHero
      title="Weigh vehicles with a single image."
      description="VizWeight is a SaaS platform that identifies vehicle weight from visual characteristics — specializing in tire-based analysis. Integrate accurate, instant weight estimation into your stack with a single API call."
      :links="[{
        label: 'Get started',
        to: '/sign-up',
        trailingIcon: 'i-lucide-arrow-right',
        size: 'xl'
      }, {
        label: 'Sign in',
        to: '/sign-in',
        size: 'xl',
        color: 'neutral',
        variant: 'subtle'
      }]"
    />

    <UPageSection
      id="features"
      title="Computer vision built for weight estimation"
      description="Drop VizWeight into your existing systems — from tollway enforcement to logistics yards — and turn a camera feed into structured weight data."
      :features="[{
        icon: 'i-lucide-cctv',
        title: 'Camera-ready ingestion',
        description: 'Accepts frames from CCTV, ANPR, and inspection cameras. Works with single-shot images or live streams.'
      }, {
        icon: 'i-lucide-scan-eye',
        title: 'Tire-based identification',
        description: 'Our models read tire geometry, tread deflection, sidewall profile, and axle configuration to infer vehicle weight.'
      }, {
        icon: 'i-lucide-code-2',
        title: 'Simple REST API',
        description: 'Authenticate with an API key, POST an image, get a weight estimate back. Predictable schemas, typed SDKs, zero guesswork.'
      }, {
        icon: 'i-lucide-gauge',
        title: 'Low-latency inference',
        description: 'Sub-second responses on standard payloads, so VizWeight keeps up with real-time checkpoints and enforcement flows.'
      }, {
        icon: 'i-lucide-shield-check',
        title: 'Privacy-first processing',
        description: 'Imagery is processed in isolated tenants, never used for training, and purged on a schedule you control.'
      }, {
        icon: 'i-lucide-bar-chart-3',
        title: 'Usage & billing built in',
        description: 'Track requests, monitor accuracy, manage API keys, and download invoices straight from your dashboard.'
      }]"
    />

    <UPageSection>
      <UPageCTA
        title="Ready to turn cameras into scales?"
        description="Create an account, grab an API key, and start weighing vehicles from imagery in minutes."
        variant="subtle"
        :links="[{
          label: 'Create account',
          to: '/sign-up',
          trailingIcon: 'i-lucide-arrow-right',
          color: 'neutral'
        }, {
          label: 'Sign in',
          to: '/sign-in',
          color: 'neutral',
          variant: 'outline'
        }]"
      />
    </UPageSection>
  </div>
</template>
