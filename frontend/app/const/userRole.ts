import type { BadgeProps } from "@nuxt/ui";
import type { UserRole } from "~/client";

export const userRoleBadge: Record<UserRole, {color: BadgeProps['color']}> = {
    CUSTOMER: {
        color: "info"
    },
    ADMIN: {
        color: "warning"
    },
};