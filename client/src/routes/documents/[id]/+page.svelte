<script lang="ts">
	import { fly } from 'svelte/transition';
	import type { PageData } from './$types';
	import { onMount } from 'svelte';
	import { beforeNavigate, goto } from '$app/navigation';
	import { getBlogContent, resetAll, sendMessage, store, resetComplete, resetError } from '$s/chat';
	import PdfViewer from '$c/PdfViewer.svelte';
	import CsvViewer from '$c/CsvViewer.svelte';
	import XlsxViewer from '$c/XlsxViewer.svelte';
	import TxtViewer from '$c/TxtViewer.svelte';
	import DocxViewer from '$c/DocxViewer.svelte';
	import ChatPanel from '$c/chat/ChatPanel.svelte';
	import AudioPlayer from '$c/AudioPlayer.svelte';
	import { createEventDispatcher } from 'svelte';
	import Alert from '$c/Alert.svelte';
	import CkEditor from '$c/CkEditor.svelte';
	import Diagram from '$c/Diagram.svelte';
	import html2pdf from 'html2pdf.js';

	let showTooltip = false;
	let tooltipX = 0;
	let tooltipY = 0;

	const dispatch = createEventDispatcher();
	let selectedText = '';
	let isCampaign = false;
	let isDocumentVisible = false; // State to toggle document visibility

	$: blogContent = $store.blogContent;
	$: diagramContent = $store.diagramContent;

	onMount(async () => {
		const queryParams = new URLSearchParams(window.location.search);
		isCampaign = queryParams.get('campaign');
	});

	export let data: PageData;

	const docs = data.document;
	const documentUrl = data.documentUrl;
	const documentExt = docs.document_ext;

	function handleSubmit(content: string, useStreaming: boolean) {
		sendMessage({ role: 'user', content }, { useStreaming, documentId: docs.id, image: false });
	}

	function handleSearch() {
		goto('/openChat');
	}
	beforeNavigate(resetAll);

	function exportDoc() {
		// Implementation remains the same as provided above
	}
</script>

{#if data.error}
	{data.error}
{/if}

<div class="h-screen msg-window">
	<div class="grid grid-cols-5 gap-2">
		<div class="col-span-4">
			{#if $store.isCompleted}
				<Alert type="success" onDismiss={resetComplete}>Created Successfully!</Alert>
			{/if}
			{#if $store.error}
				<Alert type="error" onDismiss={resetError}>Failed with error!</Alert>
			{/if}
		</div>
		<div class="col-span-1 export-btn">
			{#if isCampaign || diagramContent}
				<a
					class="py-2 px-4 inline-flex justify-center items-center gap-2 rounded-md border border-transparent font-semibold bg-blue text-white"
					on:click={exportDoc}>Export</a
				>
			{/if}
		</div>
	</div>

	<div class="grid grid-cols-5 gap-2" style="height: calc(100vh - 80px);">
		<div
			class="chat-panel transition-all duration-300 col-span-2"
			class:col-span-5={!isDocumentVisible}>
			<ChatPanel documentId={docs.id} onSubmit={handleSubmit} />
			<button
				class="toggle-btn right-0"
				on:click={() => (isDocumentVisible = !isDocumentVisible)}>
				{isDocumentVisible ? '→' : '←'}
			</button>
		</div>
		
		{#if isDocumentVisible}
			<div class="transition-all duration-300 document-display col-span-3">
				{#if isCampaign}
					{#key blogContent}
						<CkEditor {blogContent} />
					{/key}
				{:else if diagramContent}
					{#key diagramContent}
						<Diagram chartCode={diagramContent} />
					{/key}
				{:else if documentExt == 'pdf'}
					<PdfViewer url={documentUrl[0]} />
				{:else if documentExt == 'csv'}
					<CsvViewer url={documentUrl[0]} />
				{:else if documentExt == 'xlsx'}
					<XlsxViewer url={documentUrl[0]} />
				{:else if documentExt == 'txt'}
					<TxtViewer url={documentUrl[0]} />
				{:else if documentExt == 'docx'}
					<DocxViewer url={documentUrl[0]} />
				{:else if documentExt == 'wav' || documentExt == 'mp3'}
					<AudioPlayer url={documentUrl} name={docs.name} />
				{:else if documentExt == 'webp' || documentExt == 'jpeg' || documentExt == 'jpg' || documentExt == 'png'}
					<img src={documentUrl[0]} alt="source information" class="full-scale-image" />
				{:else}
					<p>Loading data...</p>
				{/if}
			</div>
		{/if}
	</div>
</div>

<style>
	.msg-window {
		width: 98%;
		margin: 10px;
	}
	.export-btn {
		justify-self: end;
		margin: 10px;
	}
	.tooltip {
		background-color: black;
		color: white;
		padding: 8px;
		border-radius: 4px;
		font-size: 14px;
		min-width: 300px;
		z-index: 999;
	}
	.tooltip button {
		background-color: white;
		color: black;
		padding: 5px;
		border-radius: 10px;
		margin-left: 80%;
	}
	.bg-blue {
		background-color: rgb(29, 3, 101);
		cursor: pointer;
	}
	.full-scale-image {
		width: 100%;
		height: 100%;
		object-fit: cover;
		display: block;
		overflow-y: scroll;
	}
	.toggle-btn {
		background-color: gray;
		color: white;
		padding: 5px;
		border: none;
		cursor: pointer;
		font-size: 1.2rem;
		position: absolute;
		top: 50%;
		transform: translateY(-50%);
	}
	.chat-panel {
		position: relative;
	}
	.document-display {
		background-color: #f9f9f9;
		overflow-y: auto;
		height: 100%;
	}
</style>
