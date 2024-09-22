<script lang="ts">
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

	$: blogContent = $store.blogContent;
	$: diagramContent = $store.diagramContent;

	onMount(async () => {
		// Get the query parameter `id` from the URL
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
		let content =
			$store.diagramContent
				? document.querySelector('.mermaid')?.innerHTML
				: sessionStorage.getItem('editor-content');
		if (content) {
			const element = document.createElement('div');
			element.innerHTML = content;

			const options = {
				margin: [0.5, 0.5, 0.7, 0.5], // Increased bottom margin
				filename: 'document.pdf',
				image: { type: 'jpeg', quality: 1 },
				html2canvas: {
					scale: 2,
					useCORS: true,
					logging: true,
					letterRendering: true,
					scrollY: -window.scrollY // Adjust for scroll position
				},
				jsPDF: {
					unit: 'in',
					format: 'a4',
					orientation: 'portrait',
					compress: false
				},
				pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
			};

			const addPageNumbers = (pdf) => {
				const pageCount = pdf.internal.getNumberOfPages();
				for (let i = 1; i <= pageCount; i++) {
					pdf.setPage(i);
					pdf.setFontSize(10);
					pdf.setTextColor(100);
					pdf.text(
						`Page ${i} of ${pageCount}`,
						pdf.internal.pageSize.getWidth() / 2,
						pdf.internal.pageSize.getHeight() - 0.4,
						{ align: 'center' }
					);
				}
			};

			// Pre-processing step
			const preProcess = () => {
				const contentDiv = document.createElement('div');
				contentDiv.innerHTML = content;

				// Add padding to ensure content is not cut off
				contentDiv.style.padding = '20px';

				// Force page breaks before and after the content
				const pageBreakBefore = document.createElement('div');
				pageBreakBefore.style.pageBreakBefore = 'always';
				const pageBreakAfter = document.createElement('div');
				pageBreakAfter.style.pageBreakAfter = 'always';

				contentDiv.insertBefore(pageBreakBefore, contentDiv.firstChild);
				contentDiv.appendChild(pageBreakAfter);

				return contentDiv;
			};

			const processedElement = preProcess();
			// Function to convert PNG images to JPEG
			const convertPngToJpeg = async (element) => {
				const pngImages = element.querySelectorAll('img[src$=".png"]');
				for (let img of pngImages) {
					const canvas = document.createElement('canvas');
					const ctx = canvas.getContext('2d');
					const image = new Image();
					image.crossOrigin = 'anonymous';
					await new Promise((resolve) => {
						image.onload = resolve;
						image.src = img.src;
					});
					canvas.width = image.width;
					canvas.height = image.height;
					ctx.drawImage(image, 0, 0);
					img.src = canvas.toDataURL('image/jpeg', 1.0);
				}
			};

			// Convert PNG to JPEG before generating PDF
			convertPngToJpeg(processedElement).then(() => {
				html2pdf()
					.from(processedElement)
					.set(options)
					.toPdf()
					.get('pdf')
					.then((pdf) => {
						addPageNumbers(pdf);
						pdf.save('document.pdf');
					});
			});
		}
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
			<!-- svelte-ignore a11y-missing-attribute -->
			{#if isCampaign || diagramContent}
				<a
					class="py-2 px-4 inline-flex justify-center items-center gap-2 rounded-md border border-transparent font-semibold bg-blue text-white"
					on:click={exportDoc}>Export</a
				>
			{/if}
		</div>
	</div>
	{#if document}
		<div class="grid grid-cols-5 gap-2" style="height: calc(100vh - 80px);">
			<div class="col-span-2">
				<ChatPanel documentId={docs.id} onSubmit={handleSubmit} />
			</div>
			<!-- svelte-ignore a11y-click-events-have-key-events 
			 <div class="col-span-3" on:contextmenu|preventDefault={handleRightClick} on:click|preventDefault={handleLeftClick} >
			 -->
			<div class="col-span-3">
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
				{#if showTooltip}
					<div class="tooltip" style="position: absolute; left: {tooltipX}px; top: {tooltipY}px;">
						<span>{selectedText}</span>
						<button on:click={() => handleSearch()}>Search</button>
					</div>
				{/if}
			</div>
		</div>
	{/if}
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
		object-fit: cover; /* Ensures the image covers the container while maintaining aspect ratio */
		display: block; /* Removes any extra space caused by inline elements */
		overflow-y: scroll;
	}
</style>
