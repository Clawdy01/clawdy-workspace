#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
SCRIPT = ROOT / 'scripts' / 'ai-briefing-regression-check.py'
ORDER = [58, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 26, 28, 24, 27, 22, 25, 20, 23, 18, 21, 16, 19, 14, 17, 12, 15, 10, 13, 8, 11, 6, 9, 4, 7, 2, 5, 0, 3, 1, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460]


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ['python3', str(SCRIPT), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def unique(seq):
    out = []
    for item in seq:
        if item not in out:
            out.append(item)
    return out


list_proc = run('--list-cases')
if list_proc.returncode != 0:
    raise SystemExit(f'--list-cases faalde met code {list_proc.returncode}: {list_proc.stderr or list_proc.stdout}')
all_cases = [line.strip() for line in list_proc.stdout.splitlines() if line.strip()]
valid_cases = all_cases[:471]
if len(valid_cases) != 471:
    raise SystemExit(f'kon geen vierhonderdzesentachtig geldige casenamen vinden, kreeg {valid_cases}')

case_names = [valid_cases[index] for index in ORDER] + [valid_cases[index] for index in ORDER]
case_args = [arg for case_name in case_names for arg in ('--case', case_name)]
expected_requested = unique(case_names)
expected_discoverable = sorted(expected_requested)

plain_list_proc = run('--list-cases', *case_args)
if plain_list_proc.returncode != 0:
    raise SystemExit(f'plain --list-cases exitcode verwacht 0, kreeg {plain_list_proc.returncode}')
if plain_list_proc.stderr.strip():
    raise SystemExit(f'plain --list-cases hoort geen stderr te geven, kreeg: {plain_list_proc.stderr}')
plain_list_cases = [line.strip() for line in plain_list_proc.stdout.splitlines() if line.strip()]
if plain_list_cases != expected_discoverable:
    raise SystemExit(f'plain --list-cases mismatch: {plain_list_cases} != {expected_discoverable}')

json_list_proc = run('--json', '--list-cases', *case_args)
if json_list_proc.returncode != 0:
    raise SystemExit(f'json --list-cases exitcode verwacht 0, kreeg {json_list_proc.returncode}')
if json_list_proc.stderr.strip():
    raise SystemExit(f'json --list-cases hoort geen stderr te geven, kreeg: {json_list_proc.stderr}')
json_list_payload = json.loads(json_list_proc.stdout)
if json_list_payload.get('requested_case_names') != expected_requested:
    raise SystemExit(
        'json --list-cases requested_case_names mismatch: '
        f'{json_list_payload.get("requested_case_names")} != {expected_requested}'
    )
if json_list_payload.get('requested_case_count') != len(expected_requested):
    raise SystemExit(
        'json --list-cases requested_case_count mismatch: '
        f'{json_list_payload.get("requested_case_count")} != {len(expected_requested)}'
    )
if json_list_payload.get('selected_case_names') != expected_discoverable:
    raise SystemExit(
        'json --list-cases selected_case_names mismatch: '
        f'{json_list_payload.get("selected_case_names")} != {expected_discoverable}'
    )
if json_list_payload.get('selected_case_count') != len(expected_discoverable):
    raise SystemExit(
        'json --list-cases selected_case_count mismatch: '
        f'{json_list_payload.get("selected_case_count")} != {len(expected_discoverable)}'
    )
if json_list_payload.get('cases') != expected_discoverable:
    raise SystemExit(f'json --list-cases cases mismatch: {json_list_payload.get("cases")} != {expected_discoverable}')
if json_list_payload.get('case_count') != len(expected_discoverable):
    raise SystemExit(
        'json --list-cases case_count mismatch: '
        f'{json_list_payload.get("case_count")} != {len(expected_discoverable)}'
    )
if json_list_payload.get('available_case_names') != all_cases:
    raise SystemExit('json --list-cases available_case_names mismatch met volledige --list-cases uitvoer')
if json_list_payload.get('available_case_count') != len(all_cases):
    raise SystemExit(
        'json --list-cases available_case_count mismatch: '
        f'{json_list_payload.get("available_case_count")} != {len(all_cases)}'
    )
if json_list_payload.get('ok') is not True:
    raise SystemExit(f'json --list-cases ok verwacht True, kreeg {json_list_payload.get("ok")}')

print(json.dumps({
    'ok': True,
    'valid_case_names': valid_cases,
    'requested_case_names': expected_requested,
    'discoverable_case_names': expected_discoverable,
}, ensure_ascii=False))
