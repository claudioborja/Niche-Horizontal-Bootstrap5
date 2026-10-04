#!/usr/bin/env python3
"""Measure representative pages with optional Lighthouse tooling, sequentially."""
import argparse
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import statistics
import subprocess
import threading

ROOT = Path(__file__).resolve().parents[1]
METRICS = {
    'fcp_ms': 'first-contentful-paint',
    'lcp_ms': 'largest-contentful-paint',
    'tbt_ms': 'total-blocking-time',
    'cls': 'cumulative-layout-shift',
    'bytes': 'total-byte-weight',
}


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--node', default=shutil.which('node'))
    parser.add_argument('--cli', type=Path, default=ROOT / 'tools/lighthouse/node_modules/lighthouse/cli/index.js')
    parser.add_argument('--output', type=Path, default=ROOT / 'tools/performance-results')
    parser.add_argument('--runs', type=int, default=3)
    parser.add_argument('--pages', nargs='+', default=['index.html', 'pages/pages-blank.html', 'tables/table-data-table.html'])
    parser.add_argument('--chrome-flags', default='--headless')
    args = parser.parse_args()
    if not args.node or not args.cli.is_file():
        parser.error('Install Node.js and run npm ci --prefix tools/lighthouse (see README).')
    if args.runs < 1:
        parser.error('--runs must be positive')
    for page in args.pages:
        path = (ROOT / page).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file() or path.suffix != '.html':
            parser.error('Invalid local page: ' + page)
    args.output.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    results = []
    try:
        for page in args.pages:
            for profile in ('mobile', 'desktop'):
                samples = []
                for run in range(args.runs):
                    output = args.output / f'{Path(page).stem}-{profile}-{run + 1}.json'
                    command = [args.node, str(args.cli), f'http://127.0.0.1:{server.server_port}/{page}',
                               '--only-categories=performance', '--output=json', '--quiet',
                               '--output-path=' + str(output.resolve()), '--chrome-flags=' + args.chrome_flags]
                    if profile == 'desktop':
                        command.append('--preset=desktop')
                    print(f'Measuring {page} / {profile} / {run + 1} of {args.runs}', flush=True)
                    subprocess.run(command, check=True, timeout=180, env=os.environ.copy())
                    report = json.loads(output.read_text())
                    if report.get('runtimeError'):
                        raise RuntimeError(str(report['runtimeError']))
                    sample = {key: report['audits'][audit]['numericValue'] for key, audit in METRICS.items()}
                    sample['score'] = report['categories']['performance']['score'] * 100
                    samples.append(sample)
                entry = {'page': page, 'profile': profile, 'samples': samples,
                         'median': {key: statistics.median(sample[key] for sample in samples) for key in samples[0]},
                         'lighthouse': report['lighthouseVersion'], 'browser': report['environment']['hostUserAgent'],
                         'settings': report['configSettings']}
                results.append(entry)
                print(json.dumps(entry['median']), flush=True)
        (args.output / 'summary.json').write_text(json.dumps(results, indent=2) + '\n')
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    main()
