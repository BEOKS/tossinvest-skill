# 토스증권 Open API Agent Skill

Codex, Claude Code 같은 에이전트에서 토스증권 Open API를 바로 탐색하고 안전하게 호출할 수 있도록 만든 Agent Skill입니다. 공식 OpenAPI 문서, 작업 흐름, 표준 라이브러리 기반 CLI, 주문 dry-run 안전장치를 함께 묶었습니다.

```bash
npx skills add BEOKS/tossinvest-skill
```

## 왜 쓰나요

- 토스증권 Open API의 인증, 시세, 종목, 계좌, 주문 API를 에이전트가 문서와 스키마 기반으로 다룰 수 있습니다.
- `scripts/tossinvest.py`로 문서 확인에서 끝나지 않고 실제 조회 호출까지 빠르게 검증할 수 있습니다.
- 주문 생성/정정/취소는 기본 dry-run이며, 실제 실행은 `--execute --yes`가 있어야만 동작합니다.

## 빠른 데모

설치된 스킬 디렉터리 또는 이 저장소 루트에서 실행합니다.

```bash
python3 scripts/tossinvest.py list-endpoints
python3 scripts/tossinvest.py stocks --symbols 005930,AAPL
python3 scripts/tossinvest.py prices --symbols 005930,AAPL
```

주문 요청은 기본적으로 실제 주문을 넣지 않고 요청 본문만 보여줍니다.

```bash
python3 scripts/tossinvest.py create-order \
  --account 1 \
  --symbol 005930 \
  --side BUY \
  --order-type LIMIT \
  --quantity 1 \
  --price 70000 \
  --client-order-id dryrun-001
```

예상 출력:

```json
{
  "dryRun": true,
  "method": "POST",
  "path": "/api/v1/orders",
  "account": "1",
  "body": {
    "symbol": "005930",
    "side": "BUY",
    "orderType": "LIMIT",
    "clientOrderId": "dryrun-001",
    "quantity": "1",
    "price": "70000"
  },
  "executeHint": "Re-run with --execute --yes only after explicit user confirmation."
}
```

## 설치

전체 지원 에이전트 대상으로 설치:

```bash
npx skills add BEOKS/tossinvest-skill
```

Claude Code처럼 특정 에이전트만 지정:

```bash
npx skills add BEOKS/tossinvest-skill --agent claude-code
```

설치 없이 프롬프트로 사용:

```bash
npx skills use BEOKS/tossinvest-skill --skill tossinvest-skill --agent claude-code
```

## 지원 에이전트

`npx skills`가 지원하는 에이전트에서 사용할 수 있습니다. 예를 들어 Codex, Claude Code 등에서 스킬 본문과 참조 문서, CLI 사용법을 읽어 작업할 수 있습니다.

OpenAI/Codex 계열 UI를 위한 `agents/openai.yaml`도 포함되어 있지만, 핵심은 범용 `SKILL.md`, `references/`, `scripts/` 구조입니다.

## 주요 기능

- OAuth2 Client Credentials 토큰 발급
- 국내/미국 주식 종목 정보, 현재가, 호가, 체결, 상하한가, 캔들 조회
- KRW/USD 환율과 국내/미국 장 운영 캘린더 조회
- 계좌 목록, 보유 주식, 주문 목록, 주문 상세 조회
- 매수 가능 금액, 매도 가능 수량, 수수료 조회
- 주문 생성, 정정, 취소 dry-run 및 명시적 실행
- 공식 OpenAPI JSON 기반 스키마/엔드포인트 탐색

## 에이전트에게 시킬 수 있는 일

```text
Use $tossinvest-skill to summarize available Toss Securities Open API endpoints.
```

```text
Use $tossinvest-skill to check my account holdings and explain the response fields.
```

```text
Use $tossinvest-skill to prepare a dry-run order request for Samsung Electronics.
```

## 자격증명

다음 환경변수를 설정합니다.

```bash
export TOSS_API_KEY="..."
export TOSS_SECRET_KEY="..."
```

CLI는 프로세스 환경변수를 먼저 읽고, 없으면 `~/.zshrc`, `~/.zprofile`, `~/.profile`의 단순 assignment도 읽습니다. 계좌 API를 자주 쓰면 아래 중 하나를 추가로 설정할 수 있습니다.

```bash
export TOSSINVEST_ACCOUNT="1"
```

토큰은 기본 출력에서 마스킹됩니다. 전체 access token이 꼭 필요한 경우에만 `token --show-token`을 사용하세요.

## CLI 예시

```bash
python3 scripts/tossinvest.py token
python3 scripts/tossinvest.py orderbook --symbol 005930
python3 scripts/tossinvest.py trades --symbol AAPL --count 20
python3 scripts/tossinvest.py candles --symbol 005930 --interval 1d --count 30
python3 scripts/tossinvest.py market-calendar --country KR
```

계좌가 필요한 API:

```bash
python3 scripts/tossinvest.py accounts
python3 scripts/tossinvest.py holdings --account 1
python3 scripts/tossinvest.py buying-power --account 1 --currency KRW
python3 scripts/tossinvest.py sellable-quantity --account 1 --symbol 005930
python3 scripts/tossinvest.py orders --account 1 --status OPEN
```

## 주문 안전장치

`create-order`, `modify-order`, `cancel-order`는 실제 금융 거래에 영향을 줄 수 있으므로 기본값은 dry-run입니다.

실제 실행은 사용자가 주문 내용과 계좌를 명확히 확인한 뒤에만 아래처럼 `--execute --yes`를 함께 전달해야 합니다.

```bash
python3 scripts/tossinvest.py create-order \
  --account 1 \
  --symbol 005930 \
  --side BUY \
  --order-type LIMIT \
  --quantity 1 \
  --price 70000 \
  --client-order-id order-001 \
  --execute \
  --yes
```

라이브 주문 생성은 기본적으로 `--client-order-id`도 요구합니다. 멱등성 키 없이 실행하려면 의도적으로 `--allow-no-client-order-id`를 추가해야 합니다.

## 저장소 구성

- `SKILL.md`: 에이전트가 읽는 스킬 진입점
- `agents/openai.yaml`: OpenAI/Codex 계열 UI 메타데이터
- `references/workflows.md`: 엔드포인트 맵과 작업 흐름
- `references/openapi.json`: 공식 OpenAPI JSON 사본
- `references/official-overview.md`: 공식 개요 문서 사본
- `references/api-reference-index.md`: 공식 API reference index 사본
- `scripts/tossinvest.py`: 표준 라이브러리 기반 CLI 헬퍼

## 검증

```bash
python3 scripts/tossinvest.py list-endpoints
python3 scripts/tossinvest.py create-order --account 1 --symbol 005930 --side BUY --order-type LIMIT --quantity 1 --price 70000 --client-order-id dryrun-001
```

스킬 메타데이터는 `skill-creator` validator로 검증했습니다. `npx skills add BEOKS/tossinvest-skill`로 원격 설치도 확인했습니다.

## 주의

이 프로젝트는 투자 조언을 제공하지 않습니다. 계좌 조회와 주문 API는 실제 금융 계정에 영향을 줄 수 있으므로, 라이브 주문 실행 전 계좌, 종목, 방향, 수량, 가격을 반드시 직접 확인하세요.
