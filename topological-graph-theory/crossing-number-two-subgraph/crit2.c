/* crit2.c -- exhaustive census of 2-crossing-critical graphs.
 *
 * Reads simple graphs in graph6 format on stdin.  For each input graph G:
 *   (1) reject if cr(G) <= 1;
 *   (2) reject unless cr(G-e) <= 1 for every edge e   [2-crossing-criticality];
 *   (3) report G, and decide whether cr(G) <= 2.
 * A graph surviving (1)+(2) is 2-crossing-critical.  If some survivor has
 * cr(G) >= 3 it is a counterexample to the Bloom-Kennedy-Quintas conjecture
 * ("every graph with cr >= 2 has a subgraph with cr = 2").
 *
 * All decisions reduce to planarity of explicit planarizations, using the
 * Boyer-Myrvold implementation shipped with nauty (planarity.c).
 *
 * Facts used (good drawings): some optimal drawing has no two adjacent edges
 * crossing and no two edges crossing twice.  Hence
 *   cr(G) <= 1  iff  G planar, or some planarization at one independent edge
 *                    pair is planar;
 *   cr(G) <= 2  iff  cr(G) <= 1, or some planarization at two crossings
 *                    (either two disjoint independent pairs, or one edge
 *                     crossed by two others) is planar.
 *
 * Build:
 *   cc -O3 -o crit2 crit2.c planarity.c gtools.o -I. -o crit2
 */

#include "gtools.h"
#include "planarity.h"

#define MAXV 32
#define MAXEDG 128

/* ------------------------------------------------------------------ */
/* planarity of an explicit edge list on n vertices                    */
/* ------------------------------------------------------------------ */

static t_ver_sparse_rep  PV[MAXV];
static t_adjl_sparse_rep PA[2 * MAXEDG + 2];
static int adjhead[MAXV], adjnext[2 * MAXEDG + 2], adjto[2 * MAXEDG + 2];

static long long n_planar_calls = 0;

static boolean
planar_edges(int n, int ne, const int *eu, const int *ev)
{
    int i, k, p;
    t_dlcl **dfs_tree, **back_edges, **mult_edges;
    t_ver_edge *embed_graph;
    int edge_pos, v, w, c;
    boolean ans;

    ++n_planar_calls;

    for (i = 0; i < n; ++i) adjhead[i] = -1;
    k = 0;
    for (i = 0; i < ne; ++i) {
        adjto[k] = ev[i]; adjnext[k] = adjhead[eu[i]]; adjhead[eu[i]] = k; ++k;
        adjto[k] = eu[i]; adjnext[k] = adjhead[ev[i]]; adjhead[ev[i]] = k; ++k;
    }

    k = 0;
    for (i = 0; i < n; ++i) {
        if (adjhead[i] < 0) { PV[i].first_edge = NIL; continue; }
        PV[i].first_edge = k;
        for (p = adjhead[i]; p >= 0; p = adjnext[p]) {
            PA[k].end_vertex = adjto[p];
            PA[k].next = k + 1;
            ++k;
        }
        PA[k - 1].next = NIL;
    }

    ans = sparseg_adjl_is_planar(PV, n, PA, &c, &dfs_tree, &back_edges,
                                 &mult_edges, &embed_graph, &edge_pos, &v, &w);
    sparseg_dlcl_delete(dfs_tree, n);
    sparseg_dlcl_delete(back_edges, n);
    sparseg_dlcl_delete(mult_edges, n);
    embedg_VES_delete(embed_graph, n);
    return ans;
}

/* ------------------------------------------------------------------ */
/* current graph                                                       */
/* ------------------------------------------------------------------ */

static int N, M;
static int EU[MAXEDG], EV[MAXEDG];

/* scratch edge list */
static int bu[MAXEDG + 8], bv[MAXEDG + 8];

#define INDEP(i, j) (EU[i] != EU[j] && EU[i] != EV[j] && \
                     EV[i] != EU[j] && EV[i] != EV[j])

/* copy all edges except those with index in the "skip" mask */
static int
copy_except(unsigned long long skip)
{
    int i, k = 0;
    for (i = 0; i < M; ++i)
        if (!((skip >> i) & 1ULL)) { bu[k] = EU[i]; bv[k] = EV[i]; ++k; }
    return k;
}

/* planar(G - skip) */
static boolean
planar_del(unsigned long long skip)
{
    int k = copy_except(skip);
    return planar_edges(N, k, bu, bv);
}

/* planarization of G - skip with one crossing between edges a and b
 * (a, b independent, both in skip).  New vertex N. */
static boolean
planar_x1(unsigned long long skip, int a, int b)
{
    int k = copy_except(skip);
    bu[k] = EU[a]; bv[k] = N; ++k;
    bu[k] = N;     bv[k] = EV[a]; ++k;
    bu[k] = EU[b]; bv[k] = N; ++k;
    bu[k] = N;     bv[k] = EV[b]; ++k;
    return planar_edges(N + 1, k, bu, bv);
}

/* two disjoint crossings: {a,b} at dummy N, {c,d} at dummy N+1 */
static boolean
planar_x2_disjoint(int a, int b, int c, int d)
{
    unsigned long long skip = (1ULL << a) | (1ULL << b) | (1ULL << c) | (1ULL << d);
    int k = copy_except(skip);
    bu[k] = EU[a]; bv[k] = N;   ++k;
    bu[k] = N;     bv[k] = EV[a]; ++k;
    bu[k] = EU[b]; bv[k] = N;   ++k;
    bu[k] = N;     bv[k] = EV[b]; ++k;
    bu[k] = EU[c]; bv[k] = N + 1; ++k;
    bu[k] = N + 1; bv[k] = EV[c]; ++k;
    bu[k] = EU[d]; bv[k] = N + 1; ++k;
    bu[k] = N + 1; bv[k] = EV[d]; ++k;
    return planar_edges(N + 2, k, bu, bv);
}

/* edge e crossed twice: first by f (dummy N), then by g (dummy N+1),
 * in that order along e from EU[e] to EV[e]. */
static boolean
planar_x2_shared(int e, int f, int g)
{
    unsigned long long skip = (1ULL << e) | (1ULL << f) | (1ULL << g);
    int k = copy_except(skip);
    bu[k] = EU[e]; bv[k] = N;     ++k;   /* e split into 3 arcs */
    bu[k] = N;     bv[k] = N + 1; ++k;
    bu[k] = N + 1; bv[k] = EV[e]; ++k;
    bu[k] = EU[f]; bv[k] = N;     ++k;   /* f split by dummy N */
    bu[k] = N;     bv[k] = EV[f]; ++k;
    bu[k] = EU[g]; bv[k] = N + 1; ++k;   /* g split by dummy N+1 */
    bu[k] = N + 1; bv[k] = EV[g]; ++k;
    return planar_edges(N + 2, k, bu, bv);
}

/* ------------------------------------------------------------------ */
/* cr(G - skip) <= 1 ?                                                 */
/* ------------------------------------------------------------------ */

static boolean
cr_le_1(unsigned long long skip)
{
    int a, b;
    if (planar_del(skip)) return TRUE;
    for (a = 0; a < M; ++a) {
        if ((skip >> a) & 1ULL) continue;
        if (!planar_del(skip | (1ULL << a))) continue;   /* need G-skip-a planar */
        for (b = 0; b < M; ++b) {
            if (b == a || ((skip >> b) & 1ULL)) continue;
            if (!INDEP(a, b)) continue;
            if (planar_x1(skip | (1ULL << a) | (1ULL << b), a, b)) return TRUE;
        }
    }
    return FALSE;
}

/* cr(G) <= 2 ?  (called only when cr(G) >= 2 is already known) */
static boolean
cr_le_2(void)
{
    int a, b, c, d, e, f, g;
    /* case 1: two disjoint independent pairs */
    for (a = 0; a < M; ++a)
        for (b = a + 1; b < M; ++b) {
            if (!INDEP(a, b)) continue;
            for (c = a + 1; c < M; ++c) {
                if (c == b) continue;
                for (d = c + 1; d < M; ++d) {
                    if (d == b || !INDEP(c, d)) continue;
                    if (planar_x2_disjoint(a, b, c, d)) return TRUE;
                }
            }
        }
    /* case 2: edge e crossed by f then g */
    for (e = 0; e < M; ++e)
        for (f = 0; f < M; ++f) {
            if (f == e || !INDEP(e, f)) continue;
            for (g = 0; g < M; ++g) {
                if (g == e || g == f || !INDEP(e, g)) continue;
                if (planar_x2_shared(e, f, g)) return TRUE;
            }
        }
    return FALSE;
}

/* ------------------------------------------------------------------ */

int
main(int argc, char *argv[])
{
    graph *gg;
    int n, m_words, i, j, e;
    long long nin = 0, ncrit = 0, nbad = 0;
    char *s;
    set *gv;
    boolean ok;
    unsigned long long skip;
    int verbose = (argc > 1 && argv[1][0] == 'v');

    while ((gg = readg(stdin, NULL, 0, &m_words, &n)) != NULL) {
        ++nin;
        if (n > MAXV - 4) { fprintf(stderr, "n too large\n"); exit(1); }
        N = n; M = 0;
        for (i = 0; i < n; ++i) {
            gv = GRAPHROW(gg, i, m_words);
            for (j = i + 1; j < n; ++j)
                if (ISELEMENT(gv, j)) {
                    if (M >= 63) { fprintf(stderr, "too many edges\n"); exit(1); }
                    EU[M] = i; EV[M] = j; ++M;
                }
        }
        FREES(gg);

        if (planar_del(0ULL)) continue;              /* cr = 0 */

        ok = TRUE;                                   /* criticality */
        for (e = 0; e < M; ++e) {
            skip = 1ULL << e;
            if (!cr_le_1(skip)) { ok = FALSE; break; }
        }
        if (!ok) continue;

        if (cr_le_1(0ULL)) continue;                 /* cr(G) <= 1 */

        ++ncrit;
        if (cr_le_2()) {
            printf("CRIT2 %d %d ", N, M);
        } else {
            ++nbad;
            printf("CRIT_GE3 %d %d ", N, M);
        }
        for (e = 0; e < M; ++e) printf("%d-%d,", EU[e], EV[e]);
        printf("\n");
        fflush(stdout);
    }

    fprintf(stderr,
            "read %lld graphs; %lld 2-crossing-critical; %lld with cr>=3; "
            "%lld planarity calls\n",
            nin, ncrit, nbad, n_planar_calls);
    return 0;
}
