import type { BadgeProps } from '@nuxt/ui'
import type { WeightClassStatus, WeightClassResult } from '~/client'

export const badgeStatusColor: Record<WeightClassStatus, BadgeProps['color']> = {
  PENDING: 'neutral',
  FRAMES_SPLIT: 'info',
  MASKS_EXTRACTED: 'info',
  FEATURES_EXTRACTED: 'info',
  COMPLETED: 'success'
}

export const badgeResultColor: Record<WeightClassResult, BadgeProps['color']> = {
  EMPTY: 'info',
  LOADED: 'warning'
}
