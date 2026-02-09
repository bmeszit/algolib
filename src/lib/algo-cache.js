const _byPage = new Map();

export function getAlgoRunState(page) {
  return _byPage.get(page) ?? null;
}

export function setAlgoRunState(page, state) {
  _byPage.set(page, state);
}
