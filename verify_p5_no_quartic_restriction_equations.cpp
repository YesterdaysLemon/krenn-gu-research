// Verify that the P5 restriction image has no quartic equations.
//
// All contraction and row-reduction arithmetic is exact in F_5.
// Nonzero modular ranks lift to characteristic zero because the S4
// matrix-unit denominator 24 is invertible modulo five.

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

using Perm = std::array<int, 4>;
using Matrix = std::vector<std::vector<int>>;

constexpr int PRIME = 5;
constexpr int SOURCES = 5;
constexpr int MODES = 5;
constexpr int MASK = (1 << SOURCES) - 1;
constexpr int CHARACTERS[4][5] = {
    {1, 1, 1, 1, 1},
    {3, 1, -1, 0, -1},
    {3, -1, -1, 0, 1},
    {2, 0, 2, -1, 0},
};

struct Rep {
    char name;
    int dimension;
    int schur_dimension;
    std::vector<Matrix> matrices;
};

struct Transition {
    int next;
    int local_index;
};

struct Layer {
    std::vector<int> states;
    std::vector<std::vector<Transition>> transitions;
};

int mod(int value) {
    value %= PRIME;
    return value < 0 ? value + PRIME : value;
}

int mod_power(int base, int exponent) {
    int output = 1;
    while (exponent) {
        if (exponent & 1) {
            output = mod(output * base);
        }
        base = mod(base * base);
        exponent >>= 1;
    }
    return output;
}

int mod_inverse(int value) {
    return mod_power(mod(value), PRIME - 2);
}

Perm compose(const Perm& left, const Perm& right) {
    Perm output{};
    for (int index = 0; index < 4; ++index) {
        output[index] = left[right[index]];
    }
    return output;
}

Perm inverse(const Perm& permutation) {
    Perm output{};
    for (int old = 0; old < 4; ++old) {
        output[permutation[old]] = old;
    }
    return output;
}

int sign(const Perm& permutation) {
    int inversions = 0;
    for (int left = 0; left < 4; ++left) {
        for (int right = left + 1; right < 4; ++right) {
            inversions += permutation[left] > permutation[right];
        }
    }
    return inversions % 2 ? -1 : 1;
}

int cycle_class(const Perm& permutation) {
    std::array<bool, 4> seen{};
    std::vector<int> lengths;
    for (int start = 0; start < 4; ++start) {
        if (seen[start]) continue;
        int current = start;
        int length = 0;
        while (!seen[current]) {
            seen[current] = true;
            current = permutation[current];
            ++length;
        }
        lengths.push_back(length);
    }
    std::sort(lengths.begin(), lengths.end(), std::greater<int>());
    if (lengths == std::vector<int>{1, 1, 1, 1}) return 0;
    if (lengths == std::vector<int>{2, 1, 1}) return 1;
    if (lengths == std::vector<int>{2, 2}) return 2;
    if (lengths == std::vector<int>{3, 1}) return 3;
    if (lengths == std::vector<int>{4}) return 4;
    throw std::runtime_error("unknown S4 cycle class");
}

int permutation_key(const Perm& permutation) {
    int key = 0;
    for (int value : permutation) {
        key = 4 * key + value;
    }
    return key;
}

std::vector<Perm> permutations4() {
    Perm permutation{0, 1, 2, 3};
    std::vector<Perm> output;
    do {
        output.push_back(permutation);
    } while (std::next_permutation(
        permutation.begin(), permutation.end()
    ));
    if (output.size() != 24) {
        throw std::runtime_error("S4 enumeration failed");
    }
    return output;
}

Matrix identity_matrix(int dimension) {
    Matrix output(
        dimension, std::vector<int>(dimension, 0)
    );
    for (int index = 0; index < dimension; ++index) {
        output[index][index] = 1;
    }
    return output;
}

Matrix matrix_product(const Matrix& left, const Matrix& right) {
    int dimension = static_cast<int>(left.size());
    Matrix output(
        dimension, std::vector<int>(dimension, 0)
    );
    for (int row = 0; row < dimension; ++row) {
        for (int middle = 0; middle < dimension; ++middle) {
            for (int column = 0; column < dimension; ++column) {
                output[row][column] = mod(
                    output[row][column]
                    + left[row][middle] * right[middle][column]
                );
            }
        }
    }
    return output;
}

Matrix standard4(const Perm& permutation) {
    std::array<std::array<int, 4>, 3> basis{{
        {1, 0, 0, -1},
        {0, 1, 0, -1},
        {0, 0, 1, -1},
    }};
    Matrix output(3, std::vector<int>(3, 0));
    for (int column = 0; column < 3; ++column) {
        std::array<int, 4> image{};
        for (int old = 0; old < 4; ++old) {
            image[permutation[old]] = basis[column][old];
        }
        output[0][column] = mod(image[0]);
        output[1][column] = mod(image[1]);
        output[2][column] = mod(image[2]);
    }
    return output;
}

std::array<std::array<std::array<int, 2>, 2>, 3> pairings() {
    return {{
        {{{0, 1}, {2, 3}}},
        {{{0, 2}, {1, 3}}},
        {{{0, 3}, {1, 2}}},
    }};
}

std::array<int, 2> sorted_pair(int left, int right) {
    if (left > right) {
        std::swap(left, right);
    }
    return {left, right};
}

int pairing_image(
    int pairing_index,
    const Perm& permutation
) {
    auto all = pairings();
    std::array<std::array<int, 2>, 2> image{{
        sorted_pair(
            permutation[all[pairing_index][0][0]],
            permutation[all[pairing_index][0][1]]
        ),
        sorted_pair(
            permutation[all[pairing_index][1][0]],
            permutation[all[pairing_index][1][1]]
        ),
    }};
    if (image[1] < image[0]) {
        std::swap(image[0], image[1]);
    }
    for (int candidate = 0; candidate < 3; ++candidate) {
        auto target = all[candidate];
        if (target[1] < target[0]) {
            std::swap(target[0], target[1]);
        }
        if (target == image) {
            return candidate;
        }
    }
    throw std::runtime_error("pairing image not found");
}

Matrix doublet22(const Perm& permutation) {
    std::array<int, 3> induced{};
    for (int old = 0; old < 3; ++old) {
        induced[old] = pairing_image(old, permutation);
    }
    std::array<std::array<int, 3>, 2> basis{{
        {1, 0, -1},
        {0, 1, -1},
    }};
    Matrix output(2, std::vector<int>(2, 0));
    for (int column = 0; column < 2; ++column) {
        std::array<int, 3> image{};
        for (int old = 0; old < 3; ++old) {
            image[induced[old]] = basis[column][old];
        }
        output[0][column] = mod(image[0]);
        output[1][column] = mod(image[1]);
    }
    return output;
}

std::vector<Rep> representations(
    const std::vector<Perm>& permutations
) {
    std::vector<Rep> output{
        {'T', 1, 15, {}},
        {'S', 3, 15, {}},
        {'R', 3, 3, {}},
        {'D', 2, 6, {}},
    };
    for (const auto& permutation : permutations) {
        Matrix standard = standard4(permutation);
        output[0].matrices.push_back({{1}});
        output[1].matrices.push_back(standard);
        Matrix signed_standard = standard;
        for (auto& row : signed_standard) {
            for (int& value : row) {
                value = mod(sign(permutation) * value);
            }
        }
        output[2].matrices.push_back(signed_standard);
        output[3].matrices.push_back(doublet22(permutation));
    }
    return output;
}

void check_representations(
    const std::vector<Perm>& permutations,
    const std::vector<Rep>& reps
) {
    std::unordered_map<int, int> index;
    for (int position = 0; position < 24; ++position) {
        index[permutation_key(permutations[position])] = position;
    }
    for (int type = 0; type < static_cast<int>(reps.size()); ++type) {
        const auto& rep = reps[type];
        if (rep.matrices[0] != identity_matrix(rep.dimension)) {
            throw std::runtime_error("representation identity failed");
        }
        for (int p = 0; p < 24; ++p) {
            int trace = 0;
            for (int index = 0; index < rep.dimension; ++index) {
                trace += rep.matrices[p][index][index];
            }
            if (
                mod(trace)
                != mod(CHARACTERS[type][cycle_class(permutations[p])])
            ) {
                throw std::runtime_error(
                    "representation character table failed"
                );
            }
        }
        for (int left = 0; left < 24; ++left) {
            for (int right = 0; right < 24; ++right) {
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
        int inverse_order = mod_inverse(24);
        for (int row = 0; row < rep.dimension; ++row) {
            for (int column = 0; column < rep.dimension; ++column) {
                Matrix matrix_unit(
                    rep.dimension,
                    std::vector<int>(rep.dimension, 0)
                );
                for (int p = 0; p < 24; ++p) {
                    int inverse_index = index.at(permutation_key(
                        inverse(permutations[p])
                    ));
                    int coefficient = mod(
                        rep.dimension * inverse_order
                        * rep.matrices[inverse_index][column][row]
                    );
                    for (int out = 0; out < rep.dimension; ++out) {
                        for (int in = 0; in < rep.dimension; ++in) {
                            matrix_unit[out][in] = mod(
                                matrix_unit[out][in]
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
                if (matrix_unit != expected) {
                    throw std::runtime_error(
                        "matrix-unit orthogonality failed"
                    );
                }
            }
        }
    }
}

int popcount(int value) {
    return __builtin_popcount(
        static_cast<unsigned int>(value)
    );
}

int state_key(const std::array<int, 4>& masks) {
    return (
        masks[0]
        | (masks[1] << 5)
        | (masks[2] << 10)
        | (masks[3] << 15)
    );
}

std::array<int, 4> state_masks(int key) {
    return {
        key & MASK,
        (key >> 5) & MASK,
        (key >> 10) & MASK,
        (key >> 15) & MASK,
    };
}

int local_index(const std::array<int, 4>& sources) {
    int output = 0;
    for (int source : sources) {
        output = SOURCES * output + source;
    }
    return output;
}

std::array<Layer, 5> build_layers() {
    std::array<std::vector<int>, 6> states;
    for (int first = 0; first <= MASK; ++first) {
        for (int second = 0; second <= MASK; ++second) {
            for (int third = 0; third <= MASK; ++third) {
                for (int fourth = 0; fourth <= MASK; ++fourth) {
                    int size = popcount(first);
                    if (
                        popcount(second) == size
                        && popcount(third) == size
                        && popcount(fourth) == size
                    ) {
                        states[size].push_back(state_key(
                            {first, second, third, fourth}
                        ));
                    }
                }
            }
        }
    }
    std::array<int, 6> expected{1, 625, 10000, 10000, 625, 1};
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
                            std::array<int, 4> sources_tuple{a, b, c, d};
                            std::array<int, 4> new_masks{
                                masks[0] | (1 << a),
                                masks[1] | (1 << b),
                                masks[2] | (1 << c),
                                masks[3] | (1 << d),
                            };
                            layers[size].transitions[position].push_back({
                                next_index.at(state_key(new_masks)),
                                local_index(sources_tuple),
                            });
                        }
                    }
                }
            }
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

int tuple_index(const std::array<int, 4>& tuple) {
    int output = 0;
    for (int value : tuple) {
        output = SOURCES * output + value;
    }
    return output;
}

std::array<int, 4> tuple_values(int index) {
    std::array<int, 4> output{};
    for (int position = 3; position >= 0; --position) {
        output[position] = index % SOURCES;
        index /= SOURCES;
    }
    return output;
}

std::vector<uint8_t> matrix_unit_covectors(
    const Rep& rep,
    const std::vector<Perm>& permutations,
    const std::unordered_map<int, int>& permutation_index,
    XorShift& rng
) {
    constexpr int local_size = 625;
    std::vector<int> seed(local_size);
    for (int& value : seed) {
        value = rng.field();
    }
    std::vector<uint8_t> output(
        rep.dimension * local_size, 0
    );
    int inverse_order = mod_inverse(24);
    for (int column = 0; column < rep.dimension; ++column) {
        for (int p = 0; p < 24; ++p) {
            int inverse_index = permutation_index.at(
                permutation_key(inverse(permutations[p]))
            );
            int coefficient = mod(
                rep.dimension
                * inverse_order
                * rep.matrices[inverse_index][column][0]
            );
            if (!coefficient) continue;
            Perm inverse_permutation = inverse(permutations[p]);
            for (int index = 0; index < local_size; ++index) {
                auto observed = tuple_values(index);
                std::array<int, 4> source{};
                for (int position = 0; position < 4; ++position) {
                    source[position] = observed[
                        inverse_permutation[position]
                    ];
                }
                int destination = column * local_size + index;
                output[destination] = static_cast<uint8_t>(mod(
                    output[destination]
                    + coefficient * seed[tuple_index(source)]
                ));
            }
        }
    }
    return output;
}

std::vector<int> permanent_contraction(
    const std::array<Layer, 5>& layers,
    const std::array<std::vector<uint8_t>, 5>& local,
    const std::array<int, 5>& dimensions
) {
    std::vector<uint8_t> current(1, 1);
    int width = 1;
    for (int mode = 0; mode < MODES; ++mode) {
        int next_width = width * dimensions[mode];
        int next_states = (
            mode == 4
            ? 1
            : static_cast<int>(layers[mode + 1].states.size())
        );
        std::vector<uint8_t> next(
            next_states * next_width, 0
        );
        for (
            int state = 0;
            state < static_cast<int>(layers[mode].states.size());
            ++state
        ) {
            for (const auto& transition : layers[mode].transitions[state]) {
                for (int prefix = 0; prefix < width; ++prefix) {
                    int value = current[state * width + prefix];
                    if (!value) continue;
                    for (int index = 0; index < dimensions[mode]; ++index) {
                        int factor = local[mode][
                            index * 625 + transition.local_index
                        ];
                        int destination = (
                            transition.next * next_width
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
    return std::vector<int>(current.begin(), current.end());
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
    for (int p = 0; p < 24; ++p) {
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
                "multiplicity vector is not S4-invariant"
            );
        }
    }
}

int matrix_rank(std::vector<std::vector<int>> matrix) {
    if (matrix.empty()) return 0;
    int rows = static_cast<int>(matrix.size());
    int columns = static_cast<int>(matrix[0].size());
    int rank = 0;
    for (int column = 0; column < columns && rank < rows; ++column) {
        int pivot = rank;
        while (pivot < rows && !mod(matrix[pivot][column])) {
            ++pivot;
        }
        if (pivot == rows) continue;
        std::swap(matrix[rank], matrix[pivot]);
        int inverse_pivot = mod_inverse(matrix[rank][column]);
        for (int entry = column; entry < columns; ++entry) {
            matrix[rank][entry] = mod(
                matrix[rank][entry] * inverse_pivot
            );
        }
        for (int row = 0; row < rows; ++row) {
            if (row == rank) continue;
            int multiplier = mod(matrix[row][column]);
            if (!multiplier) continue;
            for (int entry = column; entry < columns; ++entry) {
                matrix[row][entry] = mod(
                    matrix[row][entry]
                    - multiplier * matrix[rank][entry]
                );
            }
        }
        ++rank;
    }
    return rank;
}

int invariant_multiplicity(const std::array<int, 5>& types) {
    std::array<int, 5> class_sizes{1, 6, 3, 8, 6};
    int numerator = 0;
    for (int class_index = 0; class_index < 5; ++class_index) {
        int product = class_sizes[class_index];
        for (int type : types) {
            product *= CHARACTERS[type][class_index];
        }
        numerator += product;
    }
    if (numerator % 24) {
        throw std::runtime_error("nonintegral S4 multiplicity");
    }
    return numerator / 24;
}

long long factorial(int value) {
    long long output = 1;
    for (int factor = 2; factor <= value; ++factor) {
        output *= factor;
    }
    return output;
}

long long binomial(int total, int selected) {
    if (selected < 0 || selected > total) return 0;
    selected = std::min(selected, total - selected);
    long long output = 1;
    for (int index = 1; index <= selected; ++index) {
        output = output * (total - selected + index) / index;
    }
    return output;
}

int orbit_size(const std::array<int, 5>& types) {
    std::array<int, 4> counts{};
    for (int type : types) ++counts[type];
    long long denominator = 1;
    for (int count : counts) denominator *= factorial(count);
    return static_cast<int>(factorial(5) / denominator);
}

std::vector<std::array<int, 5>> type_representatives() {
    std::vector<std::array<int, 5>> output;
    for (int t = 0; t <= 5; ++t) {
        for (int s = 0; s <= 5 - t; ++s) {
            for (int r = 0; r <= 5 - t - s; ++r) {
                int d = 5 - t - s - r;
                std::array<int, 5> types{};
                int position = 0;
                for (int count = 0; count < t; ++count) types[position++] = 0;
                for (int count = 0; count < s; ++count) types[position++] = 1;
                for (int count = 0; count < r; ++count) types[position++] = 2;
                for (int count = 0; count < d; ++count) types[position++] = 3;
                if (invariant_multiplicity(types)) {
                    output.push_back(types);
                }
            }
        }
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

int main() {
    auto permutations = permutations4();
    auto reps = representations(permutations);
    check_representations(permutations, reps);
    std::unordered_map<int, int> permutation_index;
    for (int index = 0; index < 24; ++index) {
        permutation_index[permutation_key(permutations[index])] = index;
    }
    auto layers = build_layers();
    auto representatives = type_representatives();
    if (representatives.size() != 44) {
        throw std::runtime_error("quartic representative count changed");
    }
    int ordered_modules = 0;
    for (const auto& types : representatives) {
        ordered_modules += orbit_size(types);
    }
    if (ordered_modules != 839) {
        throw std::runtime_error("quartic module count changed");
    }
    long long decomposed_dimension = 0;
    int direct_ordered_modules = 0;
    for (int encoded = 0; encoded < 1024; ++encoded) {
        int remainder = encoded;
        std::array<int, 5> types{};
        for (int mode = 4; mode >= 0; --mode) {
            types[mode] = remainder % 4;
            remainder /= 4;
        }
        int multiplicity = invariant_multiplicity(types);
        if (!multiplicity) continue;
        ++direct_ordered_modules;
        long long module_dimension = multiplicity;
        for (int type : types) {
            module_dimension *= reps[type].schur_dimension;
        }
        decomposed_dimension += module_dimension;
    }
    int tensor_dimension = 1;
    for (int mode = 0; mode < MODES; ++mode) {
        tensor_dimension *= 3;
    }
    long long quartic_dimension = binomial(
        tensor_dimension + 3, 4
    );
    if (
        direct_ordered_modules != ordered_modules
        || decomposed_dimension != quartic_dimension
    ) {
        throw std::runtime_error(
            "quartic Schur-Weyl decomposition is incomplete"
        );
    }

    XorShift rng(20260727);
    bool all_full = true;
    for (const auto& types : representatives) {
        int multiplicity = invariant_multiplicity(types);
        std::array<int, 5> dimensions{};
        for (int mode = 0; mode < MODES; ++mode) {
            dimensions[mode] = reps[types[mode]].dimension;
        }
        std::vector<std::vector<int>> rows;
        int rank = 0;
        for (int sample = 0; sample < multiplicity + 10; ++sample) {
            std::array<std::vector<uint8_t>, 5> local;
            for (int mode = 0; mode < MODES; ++mode) {
                local[mode] = matrix_unit_covectors(
                    reps[types[mode]],
                    permutations,
                    permutation_index,
                    rng
                );
            }
            auto vector = permanent_contraction(
                layers, local, dimensions
            );
            require_invariant(vector, types, dimensions, reps);
            rows.push_back(std::move(vector));
            rank = matrix_rank(rows);
            if (rank == multiplicity) break;
        }
        if (rank != multiplicity) all_full = false;
        std::cout
            << "{\"types\":\"" << type_string(types, reps)
            << "\",\"orbit\":" << orbit_size(types)
            << ",\"multiplicity\":" << multiplicity
            << ",\"rank\":" << rank
            << ",\"samples\":" << rows.size()
            << ",\"ambient\":" << rows[0].size()
            << "}" << std::endl;
    }
    std::cout
        << "{\"verified\":true,\"field_for_rank_witnesses\":\"F_5\","
        << "\"degree\":4,\"target_tensor_space_dimension\":"
        << tensor_dimension
        << ",\"quartic_polynomial_space_dimension\":"
        << quartic_dimension << ","
        << "\"representatives\":44,\"ordered_modules\":839,"
        << "\"all_p5_multiplicity_ranks_full\":"
        << (all_full ? "true" : "false") << ","
        << "\"quartic_pullback_injective_over_Q\":"
        << (all_full ? "true" : "false") << ","
        << "\"nonzero_quartic_restriction_equations\":0,"
        << "\"global_conjecture_resolved\":false}"
        << std::endl;
    return all_full ? 0 : 2;
}
