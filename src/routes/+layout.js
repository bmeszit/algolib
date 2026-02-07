import { setupI18n } from '$lib/i18n';

export const ssr = false;
export const prerender = true;

export const load = ({ url }) => {
  const lang = url.searchParams.get('lang') || 'hu';
  setupI18n(lang);
  return { lang };
};