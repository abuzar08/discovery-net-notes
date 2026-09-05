"""Extract BORS Figure 15.1's (T,U)-configurations from the PDF's vector art.

arXiv:1312.3712 Figure 15.1 displays the configurations that Theorem 17.1(3)
allows as replacement patches.  The figure is vector drawing, not raster, so
pymupdf's get_drawings() returns the actual path objects and the graphs can be
reconstructed exactly instead of read off a rendered image.

Encoding used by the figure:
  * a terminal (x, y or z) is a circle with white fill;
  * an internal vertex is a circle with black fill;
  * an edge is a stroked path from one circle to another, straight or curved;
    PARALLEL EDGES are drawn as two paths with the same endpoints, which is why
    the patches must be read as multigraphs.

Method: snap each path's on-curve points to the nearest vertex centre, then cut
the path into edges at the snapped points.  A path whose points all snap to one
vertex is that vertex's own outline and is discarded.  Configurations are the
connected components of the result.
"""
import collections
import math
import sys

import pymupdf

PAGE = 150
SNAP = 6.0          # pt; edge ends stop at the circle boundary, radius <= 4


def load(path, page=PAGE):
    return pymupdf.open(path)[page].get_drawings()


def centre(g):
    r = g['rect']
    return ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)


def polyline(g):
    """The path's on-curve points in drawing order."""
    pts = []
    for it in g['items']:
        if it[0] == 'l':
            a, b = tuple(it[1]), tuple(it[2])
        elif it[0] == 'c':
            a, b = tuple(it[1]), tuple(it[4])
        elif it[0] == 'qu':
            # a quad is four line segments the writer collapsed into one item;
            # it must be walked as the closed cycle ul -> ur -> lr -> ll -> ul,
            # not as a pair of opposite corners
            q = it[1]
            corners = [tuple(q.ul), tuple(q.ur), tuple(q.lr), tuple(q.ll),
                       tuple(q.ul)]
            if not pts or math.dist(pts[-1], corners[0]) > 0.01:
                pts.append(corners[0])
            pts.extend(corners[1:])
            continue
        elif it[0] == 're':
            r = it[1]
            a, b = (r.x0, r.y0), (r.x1, r.y1)
        else:
            continue
        if not pts or math.dist(pts[-1], a) > 0.01:
            pts.append(a)
        pts.append(b)
    return pts


def extract(pdf, page=PAGE):
    dr = load(pdf, page)
    verts, paths = [], []
    for g in dr:
        f = g.get('fill')
        if f == (1.0, 1.0, 1.0):
            verts.append((centre(g), 'T'))
        elif f == (0.0, 0.0, 0.0):
            verts.append((centre(g), 'I'))
        else:
            paths.append(g)

    def snap(p):
        best, bd = None, 1e9
        for i, (c, _) in enumerate(verts):
            d = math.dist(p, c)
            if d < bd:
                best, bd = i, d
        return best if bd <= SNAP else None

    E = collections.Counter()
    for g in paths:
        if max(g['rect'].width, g['rect'].height) < 4:
            continue                                  # a vertex's own outline
        pts = polyline(g)
        hits = [(k, snap(p)) for k, p in enumerate(pts)]
        hits = [(k, v) for k, v in hits if v is not None]
        # a parallel pair is drawn as a closed lens: two arcs between the same
        # two circles, forming one closed path whose two turning points are arc
        # midpoints that snap to nothing.  Walking such a path linearly sees a
        # single edge, so close the walk when the path itself is closed.
        if len(pts) > 2 and math.dist(pts[0], pts[-1]) < 0.01 and hits:
            hits = hits + [hits[0]]
        for (k1, v1), (k2, v2) in zip(hits, hits[1:]):
            if v1 == v2:
                continue                              # arc within one circle
            E[(min(v1, v2), max(v1, v2))] += 1
    return verts, E


def components(verts, E):
    par = list(range(len(verts)))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for a, b in E:
        x, y = find(a), find(b)
        if x != y:
            par[x] = y
    comp = collections.defaultdict(list)
    for i in range(len(verts)):
        comp[find(i)].append(i)
    return list(comp.values())


if __name__ == '__main__':
    v, E = extract(sys.argv[1] if len(sys.argv) > 1 else 'bors.pdf')
    print(f"vertices {len(v)} "
          f"({sum(1 for _, k in v if k=='T')} terminal, "
          f"{sum(1 for _, k in v if k=='I')} internal)")
    print(f"edge instances {sum(E.values())}  distinct pairs {len(E)}")
    print(f"multiplicities {dict(sorted(collections.Counter(E.values()).items()))}")
    C = components(v, E)
    print(f"components {len(C)}")
    sig = collections.Counter(
        (sum(1 for i in c if v[i][1] == 'T'), sum(1 for i in c if v[i][1] == 'I'))
        for c in C)
    print("(terminals,internal) per component:", dict(sorted(sig.items())))
