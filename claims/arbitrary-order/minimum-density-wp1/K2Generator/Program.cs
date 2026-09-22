using System.Text;

static class Program
{
    static readonly int[,,] M = new int[3, 2, 2]
    {
        { { 0, 1 }, { 2, 3 } },
        { { 0, 2 }, { 1, 3 } },
        { { 0, 3 }, { 1, 2 } },
    };

    static int EdgeIndex(int u, int v)
    {
        if (u > v) (u, v) = (v, u);
        int index = 0;
        for (int a = 0; a < u; ++a) index += 7 - a;
        return index + v - u - 1;
    }

    static void GeneratePmsRec(List<int> vertices, List<(int, int)> chosen,
                               List<(int, int)[]> output)
    {
        if (vertices.Count == 0)
        {
            output.Add(chosen.ToArray());
            return;
        }
        int u = vertices[0];
        for (int i = 1; i < vertices.Count; ++i)
        {
            int v = vertices[i];
            var rest = new List<int>();
            for (int j = 1; j < vertices.Count; ++j)
                if (j != i) rest.Add(vertices[j]);
            var next = new List<(int, int)>(chosen) { (u, v) };
            GeneratePmsRec(rest, next, output);
        }
    }

    static List<(int, int)[]> GeneratePms()
    {
        var output = new List<(int, int)[]>();
        GeneratePmsRec(Enumerable.Range(0, 8).ToList(), new(), output);
        return output;
    }

    static int OtherRank(int color, int other)
    {
        int rank = 0;
        for (int b = 0; b < 3; ++b)
        {
            if (b == color) continue;
            if (b == other) return rank;
            ++rank;
        }
        throw new ArgumentException();
    }

    static int AllocationDigit(int code, int side, int color)
    {
        int position = 3 * side + color;
        for (int i = 0; i < position; ++i) code /= 4;
        return code % 4;
    }

    static int PairChoice(int code, int side, int color, int other)
    {
        int digit = AllocationDigit(code, side, color);
        return OtherRank(color, other) == 0 ? ((digit >> 1) & 1) : (digit & 1);
    }

    static bool IsLowQMixed(int wordCode)
    {
        int[] color = new int[8];
        for (int v = 0; v < 8; ++v)
        {
            color[v] = wordCode % 3;
            wordCode /= 3;
        }
        if (color.All(x => x == color[0])) return false;
        for (int c = 0; c < 3; ++c)
        {
            int q = 0;
            for (int side = 0; side < 2; ++side)
            {
                int off = 4 * side;
                for (int p = 0; p < 2; ++p)
                    if (color[off + M[c, p, 0]] != c && color[off + M[c, p, 1]] != c)
                        ++q;
            }
            if (q <= 1) return true;
        }
        return false;
    }

    static void AddEntry(ushort[] masks, int u, int v, int cu, int cv)
    {
        if (u > v) { (u, v) = (v, u); (cu, cv) = (cv, cu); }
        ushort bit = (ushort)(1 << (3 * cu + cv));
        int edge = EdgeIndex(u, v);
        if ((masks[edge] & bit) != 0) throw new Exception("duplicate scalar entry");
        masks[edge] |= bit;
    }

    static ushort[] BuildMasks(int allocation, int orientation)
    {
        ushort[] masks = new ushort[28];
        for (int side = 0; side < 2; ++side)
        {
            int off = 4 * side;
            for (int c = 0; c < 3; ++c)
                for (int p = 0; p < 2; ++p)
                    AddEntry(masks, off + M[c, p, 0], off + M[c, p, 1], c, c);
        }
        int gadget = 0;
        for (int a = 0; a < 3; ++a)
        for (int b = 0; b < 3; ++b)
        {
            if (a == b) continue;
            int lp = PairChoice(allocation, 0, a, b);
            int rp = PairChoice(allocation, 1, b, a);
            int l0 = M[a, lp, 0], l1 = M[a, lp, 1];
            int r0 = 4 + M[b, rp, 0], r1 = 4 + M[b, rp, 1];
            if (((orientation >> gadget) & 1) != 0) (r0, r1) = (r1, r0);
            AddEntry(masks, l0, r0, a, b);
            AddEntry(masks, l1, r1, a, b);
            ++gadget;
        }
        return masks;
    }

    static int Main(string[] args)
    {
        string output = args.Length > 0 ? args[0] : "k2-witness-table.bin";
        var pms = GeneratePms();
        if (pms.Count != 105) return 4;
        int[] pow3 = new int[8]; pow3[0] = 1;
        for (int i = 1; i < 8; ++i) pow3[i] = 3 * pow3[i - 1];
        bool[] lowQ = Enumerable.Range(0, 6561).Select(IsLowQMixed).ToArray();

        const int total = 4096 * 64;
        ushort[] witnesses = Enumerable.Repeat((ushort)0xffff, total).ToArray();
        byte[] counts = new byte[6561];
        long totalTerms = 0;
        for (int allocation = 0; allocation < 4096; ++allocation)
        {
            for (int orientation = 0; orientation < 64; ++orientation)
            {
                Array.Clear(counts);
                ushort[] masks = BuildMasks(allocation, orientation);
                foreach (var pm in pms)
                {
                    ushort m0 = masks[EdgeIndex(pm[0].Item1, pm[0].Item2)];
                    ushort m1 = masks[EdgeIndex(pm[1].Item1, pm[1].Item2)];
                    ushort m2 = masks[EdgeIndex(pm[2].Item1, pm[2].Item2)];
                    ushort m3 = masks[EdgeIndex(pm[3].Item1, pm[3].Item2)];
                    if (m0 == 0 || m1 == 0 || m2 == 0 || m3 == 0) continue;
                    for (int c0 = 0; c0 < 9; ++c0) if ((m0 & (1 << c0)) != 0)
                    for (int c1 = 0; c1 < 9; ++c1) if ((m1 & (1 << c1)) != 0)
                    for (int c2 = 0; c2 < 9; ++c2) if ((m2 & (1 << c2)) != 0)
                    for (int c3 = 0; c3 < 9; ++c3) if ((m3 & (1 << c3)) != 0)
                    {
                        int[] codes = { c0, c1, c2, c3 };
                        int word = 0;
                        for (int j = 0; j < 4; ++j)
                        {
                            var (u, v) = pm[j];
                            word += (codes[j] / 3) * pow3[u] + (codes[j] % 3) * pow3[v];
                        }
                        if (counts[word] < 2) ++counts[word];
                        ++totalTerms;
                    }
                }
                ushort witness = 0xffff;
                for (int word = 0; word < 6561; ++word)
                    if (lowQ[word] && counts[word] == 1) { witness = (ushort)word; break; }
                witnesses[(allocation << 6) | orientation] = witness;
                if (witness == 0xffff)
                {
                    Console.Error.WriteLine($"COUNTERCONTROL allocation={allocation} orientation={orientation}");
                    return 2;
                }
            }
            if ((allocation + 1) % 1024 == 0)
                Console.WriteLine($"allocations={allocation + 1} supports={(allocation + 1) * 64}");
        }

        Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(output))!);
        using var stream = File.Create(output);
        using var writer = new BinaryWriter(stream, Encoding.ASCII, false);
        writer.Write(Encoding.ASCII.GetBytes("K2W1"));
        writer.Write((uint)total);
        foreach (ushort witness in witnesses) writer.Write(witness);
        Console.WriteLine($"K2_MINIMUM_DENSITY_COVER_PASS supports={total} enumerated_terms={totalTerms} table={output}");
        return 0;
    }
}
