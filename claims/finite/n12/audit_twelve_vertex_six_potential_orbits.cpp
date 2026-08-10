#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <tuple>
#include <unordered_map>
#include <vector>

namespace {

constexpr int N = 12;
constexpr int C = 3;
constexpr int RAYS = 6;
constexpr int D_COUNT = 18;
constexpr int K_COUNT = 18;
constexpr int EDGE_COUNT = D_COUNT + K_COUNT;
constexpr std::uint64_t OFFSET = 1469598103934665603ULL;
constexpr std::uint64_t PRIME = 1099511628211ULL;

constexpr std::array<std::array<int, C>, RAYS> PERMUTATIONS{{
    {{0, 1, 2}},
    {{0, 2, 1}},
    {{1, 0, 2}},
    {{1, 2, 0}},
    {{2, 0, 1}},
    {{2, 1, 0}},
}};

struct Diagonal {
    int u;
    int v;
    int colour;
};

struct Port {
    int u;
    int v;
    int cu;
    int cv;

    auto key() const {
        return std::tuple{u, v, cu, cv};
    }
};

struct Edge {
    int u;
    int v;
    int cu;
    int cv;
};

struct Cell {
    int id;
    int graph_index;
    int cell_index;
    std::uint64_t orbit_size;
    int stabilizer_size;
    std::uint64_t expected;
    std::array<Diagonal, D_COUNT> diagonal{};
    std::array<std::array<int, C>, N> normal{};
};

struct Result {
    std::uint64_t ports = 0;
    std::uint64_t survivors = 0;
    std::uint64_t port_xor = 0;
    std::uint64_t port_sum = 0;
    std::uint64_t classification_xor = 0;
    std::uint64_t classification_sum = 0;
    std::array<std::uint64_t, 64> masks{};
};

std::uint64_t mix(std::uint64_t hash, std::uint64_t value) {
    for (int byte = 0; byte < 8; ++byte) {
        hash ^= (value >> (8 * byte)) & 0xffULL;
        hash *= PRIME;
    }
    return hash;
}

std::uint64_t hash_ports(
    int cell_id,
    const std::array<Port, K_COUNT>& raw
) {
    auto ports = raw;
    std::sort(
        ports.begin(),
        ports.end(),
        [](const Port& left, const Port& right) {
            return left.key() < right.key();
        }
    );
    std::uint64_t hash = mix(OFFSET, cell_id);
    for (const auto& port : ports) {
        hash = mix(hash, port.u);
        hash = mix(hash, port.v);
        hash = mix(hash, port.cu);
        hash = mix(hash, port.cv);
    }
    return hash;
}

class Auditor {
public:
    explicit Auditor(const Cell& cell) : cell_(cell) {
        for (auto& row : is_diagonal_) {
            row.fill(false);
        }
        for (const auto& edge : cell.diagonal) {
            is_diagonal_[edge.u][edge.v] = true;
            is_diagonal_[edge.v][edge.u] = true;
        }
        build_potentials();
        build_stub_options();
        for (int vertex = 0, power = 1; vertex < N; ++vertex) {
            power3_[vertex] = power;
            power *= C;
        }
    }

    Result run() {
        std::array<std::array<bool, N>, N> pair_used{};
        enumerate_ports((1ULL << (C * N)) - 1ULL, pair_used);
        if (result_.ports != cell_.expected) {
            throw std::runtime_error(
                "independent port count disagrees with input"
            );
        }
        return result_;
    }

private:
    const Cell& cell_;
    Result result_{};
    std::array<std::array<bool, N>, N> is_diagonal_{};
    std::array<std::vector<int>, C * N> options_{};
    std::array<Port, K_COUNT> ports_{};
    int port_cursor_ = 0;
    std::array<std::array<std::array<int, RAYS>, C>, N> q_{};
    std::array<int, N> power3_{};

    void build_potentials() {
        for (int vertex = 0; vertex < N; ++vertex) {
            for (int ray = 0; ray < RAYS; ++ray) {
                const auto& permutation = PERMUTATIONS[ray];
                std::array<int, C> relabelled{{-1, -1, -1}};
                for (int colour = 0; colour < C; ++colour) {
                    relabelled[permutation[colour]] =
                        permutation[cell_.normal[vertex][colour]];
                }
                const int b0 = relabelled[0] == 2;
                const int b1 = relabelled[1] == 2;
                const int b2 = relabelled[2] == 1;
                const std::array<int, C> base{{
                    1 - 2 * b2,
                    2 * (b2 - b0),
                    2 * (b0 + b1 - 1),
                }};
                for (int colour = 0; colour < C; ++colour) {
                    q_[vertex][colour][ray] =
                        base[permutation[colour]];
                }
            }
        }
        for (const auto& edge : cell_.diagonal) {
            for (int ray = 0; ray < RAYS; ++ray) {
                if (
                    q_[edge.u][edge.colour][ray]
                    + q_[edge.v][edge.colour][ray]
                    != 0
                ) {
                    throw std::runtime_error(
                        "diagonal edge has nonzero potential"
                    );
                }
            }
        }
    }

    void build_stub_options() {
        for (int vertex = 0; vertex < N; ++vertex) {
            for (int colour = 0; colour < C; ++colour) {
                const int stub = C * vertex + colour;
                const int partner_colour =
                    cell_.normal[vertex][colour];
                for (int other = 0; other < N; ++other) {
                    if (
                        other == vertex
                        || is_diagonal_[vertex][other]
                        || cell_.normal[other][partner_colour] != colour
                        || !unit_survives_bridge_table(
                            vertex,
                            other,
                            partner_colour,
                            colour
                        )
                    ) {
                        continue;
                    }
                    options_[stub].push_back(
                        C * other + partner_colour
                    );
                }
                std::sort(
                    options_[stub].begin(), options_[stub].end()
                );
            }
        }
    }

    bool unit_survives_bridge_table(
        int left,
        int right,
        int left_colour,
        int right_colour
    ) const {
        for (int target = 0; target < C; ++target) {
            if (
                !(left_colour == target && right_colour == target)
                && left_colour != cell_.normal[left][target]
                && right_colour != cell_.normal[right][target]
            ) {
                return false;
            }
        }
        return true;
    }

    void enumerate_ports(
        std::uint64_t remaining,
        std::array<std::array<bool, N>, N>& pair_used
    ) {
        if (remaining == 0) {
            if (port_cursor_ != K_COUNT) {
                throw std::runtime_error("port cursor changed");
            }
            audit_architecture();
            return;
        }

        int chosen = -1;
        int fewest = std::numeric_limits<int>::max();
        // Deliberately reverse the primary program's tie order.
        for (int stub = C * N - 1; stub >= 0; --stub) {
            if (((remaining >> stub) & 1ULL) == 0) {
                continue;
            }
            int candidates = 0;
            const int vertex = stub / C;
            for (const int partner : options_[stub]) {
                const int other = partner / C;
                candidates += (
                    ((remaining >> partner) & 1ULL)
                    && !pair_used[vertex][other]
                );
            }
            if (candidates < fewest) {
                chosen = stub;
                fewest = candidates;
            }
        }
        if (chosen < 0 || fewest == 0) {
            return;
        }

        const int vertex = chosen / C;
        const int colour = chosen % C;
        for (auto iterator = options_[chosen].rbegin();
             iterator != options_[chosen].rend();
             ++iterator) {
            const int partner = *iterator;
            if (((remaining >> partner) & 1ULL) == 0) {
                continue;
            }
            const int other = partner / C;
            const int other_colour = partner % C;
            if (pair_used[vertex][other]) {
                continue;
            }
            const int u = std::min(vertex, other);
            const int v = std::max(vertex, other);
            ports_[port_cursor_++] = Port{
                u,
                v,
                u == vertex ? other_colour : colour,
                v == other ? colour : other_colour,
            };
            pair_used[vertex][other] = true;
            pair_used[other][vertex] = true;
            enumerate_ports(
                remaining
                    ^ (1ULL << chosen)
                    ^ (1ULL << partner),
                pair_used
            );
            pair_used[vertex][other] = false;
            pair_used[other][vertex] = false;
            --port_cursor_;
        }
    }

    std::uint8_t classify() const {
        std::array<Edge, EDGE_COUNT> edges{};
        int cursor = 0;
        for (const auto& item : cell_.diagonal) {
            edges[cursor++] = Edge{
                item.u, item.v, item.colour, item.colour
            };
        }
        for (const auto& item : ports_) {
            edges[cursor++] = Edge{
                item.u, item.v, item.cu, item.cv
            };
        }
        if (cursor != EDGE_COUNT) {
            throw std::runtime_error("edge cursor changed");
        }

        std::array<std::vector<int>, N> incident{};
        for (int edge_id = 0; edge_id < EDGE_COUNT; ++edge_id) {
            incident[edges[edge_id].u].push_back(edge_id);
            incident[edges[edge_id].v].push_back(edge_id);
        }
        std::unordered_map<int, std::uint8_t> counts;

        const auto enumerate = [&](
            auto&& self,
            std::uint16_t remaining,
            int colouring_code,
            int colour_mask
        ) -> void {
            if (remaining == 0) {
                if (std::popcount(
                        static_cast<unsigned int>(colour_mask)
                    ) < 2) {
                    return;
                }
                auto& count = counts[colouring_code];
                if (count < 2) {
                    ++count;
                }
                return;
            }
            const int left = std::countr_zero(remaining);
            for (const int edge_id : incident[left]) {
                auto edge = edges[edge_id];
                if (edge.v == left) {
                    std::swap(edge.u, edge.v);
                    std::swap(edge.cu, edge.cv);
                }
                if (((remaining >> edge.v) & 1U) == 0) {
                    continue;
                }
                self(
                    self,
                    remaining
                        ^ static_cast<std::uint16_t>(1U << edge.u)
                        ^ static_cast<std::uint16_t>(1U << edge.v),
                    colouring_code
                        + edge.cu * power3_[edge.u]
                        + edge.cv * power3_[edge.v],
                    colour_mask
                        | (1 << edge.cu)
                        | (1 << edge.cv)
                );
            }
        };
        enumerate(
            enumerate,
            static_cast<std::uint16_t>((1U << N) - 1U),
            0,
            0
        );
        if (counts.empty()) {
            throw std::runtime_error("no mixed matching");
        }

        std::array<int, RAYS> minima{};
        minima.fill(std::numeric_limits<int>::max());
        for (const auto& [code, count] : counts) {
            (void)count;
            int remaining_code = code;
            std::array<int, RAYS> values{};
            for (int vertex = 0; vertex < N; ++vertex) {
                const int colour = remaining_code % C;
                remaining_code /= C;
                for (int ray = 0; ray < RAYS; ++ray) {
                    values[ray] += q_[vertex][colour][ray];
                }
            }
            for (int ray = 0; ray < RAYS; ++ray) {
                minima[ray] = std::min(minima[ray], values[ray]);
            }
        }

        std::uint8_t mask = 0;
        for (const auto& [code, count] : counts) {
            if (count != 1) {
                continue;
            }
            int remaining_code = code;
            std::array<int, RAYS> values{};
            for (int vertex = 0; vertex < N; ++vertex) {
                const int colour = remaining_code % C;
                remaining_code /= C;
                for (int ray = 0; ray < RAYS; ++ray) {
                    values[ray] += q_[vertex][colour][ray];
                }
            }
            for (int ray = 0; ray < RAYS; ++ray) {
                if (values[ray] == minima[ray]) {
                    mask |= static_cast<std::uint8_t>(1U << ray);
                }
            }
        }
        return mask;
    }

    void audit_architecture() {
        const std::uint64_t hash = hash_ports(cell_.id, ports_);
        const std::uint8_t mask = classify();
        ++result_.ports;
        result_.port_xor ^= hash;
        result_.port_sum += hash;
        ++result_.masks[mask];
        const std::uint64_t classified = mix(hash, mask);
        result_.classification_xor ^= classified;
        result_.classification_sum += classified;
        result_.survivors += mask == 0;
    }
};

std::vector<Cell> read_cells(const char* path) {
    std::ifstream stream(path);
    if (!stream) {
        throw std::runtime_error("cannot open input");
    }
    int count = 0;
    stream >> count;
    if (count != 154) {
        throw std::runtime_error("cell count changed");
    }
    std::vector<Cell> cells(count);
    for (auto& cell : cells) {
        stream
            >> cell.id
            >> cell.graph_index
            >> cell.cell_index
            >> cell.orbit_size
            >> cell.stabilizer_size
            >> cell.expected;
        for (auto& edge : cell.diagonal) {
            stream >> edge.u >> edge.v >> edge.colour;
        }
        for (auto& normal : cell.normal) {
            stream >> normal[0] >> normal[1] >> normal[2];
        }
        if (!stream) {
            throw std::runtime_error("input truncated");
        }
    }
    return cells;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "usage: audit INPUT OUTPUT_TSV\n";
        return 2;
    }
    try {
        const auto cells = read_cells(argv[1]);
        std::ofstream output(argv[2]);
        if (!output) {
            throw std::runtime_error("cannot open output");
        }
        const auto started = std::chrono::steady_clock::now();
        std::uint64_t total = 0;
        std::uint64_t survivors = 0;
        for (std::size_t index = 0; index < cells.size(); ++index) {
            Auditor auditor(cells[index]);
            const Result result = auditor.run();
            total += result.ports;
            survivors += result.survivors;
            output
                << cells[index].id << ' '
                << result.ports << ' '
                << result.survivors << ' '
                << result.port_xor << ' '
                << result.port_sum << ' '
                << result.classification_xor << ' '
                << result.classification_sum;
            for (const auto count : result.masks) {
                output << ' ' << count;
            }
            output << '\n';
            const double elapsed = std::chrono::duration<double>(
                std::chrono::steady_clock::now() - started
            ).count();
            std::cout
                << "cell " << index + 1 << " / " << cells.size()
                << " ports " << result.ports
                << " survivors " << result.survivors
                << " total " << total
                << " elapsed " << elapsed << '\n'
                << std::flush;
        }
        std::cout
            << "complete ports " << total
            << " survivors " << survivors << '\n';
    } catch (const std::exception& error) {
        std::cerr << "audit error: " << error.what() << '\n';
        return 1;
    }
    return 0;
}
