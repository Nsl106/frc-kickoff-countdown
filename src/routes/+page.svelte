<script lang="ts">
	import { onMount } from 'svelte';
	import { base } from '$app/paths';
	import teamsData from '$lib/teams.json';

	// Kickoff: January 10, 2026, 12:00 PM EST
	const KICKOFF_DATE = new Date('2026-01-10T12:00:00-05:00');

	interface TimeLeft {
		days: number;
		hours: number;
		minutes: number;
		seconds: number;
		total: number;
	}

	let timeLeft = $state<TimeLeft>({
		days: 0,
		hours: 0,
		minutes: 0,
		seconds: 0,
		total: 0
	});

	let kickoffStarted = $state(false);
	let showTotalSeconds = $state(false);

	function calculateTimeLeft(): TimeLeft {
		const now = new Date();
		const difference = KICKOFF_DATE.getTime() - now.getTime();

		if (difference <= 0) {
			return { days: 0, hours: 0, minutes: 0, seconds: 0, total: 0 };
		}

		return {
			days: Math.floor(difference / (1000 * 60 * 60 * 24)),
			hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
			minutes: Math.floor((difference / (1000 * 60)) % 60),
			seconds: Math.floor((difference / 1000) % 60),
			total: difference
		};
	}

	function padZero(num: number): string {
		return num.toString().padStart(2, '0');
	}

	// Get total seconds remaining
	function getTotalSeconds(): number {
		return Math.floor(timeLeft.total / 1000);
	}

	// Extract team number - try 5-digit first, fallback to 4-digit
	function getTeamNumber(): number {
		if (showTotalSeconds) {
			// Try 5-digit team from last 5 digits of total seconds
			const fiveDigit = getTotalSeconds() % 100000;
			if (fiveDigit >= 10000 && getTeamInfo(fiveDigit)) {
				return fiveDigit;
			}
			return getTotalSeconds() % 10000;
		}
		// Calculate 5-digit team: (hours % 10) * 10000 + minutes * 100 + seconds
		const fiveDigitTeam = (timeLeft.hours % 10) * 10000 + timeLeft.minutes * 100 + timeLeft.seconds;
		// Check if 5-digit team exists (and hours ones digit > 0)
		if ((timeLeft.hours % 10) > 0 && getTeamInfo(fiveDigitTeam)) {
			return fiveDigitTeam;
		}
		// Fallback to 4-digit team
		return timeLeft.minutes * 100 + timeLeft.seconds;
	}

	// Get team info from data
	function getTeamInfo(teamNum: number): { name: string } | null {
		const team = (teamsData as Record<string, { name: string }>)[teamNum.toString()];
		return team || null;
	}

	// Split total seconds into prefix (non-highlighted) and suffix (highlighted)
	// Suffix length is 5 digits for 5-digit teams, 4 digits otherwise
	function splitTotalSeconds(isFiveDigit: boolean): { prefix: string; suffix: string } {
		const total = getTotalSeconds();
		const totalStr = total.toString();
		const suffixLength = isFiveDigit ? 5 : 4;

		if (totalStr.length <= suffixLength) {
			return { prefix: '', suffix: totalStr };
		}

		return {
			prefix: totalStr.slice(0, -suffixLength),
			suffix: totalStr.slice(-suffixLength)
		};
	}

	onMount(() => {
		timeLeft = calculateTimeLeft();
		kickoffStarted = timeLeft.total <= 0;

		const interval = setInterval(() => {
			timeLeft = calculateTimeLeft();
			if (timeLeft.total <= 0) {
				kickoffStarted = true;
				clearInterval(interval);
			}
		}, 1000);

		return () => clearInterval(interval);
	});

	const teamNumber = $derived(getTeamNumber());
	const teamInfo = $derived(getTeamInfo(teamNumber));
	const isFiveDigitTeam = $derived(teamNumber >= 10000);
</script>

<svelte:head>
	<title>FRC 2026 Kickoff Countdown</title>
	<meta name="description" content="Countdown to FIRST Robotics Competition 2026 REBUILT Kickoff" />
</svelte:head>

<main
	class="relative flex min-h-screen flex-col items-center justify-center bg-cover bg-center bg-no-repeat px-2 md:px-4"
	style="background-image: url('{base}/background.png');"
>
	{#if kickoffStarted}
		<!-- Kickoff Started State -->
		<div class="flex flex-col items-center text-center">
			<img src="{base}/rebuilt_logo.png" alt="REBUILT Logo" class="mb-2 w-48 md:mb-8 md:w-[32rem] lg:w-[40rem]" />

			<!-- Timer Display (at zero) -->
			<div
				class="mb-2 rounded-lg bg-white/90 px-3 py-2 font-mono text-2xl font-bold md:mb-4 md:px-8 md:py-4 md:text-7xl lg:text-8xl"
			>
				<span class="text-frc-blue">00</span>
				<span class="text-frc-blue/50">:</span>
				<span class="text-frc-blue">00</span>
				<span class="text-frc-blue/50">:</span>
				<span class="text-frc-blue">00</span>
				<span class="text-frc-blue/50">:</span>
				<span class="text-frc-blue">00</span>
			</div>

			<div class="rounded-lg bg-white/90 px-4 py-2 md:px-8 md:py-4">
				<h1 class="text-xl font-bold text-frc-orange md:text-5xl">Happy Kickoff!</h1>
			</div>
		</div>
	{:else}
		<!-- Countdown State -->
		<div class="flex flex-col items-center text-center">
			<!-- Logo -->
			<img src="{base}/rebuilt_logo.png" alt="REBUILT Logo" class="mb-2 w-48 md:mb-8 md:w-[32rem] lg:w-[40rem]" />

			<!-- Timer Display -->
			<div
				class="mb-2 rounded-lg bg-white/90 px-3 py-2 font-mono text-2xl font-bold md:mb-4 md:px-8 md:py-4 md:text-7xl lg:text-8xl"
			>
				{#if showTotalSeconds}
					{@const parts = splitTotalSeconds(isFiveDigitTeam)}{#if parts.prefix}<span class="text-frc-blue">{parts.prefix}</span>{/if}<span class="text-frc-gold">{parts.suffix}</span>
				{:else}
					<span class="text-frc-blue">{padZero(timeLeft.days)}</span>
					<span class="text-frc-blue/50">:</span>
					{#if isFiveDigitTeam}
						<span class="text-frc-blue">{Math.floor(timeLeft.hours / 10)}</span><span class="text-frc-gold">{timeLeft.hours % 10}</span>
					{:else}
						<span class="text-frc-blue">{padZero(timeLeft.hours)}</span>
					{/if}
					<span class={isFiveDigitTeam ? 'text-frc-gold' : 'text-frc-blue/50'}>:</span>
					{#if isFiveDigitTeam}
						<span class="text-frc-gold">{padZero(timeLeft.minutes)}</span>
					{:else if timeLeft.minutes >= 10}
						<span class="text-frc-gold">{padZero(timeLeft.minutes)}</span>
					{:else if timeLeft.minutes > 0}
						<span class="text-frc-blue">0</span><span class="text-frc-gold">{timeLeft.minutes}</span>
					{:else}
						<span class="text-frc-blue">00</span>
					{/if}
					<span class={isFiveDigitTeam || timeLeft.minutes > 0 ? 'text-frc-gold' : 'text-frc-blue/50'}>:</span>
					{#if isFiveDigitTeam}
						<span class="text-frc-gold">{padZero(timeLeft.seconds)}</span>
					{:else if timeLeft.minutes > 0 || timeLeft.seconds >= 10}
						<span class="text-frc-gold">{padZero(timeLeft.seconds)}</span>
					{:else if timeLeft.seconds > 0}
						<span class="text-frc-blue">0</span><span class="text-frc-gold">{timeLeft.seconds}</span>
					{:else}
						<span class="text-frc-blue">00</span>
					{/if}
				{/if}
			</div>

			<!-- Team Display -->
			<div class="min-w-40 rounded-lg bg-white/90 px-3 py-2 text-sm font-bold md:min-w-80 md:px-8 md:py-4 md:text-xl">
				{#if teamInfo}
					<span class="text-frc-blue">{teamInfo.name}</span>
				{:else}
					<span class="text-frc-blue/70">Team Not Found</span>
				{/if}
			</div>

			<!-- Toggle Button -->
			<button
				class="mt-2 rounded-lg bg-white/90 px-3 py-1.5 text-xs font-medium text-frc-blue transition-colors hover:bg-white md:mt-4 md:px-4 md:py-2 md:text-sm"
				onclick={() => (showTotalSeconds = !showTotalSeconds)}
			>
				{showTotalSeconds ? 'Show Clock' : 'Show Total Seconds'}
			</button>
		</div>
	{/if}

	<!-- GitHub Link -->
	<a
		href="https://github.com/Nsl106/frc-kickoff-countdown"
		target="_blank"
		rel="noopener noreferrer"
		class="absolute bottom-4 left-4 rounded-full bg-white/80 p-2 text-gray-700 transition-colors hover:bg-white hover:text-black"
		aria-label="View source on GitHub"
	>
		<svg class="h-5 w-5 md:h-6 md:w-6" fill="currentColor" viewBox="0 0 24 24">
			<path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
		</svg>
	</a>
</main>
