import contextlib
import gzip
import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

spec = importlib.util.spec_from_file_location('tossinvest', Path(__file__).resolve().parents[1] / 'tossinvest.py')
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


class ClientTests(unittest.TestCase):
    def test_gzip_and_plain_json(self):
        payload = {'error': 'invalid_client', 'error_description': '인증 실패'}
        raw = json.dumps(payload, ensure_ascii=False).encode()
        self.assertEqual(cli.decode_body(raw), payload)
        self.assertEqual(cli.decode_body(gzip.compress(raw)), payload)
        self.assertEqual(cli.decode_body(b''), None)
        self.assertEqual(cli.decode_body(b'not json'), 'not json')

    def test_gzip_http_error_retains_diagnostics(self):
        args = cli.build_parser().parse_args(['accounts'])
        body = {'error': 'invalid_client'}
        error = HTTPError('https://example.invalid', 401, 'Unauthorized',
                          {'X-Request-Id': 'test-id', 'ReferenceId': 'ref-id'},
                          io.BytesIO(gzip.compress(json.dumps(body).encode())))
        self.addCleanup(error.close)
        with patch.object(cli, 'urlopen', side_effect=error):
            with self.assertRaises(cli.TossApiError) as caught:
                cli.request_json('GET', '/api/v1/accounts', auth=False, args=args)
        self.assertEqual(caught.exception.body, body)
        self.assertEqual(cli.selected_headers(caught.exception.headers)['referenceid'], 'ref-id')

    def test_gzip_oauth_success(self):
        args = cli.build_parser().parse_args(['--no-token-cache', 'token'])
        response = io.BytesIO(gzip.compress(b'{"access_token":"test-token","expires_in":600}'))
        with patch.object(cli, 'env_first', return_value='test-credential'), patch.object(cli, 'urlopen', return_value=response):
            self.assertEqual(cli.get_access_token(args), 'test-token')

    def test_gzip_429_retry_preserves_request(self):
        args = cli.build_parser().parse_args(['--max-retries', '1', 'accounts'])
        error = HTTPError('https://example.invalid', 429, 'Rate limited',
                          {'Retry-After': '1'}, io.BytesIO(gzip.compress(b'{"error":"rate-limit-exceeded"}')))
        self.addCleanup(error.close)
        response = io.BytesIO(gzip.compress(b'{"result":[]}'))
        response.status, response.headers = 200, {}
        with patch.object(cli, 'urlopen', side_effect=[error, response]) as send, patch.object(cli.time, 'sleep') as sleep:
            status, _, body = cli.request_json('GET', '/api/v1/accounts', auth=False, args=args)
        self.assertEqual((status, body), (200, {'result': []}))
        self.assertEqual(send.call_count, 2)
        self.assertEqual(send.call_args_list[0].args[0].full_url, send.call_args_list[1].args[0].full_url)
        self.assertGreaterEqual(sleep.call_args.args[0], 1)

    def test_stale_cached_token_refreshes_once(self):
        args = cli.build_parser().parse_args(['accounts'])
        errors = [HTTPError('https://example.invalid', 401, 'Unauthorized', {},
                            io.BytesIO(gzip.compress(b'{"error":"invalid-token"}'))) for _ in range(2)]
        for error in errors:
            self.addCleanup(error.close)
        with patch.object(cli, 'TOKEN_FROM_CACHE', True), patch.object(cli, 'get_access_token', return_value='test-token') as token, patch.object(cli, 'urlopen', side_effect=errors) as send:
            with self.assertRaises(cli.TossApiError):
                cli.request_json('GET', '/api/v1/accounts', args=args)
        self.assertEqual(send.call_count, 2)
        self.assertFalse(token.call_args_list[0].kwargs['force_refresh'])
        self.assertTrue(token.call_args_list[1].kwargs['force_refresh'])

    def test_opg_dry_run_and_no_network(self):
        args = cli.build_parser().parse_args(['create-order', '--account', '1', '--symbol', '005930', '--side', 'BUY', '--order-type', 'LIMIT', '--quantity', '1', '--price', '70000', '--time-in-force', 'OPG'])
        with patch.object(cli, 'request_json', side_effect=AssertionError('unexpected network')), contextlib.redirect_stdout(io.StringIO()) as out:
            args.func(args)
        self.assertEqual(json.loads(out.getvalue())['body']['timeInForce'], 'OPG')

    def test_conditional_order_mutations_default_to_dry_run(self):
        for method, path in [('POST', '/api/v1/conditional-orders'), ('POST', '/api/v1/conditional-orders/example/modify'), ('DELETE', '/api/v1/conditional-orders/example')]:
            args = cli.build_parser().parse_args(['request', '--method', method, '--path', path, '--account', '1'])
            with patch.object(cli, 'request_json', side_effect=AssertionError('unexpected network')), contextlib.redirect_stdout(io.StringIO()) as out:
                args.func(args)
            self.assertTrue(json.loads(out.getvalue())['dryRun'])
            args.execute = True
            with patch.object(cli, 'request_json', side_effect=AssertionError('unexpected network')), self.assertRaisesRegex(SystemExit, '--execute and --yes'):
                args.func(args)


if __name__ == '__main__':
    unittest.main()
