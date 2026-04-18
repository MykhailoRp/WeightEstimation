<template>
	<UCard>
		<template #header>
			<div class="flex gap-3">
				<p class="font-bold">mail@mail.com</p>
				<UBadge size="sm" variant="soft" color="info" label="CUSTOMER"/>
			</div>
		</template>
			<div class="grid grid-cols-3 gap-3">

				<Item variant="muted">
					<ItemHeader>
						Email
					</ItemHeader>
					<ItemContent>
						<ItemTitle>
							mail@mail.com
							<UBadge :leading-icon="CheckCircle" size="sm" label="Verified" variant="soft" color="success" />
						</ItemTitle>
					</ItemContent>
					<ItemActions>
						<UButton size="sm" :icon="Edit" variant="ghost" />
					</ItemActions>
				</Item>

				<Item variant="muted">
					<ItemHeader>
						Funds
					</ItemHeader>
					<ItemContent>
						<ItemTitle>
							$10.95
						</ItemTitle>
					</ItemContent>
					<ItemActions>
						<UButton size="sm" label="Deposit" :trailing-icon="Plus" variant="ghost" color="success" />
					</ItemActions>
				</Item>

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
						<UButton size="sm" label="Details" :trailing-icon="ArrowRight" variant="outline" color="primary" />
					</ItemActions>
				</Item>

			</div>

		<template #footer>
			<div class="grid grid-cols-3 gap-3">
				<NuxtLink to="account">
					<Item variant="outline" as="a">
							<ItemContent>
								<ItemTitle>
									Go to Verifications
								</ItemTitle>
							</ItemContent>
							<ItemActions>
								<UBadge size="md" :icon="ArrowRight" variant="soft" />
							</ItemActions>
					</Item>
				</NuxtLink>

				<Item variant="outline" as="a">
					<ItemContent>
						<ItemTitle>
							Go to Invoices
						</ItemTitle>
					</ItemContent>
					<ItemActions>
						<UBadge size="md" :icon="ArrowRight" variant="soft" />
					</ItemActions>
				</Item>

				<Item variant="outline" as="a">
					<ItemContent>
						<ItemTitle>
							Go to API integration
						</ItemTitle>
					</ItemContent>
					<ItemActions>
						<UBadge size="md" :icon="ArrowRight" variant="soft" />
					</ItemActions>
				</Item>

				<Item variant="outline">
					<ItemContent>
						<ItemTitle>
							Promote to Admin
						</ItemTitle>
					</ItemContent>
					<ItemActions>
						<UButton size="md" :trailing-icon="UserKey" variant="ghost" />
					</ItemActions>
				</Item>

			</div>
		</template>
	</UCard>
</template>


  
<script setup lang="ts">
import { CheckCircle, Edit, Plus, ArrowRight, UserKey } from '@lucide/vue';

</script>
