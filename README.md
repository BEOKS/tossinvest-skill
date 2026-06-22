> **투자 책임 고지:** 이 스킬을 활용해 투자 분석, 자동/자율 주문, 매수/매도 실행을 하는 모든 판단과 결과의 책임은 전적으로 사용자 본인에게 있습니다. 이 프로젝트와 에이전트는 수익을 보장하지 않으며, 손실 가능성을 없애지 않습니다.

# 토스증권 Open API Agent Skill

Codex, Claude Code 같은 에이전트에서 토스증권 Open API를 바로 탐색하고 호출할 수 있도록 만든 Agent Skill입니다. 공식 OpenAPI 문서, 작업 흐름, 표준 라이브러리 기반 CLI, 주문 dry-run, 그리고 사용자가 자연어로 위임한 자율 매수/매도 실행 흐름을 함께 묶었습니다.

```bash
npx skills add BEOKS/tossinvest-skill
```

## 왜 쓰나요

- 토스증권 Open API의 인증, 시세, 종목, 계좌, 주문 API를 에이전트가 문서와 스키마 기반으로 다룰 수 있습니다.
- `scripts/tossinvest.py`로 문서 확인에서 끝나지 않고 실제 조회 호출까지 빠르게 검증할 수 있습니다.
- 사용자가 자율거래를 위임하면 에이전트가 계좌, 시세, 호가, 체결, 장 상태를 확인하면서 매수/매도/정정/취소를 반복 수행할 수 있습니다.
- 주문 생성/정정/취소는 CLI 기본값이 dry-run이며, 실제 실행은 `--execute --yes`가 있어야만 동작합니다.

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
  "executeHint": "Re-run with --execute --yes after explicit confirmation, or while operating under a user-delegated autonomous trading instruction."
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
- 자연어로 위임된 자율 매수/매도 주문 루프
- 주문 생성, 정정, 취소 dry-run 및 live 실행
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

```text
Use $tossinvest-skill to trade my Toss account autonomously during today's KR market session.
```

```text
Use $tossinvest-skill to manage delegated buy and sell orders for short-term profit.
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

## 자율 주문 실행

`create-order`, `modify-order`, `cancel-order`는 실제 금융 거래에 영향을 줄 수 있으므로 기본값은 dry-run입니다.

사용자가 자연어로 자율거래를 위임하면 에이전트는 현재 계좌, 매수 가능 금액, 매도 가능 수량, 장 운영 상태, 종목 경고, 수수료, 현재가, 호가, 체결, 캔들을 확인하면서 주문 생성, 정정, 취소를 반복 수행할 수 있습니다. 이 모델은 매 주문마다 다시 확인받는 방식이 아니라, 사용자의 위임이 유지되는 동안 에이전트가 live mutation에 `--execute --yes`를 붙여 실행할 수 있는 방식입니다.

직접 CLI로 live 주문을 실행할 때도 아래처럼 `--execute --yes`를 함께 전달해야 합니다.

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

이 프로젝트는 수익을 보장하지 않습니다. 계좌 조회와 주문 API는 실제 금융 계정에 영향을 줄 수 있으며, 사용자가 자율거래를 위임하면 에이전트의 live 주문 실행 결과도 사용자 본인의 책임입니다.
