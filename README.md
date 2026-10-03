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

추가 텍스트 폰트는 로캘이 아닌 폰트별 루트 디렉터리로 관리합니다.
Musecat이 한국어·영어·일본어에서 선택 가능한 폰트 목록을 결정하며, 여러 로캘은
같은 폰트 파일을 공유합니다. 기본값은 기존 Pretendard입니다.

- 한국어: SkyBori, MapoFlowerIsland, HSBombaram, SeoulHangang, NanumSquareNeo
- 한국어·영어: NeoDunggeunmoPro, SUITE, Maplestory
- 일본어: PixelMplus, KokuMincho, Checkpoint (제공받은 CP Font), LightNovelPOP
- 중국어: 미정

`SUITE`와 `NanumSquareNeo`는 공식 WOFF2 VF를 사용합니다. 다른 폰트는 제공되는 실제
굵기를 개별 WOFF2로 등록합니다. 단일 굵기 폰트를 가짜 VF로 변환하지 않습니다.
| 추가 폰트 | 실제 제공 굵기 |
| --- | --- |
| SkyBori | Regular 400 |
| MapoFlowerIsland | Regular 400 |
| HSBombaram 3.0 | Thin·Regular |
| SeoulHangang | Light·Medium·Bold·ExtraBold |
| NanumSquareNeo | VF 100–900 |
| NeoDunggeunmoPro | Regular 400 |
| SUITE | VF 300–900 |
| Maplestory | Light 300·Bold 700 |
| PixelMplus 12 | Regular 400·Bold 700 |
| KokuMincho | Regular 400 |
| Checkpoint (CP Font 2.076) | Regular 400 |
| LightNovelPOP | 단일 굵기 |

단일 굵기 폰트의 다른 weight는 브라우저의 합성 굵기를 사용합니다.
각 디렉터리의 SOURCE.json과 동봉 라이선스/안내문을 확인하세요. WOFF2 변환은
fontTools+Brotli로 수행하며 글리프와 저작권 이름은 바꾸지 않습니다.

Musecat Web은 이 저장소의 푸시된 커밋 SHA에 고정한 jsDelivr URL로 폰트를
불러옵니다. 원본 수정 후 이 저장소를 먼저 푸시하고 Web의 참조 커밋을 갱신합니다.
웹 배포에는 폰트 파일 사본을 저장하지 않습니다. 네이티브 에셋은 별도로 유지합니다.
기존 AstaSans, JetBrainsMono, MinIcon, SourceHanSerifKR 파일은 유지합니다.

`MinIcon/MinIconVF.woff2` is the canonical Musecat MinIcon source. Product
repositories reference this asset instead of storing a second Web WOFF2 copy.
Musecat-specific glyph construction and Native static-face generation scripts
live in `MinIcon/tools/`.

Rebuild `iImageRotated` (U+EC3C, including the `ss09` filled alternate) with
`python3 MinIcon/tools/extend_image_rotated.py`. Its compact arrow matches the
image frame stroke and balances the top/left padding. The script requires
fontTools with WOFF2/Brotli support.
