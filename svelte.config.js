import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),

	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: undefined,
			precompress: false,
			strict: true
		}),
		paths: {
			// Set this to your repo name if deploying to github.io/repo-name
			// Leave empty if deploying to custom domain or root
			base: process.env.NODE_ENV === 'production' ? '/frc-kickoff-countdown' : ''
		}
	}
};

export default config;
