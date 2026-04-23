<template>
  <svg
    width="1020"
    height="200"
    viewBox="0 0 1020 200"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <!-- Wall mount plate -->
    <rect
      x="34"
      y="20"
      width="64"
      height="14"
      rx="3"
      fill="currentColor"
    />
    <!-- Mount arm -->
    <rect
      x="58"
      y="34"
      width="16"
      height="30"
      fill="currentColor"
    />

    <!-- Camera body -->
    <path
      d="M 14 72 H 196 A 44 44 0 0 1 196 160 H 14 A 10 10 0 0 1 4 150 V 82 A 10 10 0 0 1 14 72 Z"
      fill="var(--ui-primary)"
    />

    <!-- Record LED indicator at back -->
    <circle
      cx="32"
      cy="116"
      r="7"
      fill="currentColor"
    />

    <!-- Lens housing ring -->
    <circle
      cx="204"
      cy="116"
      r="34"
      fill="currentColor"
    />
    <!-- Lens glass -->
    <circle
      cx="204"
      cy="116"
      r="22"
      fill="var(--ui-primary)"
    />
    <!-- Lens pupil -->
    <circle
      cx="204"
      cy="116"
      r="9"
      fill="currentColor"
    />
    <!-- Lens highlight -->
    <circle
      cx="211"
      cy="108"
      r="3"
      fill="var(--ui-primary)"
    />

    <!-- Wordmark: VizWeight -->
    <text
      x="288"
      y="152"
      font-family="ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
      font-size="132"
      font-weight="800"
      letter-spacing="-5"
      fill="currentColor"
    >
      <tspan fill="var(--ui-primary)">Viz</tspan><tspan>Weight</tspan>
    </text>
  </svg>
</template>
