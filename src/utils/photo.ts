// Уменьшенные копии фото из Directus: сервер сам ужимает картинку до нужной ширины
// и отдаёт webp, поэтому телефон не качает многомегабайтный оригинал.
const WIDTHS = [480, 800, 1200, 1600]

function sized(url: string, width: number): string {
  return `${url}?width=${width}&quality=78&format=webp`
}

function isDirectusAsset(url: string): boolean {
  return url.includes('/assets/')
}

export function photoSrc(url: string, width = 800): string {
  return isDirectusAsset(url) ? sized(url, width) : url
}

export function photoSrcset(url: string): string | undefined {
  if (!isDirectusAsset(url)) return undefined
  return WIDTHS.map((w) => `${sized(url, w)} ${w}w`).join(', ')
}
