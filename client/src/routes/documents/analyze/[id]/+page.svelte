<script lang="ts">
	import type { PageData } from './$types';
	import { beforeNavigate } from '$app/navigation';
	import {
		store,
		resetAll,
		sendMessage,
		createConversation,
		getActiveConversation
	} from '$s/chat/index';
	import AnalyzerMessages from '$c/chat/AnalyzerMessages.svelte';
	import { createEventDispatcher, onMount } from 'svelte';

	const dispatch = createEventDispatcher();

	$: activeConversation = $store.activeConversationId ? getActiveConversation() : null;

	export let data: PageData;

	const document = data.document;
	const documentUrl = data.documentUrl;
	const name = document.name?.split('.')[0];

	onMount(async () => {
		await createConversation(document.id);
		sendMessage({ isAnalysis: true }, { useStreaming: false });
	});
	beforeNavigate(resetAll);
</script>

{#if data.error}
	{data.error}
{/if}

<div class="container mx-auto h-screen">
	{#if document}
		<div class="open-chat-panel">
			<div class="msg-panel">
				<AnalyzerMessages messages={activeConversation?.messages || []} {name} />
			</div>
		</div>
	{/if}
</div>

<style>
	.open-chat-panel {
		height: 80%;
	}
	.msg-panel {
		width: 60%;
		margin-left: 20%;
	}
</style>
