import test from 'node:test';
import assert from 'node:assert/strict';
import { parseFps, positive } from './render-options.mjs';
test('decimal and rational frame rates preserve capture and encode timing', () => {
  assert.equal(parseFps('29.97').rate, 29.97);
  assert.equal(parseFps('30000/1001').rate, 30000 / 1001);
  assert.equal(parseFps('30000/1001').ffmpeg, '30000/1001');
  assert.equal(Math.round(60 * parseFps('30000/1001').rate), 1798);
});
test('bad rates fail instead of requesting enormous renders', () => {
  for (const value of ['0', '-1', '30000', '30/0', 'NaN', 'Infinity', '29junk', '']) assert.throws(() => parseFps(value));
  assert.throws(() => positive('0.5', 'width', 7680, true));
});
