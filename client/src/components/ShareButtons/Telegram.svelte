<script>
	import TelegramIcon from '$c/Icons/Telegram.svelte';

	export let url;
	export let title;

	const TELEGRAM_BLUE = '#49a9e9';

	const baseUrl = 'https://telegram.me/share/url';
	const parametersObject = {
		url,
		text: title,
	};

	const params = Object.entries(parametersObject)
		.filter(([, value]) => value ?? false)
		.map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`)
		.join('&');

	const urlWithParameters = params === '' ? baseUrl : `${baseUrl}?${params}`;

	function handleClick() {
		const config = {
			height: 550,
			width: 400,
			location: 'no',
			toolbar: 'no',
			status: 'no',
			directories: 'no',
			menubar: 'no',
			scrollbars: 'yes',
			resizable: 'no',
			centerscreen: 'yes',
			chrome: 'yes',
		};
		return window.open(
			urlWithParameters,
			'',
			Object.keys(config)
				.map((key) => `${key}=${config[key]}`)
				.join(','),
		);
	}
</script>

<button on:click={handleClick}
	><TelegramIcon
		colour={TELEGRAM_BLUE}
		width={30}
	/></button
>

<style>

	button {
		background: transparent;
		border-style: none;
		transition: all 0.2s ease-in-out;
		margin-right: 0.5rem;
	}

	@media (prefers-reduced-motion: reduce) {
		button {
			transition: all 2s ease-in-out;
		}
	}

	button:focus,
	button:hover {
		transform: scale(1.1);
	}

</style>
