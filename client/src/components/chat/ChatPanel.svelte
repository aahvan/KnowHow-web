<script lang="ts">
	import { onMount } from 'svelte';
	import {
		store,
		resetError,
		fetchConversations,
		createConversation,
		getActiveConversation
	} from '$s/chat';
	import Alert from '$c/Alert.svelte';
	import ChatInput from '$c/chat/ChatInput.svelte';
	import ChatList from '$c/chat/ChatList.svelte';
	import ConversationSelect from '$c/chat/ConversationSelect.svelte';
	import PromptTemplate from './PromptTemplate.svelte';

	export let onSubmit: (text: string, useStreaming: boolean) => void;
	export let documentId: number;

	let useStreaming = !!localStorage.getItem('streaming');

	$: localStorage.setItem('streaming', useStreaming ? 'true' : '');
	$: activeConversation = $store.activeConversationId ? getActiveConversation() : null;
	let showPrompt = true

	function handleSubmit(event: CustomEvent<string>) {
		if (onSubmit) {
			onSubmit(event.detail, true);
			showPrompt = false
		}
	}

	function handleNewChat() {
		createConversation(documentId);
	}
	function resetPromptFlag(){
		showPrompt = true
	}
	onMount(() => {
		fetchConversations(documentId);
	});
</script>

<div
	style="height: calc(100vh - 80px);"
	class="flex flex-col h-full bg-slate-50 border rounded-xl shadow"
>
	<div class="rounded-lg border-b px-3 py-2 flex flex-row items-center justify-between">
		<div class="flex gap-1">
			
			<button class="rounded text-sm border border-blue-500 px-2 py-0.5 p-2" on:click={handleNewChat}
				>New Chat</button
			>
			<ConversationSelect conversations={$store.conversations} />
			
		</div>
		<PromptTemplate resetPromptFlag={resetPromptFlag}/>
	</div>
	<div class="flex flex-col flex-1 px-3 py-2 overflow-y-scroll">
		<ChatList messages={activeConversation?.messages || []} />
		<div class="relative">
			{#if $store.error && $store.error.length < 200}
				<div class="p-4">
					<Alert type="error" onDismiss={resetError}>
						{$store.error}
					</Alert>
				</div>
			{/if}
			{#if $store.activePrompt && showPrompt}
			<div class="p-4 mb-2.5">
				<span class="sl-template">
					{$store.activePrompt}
				</span>
			</div>
			{/if}
			<ChatInput on:submit={handleSubmit} />
		</div>
	</div>
</div>

<style>
	.sl-template{
		padding:20px;
		border-radius: 15px;
		border: 1px solid #f4e6e6;
		margin-bottom: 10px;
	}
	.gap-1{
		gap: 1rem
	}
</style>

