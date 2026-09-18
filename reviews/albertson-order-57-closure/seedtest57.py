"""reviewer-1: does the order-57 closure survive the conservative crossing-number
seed? The lane's own control tests only g(58,f); this tests the order-57 scripts."""
import io, sys, contextlib, runpy
import verify_range as V

def run(script, base, basename):
    V.set_base(base)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            runpy.run_path(script, run_name='__main__')
    except SystemExit:
        pass
    except Exception as e:
        return f'{script}: ERROR {type(e).__name__}: {e}'
    out = buf.getvalue()
    keys = [l.strip() for l in out.split('\n')
            if any(w in l.lower() for w in ('closed', 'impossible', 'survivor',
                                            'eliminat', 'open', 'remain'))]
    return f'--- {script} under {basename}:\n' + '\n'.join('    ' + k for k in keys[-8:])

for script in ('cover57.py', 'aug57.py', 'close57.py', 'residue57.py', 'hall57.py'):
    for base, name in ((V.BASE_CCCG2021, 'CCCG 2021 (cr(K13)=225)'),
                       (V.BASE_CONSERVATIVE, 'counting only (cr(K13)>=217)')):
        print(run(script, base, name), flush=True)
