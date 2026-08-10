// Verify that the P5 restriction image has no quintic equations.
//
// All contraction and row-reduction arithmetic is exact in F_7.  Nonzero
// modular ranks lift to characteristic zero because the S5 matrix-unit
// denominator 120 is invertible modulo seven.  The default run checks all
// 115 mode-symmetry representatives.  The min/max product flags allow the
// exact workload to be split into disjoint, independently replayable shards.

#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

using Perm = std::array<int, 5>;
using Matrix = std::vector<std::vector<int>>;

constexpr int PRIME = 7;
constexpr int DEGREE = 5;
constexpr int SOURCES = 5;
constexpr int MODES = 5;
constexpr int MASK = (1 << SOURCES) - 1;
constexpr int LOCAL_SIZE = 3125;

struct Rep {
    char name;
    std::string partition;
    int dimension;
    int schur_dimension;
    std::vector<Matrix> matrices;
    std::vector<int> characters;
};

struct Layer {
    std::vector<int> states;
    std::vector<std::vector<uint32_t>> transitions;
};

int mod(long long value) {
    value %= PRIME;
    return value < 0 ? static_cast<int>(value + PRIME)
                     : static_cast<int>(value);
}

int mod_power(int base, int exponent) {
    int output = 1;
    while (exponent) {
        if (exponent & 1) output = mod(output * base);
        base = mod(base * base);
        exponent >>= 1;
    }
    return output;
}

int mod_inverse(int value) {
    if (!mod(value)) throw std::runtime_error("division by zero");
    return mod_power(mod(value), PRIME - 2);
}

Perm compose(const Perm& left, const Perm& right) {
    Perm output{};
    for (int index = 0; index < DEGREE; ++index) {
        output[index] = left[right[index]];
    }
    return output;
}

Perm inverse(const Perm& permutation) {
    Perm output{};
    for (int old = 0; old < DEGREE; ++old) {
        output[permutation[old]] = old;
    }
    return output;
}

int sign(const Perm& permutation) {
    int inversions = 0;
    for (int left = 0; left < DEGREE; ++left) {
        for (int right = left + 1; right < DEGREE; ++right) {
            inversions += permutation[left] > permutation[right];
        }
    }
    return inversions % 2 ? -1 : 1;
}

int fixed_points(const Perm& permutation) {
    int output = 0;
    for (int index = 0; index < DEGREE; ++index) {
        output += permutation[index] == index;
    }
    return output;
}

int two_cycles(const Perm& permutation) {
    int output = 0;
    for (int left = 0; left < DEGREE; ++left) {
        for (int right = left + 1; right < DEGREE; ++right) {
            output += (
                permutation[left] == right
                && permutation[right] == left
            );
        }
    }
    return output;
}

int permutation_key(const Perm& permutation) {
    int key = 0;
    for (int value : permutation) key = DEGREE * key + value;
    return key;
}

std::vector<Perm> permutations5() {
    Perm permutation{0, 1, 2, 3, 4};
    std::vector<Perm> output;
    do {
        output.push_back(permutation);
    } while (std::next_permutation(
        permutation.begin(), permutation.end()
    ));
    if (output.size() != 120) {
        throw std::runtime_error("S5 enumeration failed");
    }
    return output;
}

Matrix identity_matrix(int dimension) {
    Matrix output(dimension, std::vector<int>(dimension, 0));
    for (int index = 0; index < dimension; ++index) {
        output[index][index] = 1;
    }
    return output;
}

Matrix matrix_product(const Matrix& left, const Matrix& right) {
    int rows = static_cast<int>(left.size());
    int middle = static_cast<int>(right.size());
    int columns = static_cast<int>(right[0].size());
    Matrix output(rows, std::vector<int>(columns, 0));
    for (int row = 0; row < rows; ++row) {
        for (int inner = 0; inner < middle; ++inner) {
            if (!left[row][inner]) continue;
            for (int column = 0; column < columns; ++column) {
                output[row][column] = mod(
                    output[row][column]
                    + left[row][inner] * right[inner][column]
                );
            }
        }
    }
    return output;
}

Matrix standard5(const Perm& permutation) {
    std::array<std::array<int, 5>, 4> basis{{
        {1, 0, 0, 0, -1},
        {0, 1, 0, 0, -1},
        {0, 0, 1, 0, -1},
        {0, 0, 0, 1, -1},
    }};
    Matrix output(4, std::vector<int>(4, 0));
    for (int column = 0; column < 4; ++column) {
        std::array<int, 5> image{};
        for (int old = 0; old < 5; ++old) {
            image[permutation[old]] = basis[column][old];
        }
        for (int row = 0; row < 4; ++row) {
            output[row][column] = mod(image[row]);
        }
    }
    return output;
}

std::vector<std::array<int, 2>> pairs(int size) {
    std::vector<std::array<int, 2>> output;
    for (int left = 0; left < size; ++left) {
        for (int right = left + 1; right < size; ++right) {
            output.push_back({left, right});
        }
    }
    return output;
}

Matrix exterior_square(const Matrix& matrix) {
    auto basis = pairs(static_cast<int>(matrix.size()));
    Matrix output(
        static_cast<int>(basis.size()),
        std::vector<int>(static_cast<int>(basis.size()), 0)
    );
    for (int column = 0; column < static_cast<int>(basis.size()); ++column) {
        auto [first, second] = basis[column];
        for (int row = 0; row < static_cast<int>(basis.size()); ++row) {
            auto [left, right] = basis[row];
            output[row][column] = mod(
                matrix[left][first] * matrix[right][second]
                - matrix[left][second] * matrix[right][first]
            );
        }
    }
    return output;
}

struct Nullspace {
    Matrix columns;
    std::vector<int> free_columns;
};

Nullspace nullspace_basis(Matrix matrix) {
    int rows = static_cast<int>(matrix.size());
    int columns = static_cast<int>(matrix[0].size());
    int rank = 0;
    std::vector<int> pivots;
    for (int column = 0; column < columns && rank < rows; ++column) {
        int pivot = rank;
        while (pivot < rows && !matrix[pivot][column]) ++pivot;
        if (pivot == rows) continue;
        std::swap(matrix[rank], matrix[pivot]);
        int scale = mod_inverse(matrix[rank][column]);
        for (int entry = 0; entry < columns; ++entry) {
            matrix[rank][entry] = mod(matrix[rank][entry] * scale);
        }
        for (int row = 0; row < rows; ++row) {
            if (row == rank || !matrix[row][column]) continue;
            int multiplier = matrix[row][column];
            for (int entry = 0; entry < columns; ++entry) {
                matrix[row][entry] = mod(
                    matrix[row][entry]
                    - multiplier * matrix[rank][entry]
                );
            }
        }
        pivots.push_back(column);
        ++rank;
    }
    std::vector<int> is_pivot(columns, 0);
    for (int pivot : pivots) is_pivot[pivot] = 1;
    std::vector<int> free;
    for (int column = 0; column < columns; ++column) {
        if (!is_pivot[column]) free.push_back(column);
    }
    Matrix basis(columns, std::vector<int>(free.size(), 0));
    for (int vector = 0; vector < static_cast<int>(free.size()); ++vector) {
        basis[free[vector]][vector] = 1;
        for (int row = 0; row < rank; ++row) {
            basis[pivots[row]][vector] = mod(
                -matrix[row][free[vector]]
            );
        }
    }
    return {basis, free};
}

int pair_index(
    const std::vector<std::array<int, 2>>& all,
    int left,
    int right
) {
    if (left > right) std::swap(left, right);
    for (int index = 0; index < static_cast<int>(all.size()); ++index) {
        if (all[index] == std::array<int, 2>{left, right}) return index;
    }
    throw std::runtime_error("pair index not found");
}

struct PairKernel {
    std::vector<std::array<int, 2>> edge_pairs;
    Matrix basis;
    std::vector<int> coordinate_rows;
};

PairKernel pair_kernel_basis() {
    auto edge_pairs = pairs(5);
    Matrix incidence(5, std::vector<int>(10, 0));
    for (int edge = 0; edge < 10; ++edge) {
        incidence[edge_pairs[edge][0]][edge] = 1;
        incidence[edge_pairs[edge][1]][edge] = 1;
    }
    auto kernel = nullspace_basis(incidence);
    if (kernel.free_columns.size() != 5) {
        throw std::runtime_error("pair-kernel dimension changed");
    }
    return {edge_pairs, kernel.columns, kernel.free_columns};
}

Matrix pair_kernel_representation(
    const Perm& permutation,
    const PairKernel& kernel
) {
    Matrix output(5, std::vector<int>(5, 0));
    for (int column = 0; column < 5; ++column) {
        std::array<int, 10> image{};
        for (int old_edge = 0; old_edge < 10; ++old_edge) {
            auto edge = kernel.edge_pairs[old_edge];
            int new_edge = pair_index(
                kernel.edge_pairs,
                permutation[edge[0]],
                permutation[edge[1]]
            );
            image[new_edge] = mod(
                image[new_edge] + kernel.basis[old_edge][column]
            );
        }
        for (int row = 0; row < 5; ++row) {
            output[row][column] = image[kernel.coordinate_rows[row]];
        }
    }
    return output;
}

std::vector<Rep> representations(
    const std::vector<Perm>& permutations
) {
    std::vector<Rep> output{
        {'T', "[5]", 1, 21, {}, {}},
        {'U', "[4,1]", 4, 24, {}, {}},
        {'V', "[3,2]", 5, 15, {}, {}},
        {'X', "[2,2,1]", 5, 3, {}, {}},
        {'W', "[3,1,1]", 6, 6, {}, {}},
    };
    auto kernel = pair_kernel_basis();
    for (const auto& permutation : permutations) {
        Matrix standard = standard5(permutation);
        Matrix pair_rep = pair_kernel_representation(permutation, kernel);
        Matrix signed_pair = pair_rep;
        for (auto& row : signed_pair) {
            for (int& value : row) {
                value = mod(sign(permutation) * value);
            }
        }
        output[0].matrices.push_back({{1}});
        output[1].matrices.push_back(standard);
        output[2].matrices.push_back(pair_rep);
        output[3].matrices.push_back(signed_pair);
        output[4].matrices.push_back(exterior_square(standard));

        int fixed = fixed_points(permutation);
        Perm square = compose(permutation, permutation);
        int standard_character = fixed - 1;
        int pair_character = (
            fixed * (fixed - 1) / 2 + two_cycles(permutation)
        );
        int v_character = pair_character - 1 - standard_character;
        int wedge_character = (
            standard_character * standard_character
            - (fixed_points(square) - 1)
        ) / 2;
        output[0].characters.push_back(1);
        output[1].characters.push_back(standard_character);
        output[2].characters.push_back(v_character);
        output[3].characters.push_back(sign(permutation) * v_character);
        output[4].characters.push_back(wedge_character);
    }
    return output;
}

void check_representations(
    const std::vector<Perm>& permutations,
    const std::vector<Rep>& reps
) {
    std::unordered_map<int, int> index;
    for (int position = 0; position < 120; ++position) {
        index[permutation_key(permutations[position])] = position;
    }
    for (const auto& rep : reps) {
        if (rep.matrices[0] != identity_matrix(rep.dimension)) {
            throw std::runtime_error("representation identity failed");
        }
        for (int p = 0; p < 120; ++p) {
            int trace = 0;
            for (int diagonal = 0; diagonal < rep.dimension; ++diagonal) {
                trace += rep.matrices[p][diagonal][diagonal];
            }
            if (mod(trace) != mod(rep.characters[p])) {
                throw std::runtime_error("character check failed");
            }
        }
        for (int left = 0; left < 120; ++left) {
            for (int right = 0; right < 120; ++right) {
                int product_index = index.at(permutation_key(
                    compose(permutations[left], permutations[right])
                ));
                if (
                    matrix_product(
                        rep.matrices[left], rep.matrices[right]
                    )
                    != rep.matrices[product_index]
                ) {
                    throw std::runtime_error(
                        "representation multiplication failed"
                    );
                }
            }
        }
        int inverse_order = mod_inverse(120);
        for (int row = 0; row < rep.dimension; ++row) {
            for (int column = 0; column < rep.dimension; ++column) {
                Matrix observed(
                    rep.dimension,
                    std::vector<int>(rep.dimension, 0)
                );
                for (int p = 0; p < 120; ++p) {
                    int inverse_index = index.at(permutation_key(
                        inverse(permutations[p])
                    ));
                    int coefficient = mod(
                        rep.dimension * inverse_order
                        * rep.matrices[inverse_index][column][row]
                    );
                    for (int out = 0; out < rep.dimension; ++out) {
                        for (int in = 0; in < rep.dimension; ++in) {
                            observed[out][in] = mod(
                                observed[out][in]
                                + coefficient
                                * rep.matrices[p][out][in]
                            );
                        }
                    }
                }
                Matrix expected(
                    rep.dimension,
                    std::vector<int>(rep.dimension, 0)
                );
                expected[row][column] = 1;
                if (observed != expected) {
                    throw std::runtime_error(
                        "matrix-unit orthogonality failed"
                    );
                }
            }
        }
    }
    for (int left = 0; left < static_cast<int>(reps.size()); ++left) {
        for (int right = 0; right < static_cast<int>(reps.size()); ++right) {
            int inner_product = 0;
            for (int p = 0; p < 120; ++p) {
                inner_product += (
                    reps[left].characters[p]
                    * reps[right].characters[p]
                );
            }
            int expected = left == right ? 120 : 0;
            if (inner_product != expected) {
                throw std::runtime_error(
                    "S5 character orthogonality failed"
                );
            }
        }
    }
}

int popcount(int value) {
    return __builtin_popcount(static_cast<unsigned int>(value));
}

int state_key(const std::array<int, 5>& masks) {
    return (
        masks[0]
        | (masks[1] << 5)
        | (masks[2] << 10)
        | (masks[3] << 15)
        | (masks[4] << 20)
    );
}

std::array<int, 5> state_masks(int key) {
    return {
        key & MASK,
        (key >> 5) & MASK,
        (key >> 10) & MASK,
        (key >> 15) & MASK,
        (key >> 20) & MASK,
    };
}

int local_index(const std::array<int, 5>& sources) {
    int output = 0;
    for (int source : sources) output = SOURCES * output + source;
    return output;
}

std::array<Layer, 5> build_layers() {
    std::array<std::vector<int>, 6> masks_by_size;
    for (int mask = 0; mask <= MASK; ++mask) {
        masks_by_size[popcount(mask)].push_back(mask);
    }
    std::array<std::vector<int>, 6> states;
    for (int size = 0; size <= 5; ++size) {
        for (int a : masks_by_size[size])
        for (int b : masks_by_size[size])
        for (int c : masks_by_size[size])
        for (int d : masks_by_size[size])
        for (int e : masks_by_size[size]) {
            states[size].push_back(state_key({a, b, c, d, e}));
        }
    }
    std::array<int, 6> expected{1, 3125, 100000, 100000, 3125, 1};
    for (int size = 0; size <= 5; ++size) {
        if (states[size].size() != static_cast<size_t>(expected[size])) {
            throw std::runtime_error("state layer size changed");
        }
    }
    std::array<Layer, 5> layers;
    for (int size = 0; size < 5; ++size) {
        layers[size].states = states[size];
        layers[size].transitions.resize(states[size].size());
        std::unordered_map<int, int> next_index;
        next_index.reserve(states[size + 1].size() * 2);
        for (int position = 0; position < expected[size + 1]; ++position) {
            next_index[states[size + 1][position]] = position;
        }
        for (int position = 0; position < expected[size]; ++position) {
            auto masks = state_masks(states[size][position]);
            for (int a = 0; a < SOURCES; ++a) {
                if (masks[0] & (1 << a)) continue;
                for (int b = 0; b < SOURCES; ++b) {
                    if (masks[1] & (1 << b)) continue;
                    for (int c = 0; c < SOURCES; ++c) {
                        if (masks[2] & (1 << c)) continue;
                        for (int d = 0; d < SOURCES; ++d) {
                            if (masks[3] & (1 << d)) continue;
                            for (int e = 0; e < SOURCES; ++e) {
                                if (masks[4] & (1 << e)) continue;
                                std::array<int, 5> sources{a, b, c, d, e};
                                std::array<int, 5> next_masks{
                                    masks[0] | (1 << a),
                                    masks[1] | (1 << b),
                                    masks[2] | (1 << c),
                                    masks[3] | (1 << d),
                                    masks[4] | (1 << e),
                                };
                                uint32_t next = static_cast<uint32_t>(
                                    next_index.at(state_key(next_masks))
                                );
                                uint32_t local = static_cast<uint32_t>(
                                    local_index(sources)
                                );
                                layers[size].transitions[position].push_back(
                                    next * LOCAL_SIZE + local
                                );
                            }
                        }
                    }
                }
            }
        }
        long long transition_count = 0;
        for (const auto& transitions : layers[size].transitions) {
            transition_count += transitions.size();
        }
        std::array<long long, 5> expected_transitions{
            3125, 3200000, 24300000, 3200000, 3125
        };
        if (transition_count != expected_transitions[size]) {
            throw std::runtime_error("DP transition count changed");
        }
    }
    return layers;
}

struct XorShift {
    uint64_t state;
    explicit XorShift(uint64_t seed) : state(seed) {}
    uint64_t next() {
        state ^= state << 13;
        state ^= state >> 7;
        state ^= state << 17;
        return state;
    }
    int field() {
        return static_cast<int>(next() % PRIME);
    }
};

std::array<int, 5> tuple_values(int index) {
    std::array<int, 5> output{};
    for (int position = 4; position >= 0; --position) {
        output[position] = index % SOURCES;
        index /= SOURCES;
    }
    return output;
}

int tuple_index(const std::array<int, 5>& tuple) {
    int output = 0;
    for (int value : tuple) output = SOURCES * output + value;
    return output;
}

std::vector<uint8_t> matrix_unit_covectors(
    const Rep& rep,
    const std::vector<Perm>& permutations,
    const std::unordered_map<int, int>& permutation_index,
    XorShift& rng
) {
    std::vector<int> seed(LOCAL_SIZE);
    for (int& value : seed) value = rng.field();
    std::vector<uint8_t> output(
        rep.dimension * LOCAL_SIZE, 0
    );
    int inverse_order = mod_inverse(120);
    for (int column = 0; column < rep.dimension; ++column) {
        for (int p = 0; p < 120; ++p) {
            int inverse_index = permutation_index.at(
                permutation_key(inverse(permutations[p]))
            );
            int coefficient = mod(
                rep.dimension * inverse_order
                * rep.matrices[inverse_index][column][0]
            );
            if (!coefficient) continue;
            Perm inverse_permutation = inverse(permutations[p]);
            for (int index = 0; index < LOCAL_SIZE; ++index) {
                auto observed = tuple_values(index);
                std::array<int, 5> source{};
                for (int position = 0; position < DEGREE; ++position) {
                    source[position] = observed[
                        inverse_permutation[position]
                    ];
                }
                int destination = column * LOCAL_SIZE + index;
                output[destination] = static_cast<uint8_t>(mod(
                    output[destination]
                    + coefficient * seed[tuple_index(source)]
                ));
            }
        }
    }
    return output;
}

struct Prefix {
    std::vector<uint8_t> values;
    int width;
};

Prefix permanent_prefix(
    const std::array<Layer, 5>& layers,
    const std::array<std::vector<uint8_t>, 4>& local,
    const std::array<int, 5>& dimensions
) {
    std::vector<uint8_t> current(1, 1);
    int width = 1;
    for (int mode = 0; mode < 4; ++mode) {
        int next_width = width * dimensions[mode];
        int next_states = static_cast<int>(
            layers[mode + 1].states.size()
        );
        std::vector<uint8_t> next(next_states * next_width, 0);
        for (
            int state = 0;
            state < static_cast<int>(layers[mode].states.size());
            ++state
        ) {
            for (uint32_t encoded : layers[mode].transitions[state]) {
                int next_state = static_cast<int>(encoded / LOCAL_SIZE);
                int local_position = static_cast<int>(
                    encoded % LOCAL_SIZE
                );
                for (int prefix = 0; prefix < width; ++prefix) {
                    int value = current[state * width + prefix];
                    if (!value) continue;
                    for (
                        int index = 0;
                        index < dimensions[mode];
                        ++index
                    ) {
                        int factor = local[mode][
                            index * LOCAL_SIZE + local_position
                        ];
                        int destination = (
                            next_state * next_width
                            + prefix * dimensions[mode]
                            + index
                        );
                        next[destination] = static_cast<uint8_t>(mod(
                            next[destination] + value * factor
                        ));
                    }
                }
            }
        }
        current.swap(next);
        width = next_width;
    }
    return {std::move(current), width};
}

std::vector<int> permanent_finish(
    const Layer& layer,
    const Prefix& prefix,
    const std::vector<uint8_t>& local,
    int last_dimension
) {
    int output_width = prefix.width * last_dimension;
    std::vector<int> output(output_width, 0);
    for (
        int state = 0;
        state < static_cast<int>(layer.states.size());
        ++state
    ) {
        if (layer.transitions[state].size() != 1) {
            throw std::runtime_error("final transition is not unique");
        }
        int local_position = static_cast<int>(
            layer.transitions[state][0] % LOCAL_SIZE
        );
        for (int before = 0; before < prefix.width; ++before) {
            int value = prefix.values[state * prefix.width + before];
            if (!value) continue;
            for (int index = 0; index < last_dimension; ++index) {
                output[before * last_dimension + index] = mod(
                    output[before * last_dimension + index]
                    + value * local[
                        index * LOCAL_SIZE + local_position
                    ]
                );
            }
        }
    }
    return output;
}

void check_permanent_copy_dp(const std::array<Layer, 5>& layers) {
    std::array<Perm, 5> copies{{
        {0, 1, 2, 3, 4},
        {1, 2, 3, 4, 0},
        {4, 3, 2, 1, 0},
        {2, 4, 1, 3, 0},
        {3, 0, 4, 2, 1},
    }};
    std::array<std::vector<uint8_t>, 5> local;
    for (int mode = 0; mode < MODES; ++mode) {
        local[mode].assign(LOCAL_SIZE, 0);
        std::array<int, 5> sources{};
        for (int copy = 0; copy < DEGREE; ++copy) {
            sources[copy] = copies[copy][mode];
        }
        local[mode][local_index(sources)] = 1;
    }
    std::array<std::vector<uint8_t>, 4> prefix_local{
        local[0], local[1], local[2], local[3]
    };
    std::array<int, 5> dimensions{1, 1, 1, 1, 1};
    auto prefix = permanent_prefix(
        layers, prefix_local, dimensions
    );
    auto observed = permanent_finish(
        layers[4], prefix, local[4], 1
    );
    if (observed != std::vector<int>{1}) {
        throw std::runtime_error(
            "permanent-copy DP isolated witness failed"
        );
    }

    local[4].assign(LOCAL_SIZE, 0);
    std::array<int, 5> invalid_sources{};
    for (int copy = 0; copy < DEGREE; ++copy) {
        invalid_sources[copy] = copies[copy][4];
    }
    invalid_sources[0] = copies[0][3];
    local[4][local_index(invalid_sources)] = 1;
    observed = permanent_finish(
        layers[4], prefix, local[4], 1
    );
    if (observed != std::vector<int>{0}) {
        throw std::runtime_error(
            "permanent-copy DP invalid witness was not zero"
        );
    }
}

std::vector<int> apply_local_matrix(
    const std::vector<int>& vector,
    const std::array<int, 5>& dimensions,
    int mode,
    const Matrix& matrix
) {
    int before = 1;
    for (int index = 0; index < mode; ++index) {
        before *= dimensions[index];
    }
    int after = 1;
    for (int index = mode + 1; index < MODES; ++index) {
        after *= dimensions[index];
    }
    int dimension = dimensions[mode];
    std::vector<int> output(vector.size(), 0);
    for (int prefix = 0; prefix < before; ++prefix) {
        for (int suffix = 0; suffix < after; ++suffix) {
            for (int out = 0; out < dimension; ++out) {
                int value = 0;
                for (int in = 0; in < dimension; ++in) {
                    int source = (
                        (prefix * dimension + in) * after + suffix
                    );
                    value += matrix[out][in] * vector[source];
                }
                int destination = (
                    (prefix * dimension + out) * after + suffix
                );
                output[destination] = mod(value);
            }
        }
    }
    return output;
}

void require_invariant(
    const std::vector<int>& vector,
    const std::array<int, 5>& types,
    const std::array<int, 5>& dimensions,
    const std::vector<Rep>& reps
) {
    for (int p = 0; p < 120; ++p) {
        std::vector<int> image = vector;
        for (int mode = 0; mode < MODES; ++mode) {
            image = apply_local_matrix(
                image,
                dimensions,
                mode,
                reps[types[mode]].matrices[p]
            );
        }
        if (image != vector) {
            throw std::runtime_error(
                "multiplicity vector is not S5-invariant"
            );
        }
    }
}

struct RowBasis {
    std::map<int, std::vector<int>> rows;

    bool add(std::vector<int> row) {
        for (const auto& [pivot, basis] : rows) {
            int multiplier = row[pivot];
            if (!multiplier) continue;
            for (int column = pivot; column < static_cast<int>(row.size());
                 ++column) {
                row[column] = mod(
                    row[column] - multiplier * basis[column]
                );
            }
        }
        int pivot = -1;
        for (int column = 0; column < static_cast<int>(row.size()); ++column) {
            if (row[column]) {
                pivot = column;
                break;
            }
        }
        if (pivot < 0) return false;
        int scale = mod_inverse(row[pivot]);
        for (int& value : row) value = mod(value * scale);
        for (auto& [old_pivot, basis] : rows) {
            int multiplier = basis[pivot];
            if (!multiplier) continue;
            for (int column = pivot; column < static_cast<int>(basis.size());
                 ++column) {
                basis[column] = mod(
                    basis[column] - multiplier * row[column]
                );
            }
        }
        rows.emplace(pivot, std::move(row));
        return true;
    }

    int rank() const {
        return static_cast<int>(rows.size());
    }
};

int invariant_multiplicity(
    const std::array<int, 5>& types,
    const std::vector<Rep>& reps
) {
    long long numerator = 0;
    for (int p = 0; p < 120; ++p) {
        long long product = 1;
        for (int type : types) product *= reps[type].characters[p];
        numerator += product;
    }
    if (numerator % 120) {
        throw std::runtime_error("nonintegral S5 multiplicity");
    }
    return static_cast<int>(numerator / 120);
}

long long factorial(int value) {
    long long output = 1;
    for (int factor = 2; factor <= value; ++factor) output *= factor;
    return output;
}

long long binomial(int total, int selected) {
    selected = std::min(selected, total - selected);
    long long output = 1;
    for (int index = 1; index <= selected; ++index) {
        output = output * (total - selected + index) / index;
    }
    return output;
}

int orbit_size(const std::array<int, 5>& types) {
    std::array<int, 5> counts{};
    for (int type : types) ++counts[type];
    long long denominator = 1;
    for (int count : counts) denominator *= factorial(count);
    return static_cast<int>(factorial(5) / denominator);
}

std::vector<std::array<int, 5>> type_representatives(
    const std::vector<Rep>& reps
) {
    std::vector<std::array<int, 5>> output;
    for (int t = 0; t <= 5; ++t)
    for (int u = 0; u <= 5 - t; ++u)
    for (int v = 0; v <= 5 - t - u; ++v)
    for (int x = 0; x <= 5 - t - u - v; ++x) {
        int w = 5 - t - u - v - x;
        std::array<int, 5> types{};
        int position = 0;
        for (int count = 0; count < t; ++count) types[position++] = 0;
        for (int count = 0; count < u; ++count) types[position++] = 1;
        for (int count = 0; count < v; ++count) types[position++] = 2;
        for (int count = 0; count < x; ++count) types[position++] = 3;
        for (int count = 0; count < w; ++count) types[position++] = 4;
        if (invariant_multiplicity(types, reps)) output.push_back(types);
    }
    return output;
}

std::string type_string(
    const std::array<int, 5>& types,
    const std::vector<Rep>& reps
) {
    std::string output;
    for (int type : types) output.push_back(reps[type].name);
    return output;
}

int main(int argc, char** argv) {
    int min_first_three_product = 0;
    int max_first_three_product = 216;
    int attempts = 2;
    int sample_slack = 3;
    for (int index = 1; index < argc; ++index) {
        std::string argument = argv[index];
        if (
            argument == "--min-first-three-product"
            && index + 1 < argc
        ) {
            min_first_three_product = std::stoi(argv[++index]);
        } else if (
            argument == "--max-first-three-product"
            && index + 1 < argc
        ) {
            max_first_three_product = std::stoi(argv[++index]);
        } else if (argument == "--attempts" && index + 1 < argc) {
            attempts = std::stoi(argv[++index]);
        } else if (argument == "--sample-slack" && index + 1 < argc) {
            sample_slack = std::stoi(argv[++index]);
        } else {
            throw std::runtime_error("unknown or incomplete argument");
        }
    }

    auto permutations = permutations5();
    auto reps = representations(permutations);
    check_representations(permutations, reps);
    std::unordered_map<int, int> permutation_index;
    for (int index = 0; index < 120; ++index) {
        permutation_index[permutation_key(permutations[index])] = index;
    }
    auto representatives = type_representatives(reps);
    if (representatives.size() != 115) {
        throw std::runtime_error("degree-five representative count changed");
    }
    int ordered_modules = 0;
    long long decomposed_dimension = 0;
    for (const auto& types : representatives) {
        int multiplicity = invariant_multiplicity(types, reps);
        ordered_modules += orbit_size(types);
        long long module_dimension = multiplicity;
        for (int type : types) {
            module_dimension *= reps[type].schur_dimension;
        }
        decomposed_dimension += module_dimension * orbit_size(types);
    }
    long long polynomial_dimension = binomial(243 + 4, 5);
    if (
        ordered_modules != 2955
        || decomposed_dimension != polynomial_dimension
    ) {
        throw std::runtime_error(
            "degree-five Schur-Weyl decomposition is incomplete"
        );
    }

    std::cout
        << "{\"phase\":\"census\",\"representatives\":115,"
        << "\"ordered_modules\":2955,"
        << "\"polynomial_dimension\":" << polynomial_dimension
        << ",\"field\":\"F_7\"}" << std::endl;

    auto layers = build_layers();
    check_permanent_copy_dp(layers);
    XorShift rng(20260727);
    int selected = 0;
    int full = 0;
    int inconclusive = 0;
    for (const auto& canonical_types : representatives) {
        std::array<int, 5> types = canonical_types;
        std::sort(
            types.begin(),
            types.end(),
            [&](int left, int right) {
                if (reps[left].dimension != reps[right].dimension) {
                    return reps[left].dimension < reps[right].dimension;
                }
                return left < right;
            }
        );
        int first_three_product = 1;
        for (int mode = 0; mode < 3; ++mode) {
            first_three_product *= reps[types[mode]].dimension;
        }
        if (
            first_three_product < min_first_three_product
            || first_three_product > max_first_three_product
        ) {
            continue;
        }
        ++selected;

        int multiplicity = invariant_multiplicity(types, reps);
        std::array<int, 5> dimensions{};
        for (int mode = 0; mode < MODES; ++mode) {
            dimensions[mode] = reps[types[mode]].dimension;
        }
        RowBasis basis;
        int samples = 0;
        for (
            int attempt = 0;
            attempt < attempts && basis.rank() < multiplicity;
            ++attempt
        ) {
            std::array<std::vector<uint8_t>, 4> fixed_local;
            for (int mode = 0; mode < 4; ++mode) {
                fixed_local[mode] = matrix_unit_covectors(
                    reps[types[mode]],
                    permutations,
                    permutation_index,
                    rng
                );
            }
            auto prefix = permanent_prefix(
                layers, fixed_local, dimensions
            );
            int target_samples = multiplicity + sample_slack;
            for (
                int sample = 0;
                sample < target_samples && basis.rank() < multiplicity;
                ++sample
            ) {
                auto last_local = matrix_unit_covectors(
                    reps[types[4]],
                    permutations,
                    permutation_index,
                    rng
                );
                auto vector = permanent_finish(
                    layers[4],
                    prefix,
                    last_local,
                    dimensions[4]
                );
                require_invariant(vector, types, dimensions, reps);
                basis.add(std::move(vector));
                ++samples;
            }
        }
        bool block_full = basis.rank() == multiplicity;
        full += block_full;
        inconclusive += !block_full;
        int ambient = 1;
        for (int dimension : dimensions) ambient *= dimension;
        std::cout
            << "{\"types\":\"" << type_string(types, reps)
            << "\",\"multiplicity\":" << multiplicity
            << ",\"rank\":" << basis.rank()
            << ",\"samples\":" << samples
            << ",\"ambient\":" << ambient
            << ",\"first_three_product\":" << first_three_product
            << ",\"status\":\""
            << (block_full ? "FULL_RANK" : "INCONCLUSIVE")
            << "\"}" << std::endl;
    }
    bool complete_coverage = selected == 115;
    bool all_full = inconclusive == 0;
    std::cout
        << "{\"phase\":\"selective_summary\",\"selected\":" << selected
        << ",\"full_rank\":" << full
        << ",\"inconclusive\":" << inconclusive
        << ",\"min_first_three_product\":"
        << min_first_three_product
        << ",\"max_first_three_product\":"
        << max_first_three_product
        << ",\"complete_coverage\":"
        << (complete_coverage ? "true" : "false")
        << ",\"quintic_pullback_injective_over_Q\":"
        << (
            complete_coverage && all_full
            ? "true"
            : "null"
        )
        << ",\"nonzero_quintic_restriction_equations\":"
        << (
            complete_coverage && all_full
            ? "0"
            : "null"
        )
        << ",\"global_conjecture_resolved\":false}" << std::endl;
    return inconclusive ? 2 : 0;
}
