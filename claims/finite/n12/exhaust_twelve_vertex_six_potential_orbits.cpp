#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>

namespace {

constexpr int N = 12;
constexpr int COLOURS = 3;
constexpr int POTENTIALS = 6;
constexpr int D_EDGES = 18;
constexpr int K_EDGES = 18;
constexpr int ALL_EDGES = D_EDGES + K_EDGES;

constexpr std::array<std::array<int, 3>, 6> PERMUTATIONS{{
    {{0, 1, 2}},
    {{0, 2, 1}},
    {{1, 0, 2}},
    {{1, 2, 0}},
    {{2, 0, 1}},
    {{2, 1, 0}},
}};

struct DiagonalEdge {
    int u;
    int v;
    int colour;
};

struct PortEdge {
    int u;
    int v;
    int cu;
    int cv;
    std::array<int, POTENTIALS> weight{};

    auto key() const {
        return std::tuple{u, v, cu, cv};
    }
};

struct MatchingEdge {
    int u;
    int v;
    int cu;
    int cv;
    std::array<int, POTENTIALS> weight{};
};

struct CellInput {
    int id;
    int graph_index;
    int cell_index;
    std::uint64_t orbit_size;
    int stabilizer_size;
    std::uint64_t expected_ports;
    std::array<DiagonalEdge, D_EDGES> diagonal{};
    std::array<std::array<int, 3>, N> normal{};
};

struct CellResult {
    std::uint64_t observed_ports = 0;
    std::array<std::uint64_t, 64> success_mask_histogram{};
    std::uint64_t survivor_ports = 0;
    std::uint64_t port_hash_xor = 0;
    std::uint64_t port_hash_sum = 0;
    std::uint64_t classification_hash_xor = 0;
    std::uint64_t classification_hash_sum = 0;
};

std::uint64_t fnv_mix(std::uint64_t hash, std::uint64_t value) {
    for (int byte = 0; byte < 8; ++byte) {
        hash ^= (value >> (8 * byte)) & 0xffU;
        hash *= 1099511628211ULL;
    }
    return hash;
}

std::uint64_t architecture_hash(
    int cell_id,
    const std::array<PortEdge, K_EDGES>& raw_ports
) {
    auto ports = raw_ports;
    std::sort(
        ports.begin(),
        ports.end(),
        [](const PortEdge& first, const PortEdge& second) {
            return first.key() < second.key();
        }
    );
    std::uint64_t hash = 1469598103934665603ULL;
    hash = fnv_mix(hash, static_cast<std::uint64_t>(cell_id));
    for (const auto& port : ports) {
        hash = fnv_mix(hash, static_cast<std::uint64_t>(port.u));
        hash = fnv_mix(hash, static_cast<std::uint64_t>(port.v));
        hash = fnv_mix(hash, static_cast<std::uint64_t>(port.cu));
        hash = fnv_mix(hash, static_cast<std::uint64_t>(port.cv));
    }
    return hash;
}

class CellRunner {
public:
    CellRunner(
        const CellInput& input,
        std::ofstream& residual_stream
    )
        : input_(input), residual_stream_(residual_stream) {
        for (auto& row : pair_index_) {
            row.fill(-1);
        }
        int pair_cursor = 0;
        for (int u = 0; u < N; ++u) {
            for (int v = u + 1; v < N; ++v) {
                pair_index_[u][v] = pair_cursor;
                pair_index_[v][u] = pair_cursor;
                ++pair_cursor;
            }
        }
        if (pair_cursor != 66) {
            throw std::runtime_error("physical pair census changed");
        }
        for (auto& row : diagonal_pair_) {
            row.fill(false);
        }
        for (const auto& item : input_.diagonal) {
            diagonal_pair_[item.u][item.v] = true;
            diagonal_pair_[item.v][item.u] = true;
        }
        build_potentials();
        build_port_options();
        build_diagonal_matching_edges();
        int value = 1;
        for (int vertex = 0; vertex < N; ++vertex) {
            powers_of_three_[vertex] = value;
            value *= 3;
        }
    }

    CellResult run() {
        const std::uint64_t remaining = (1ULL << (3 * N)) - 1ULL;
        enumerate_ports(remaining, 0);
        if (result_.observed_ports != input_.expected_ports) {
            throw std::runtime_error(
                "compiled port count disagrees with Python count"
            );
        }
        return result_;
    }

private:
    const CellInput& input_;
    std::ofstream& residual_stream_;
    CellResult result_{};
    std::array<std::array<int, N>, N> pair_index_{};
    std::array<std::array<bool, N>, N> diagonal_pair_{};
    std::array<std::array<std::array<int, POTENTIALS>, 3>, N>
        potential_{};
    std::array<std::vector<int>, 3 * N> port_options_{};
    std::array<PortEdge, K_EDGES> ports_{};
    int port_count_ = 0;
    std::array<MatchingEdge, ALL_EDGES> matching_edges_{};
    std::array<std::array<int, 6>, N> incident_edges_{};
    std::array<int, N> incident_degrees_{};
    std::array<int, N> powers_of_three_{};
    std::array<int, POTENTIALS> minimum_{};
    std::array<std::unordered_map<int, std::uint8_t>, POTENTIALS>
        minimum_colour_counts_{};

    void build_potentials() {
        for (int vertex = 0; vertex < N; ++vertex) {
            for (int permutation_index = 0;
                 permutation_index < POTENTIALS;
                 ++permutation_index) {
                const auto& permutation = PERMUTATIONS[permutation_index];
                std::array<int, 3> relabelled{{-1, -1, -1}};
                for (int old_colour = 0;
                     old_colour < COLOURS;
                     ++old_colour) {
                    relabelled[permutation[old_colour]] =
                        permutation[input_.normal[vertex][old_colour]];
                }
                const int b0 = relabelled[0] == 2;
                const int b1 = relabelled[1] == 2;
                const int b2 = relabelled[2] == 1;
                const std::array<int, 3> base{{
                    1 - 2 * b2,
                    2 * (b2 - b0),
                    2 * (b0 + b1 - 1),
                }};
                for (int old_colour = 0;
                     old_colour < COLOURS;
                     ++old_colour) {
                    potential_[vertex][old_colour][permutation_index] =
                        base[permutation[old_colour]];
                }
            }
        }
        for (const auto& item : input_.diagonal) {
            for (int permutation_index = 0;
                 permutation_index < POTENTIALS;
                 ++permutation_index) {
                if (
                    potential_[item.u][item.colour][permutation_index]
                    + potential_[item.v][item.colour][permutation_index]
                    != 0
                ) {
                    throw std::runtime_error(
                        "compiled diagonal potential is nonzero"
                    );
                }
            }
        }
    }

    void build_port_options() {
        for (int vertex = 0; vertex < N; ++vertex) {
            for (int colour = 0; colour < COLOURS; ++colour) {
                const int stub = 3 * vertex + colour;
                const int partner_colour = input_.normal[vertex][colour];
                for (int partner = 0; partner < N; ++partner) {
                    if (
                        partner == vertex
                        || diagonal_pair_[vertex][partner]
                        || input_.normal[partner][partner_colour] != colour
                        || !bridge_unit_allowed(
                            vertex,
                            partner,
                            partner_colour,
                            colour
                        )
                    ) {
                        continue;
                    }
                    port_options_[stub].push_back(
                        3 * partner + partner_colour
                    );
                }
                std::sort(
                    port_options_[stub].begin(),
                    port_options_[stub].end()
                );
            }
        }
    }

    bool bridge_unit_allowed(
        int left,
        int right,
        int left_colour,
        int right_colour
    ) const {
        for (int target = 0; target < COLOURS; ++target) {
            if (
                !(left_colour == target && right_colour == target)
                && left_colour != input_.normal[left][target]
                && right_colour != input_.normal[right][target]
            ) {
                return false;
            }
        }
        return true;
    }

    void build_diagonal_matching_edges() {
        for (int edge_id = 0; edge_id < D_EDGES; ++edge_id) {
            const auto& item = input_.diagonal[edge_id];
            matching_edges_[edge_id] = MatchingEdge{
                item.u,
                item.v,
                item.colour,
                item.colour,
                {},
            };
        }
    }

    bool pair_is_used(
        unsigned __int128 used_pairs,
        int u,
        int v
    ) const {
        const int index = pair_index_[u][v];
        return (used_pairs >> index) & 1U;
    }

    void enumerate_ports(
        std::uint64_t remaining,
        unsigned __int128 used_pairs
    ) {
        if (remaining == 0) {
            if (port_count_ != K_EDGES) {
                throw std::runtime_error("port edge count changed");
            }
            analyze_architecture();
            return;
        }
        int first = -1;
        int best_candidates = std::numeric_limits<int>::max();
        for (int stub = 0; stub < 3 * N; ++stub) {
            if (((remaining >> stub) & 1ULL) == 0) {
                continue;
            }
            int candidates = 0;
            const int vertex = stub / 3;
            for (const int other : port_options_[stub]) {
                if (
                    ((remaining >> other) & 1ULL)
                    && !pair_is_used(
                        used_pairs, vertex, other / 3
                    )
                ) {
                    ++candidates;
                }
            }
            if (candidates < best_candidates) {
                first = stub;
                best_candidates = candidates;
            }
        }
        if (first < 0 || best_candidates == 0) {
            return;
        }
        const int left_vertex = first / 3;
        const int left_colour = first % 3;
        for (const int second : port_options_[first]) {
            if (((remaining >> second) & 1ULL) == 0) {
                continue;
            }
            const int right_vertex = second / 3;
            const int right_colour = second % 3;
            if (pair_is_used(used_pairs, left_vertex, right_vertex)) {
                continue;
            }
            const int u = std::min(left_vertex, right_vertex);
            const int v = std::max(left_vertex, right_vertex);
            // The exact cover pairs target tasks.  The inherited
            // half-colours of the reciprocal singleton are the targets
            // at the opposite endpoints.
            const int cu = (
                u == left_vertex ? right_colour : left_colour
            );
            const int cv = (
                v == right_vertex ? left_colour : right_colour
            );
            PortEdge item{u, v, cu, cv, {}};
            for (int permutation_index = 0;
                 permutation_index < POTENTIALS;
                 ++permutation_index) {
                item.weight[permutation_index] =
                    potential_[u][cu][permutation_index]
                    + potential_[v][cv][permutation_index];
            }
            ports_[port_count_++] = item;
            const int physical_index = pair_index_[u][v];
            enumerate_ports(
                remaining
                    ^ (1ULL << first)
                    ^ (1ULL << second),
                used_pairs
                    | (static_cast<unsigned __int128>(1)
                       << physical_index)
            );
            --port_count_;
        }
    }

    void build_matching_adjacency() {
        incident_degrees_.fill(0);
        for (int index = 0; index < K_EDGES; ++index) {
            const auto& item = ports_[index];
            matching_edges_[D_EDGES + index] = MatchingEdge{
                item.u,
                item.v,
                item.cu,
                item.cv,
                item.weight,
            };
        }
        for (int edge_id = 0; edge_id < ALL_EDGES; ++edge_id) {
            const auto& item = matching_edges_[edge_id];
            incident_edges_[item.u][incident_degrees_[item.u]++] =
                edge_id;
            incident_edges_[item.v][incident_degrees_[item.v]++] =
                edge_id;
        }
        for (int vertex = 0; vertex < N; ++vertex) {
            if (incident_degrees_[vertex] != 6) {
                throw std::runtime_error(
                    "guaranteed graph is not six-regular"
                );
            }
        }
    }

    void enumerate_matchings(
        std::uint16_t remaining,
        int colouring_code,
        int colour_mask,
        std::array<int, POTENTIALS>& signature
    ) {
        if (remaining == 0) {
            if (
                colour_mask == 1
                || colour_mask == 2
                || colour_mask == 4
            ) {
                return;
            }
            for (int permutation_index = 0;
                 permutation_index < POTENTIALS;
                 ++permutation_index) {
                const int value = signature[permutation_index];
                auto& counts =
                    minimum_colour_counts_[permutation_index];
                if (value < minimum_[permutation_index]) {
                    minimum_[permutation_index] = value;
                    counts.clear();
                    counts.emplace(colouring_code, 1);
                } else if (value == minimum_[permutation_index]) {
                    auto& count = counts[colouring_code];
                    if (count < 2) {
                        ++count;
                    }
                }
            }
            return;
        }
        const int left = std::countr_zero(remaining);
        for (int position = 0;
             position < incident_degrees_[left];
             ++position) {
            const int edge_id = incident_edges_[left][position];
            const auto& raw = matching_edges_[edge_id];
            int u = raw.u;
            int v = raw.v;
            int cu = raw.cu;
            int cv = raw.cv;
            if (v == left) {
                std::swap(u, v);
                std::swap(cu, cv);
            }
            if (((remaining >> v) & 1U) == 0) {
                continue;
            }
            for (int permutation_index = 0;
                 permutation_index < POTENTIALS;
                 ++permutation_index) {
                signature[permutation_index] +=
                    raw.weight[permutation_index];
            }
            enumerate_matchings(
                remaining
                    ^ static_cast<std::uint16_t>(1U << u)
                    ^ static_cast<std::uint16_t>(1U << v),
                colouring_code
                    + cu * powers_of_three_[u]
                    + cv * powers_of_three_[v],
                colour_mask | (1 << cu) | (1 << cv),
                signature
            );
            for (int permutation_index = 0;
                 permutation_index < POTENTIALS;
                 ++permutation_index) {
                signature[permutation_index] -=
                    raw.weight[permutation_index];
            }
        }
    }

    std::uint8_t classify_architecture() {
        build_matching_adjacency();
        minimum_.fill(std::numeric_limits<int>::max());
        for (auto& counts : minimum_colour_counts_) {
            counts.clear();
        }
        std::array<int, POTENTIALS> signature{};
        enumerate_matchings(
            static_cast<std::uint16_t>((1U << N) - 1U),
            0,
            0,
            signature
        );
        std::uint8_t success_mask = 0;
        for (int permutation_index = 0;
             permutation_index < POTENTIALS;
             ++permutation_index) {
            if (
                minimum_[permutation_index]
                == std::numeric_limits<int>::max()
            ) {
                throw std::runtime_error(
                    "no mixed guaranteed perfect matching"
                );
            }
            const auto& counts =
                minimum_colour_counts_[permutation_index];
            if (std::any_of(
                    counts.begin(),
                    counts.end(),
                    [](const auto& item) {
                        return item.second == 1;
                    }
                )) {
                success_mask |= (
                    static_cast<std::uint8_t>(1U)
                    << permutation_index
                );
            }
        }
        return success_mask;
    }

    void write_residual(std::uint64_t architecture) {
        auto sorted_ports = ports_;
        std::sort(
            sorted_ports.begin(),
            sorted_ports.end(),
            [](const PortEdge& first, const PortEdge& second) {
                return first.key() < second.key();
            }
        );
        residual_stream_
            << input_.id << ' '
            << input_.graph_index << ' '
            << input_.cell_index << ' '
            << architecture;
        for (const auto& item : sorted_ports) {
            residual_stream_
                << ' ' << item.u
                << ' ' << item.v
                << ' ' << item.cu
                << ' ' << item.cv;
        }
        residual_stream_ << '\n';
    }

    void analyze_architecture() {
        const std::uint64_t hash =
            architecture_hash(input_.id, ports_);
        const std::uint8_t success_mask =
            classify_architecture();
        ++result_.observed_ports;
        ++result_.success_mask_histogram[success_mask];
        result_.port_hash_xor ^= hash;
        result_.port_hash_sum += hash;
        const std::uint64_t classification_hash =
            fnv_mix(hash, success_mask);
        result_.classification_hash_xor ^= classification_hash;
        result_.classification_hash_sum += classification_hash;
        if (success_mask == 0) {
            ++result_.survivor_ports;
            write_residual(hash);
        }
    }
};

std::vector<CellInput> read_cells(const std::string& path) {
    std::ifstream input(path);
    if (!input) {
        throw std::runtime_error("cannot open compiled orbit input");
    }
    int cell_count = 0;
    input >> cell_count;
    if (cell_count != 154) {
        throw std::runtime_error("compiled cell count changed");
    }
    std::vector<CellInput> cells(cell_count);
    for (auto& cell : cells) {
        input
            >> cell.id
            >> cell.graph_index
            >> cell.cell_index
            >> cell.orbit_size
            >> cell.stabilizer_size
            >> cell.expected_ports;
        for (auto& item : cell.diagonal) {
            input >> item.u >> item.v >> item.colour;
        }
        for (auto& normal : cell.normal) {
            input >> normal[0] >> normal[1] >> normal[2];
        }
        if (!input) {
            throw std::runtime_error("compiled orbit input truncated");
        }
    }
    return cells;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 4) {
        std::cerr
            << "usage: exhaust INPUT OUTPUT_JSON RESIDUAL_TSV\n";
        return 2;
    }
    try {
        const auto cells = read_cells(argv[1]);
        std::ofstream residual_stream(argv[3]);
        if (!residual_stream) {
            throw std::runtime_error("cannot open residual output");
        }
        std::vector<CellResult> results;
        results.reserve(cells.size());
        std::array<std::uint64_t, 64> global_mask_histogram{};
        std::uint64_t total_ports = 0;
        std::uint64_t total_labelled_ports = 0;
        std::uint64_t total_survivors = 0;
        std::uint64_t total_labelled_survivors = 0;
        const auto started = std::chrono::steady_clock::now();

        for (std::size_t index = 0; index < cells.size(); ++index) {
            CellRunner runner(cells[index], residual_stream);
            CellResult result = runner.run();
            for (int mask = 0; mask < 64; ++mask) {
                global_mask_histogram[mask] +=
                    result.success_mask_histogram[mask];
            }
            total_ports += result.observed_ports;
            total_labelled_ports += (
                result.observed_ports * cells[index].orbit_size
            );
            total_survivors += result.survivor_ports;
            total_labelled_survivors += (
                result.survivor_ports * cells[index].orbit_size
            );
            results.push_back(result);
            const double seconds =
                std::chrono::duration<double>(
                    std::chrono::steady_clock::now() - started
                ).count();
            std::cout
                << "cell " << (index + 1)
                << " / " << cells.size()
                << " ports " << result.observed_ports
                << " survivors " << result.survivor_ports
                << " total " << total_ports
                << " elapsed " << seconds
                << '\n'
                << std::flush;
        }

        std::array<std::uint64_t, 7> success_count_histogram{};
        for (int mask = 0; mask < 64; ++mask) {
            success_count_histogram[std::popcount(
                static_cast<unsigned int>(mask)
            )] += global_mask_histogram[mask];
        }
        const double elapsed =
            std::chrono::duration<double>(
                std::chrono::steady_clock::now() - started
            ).count();
        std::ofstream output(argv[2]);
        if (!output) {
            throw std::runtime_error("cannot open JSON output");
        }
        output << "{\n";
        output << "  \"verified\": true,\n";
        output << "  \"status\": \"complete_compiled_six_potential_orbit_exhaustion\",\n";
        output << "  \"scope\": \"all reciprocal cubic port realizations in all 154 order-twelve Kotzig/type cell representatives\",\n";
        output << "  \"cell_orbits\": " << cells.size() << ",\n";
        output << "  \"representative_port_realizations\": "
               << total_ports << ",\n";
        output << "  \"labelled_cell_port_realizations\": "
               << total_labelled_ports << ",\n";
        output << "  \"success_count_histogram\": {\n";
        for (int count = 0; count <= 6; ++count) {
            output << "    \"" << count << "\": "
                   << success_count_histogram[count]
                   << (count == 6 ? "\n" : ",\n");
        }
        output << "  },\n";
        output << "  \"success_mask_histogram\": {\n";
        bool first_mask = true;
        for (int mask = 0; mask < 64; ++mask) {
            if (global_mask_histogram[mask] == 0) {
                continue;
            }
            if (!first_mask) {
                output << ",\n";
            }
            first_mask = false;
            output << "    \"" << mask << "\": "
                   << global_mask_histogram[mask];
        }
        output << "\n  },\n";
        output << "  \"all_six_potential_survivors\": "
               << total_survivors << ",\n";
        output << "  \"labelled_all_six_potential_survivors\": "
               << total_labelled_survivors << ",\n";
        output << "  \"cell_results\": [\n";
        for (std::size_t index = 0; index < cells.size(); ++index) {
            const auto& cell = cells[index];
            const auto& result = results[index];
            output << "    {\n";
            output << "      \"cell_id\": " << cell.id << ",\n";
            output << "      \"graph_index\": "
                   << cell.graph_index << ",\n";
            output << "      \"cell_index\": "
                   << cell.cell_index << ",\n";
            output << "      \"orbit_size\": "
                   << cell.orbit_size << ",\n";
            output << "      \"expected_ports\": "
                   << cell.expected_ports << ",\n";
            output << "      \"observed_ports\": "
                   << result.observed_ports << ",\n";
            output << "      \"survivors\": "
                   << result.survivor_ports << ",\n";
            output << "      \"port_hash_xor\": \""
                   << result.port_hash_xor << "\",\n";
            output << "      \"port_hash_sum\": \""
                   << result.port_hash_sum << "\",\n";
            output << "      \"classification_hash_xor\": \""
                   << result.classification_hash_xor << "\",\n";
            output << "      \"classification_hash_sum\": \""
                   << result.classification_hash_sum << "\",\n";
            output << "      \"success_mask_histogram\": {";
            bool first = true;
            for (int mask = 0; mask < 64; ++mask) {
                if (result.success_mask_histogram[mask] == 0) {
                    continue;
                }
                if (!first) {
                    output << ", ";
                }
                first = false;
                output << "\"" << mask << "\": "
                       << result.success_mask_histogram[mask];
            }
            output << "}\n";
            output << "    }"
                   << (index + 1 == cells.size() ? "\n" : ",\n");
        }
        output << "  ],\n";
        output << "  \"residual_tsv\": \"" << argv[3] << "\",\n";
        output << "  \"order_twelve_pairwise_disjoint_branch_excluded\": "
               << (total_survivors == 0 ? "true" : "false")
               << ",\n";
        output << "  \"global_conjecture_resolved\": false,\n";
        output << "  \"elapsed_seconds\": " << elapsed << "\n";
        output << "}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
