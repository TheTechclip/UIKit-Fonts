# UIKit-Fonts

UIKit 내에서 사용하는 폰트 모음입니다. 각 폰트의 출처와 라이선스는 아래와 같습니다.

| 폰트 | 출처 (Source) | 라이선스 (License) |
| --- | --- | --- |
| Asta Sans | https://github.com/42dot/Asta-Sans | SIL Open Font License 1.1 (Copyright 2024 The Asta Sans Project Authors) |
| JetBrains Mono | https://github.com/jetbrains/jetbrainsmono | SIL Open Font License 1.1 (Copyright 2020 The JetBrains Mono Project Authors) |
| Min Icon | https://github.com/poposnail61/min-icon | 라이선스 확인 불가 |
| Source Han Serif | https://github.com/adobe-fonts/source-han-serif | SIL Open Font License 1.1 (Copyright 2017-2022 Adobe) |

## 폰트 목록

- `AstaSans/` — Asta Sans
- `JetBrainsMono/` — JetBrains Mono
- `MinIcon/` — Min Icon
- `SourceHanSerifKR/` — Source Han Serif (KR)

`MinIcon/MinIconVF.woff2` is the canonical Musecat MinIcon source. Product
repositories reference this asset instead of storing a second Web WOFF2 copy.
Musecat-specific glyph construction and Native static-face generation scripts
live in `MinIcon/tools/`.

Rebuild `iImageRotated` (U+EC3C, including the `ss09` filled alternate) with
`python3 MinIcon/tools/extend_image_rotated.py`. Its compact arrow matches the
image frame stroke and balances the top/left padding. The script requires
fontTools with WOFF2/Brotli support.
