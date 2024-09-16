<script lang="ts">
	import type { PageData } from './$types';
	import AuthGuard from '$c/AuthGuard.svelte';
	import Grid from 'gridjs-svelte';
	import { h, PluginPosition } from 'gridjs';
	import { goto } from '$app/navigation';
	import { updateDocIdList } from '$s/chat/index'

	const headingPlugin = {
		id: 'heading',
		position: PluginPosition.Header,
		component: () => {
			return h(
				'h1',
				{
					tyle: { width: '100%' }
				},
				'Your Documents'
			);
		}
	};
	const className = {
		error: 'error'
	};
	const style = {
		table: {
			width: '100%'
		},
		header: {
			display: 'flex',
			alignItems: 'center',
			flexDirection: 'row-reverse'
		}
	};
	const language = {
		search: {
			placeholder: 'Find file...'
		}
	};

	const columns = [
		{
			name: '',
			width: '5%',
			formatter: (cell: string, row: any) => {
				const checkBox = h('input', {
					type: 'checkbox',
					onClick: () => handleSelectionChange(cell)
				});
				return h('div', { className: 'display-flex' }, [checkBox]);
			}
		},
		{
			name: 'Name',
			width: '45%'
		},
		{
			name: 'Date',
			width: '30%'
		},
		{
			name: 'Action',
			width: '20%',
			formatter: (cell: string, row: any) => {
				const detailsBtn = h(
					'button',
					{
						className: 'btn-details',
						onClick: () =>{ updateDocIdList(docList); goto(`/documents/${cell}` )}
					},
					'Chat'
				);
				const campaignBtn = h(
					'button',
					{
						className: 'btn-analysis',
						onClick: () => goto(`/documents/${cell}?campaign=true`)
					},
					'Campaign'
				);

				return h('div', { className: 'display-flex' }, [detailsBtn, campaignBtn]);
				// return h('div', { className: 'display-flex' }, [detailsBtn]);
			}
		}
	];

	const server = {
		url: '/api/pdfs',
		total: (data: { count: any; }) => data.count,
		then: (data: any[]) =>
			data.map((document: { id: any; name: any; uploaded_on: any; }) => [document.id, document.name, document.uploaded_on, document.id])
	};

	const pagination = {
		enabled: true,
		limit: 10,
		server: {
			url: (prev: string | string[], page: number) => {
				return `${prev}${prev.includes('?') ? '&' : '?'}page=${page + 1}`;
			}
		}
	};

	const search = {
		enabled: true,
		server: {
			url: (prev: any, keyword: any) => `${prev}?search=${keyword}`
		}
	};
	const docList: string[] = [];
	function handleSelectionChange(docId: string) {
		const index = docList.indexOf(docId);
		if (index !== -1) {
			docList.splice(index, 1);
		} else {
			docList.push(docId);
		}
		
	}
</script>

<div class="container mx-auto h-screen">
	<AuthGuard />
	<div class="flex flex-row justify-between items-center my-4">
		<h2 class="text-3xl font-bold m-2">Your Documents</h2>
		<div class="">
			<a
				href="/documents/new"
				class="py-2 px-4 inline-flex justify-center items-center gap-2 rounded-md border border-transparent font-semibold bg-blue text-white hover:bg-blue focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all dark:focus:ring-offset-gray-800"
				>New</a
			>
		</div>
	</div>

	<div class="flex flex-col">
		<div class="-m-1.5 overflow-x-auto">
			<div class="p-1.5 min-w-full inline-block align-middle">
				<div class="border rounded-lg overflow-hidden p-4" style="font-size: 14px;">
					<Grid {search} {columns} {server} {pagination} {language} {className} {style} />
				</div>
			</div>
		</div>
	</div>
</div>

<style global>
	.bg-blue {
		background-color: rgb(24, 7, 132);
	}

	:root {
		--primary-color: #5296d2;
		--error-color: red;
		--secondary-color: #f2f1e7;
	}

	:global(.btn-details) {
		background-color: var(--primary-color);
		padding: 0.3rem 0.6rem;
		border-width: 0;
		border-radius: 0.5rem;
		cursor: pointer;
		font-size: 13px;
	}
	:global(.btn-analysis) {
		background-color: var(--secondary-color);
		padding: 0.3rem 0.6rem;
		border-width: 0;
		border-radius: 0.5rem;
		margin-left: 0.5rem;
		cursor: pointer;
		font-size: 13px;
	}
	:global(.display-flex) {
		display: flex;
	}
	:global(.error) {
		color: var(--error-color);
	}
</style>
