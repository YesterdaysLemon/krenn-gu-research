"""Replay every packaged DRAT proof with an independently supplied checker.

Run under Linux/WSL with an outer process-group timeout and memory limit.
The instance directory contains r1-scaffold-000.cnf through -017.cnf.
Output must be a new directory outside the certificate package. Proofs are
decompressed only into a temporary directory there, removed on normal exit.
No SAT solver or non-standard Python dependency is used.
"""
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import os
import platform
import subprocess
import tempfile
import time
import zlib

SPEC_PIN = '34d3f3557e952d0c2d03c3b2f8fcb04c2f786400209f76e8e39a7dcbc9e31b8d'
CASE_IDS = tuple(f'r1-scaffold-{i:03d}' for i in range(18))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def identity(raw):
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def check_identity(raw, expected, label):
    actual = identity(raw)
    require(actual['sha256'] == expected['sha256'] and actual['bytes'] == expected['bytes'], label + ': raw identity differs')
    return actual


def validate_cnf(raw, expected):
    actual = check_identity(raw, expected, 'CNF')
    lines = raw.decode('ascii').splitlines()
    variables, clauses = expected['variables'], expected['clauses']
    require(type(variables) is int and type(clauses) is int, 'Noninteger CNF dimensions')
    require(lines[0].split() == ['p', 'cnf', str(variables), str(clauses)], 'CNF header differs')
    require(len(lines) == clauses + 1, 'CNF clause count differs')
    for line in lines[1:]:
        literals = [int(token) for token in line.split()]
        require(bool(literals) and literals[-1] == 0, 'Unterminated CNF clause')
        require(all(0 < abs(literal) <= variables for literal in literals[:-1]), 'Out-of-range or embedded-zero CNF literal')
    return actual


def invoke(checker, cnf, proof, log, seconds):
    command = [str(checker), str(cnf), str(proof)]
    start = time.monotonic()
    timed_out = False
    with log.open('wb') as handle:
        try:
            result = subprocess.run(command, stdout=handle, stderr=subprocess.STDOUT, timeout=seconds)
            exit_code = result.returncode
        except subprocess.TimeoutExpired:
            # subprocess.run kills and waits for the native checker itself.
            # No new session is created: outer group containment also applies.
            timed_out = True
            exit_code = None
    raw_log = log.read_bytes()
    lines = raw_log.decode('utf-8', errors='replace').splitlines()
    verified = 's VERIFIED' in lines
    rejected = 's NOT VERIFIED' in lines
    return {'command': command, 'exit_code': exit_code, 'timed_out': timed_out,
            'seconds': time.monotonic() - start, 'exact_verified_line': verified,
            'exact_not_verified_line': rejected, 'log': str(log),
            'log_identity': identity(raw_log),
            'accepted': not timed_out and exit_code == 0 and verified and not rejected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--instance-dir', type=Path, required=True)
    parser.add_argument('--checker', type=Path, required=True)
    parser.add_argument('--checker-sha256', help='Expected hash of an independently trusted checker build; defaults to the recorded audited binary hash.')
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--case-timeout-seconds', type=float, default=10.0)
    args = parser.parse_args()
    require(os.name == 'posix', 'Execute this native-checker driver under Linux or WSL')
    require(0 < args.case_timeout_seconds <= 180, 'Case timeout must be in (0,180] seconds')
    certificate, instances, checker, output = (p.resolve() for p in (args.certificate, args.instance_dir, args.checker, args.output_dir))
    require(not output.is_relative_to(certificate.parent), 'Output must be outside the certificate package')
    require(not output.exists(), 'Output directory must be new; refusing to overwrite a prior replay')
    output.mkdir(parents=True)
    receipt_path = output / 'replay.json'
    receipt = {'schema': 'packaged-drat-replay-v1', 'status': 'HOLD', 'started': time.time(),
               'scope': 'All 18 exact packaged CNF/DRAT pairs only; mathematical cover and source/cut semantics are separate obligations.',
               'codec': {'module': 'gzip', 'python_version': platform.python_version(),
                         'zlib_compile_version': zlib.ZLIB_VERSION, 'zlib_runtime_version': zlib.ZLIB_RUNTIME_VERSION},
               'driver_identity': identity(Path(__file__).read_bytes()),
               'controls': [], 'cases': [{'id': label, 'status': 'PENDING'} for label in CASE_IDS]}

    def save():
        receipt_path.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')

    try:
        save()
        spec_raw = certificate.read_bytes()
        require(identity(spec_raw)['sha256'] == SPEC_PIN, 'Certificate specification hash differs')
        spec = json.loads(spec_raw)
        require(spec['schema_version'] == 1 and len(spec['cases']) == 18, 'Certificate case count/schema differs')
        by_id = {row['id']: row for row in spec['cases']}
        require(set(by_id) == set(CASE_IDS), 'Certificate case IDs incomplete or duplicated')
        checker_identity = identity(checker.read_bytes())
        reference_hash = spec['checker']['executed_binary_sha256']
        expected_checker_hash = reference_hash if args.checker_sha256 is None else args.checker_sha256.lower()
        require(len(expected_checker_hash) == 64 and all(c in '0123456789abcdef' for c in expected_checker_hash), 'Expected checker hash must be 64 hexadecimal digits')
        require(checker_identity['sha256'] == expected_checker_hash, 'Supplied checker does not match its expected executable hash')
        receipt.update(certificate_identity=identity(spec_raw), checker_identity=checker_identity,
                       checker_source_reference=spec['checker'], case_timeout_seconds=args.case_timeout_seconds,
                       expected_checker_sha256=expected_checker_hash,
                       checker_matches_recorded_audited_binary=checker_identity['sha256'] == reference_hash,
                       checker_hash_override_supplied=args.checker_sha256 is not None)
        with tempfile.TemporaryDirectory(prefix='decompressed-', dir=output) as temporary_name:
            temporary = Path(temporary_name)
            controls = [
                ('valid-proof', 'p cnf 2 4\n1 2 0\n1 -2 0\n-1 2 0\n-1 -2 0\n', '1 0\n0\n', True),
                ('invalid-empty-step', 'p cnf 2 4\n1 2 0\n1 -2 0\n-1 2 0\n-1 -2 0\n', '0\n', False),
                ('satisfiable-false-proof', 'p cnf 2 2\n1 2 0\n-1 2 0\n', '0\n', False),
            ]
            for label, cnf_text, proof_text, expected in controls:
                cnf_path, proof_path = temporary / (label + '.cnf'), temporary / (label + '.drat')
                cnf_path.write_bytes(cnf_text.encode('ascii'))
                proof_path.write_bytes(proof_text.encode('ascii'))
                result = invoke(checker, cnf_path, proof_path, output / (label + '.log'), args.case_timeout_seconds)
                result.update(id=label, expected_acceptance=expected,
                              cnf_identity=identity(cnf_path.read_bytes()), proof_identity=identity(proof_path.read_bytes()))
                result['status'] = 'PASS' if result['accepted'] == expected and not result['timed_out'] and (expected or result['exit_code'] != 0) else 'FAIL'
                receipt['controls'].append(result)
                save()
            require(all(row['status'] == 'PASS' for row in receipt['controls']), 'Checker controls failed')
            for row in receipt['cases']:
                label = row['id']
                case = by_id[label]
                cnf_path = instances / (label + '.cnf')
                compressed_path = (certificate.parent / case['proof']['file']).resolve()
                require(compressed_path.is_relative_to(certificate.parent), 'Proof path leaves package')
                cnf_raw, compressed_raw = cnf_path.read_bytes(), compressed_path.read_bytes()
                row['cnf_identity'] = validate_cnf(cnf_raw, case['cnf'])
                row['compressed_identity'] = check_identity(compressed_raw, {'sha256': case['proof']['compressed_sha256'], 'bytes': case['proof']['compressed_bytes']}, 'Compressed proof')
                proof_raw = gzip.decompress(compressed_raw)
                row['proof_identity'] = check_identity(proof_raw, case['proof'], 'Decompressed proof')
                proof_path = temporary / (label + '.drat')
                proof_path.write_bytes(proof_raw)
                row.update(status='RUNNING', cnf=str(cnf_path), compressed_proof=str(compressed_path))
                save()
                result = invoke(checker, cnf_path, proof_path, output / (label + '.log'), args.case_timeout_seconds)
                row.update(result)
                stable = (identity(cnf_path.read_bytes()) == row['cnf_identity'] and
                          identity(compressed_path.read_bytes()) == row['compressed_identity'] and
                          identity(proof_path.read_bytes()) == row['proof_identity'])
                row['input_bytes_stable'] = stable
                row['status'] = 'PASS' if row['accepted'] and stable else 'FAIL'
                save()
                print(json.dumps({'id': label, 'status': row['status'], 'exit_code': row['exit_code']}), flush=True)
                proof_path.unlink()
        require(identity(certificate.read_bytes()) == receipt['certificate_identity'], 'Certificate changed during replay')
        require(identity(checker.read_bytes()) == receipt['checker_identity'], 'Checker changed during replay')
        receipt['verified_count'] = sum(row['status'] == 'PASS' for row in receipt['cases'])
        require(receipt['verified_count'] == 18 and all(row['status'] == 'PASS' for row in receipt['cases']), 'At least one exact case failed or timed out')
        receipt.update(status='PASS', finished=time.time(), temporary_proofs_removed=True)
        save()
        print(json.dumps({'status': 'PASS', 'verified_count': 18, 'receipt': str(receipt_path), 'receipt_identity': identity(receipt_path.read_bytes())}), flush=True)
    except BaseException as error:
        receipt.update(status='HOLD', error=repr(error), finished=time.time())
        save()
        raise


if __name__ == '__main__':
    main()
