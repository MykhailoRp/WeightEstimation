import type { BadgeProps } from '@nuxt/ui'
import type { InvoiceStatus } from '~/client'

export const badgeInvoiceStatusColor: Record<InvoiceStatus, BadgeProps['color']> = {
  PROCESSING: 'info',
  COMPLETED: 'success',
  FAILED: 'error'
}
