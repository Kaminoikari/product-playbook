# 문서 변환 도구 의존성 관리

> `/export` 또는 `/parse` 명령 최초 트리거 시 로드됩니다.

## 의존성 티어

| 티어 | 도구 | 목적 | 설치 방법 | 크기 |
|------|------|------|----------|------|
| **Core (설치 불필요)** | Claude Read tool (Vision) | PDF 시맨틱 파싱 | 내장 | 0 |
| **Core (설치 불필요)** | Playwright MCP | PDF 렌더링 | 내장 | 0 |
| **Basic** | pymupdf (fitz) | PDF 텍스트 추출 + 이미지 렌더링 | `pip3 install --break-system-packages pymupdf` | ~23MB |
| **Basic** | pikepdf | PDF 북마크 삽입 + 메타데이터 | `pip3 install --break-system-packages pikepdf` | ~5MB |
| **Extended** | pandoc | DOCX / PPTX 변환 | `brew install pandoc` | ~50MB |
| **Fallback** | tesseract + chi_tra | 오프라인 OCR (Vision 사용 불가 시) | `brew install tesseract tesseract-lang` | ~150MB |
| **Advanced** | python-docx | 고품질 DOCX 출력 | `pip3 install --break-system-packages python-docx` | ~5MB |

## 시작 시 감지 플로우

사용자가 문서 변환 기능을 처음 트리거하면, 다음 순서로 감지 및 설치를 진행합니다:

### 1단계: 필요한 도구 결정

| 사용자 액션 | 필요한 도구 |
|------------|-----------|
| `/export pdf` | pymupdf + pikepdf + Playwright MCP |
| `/export docx` 또는 `/export pptx` | pandoc |
| `/parse [PDF 파일]` | pymupdf (+ Claude Vision 또는 tesseract) |
| `/parse [DOCX/PPTX 파일]` | pandoc |

### 2단계: 설치된 도구 감지

다음 Bash 명령을 실행합니다 (무음 감지, 출력 표시 안 함):

```bash
# pymupdf
python3 -c "import fitz; print(fitz.version)" 2>/dev/null && echo "pymupdf: OK" || echo "pymupdf: MISSING"

# pikepdf
python3 -c "import pikepdf; print(pikepdf.__version__)" 2>/dev/null && echo "pikepdf: OK" || echo "pikepdf: MISSING"

# pandoc
which pandoc >/dev/null 2>&1 && echo "pandoc: OK" || echo "pandoc: MISSING"

# tesseract (명시적으로 필요한 경우에만 감지)
which tesseract >/dev/null 2>&1 && tesseract --list-langs 2>&1 | grep -q chi_tra && echo "tesseract: OK" || echo "tesseract: MISSING"
```

### 3단계: 누락된 도구 자동 설치

누락된 도구가 감지되면, 다음 메시지를 표시하고 자동으로 설치합니다:

```
📦 문서 변환에 다음 도구가 필요합니다:
  ☐ [도구명] ([목적], [크기])
  ...
설치 중입니다, 잠시 기다려 주세요...
```

설치 명령을 순서대로 실행합니다:

```bash
# pymupdf + pikepdf (함께 설치)
pip3 install --break-system-packages pymupdf pikepdf

# pandoc
brew install pandoc

# tesseract (오프라인 OCR이 필요한 경우에만)
brew install tesseract tesseract-lang
```

설치 완료 후 표시:
```
✅ 도구 설치 완료, 계속 진행합니다...
```

### 4단계: Playwright MCP 감지

Playwright MCP는 PDF 렌더링의 핵심 의존성입니다. 감지 방법:

1. `mcp__plugin_playwright_playwright__browser_run_code` 호출 시도
2. MCP 사용 가능 → 정상 사용
3. MCP 사용 불가 (연결 안 됨) → 표시:

```
⚠️ Playwright MCP가 연결되어 있지 않습니다. PDF 렌더링에는 Playwright 브라우저가 필요합니다.
다음 중 하나를 수행해 주세요:
  1. Playwright MCP 시작 (권장)
  2. 또는 ! npx playwright install chromium 을 실행하여 로컬 Chromium 설치
```

**Playwright 폴백** (MCP 사용 불가 시):

사용자가 로컬 Chromium을 설치한 경우, Bash로 Node.js 스크립트를 실행하여 PDF 렌더링:
```bash
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(require('fs').readFileSync('/tmp/export.html', 'utf8'));
  await page.pdf({ path: '${OUTPUT_PATH}', format: 'A4', printBackground: true,
    margin: { top: '1.8cm', bottom: '1.8cm', left: '2cm', right: '2cm' } });
  await browser.close();
})();
"
```

## 도구 상태 캐시

최초 감지 결과를 메모리에 기록합니다 (반복 감지 방지):
- 동일 대화 세션 내에서, 설치 확인된 도구는 재감지하지 않음
- 설치 실패 시, 오류 메시지를 기록하고 다음 트리거 시 재시도

## 플랫폼 호환성

| 플랫폼 | pymupdf | pikepdf | pandoc | tesseract | Playwright |
|--------|---------|---------|--------|-----------|------------|
| macOS (Homebrew) | ✅ pip3 | ✅ pip3 | ✅ brew | ✅ brew | ✅ MCP/npx |
| Linux (apt) | ✅ pip3 | ✅ pip3 | ✅ apt | ✅ apt | ✅ MCP/npx |
| Windows (WSL) | ✅ pip3 | ✅ pip3 | ✅ choco | ✅ choco | ✅ MCP/npx |

사용자의 운영 체제에 따라 해당 패키지 관리자를 자동으로 선택합니다. 감지 방법:
```bash
[[ "$(uname)" == "Darwin" ]] && echo "macOS" || echo "Linux"
```
