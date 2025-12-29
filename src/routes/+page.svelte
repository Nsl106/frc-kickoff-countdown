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

	// Extract team number from the last 4 digits
	function getTeamNumber(): number {
		if (showTotalSeconds) {
			return getTotalSeconds() % 10000;
		}
		return timeLeft.minutes * 100 + timeLeft.seconds;
	}

	// Get team info from data
	function getTeamInfo(teamNum: number): { name: string } | null {
		const team = (teamsData as Record<string, { name: string }>)[teamNum.toString()];
		return team || null;
	}

	// Split total seconds into prefix (non-highlighted) and suffix (highlighted, last 4 digits)
	function splitTotalSeconds(): { prefix: string; suffix: string } {
		const total = getTotalSeconds();
		const totalStr = total.toString();

		if (totalStr.length <= 4) {
			return { prefix: '', suffix: totalStr };
		}

		return {
			prefix: totalStr.slice(0, -4),
			suffix: totalStr.slice(-4)
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
</script>

<svelte:head>
	<title>FRC 2026 Kickoff Countdown</title>
	<meta name="description" content="Countdown to FIRST Robotics Competition 2026 REBUILT Kickoff" />
</svelte:head>

<main
	class="flex min-h-screen flex-col items-center justify-center bg-cover bg-center bg-no-repeat px-4"
	style="background-image: url('{base}/background.png');"
>
	{#if kickoffStarted}
		<!-- Kickoff Started State -->
		<div class="flex flex-col items-center text-center">
			<img src="{base}/rebuilt_logo.png" alt="REBUILT Logo" class="mb-8 w-[32rem] md:w-[40rem]" />

			<!-- Timer Display (at zero) -->
			<div
				class="mb-4 rounded-lg bg-white/90 px-6 py-4 font-mono text-5xl font-bold md:px-8 md:text-7xl lg:text-8xl"
			>
				<span class="text-frc-blue">00</span>
				<span class="text-frc-blue/50">:</span>
				<span class="text-frc-blue">00</span>
				<span class="text-frc-blue/50">:</span>
				<span class="text-frc-blue">00</span>
				<span class="text-frc-blue/50">:</span>
				<span class="text-frc-blue">00</span>
			</div>

			<div class="rounded-lg bg-white/90 px-8 py-4">
				<h1 class="text-3xl font-bold text-frc-orange md:text-5xl">Happy Kickoff!</h1>
			</div>
		</div>
	{:else}
		<!-- Countdown State -->
		<div class="flex flex-col items-center text-center">
			<!-- Logo -->
			<img src="{base}/rebuilt_logo.png" alt="REBUILT Logo" class="mb-8 w-[32rem] md:w-[40rem]" />

			<!-- Timer Display -->
			<div
				class="mb-4 rounded-lg bg-white/90 px-6 py-4 font-mono text-5xl font-bold md:px-8 md:text-7xl lg:text-8xl"
			>
				{#if showTotalSeconds}
					{@const parts = splitTotalSeconds()}{#if parts.prefix}<span class="text-frc-blue">{parts.prefix}</span>{/if}<span class="text-frc-gold">{parts.suffix}</span>
				{:else}
					<span class="text-frc-blue">{padZero(timeLeft.days)}</span>
					<span class="text-frc-blue/50">:</span>
					<span class="text-frc-blue">{padZero(timeLeft.hours)}</span>
					<span class="text-frc-blue/50">:</span>
					{#if timeLeft.minutes >= 10}
						<span class="text-frc-gold">{padZero(timeLeft.minutes)}</span>
					{:else if timeLeft.minutes > 0}
						<span class="text-frc-blue">0</span><span class="text-frc-gold">{timeLeft.minutes}</span>
					{:else}
						<span class="text-frc-blue">00</span>
					{/if}
					<span class={timeLeft.minutes > 0 ? 'text-frc-gold' : 'text-frc-blue/50'}>:</span>
					{#if timeLeft.minutes > 0 || timeLeft.seconds >= 10}
						<span class="text-frc-gold">{padZero(timeLeft.seconds)}</span>
					{:else if timeLeft.seconds > 0}
						<span class="text-frc-blue">0</span><span class="text-frc-gold">{timeLeft.seconds}</span>
					{:else}
						<span class="text-frc-blue">00</span>
					{/if}
				{/if}
			</div>

			<!-- Team Display -->
			<div class="min-w-64 rounded-lg bg-white/90 px-6 py-4 md:min-w-80 md:px-8 text-lg font-bold md:text-xl">
				{#if teamInfo}
					<span class="text-frc-blue">{teamInfo.name}</span>
				{:else}
					<span class="text-frc-blue/70">Team Not Found</span>
				{/if}
			</div>

			<!-- Toggle Button -->
			<button
				class="mt-4 rounded-lg bg-white/90 px-4 py-2 text-sm font-medium text-frc-blue transition-colors hover:bg-white"
				onclick={() => (showTotalSeconds = !showTotalSeconds)}
			>
				{showTotalSeconds ? 'Show Clock' : 'Show Total Seconds'}
			</button>
		</div>
	{/if}
</main>
