import { addMessages, init, locale } from 'svelte-i18n';
import en from './locales/en.json';
import hu from './locales/hu.json';

addMessages('en', en);
addMessages('hu', hu);

export function setupI18n(lang) {
  init({
    fallbackLocale: 'en',
    initialLocale: lang,
  });
  locale.set(lang);
}