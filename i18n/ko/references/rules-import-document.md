# 문서 가져오기 및 파싱 규칙

> 사용자가 PDF / DOCX / PPTX 파일을 업로드하거나 `/parse [파일]`을 트리거할 때 로드됩니다.
> 최초 사용 시, 먼저 `rules-document-tools.md`를 로드하여 도구 설치 여부를 확인합니다.
> 이 규칙은 `rules-file-integration.md`와 함께 작동합니다 — 해당 파일은 "언제 트리거할지"를 정의하고, 이 파일은 "어떻게 파싱할지"를 정의합니다.

---

## 파싱 목표

모든 형식의 입력 문서를 **구조화된 Markdown**으로 변환하여 후속 플로우에 활용:
- 기능 확장 / 리비전 모드 S1 컨텍스트 수집
- 증분 업데이트 원본 문서 베이스라인
- 일반 문서 내용 추출

---

## PDF 파싱: 3계층 전략 + 페이지별 감지

### 개요

```
입력 PDF
  │
  ▼
pymupdf 페이지별 텍스트 추출 (비용 없음)
  │
  ├── 페이지 텍스트 > 30자 → ✅ Markdown으로 직접 변환 (계층 1)
  │
  └── 페이지 텍스트 ≤ 30자 (빈 페이지 / 벡터 경로 / 스캔본)
        │
        ├── 기본값 → Claude Vision 시맨틱 파싱 (계층 2)
        │
        └── Vision 사용 불가 / 토큰 예산 부족 → Tesseract OCR (계층 3)
```

### 1단계: 페이지별 유형 감지

**핵심 원칙**: 전체 문서가 아닌 "페이지" 단위로 감지합니다. 하나의 PDF에 디지털 텍스트 페이지와 스캔 이미지 페이지가 혼합될 수 있습니다.

```python
import fitz  # pymupdf

doc = fitz.open(pdf_path)
total_pages = len(doc)
page_results = {}

for i in range(total_pages):
    page = doc[i]
    text = page.get_text("text").strip()

    if len(text) > 30:
        # 계층 1: 디지털 텍스트, 직접 추출
        page_results[i] = {"type": "digital", "text": text}
    else:
        # Vision 또는 OCR 필요
        page_results[i] = {"type": "needs_vision", "text": None}

digital_count = sum(1 for p in page_results.values() if p["type"] == "digital")
vision_count = total_pages - digital_count

print(f"PDF 분석: {total_pages} 페이지, {digital_count} 직접 추출 가능, {vision_count} 시각적 파싱 필요")
```

### 2단계: 대용량 파일 처리 전략

| 조건 | 전략 |
|------|------|
| 모든 페이지가 디지털 (vision_count = 0) | 모든 페이지 직접 추출, 비용 없음 |
| vision_count ≤ 20 | 시각적 파싱이 필요한 모든 페이지를 한 번에 Claude Vision으로 읽기 |
| vision_count > 20 | 배치로 처리 (배치당 ≤ 20페이지), 결과 병합 |
| 총 페이지 > 50 그리고 vision_count > 20 | 전체 문서 파싱 또는 페이지 범위 지정 여부를 사용자에게 확인 |

**대용량 파일 (>50페이지) 사용자 확인 프롬프트**:

```
📄 이 PDF는 {total_pages} 페이지입니다:
  • {digital_count} 페이지는 직접 추출 가능 (무료)
  • {vision_count} 페이지는 시각적 파싱 필요 (Vision 토큰 소모)

선택해 주세요:
  1️⃣ 전체 문서 파싱 (완전하지만 토큰 소모 증가)
  2️⃣ 특정 페이지만 파싱 (페이지 범위 입력, 예: 1-10,15,20-25)
  3️⃣ 직접 추출 가능한 페이지만 추출 (스캔/벡터 페이지 건너뛰기)
```

### 3단계: 계층 1 — pymupdf 직접 추출

```python
def extract_digital_pages(doc, page_results):
    """모든 디지털 텍스트 페이지 추출"""
    markdown_parts = []
    for i, result in sorted(page_results.items()):
        if result["type"] == "digital":
            markdown_parts.append(f"<!-- Page {i+1} -->\n{result['text']}")
    return "\n\n".join(markdown_parts)
```

### 4단계: 계층 2 — Claude Vision 시맨틱 파싱

`needs_vision` 유형 페이지의 경우, 먼저 pymupdf로 PNG로 렌더링한 후 Claude의 Read 도구로 읽습니다.

**이미지 렌더링**:
```python
def render_pages_to_png(doc, page_indices, dpi=300):
    """지정된 페이지를 PNG로 렌더링"""
    output_files = []
    for i in page_indices:
        page = doc[i]
        pix = page.get_pixmap(dpi=dpi)
        output_path = f"/tmp/pdf-page-{i+1:04d}.png"
        pix.save(output_path)
        output_files.append((i, output_path))
    return output_files
```

**Claude Vision 파싱 프롬프트**:

시각적 파싱이 필요한 각 페이지(또는 배치)에 대해, Read 도구로 PNG를 읽은 후 다음 프롬프트로 변환:

```
You are reading page {page_num}/{total_pages} of a PDF document.
Please convert the content of this page precisely into Markdown format.

Strict rules:
1. Tables → Markdown table (preserve all columns, rows, and alignment)
2. Headings → # / ## / ### corresponding to original level
3. Numbered lists → 1. 2. 3. (preserve original numbering)
4. Bullet points → - or •
5. Bold/Italic → **bold** / *italic*
6. Charts/Images → > [Chart: brief description]
7. Headers, footers, page numbers → Ignore
8. Numbers, dates, names, account numbers → Must be 100% accurate, do not guess
9. Do not add content not present in the original
10. Do not translate — preserve the original language
```

> **OCR보다 나은 이유**: Claude는 테이블의 "시맨틱 구조"(어떤 행이 헤더인지, 어떤 열이 정렬되어 있는지)를 이해하지만, Tesseract는 문자를 하나씩 인식한 후 규칙으로 테이블을 재구성하려 시도하며, 이는 자주 실패합니다.

### 5단계: 계층 3 — Tesseract OCR 폴백

다음 상황에서만 사용:
- 사용자가 토큰 절약을 명시적으로 요청
- Claude Vision 사용 불가 (API 제한 등)
- 오프라인 환경

```python
import subprocess
from PIL import Image

def ocr_page(png_path, lang="chi_tra+eng"):
    """Tesseract OCR 단일 페이지"""
    # macOS tesseract는 PNG를 직접 읽지 못할 수 있으므로, TIFF로 변환하거나 stdin 사용
    tiff_path = png_path.replace('.png', '.tiff')
    Image.open(png_path).save(tiff_path)

    result = subprocess.run(
        ['tesseract', 'stdin', 'stdout', '-l', lang],
        stdin=open(tiff_path, 'rb'),
        capture_output=True, text=True, timeout=120
    )
    return result.stdout
```

**Tesseract 참고 사항 (실무 경험 기반)**:
- macOS에서 tesseract는 PNG 파일을 직접 읽지 못할 수 있음 — `stdin` 파이프 사용 또는 TIFF로 변환 권장
- 권장 해상도: 300dpi
- `chi_tra+eng` 언어 팩으로 중국어 번체와 영어 동시 인식
- OCR 결과는 후처리 필요: 끊어진 줄 병합, 테이블 구조 복구

### 6단계: 전체 페이지 병합

```python
def merge_all_pages(digital_md, vision_md_list):
    """모든 페이지의 Markdown을 페이지 순서대로 병합"""
    all_pages = {}
    # 디지털 페이지
    for page_num, md in digital_md.items():
        all_pages[page_num] = md
    # vision/ocr 페이지
    for page_num, md in vision_md_list.items():
        all_pages[page_num] = md

    # 페이지 번호순으로 정렬 후 병합
    final_md = []
    for i in sorted(all_pages.keys()):
        final_md.append(all_pages[i])

    return "\n\n---\n\n".join(final_md)
```

### 7단계: 출력 및 사용자 알림

```
📄 PDF 파싱 완료:
  • 총 페이지: {total_pages}
  • 직접 추출: {digital_count} 페이지 (pymupdf)
  • 시각적 파싱: {vision_count} 페이지 (Claude Vision)
  • 출력: {output_path} (Markdown, {word_count} 단어)
```

---

## DOCX 파싱

```bash
pandoc "{input_path}" -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

**후처리**:
- Pandoc이 생성한 과도한 빈 줄 제거
- 테이블 서식이 올바른지 확인

---

## PPTX 파싱

```bash
pandoc "{input_path}" -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

> Pandoc은 각 슬라이드를 `##` 제목 섹션으로 변환합니다.

---

## HTML 파싱

```bash
pandoc "{input_path}" -f html -t markdown -o "/tmp/parsed-{timestamp}.md" --wrap=none
```

---

## 이미지 파싱

Claude Read 도구를 직접 사용하여 이미지를 읽은 후, Vision 파싱 프롬프트로 Markdown으로 변환합니다.

---

## rules-file-integration.md와의 연동

`rules-file-integration.md`가 다음 시나리오를 감지하면, 이 규칙이 로드됩니다:

| 시나리오 | 작업 |
|---------|------|
| 사용자가 기능 확장 S1에서 PDF 업로드 | 이 규칙 로드 → PDF 파싱 → 기존 시스템 컨텍스트 추출 |
| 사용자가 리비전 S1에서 기존 PRD 업로드 | 이 규칙 로드 → PDF 파싱 → 리비전 베이스라인으로 활용 |
| 사용자가 `/parse` 명령 사용 | 이 규칙 로드 → 지정된 파일 파싱 → Markdown 출력 |
| 사용자가 시장 보고서 PDF 업로드 | 이 규칙 로드 → 핵심 정보 추출 → 해당 단계에 통합 |

### 원본 문서 식별

파싱 완료 후, 파일이 "원본 문서" (PRD, 스펙 등)로 식별되면 자동으로 표시:

```
📎 원본 문서 감지됨 — 최종 산출물은 이 파일을 기반으로 한 증분 업데이트가 됩니다.
  문서 구조: {section_count}개 섹션, {table_count}개 테이블
  서식 규칙: [식별된 서식 특성]
```

문서 구조는 `rules-export-document.md`에서 최종 출력 시 사용하기 위해 기록됩니다.
