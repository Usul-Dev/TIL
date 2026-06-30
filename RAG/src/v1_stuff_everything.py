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

DATA_DIR = Path(__file__).parent.parent / "data"
MODEL = "claude-opus-4-8"


def load_docs(data_dir: Path = DATA_DIR) -> dict[str, str]:
    """data/ 안의 .md 문서를 {파일명: 본문}으로 모두 읽는다."""
    files = sorted(data_dir.glob("*.md"))
    return {p.name: p.read_text(encoding="utf-8") for p in files}


def build_prompt(docs: dict[str, str], question: str) -> str:
    """모든 문서를 컨텍스트로 주입한 프롬프트를 만든다 (검색 없이 전부)."""
    context = "\n\n".join(f"## {name}\n{text}" for name, text in docs.items())
    return (
        "아래 문서만 근거로 질문에 답하라. 문서에 없는 내용은 모른다고 답하라.\n\n"
        f"# 문서\n{context}\n\n# 질문\n{question}"
    )


def ask(question: str, docs: dict[str, str] | None = None) -> str:
    """문서를 전부 주입해 LLM에 묻고 답을 받는다. ANTHROPIC_API_KEY 필요."""
    from anthropic import Anthropic

    docs = docs if docs is not None else load_docs()
    prompt = build_prompt(docs, question)
    client = Anthropic()
    msg = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def _selfcheck() -> None:
    """LLM 호출 없이 프롬프트 조립 로직만 검증한다."""
    docs = {"a.md": "Redis는 인메모리 저장소다.", "b.md": "TTL은 만료 시간이다."}
    p = build_prompt(docs, "TTL이 뭐야?")
    assert "Redis는 인메모리" in p and "TTL은 만료" in p, "모든 문서가 주입돼야 한다"
    assert "TTL이 뭐야?" in p, "질문이 포함돼야 한다"
    assert p.index("# 문서") < p.index("# 질문"), "문서가 질문보다 앞에 와야 한다"
    assert load_docs(), "data/에 문서가 있어야 한다"
    print("selfcheck ok")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(ask(sys.argv[1]))
    else:
        _selfcheck()
