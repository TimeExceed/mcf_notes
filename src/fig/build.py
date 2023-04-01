#!/usr/bin/python3
from pathlib import Path
import subprocess as sp
import hashlib
from collections import OrderedDict
import json

def to_figure_path(src):
    return src.parent.joinpath(src.stem + '.pdf')

IMAGE_ID = None

def image_id():
    global IMAGE_ID
    if IMAGE_ID is None:
        IMAGE_ID = sp.check_output(['docker', 'images', 'fathom', '-q'])
        IMAGE_ID = IMAGE_ID.strip()
    return IMAGE_ID

INIT_HASH = None

def init_hash():
    global INIT_HASH
    if INIT_HASH is None:
        INIT_HASH = hashlib.sha256()
        INIT_HASH.update(image_id())
    return INIT_HASH.copy()

def calc_digests(src):
    dst = to_figure_path(src)
    hash = init_hash()
    with open(src, 'rb') as fp:
        content = fp.read()
    hash.update(content)
    return (dst, hash.hexdigest())

DIGESTS_FILE = Path('.digests.json')

def save_digests(digests):
    digests = [(k, v) for k,v in digests.items()]
    digests.sort(key=lambda x: x[0])
    res = OrderedDict()
    for k, v in digests:
        res[str(k)] = v
    with open(DIGESTS_FILE, 'w') as fp:
        json.dump(res, fp)

def recover_digests():
    if DIGESTS_FILE.exists():
        with open(DIGESTS_FILE) as fp:
            digests = json.load(fp)
        return dict((Path(k), v) for k, v in digests.items())
    else:
        return {}

def figures_to_rebuild(real_digests, last_digests):
    return [x for x in real_digests.keys() if x not in last_digests or real_digests[x] != last_digests[x]]

def fathom(src, dst):
    pwd = Path('.').absolute()
    cmd = ['docker', 'run',
        '--user', '1000:1000',
        '--rm',
        '-v', '%s:/opt/code' % pwd,
        'fathom']
    cmd += [str(src), str(dst)]
    print(cmd)
    sp.run(cmd).check_returncode()

if __name__ == '__main__':
    figure_srcs = [
        'application-lp.py',
    ]
    figure_srcs = [Path(x) for x in figure_srcs]
    figure_dsts = [to_figure_path(x) for x in figure_srcs]
    real_digests = dict(calc_digests(x) for x in figure_srcs)
    last_digests = recover_digests()
    to_rebuild = figures_to_rebuild(real_digests, last_digests)
    dsts_to_srcs = dict(zip(figure_dsts, figure_srcs))
    for x in to_rebuild:
        fathom(dsts_to_srcs[x], x)
    save_digests(real_digests)
