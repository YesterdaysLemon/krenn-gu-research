"""Independent no-import audit for the majority-subset edge count."""


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def audit_order(vertex_count):
    m = vertex_count // 2
    vertices = set(range(vertex_count))
    for r in range(1, m):
        subset = set(range(m + r))
        complement = vertices - subset
        for matching in perfect_matchings(range(vertex_count)):
            internal = 0
            crossing = 0
            external = 0
            for i, j in matching:
                if i in subset and j in subset:
                    internal += 1
                elif i in complement and j in complement:
                    external += 1
                else:
                    crossing += 1
            assert 2 * internal + crossing == m + r
            assert 2 * external + crossing == m - r
            assert internal == external + r
            assert internal >= r


if __name__ == "__main__":
    for order in (4, 6, 8):
        audit_order(order)
    print("majority-subset internal-edge ideal independent audit: PASS")
