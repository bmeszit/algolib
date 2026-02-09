const _byPage = new Map();

export function getBenchState(page) {
  return _byPage.get(page) ?? null;
}

export function setBenchState(page, state) {
  _byPage.set(page, state);
}
