# HyperFrames animation blocks

These files are vendored from the [HeyGen HyperFrames registry](https://github.com/heygen-com/hyperframes/tree/main/registry):

- code-diff.html
- code-typing.html
- code-morph.html

The code-animation skill records hyperframes@0.7.77 as the version used for these blocks.
Branding is applied by scripts/build.mjs when building an animation. Keep the vendored
HTML separate from those generated changes.

Copyright 2026 HeyGen, Inc.

These blocks retain the [Apache License 2.0](./LICENSE), copied from the
[upstream license](https://github.com/heygen-com/hyperframes/blob/main/LICENSE).
The repository's root MIT license applies to its original material.

The blocks reference GSAP on a CDN at render time. That dependency is not vendored here.
