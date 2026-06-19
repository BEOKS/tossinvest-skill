# 토스증권 Open API Agent Skill

토스증권 Open API를 Codex, Claude Code 같은 에이전트에서 안전하게 사용할 수 있도록 만든 Agent Skill 저장소입니다. 공식 OpenAPI 문서를 참조 자료로 포함하고, 인증·시세·종목·환율·장운영·계좌·보유자산·주문조회·거래가능정보·주문 생성/정정/취소를 다루는 CLI 헬퍼를 제공합니다.

## 설치

```bash
npx skills add BEOKS/tossinvest-skill
```

설치 후 지원되는 에이전트에서 `$tossinvest-skill`을 호출해 사용할 수 있습니다.

Claude Code처럼 특정 에이전트만 지정해서 설치할 수도 있습니다.

```bash
npx skills add BEOKS/tossinvest-skill --agent claude-code
```

## 주요 기능

- OAuth2 Client Credentials 토큰 발급
- 국내/미국 주식 종목 정보, 현재가, 호가, 체결, 상하한가, 캔들 조회
- KRW/USD 환율과 국내/미국 장 운영 캘린더 조회
- 계좌 목록, 보유 주식, 주문 목록, 주문 상세 조회
- 매수 가능 금액, 매도 가능 수량, 수수료 조회
- 주문 생성, 정정, 취소 dry-run 및 명시적 실행
- 공식 OpenAPI JSON 기반 스키마/엔드포인트 탐색

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

## CLI 예시

설치된 스킬 디렉터리 또는 이 저장소 루트에서 실행합니다.

```bash
python3 scripts/tossinvest.py list-endpoints
python3 scripts/tossinvest.py token
python3 scripts/tossinvest.py stocks --symbols 005930,AAPL
python3 scripts/tossinvest.py prices --symbols 005930,AAPL
python3 scripts/tossinvest.py market-calendar --country KR
```

계좌가 필요한 API:

```bash
python3 scripts/tossinvest.py accounts
python3 scripts/tossinvest.py holdings --account 1
python3 scripts/tossinvest.py buying-power --account 1 --currency KRW
python3 scripts/tossinvest.py orders --account 1 --status OPEN
```

## 주문 안전장치

`create-order`, `modify-order`, `cancel-order`는 실제 금융 거래에 영향을 줄 수 있으므로 기본값은 dry-run입니다.

```bash
python3 scripts/tossinvest.py create-order \
  --account 1 \
  --symbol 005930 \
  --side BUY \
  --order-type LIMIT \
  --quantity 1 \
  --price 70000 \
  --client-order-id test-001
```

실제 실행은 사용자가 주문 내용과 계좌를 명확히 확인한 뒤에만 아래처럼 `--execute --yes`를 함께 전달해야 합니다.

```bash
python3 scripts/tossinvest.py create-order \
  --account 1 \
  --symbol 005930 \
  --side BUY \
  --order-type LIMIT \
  --quantity 1 \
  --price 70000 \
  --client-order-id test-001 \
  --execute \
  --yes
```

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

스킬 메타데이터는 `skill-creator` validator로 검증했습니다.
