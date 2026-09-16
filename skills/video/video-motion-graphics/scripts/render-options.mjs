export function parseFps(value = "30") {
  const text = String(value);
  if (!/^\d+(?:\.\d+)?(?:\/\d+(?:\.\d+)?)?$/.test(text)) throw new Error(`Invalid frame rate: ${text}`);
  const [numerator, denominator = "1"] = text.split("/");
  const rate = Number(numerator) / Number(denominator);
  if (!Number.isFinite(rate) || rate <= 0 || rate > 240) throw new Error("Frame rate must be greater than 0 and at most 240");
  return { rate, ffmpeg: text };
}

export function positive(value, name, max, integer = false) {
  const number = Number(value);
  if (!Number.isFinite(number) || number <= 0 || number > max || (integer && !Number.isInteger(number))) throw new Error(`Invalid ${name}: ${value}`);
  return number;
}
