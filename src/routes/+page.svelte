<script lang="ts">
	import { onMount } from 'svelte';
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

	// Extract team number from the last 4 digits (MM:SS)
	function getTeamNumber(): number {
		const mmss = timeLeft.minutes * 100 + timeLeft.seconds;
		return mmss;
	}

	// Get team info from data
	function getTeamInfo(teamNum: number): { name: string } | null {
		const team = (teamsData as Record<string, { name: string }>)[teamNum.toString()];
		return team || null;
	}

	// Format the highlighted portion (remove leading zeros from team number display)
	function formatHighlightedNumber(): string {
		const teamNum = getTeamNumber();
		if (teamNum === 0) return '0';

		// Format as M:SS or MM:SS based on value
		const minutes = timeLeft.minutes;
		const seconds = timeLeft.seconds;

		if (minutes === 0) {
			return seconds.toString();
		} else {
			return `${minutes}:${padZero(seconds)}`;
		}
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
	const highlightedDisplay = $derived(formatHighlightedNumber());
</script>

<svelte:head>
	<title>FRC 2026 Kickoff Countdown</title>
	<meta name="description" content="Countdown to FIRST Robotics Competition 2026 REBUILT Kickoff" />
</svelte:head>

<main class="flex min-h-screen flex-col items-center justify-center bg-[#0a0a0a] px-4">
	{#if kickoffStarted}
		<!-- Kickoff Started State -->
		<div class="text-center">
			<h1 class="mb-4 text-4xl font-bold text-frc-orange md:text-6xl">
				FIRST Robotics Competition 2026
			</h1>
			<h2 class="text-3xl font-bold text-frc-gold md:text-5xl">Kickoff Has Started!</h2>
			<p class="mt-8 text-xl text-frc-green">REBUILT</p>
		</div>
	{:else}
		<!-- Countdown State -->
		<div class="text-center">
			<!-- Title -->
			<h1 class="mb-2 text-2xl font-bold text-frc-orange md:text-4xl">FRC 2026</h1>
			<h2 class="mb-8 text-xl text-frc-gold md:text-2xl">REBUILT</h2>

			<!-- Timer Display -->
			<div class="mb-8 font-mono text-5xl font-bold tracking-wider md:text-7xl lg:text-8xl">
				<!-- Days -->
				<span class="text-frc-blue">{padZero(timeLeft.days)}</span>
				<span class="text-frc-blue/50">:</span>
				<!-- Hours -->
				<span class="text-frc-blue">{padZero(timeLeft.hours)}</span>
				<span class="text-frc-blue/50">:</span>
				<!-- Minutes (potentially highlighted) -->
				{#if timeLeft.minutes > 0}
					<span class="text-frc-gold drop-shadow-[0_0_10px_rgba(229,174,50,0.5)]"
						>{padZero(timeLeft.minutes)}</span
					>
				{:else}
					<span class="text-frc-blue">{padZero(timeLeft.minutes)}</span>
				{/if}
				<span class="text-frc-blue/50">:</span>
				<!-- Seconds (always highlighted as part of team number) -->
				<span class="text-frc-gold drop-shadow-[0_0_10px_rgba(229,174,50,0.5)]"
					>{padZero(timeLeft.seconds)}</span
				>
			</div>

			<!-- Time Labels -->
			<div
				class="mb-12 flex justify-center gap-6 text-xs uppercase tracking-widest text-frc-blue/70 md:gap-12 md:text-sm"
			>
				<span class="w-14 text-center md:w-20">Days</span>
				<span class="w-14 text-center md:w-20">Hours</span>
				<span class="w-14 text-center md:w-20">Min</span>
				<span class="w-14 text-center md:w-20">Sec</span>
			</div>

			<!-- Team Highlight Section -->
			<div
				class="rounded-lg border border-frc-blue/30 bg-frc-blue/10 px-6 py-4 backdrop-blur-sm md:px-8 md:py-6"
			>
				<div class="mb-2 text-sm uppercase tracking-widest text-frc-blue/70">
					Team Spotlight
				</div>
				<div class="flex items-center justify-center gap-3">
					<span
						class="font-mono text-3xl font-bold text-frc-orange drop-shadow-[0_0_8px_rgba(234,87,46,0.4)] md:text-4xl"
					>
						{highlightedDisplay}
					</span>
				</div>
				{#if teamInfo}
					<div class="mt-3">
						<span class="text-lg text-frc-green md:text-xl">
							{teamInfo.name}
						</span>
					</div>
				{:else if teamNumber > 0}
					<div class="mt-3 text-frc-blue/50">Team #{teamNumber} not found</div>
				{:else}
					<div class="mt-3 text-frc-blue/50">Team #0</div>
				{/if}
			</div>

			<!-- Kickoff Date Info -->
			<p class="mt-8 text-sm text-frc-blue/50">
				January 10, 2026 at 12:00 PM EST
			</p>
		</div>
	{/if}
</main>
