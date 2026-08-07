# Ownership and lifetime

Read this when designing a resource-owning type or investigating a leak, double free, or dangling
access.

## State ownership in the type

| Type | Contract |
|---|---|
| `T`, `T&`, `const T&` | value or non-owning reference; caller preserves the referenced lifetime |
| `T*` | nullable, non-owning observer by default |
| `unique_ptr<T>` | exclusive ownership; move transfers it |
| `shared_ptr<T>` | shared lifetime |
| `weak_ptr<T>` | observes shared state without extending its lifetime |
| handle or index | owner stays elsewhere; resolve on use |

The Core Guidelines’ I.11 rejects ownership transfer through a raw pointer or reference because the
caller cannot tell who deletes it. Return a value when possible, `unique_ptr` for exclusive dynamic
ownership, and `shared_ptr` only when owners genuinely share the lifetime.

## Bind cleanup to lifetime

Wrap every acquired resource in an object whose destructor releases it. This applies to memory,
files, locks, sockets, and library handles.

```cpp
// Bad: an exception or early return skips delete[].
auto* data = new std::byte[n];
process(data, n);
delete[] data;

// Good: every scope exit releases the allocation.
auto data = std::make_unique<std::byte[]>(n);
process(data.get(), n);
```

Prefer standard RAII types such as `scoped_lock` where they fit. Wrap a C handle once with its actual
release function instead of repeating manual cleanup. Destructors must not let failures escape;
throwing during stack unwinding terminates the program.

## Prefer the rule of zero

Compose owners from RAII members and declare no copy, move, or destructor operations. If one of
those operations needs custom behavior, consider and explicitly default or delete the full set;
declaring one can suppress or delete implicit others.

```cpp
class Buffer {
public:
    ~Buffer();
    Buffer(const Buffer&) = delete;
    Buffer& operator=(const Buffer&) = delete;
    Buffer(Buffer&&) noexcept;
    Buffer& operator=(Buffer&&) noexcept;
};
```

Make move operations `noexcept` when their implementation cannot throw. Standard containers may
copy instead of move during reallocation when that is needed to preserve exception guarantees.

For a base meant to be deleted polymorphically, use a public virtual destructor. If deletion through
the base is forbidden, use a protected non-virtual destructor. Deleting through a base without the
appropriate contract is undefined behavior.

## Pass the contract the function needs

| Intent | Parameter |
|---|---|
| inspect a cheap value | by value |
| inspect an expensive object | `const T&` |
| mutate caller state | `T&` |
| retain a value | by value then move, when its measured cost is acceptable |
| take exclusive ownership | `unique_ptr<T>` by value |
| join shared ownership | `shared_ptr<T>` by value |
| optional observer | `const T*` |

Do not pass a smart pointer when the function only observes the object; that couples the API to an
ownership policy it does not use. `string_view` and `span` are also observers: they do not extend the
source lifetime.

## Diagnose the common dangling paths

| Symptom | Cause | Replace with | Proof |
|---|---|---|---|
| access fails after return | reference or view into a local/temporary | return a value or owning type | ASan use-after-return or minimal lifetime test |
| access fails after vector growth | reallocation invalidated pointers, references, and iterators | resolve a stable index/handle after mutation | compare capacity and rerun under ASan |
| queued callback fails later | stored lambda captured a local by reference | capture required values explicitly or share a proven owner | execute callback after creator scope exits |
| cache reads freed storage | derived view outlived or missed invalidation with its source | give derived state the same owner and invalidate together | rebuild/destroy source in a focused test |
| shared graph never dies | strong-reference cycle | use `weak_ptr` for the non-owning back edge | assert destructor or owner count after release |

Container invalidation differs by operation and container; check its contract instead of applying
`vector` rules everywhere.

## Move without inventing guarantees

`std::move` only casts to an xvalue; the selected operation decides whether resources move. Standard
library objects are valid but unspecified after a move: operations without preconditions remain
safe, but do not assume a particular value such as empty. User-defined types follow their own
documented contract.

Return a named local without `std::move`; adding it can prevent named return-value optimization.
Do use `std::move` when transferring a local into an owner or member after its old value is no longer
needed.

See [the source basis](sources.md#ownership-lifetime-and-classes) for I.11, RAII, smart-pointer,
special-member, invalidation, and move contracts.
