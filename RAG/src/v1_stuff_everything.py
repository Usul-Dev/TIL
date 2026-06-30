"""v1: 검색 없는 최소 RAG.

문서를 통째로 프롬프트에 넣고 LLM에 묻는다. 벡터 검색·임베딩·청킹 없음.

ponytail: 문서가 적어 프롬프트 한도 안에 다 들어갈 때만 유효한 구조다.
문서를 늘리면 토큰이 선형으로 커지다 한도를 넘긴다 — 그 불편이 v2(벡터 검색)의 이유다.

실행:
    uv run python src/v1_stuff_everything.py         # self-check (API 키 불필요)
    uv run python src/v1_stuff_everything.py "질문"  # 실제 질의 (ANTHROPIC_API_KEY)
"""

import sys
from pathlib import Path

import pymupdf
from anthropic import Anthropic

DATA_DIR = Path(__file__).parent.parent / "data"
MODEL = "claude-opus-4-8"


def load_docs(data_dir: Path = DATA_DIR) -> dict[str, str]:
    """data/ 안의 .pdf 문서에서 텍스트를 추출해 {파일명: 본문}으로 모두 읽는다.

    실무 RAG 입력은 대부분 PDF·문서 파일이라 PDF 텍스트 추출부터 시작한다.
    추출은 PyMuPDF(속도·정확도 균형). 단 AGPL 라이선스라 상용 배포 시 주의.
    """
    docs = {}
    for p in sorted(data_dir.glob("*.pdf")):
        with pymupdf.open(p) as doc:
            docs[p.name] = "\n".join(page.get_text() for page in doc)
    return docs


def build_prompt(docs: dict[str, str], question: str) -> str:
    """모든 문서를 컨텍스트로 주입한 프롬프트를 만든다 (검색 없이 전부).

    문서마다 [파일명] 머리표를 붙여, LLM이 근거 문서를 출처로 인용할 수 있게 한다.
    """
    context = "\n\n".join(f"## [{name}]\n{text}" for name, text in docs.items())
    return (
        "아래 문서만 근거로 질문에 답하라. 문서에 없는 내용은 모른다고 답하라.\n"
        "답변 끝에 근거가 된 문서명을 `[출처: 파일명]` 형식으로 밝혀라.\n\n"
        f"# 문서\n{context}\n\n# 질문\n{question}"
    )


def ask(question: str, docs: dict[str, str] | None = None) -> str:
    """문서를 전부 주입해 LLM에 묻고 답을 받는다. ANTHROPIC_API_KEY 필요."""
    docs = docs if docs is not None else load_docs()
    if not docs:
        raise SystemExit(f"{DATA_DIR}에 PDF가 없다. 문서를 넣고 다시 실행하라.")
    prompt = build_prompt(docs, question)
    client = Anthropic()
    msg = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    # 학습용 가시성: 어떤 문서가 통째로 들어갔고 토큰이 얼마나 들었는지 보여준다.
    # ponytail: stderr로만 빼 답변(stdout)은 깨끗하게 유지.
    u = msg.usage
    print(
        f"[주입 문서] {', '.join(docs)}\n"
        f"[토큰] input={u.input_tokens:,} output={u.output_tokens:,}",
        file=sys.stderr,
    )
    return msg.content[0].text


def _selfcheck() -> None:
    """LLM 호출 없이 프롬프트 조립 로직만 검증한다."""
    docs = {"a.pdf": "Redis는 인메모리 저장소다.", "b.pdf": "TTL은 만료 시간이다."}
    p = build_prompt(docs, "TTL이 뭐야?")
    assert "Redis는 인메모리" in p and "TTL은 만료" in p, "모든 문서가 주입돼야 한다"
    assert "TTL이 뭐야?" in p, "질문이 포함돼야 한다"
    assert p.index("# 문서") < p.index("# 질문"), "문서가 질문보다 앞에 와야 한다"
    assert "[a.pdf]" in p and "출처" in p, "출처 표기(머리표·지시)가 있어야 한다"

    # 빈 입력 가드: LLM 호출 전에 막혀야 한다 (API 키 불필요)
    try:
        ask("아무 질문", docs={})
        raise AssertionError("빈 문서면 SystemExit이 나야 한다")
    except SystemExit:
        pass

    loaded = load_docs()
    assert loaded, "data/에 PDF 문서가 있어야 한다"
    assert all(v.strip() for v in loaded.values()), "PDF에서 텍스트가 추출돼야 한다"
    print("selfcheck ok")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(ask(sys.argv[1]))
    else:
        _selfcheck()
