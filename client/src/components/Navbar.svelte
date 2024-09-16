<script lang="ts">
	import AuthLinks from '$c/auth/AuthLinks.svelte';
	import { auth } from '$s/auth';
	import CtsLogo from './Icons/CtsLogo.svelte';

	$: user = $auth.user;
</script>

<header
	class="mb-2 drop-shadow flex flex-wrap sm:justify-start sm:flex-nowrap z-50 w-full bg-white text-sm py-4 dark:bg-gray-800"
>
	<nav
		class="max-w-[85rem] w-full mx-auto px-4 sm:flex sm:items-center sm:justify-between"
		aria-label="Global"
	>
		<div class="flex flex-row items-center mt-5 sm:justify-end sm:mt-0 sm:pl-5">
			<!-- <img src="../images/cts_logo1.jpeg" class="me-3 h-6 w-auto sm:h-9" alt="DocketAI Logo" /> -->
			 <CtsLogo/>
		</div>
		<div class="flex flex-row items-center gap-5 mt-5 sm:justify-end sm:mt-0 sm:pl-5">

			{#if user}
				<a
					class="font-medium text-gray-600 hover:text-gray-400 dark:text-gray-400 dark:hover:text-gray-500"
					href="/documents">Dashboard</a
				>
			{/if}
			<AuthLinks />
		</div>
	</nav>
</header>
