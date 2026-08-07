# Axmol review checklist

Use this for a scoped Axmol review. Apply `cpp-patterns` separately for language-level C++ risks.

## Review by failure surface

| Look for | Replace with | Failure avoided | Detail |
|---|---|---|---|
| `delete` on `ax::Object` | `release()` or RAII ownership | Other references becoming dangling | [Memory](memory.md) |
| `new Node` followed by `addChild()` | `Node::create()` | The initial reference leaking after scene teardown | [Memory](memory.md) |
| Raw engine pointers stored across frames | Parent lookup or `ax::RefPtr<T>` | Use-after-free after autorelease or removal | [Memory](memory.md) |
| `std::vector<Node*>` used as an owning collection | `ax::Vector<Node*>` or `RefPtr` elements | Dead pointers after external release | [Memory](memory.md) |
| Frame pixels mixed with design coordinates | One visible-rect coordinate contract | Camera, HUD, and hit tests disagreeing | [Scene and UI](scene-and-ui.md) |
| Listener or keyed schedule with no teardown | Node-bound listener or removal in `onExit` | Callback into a departed node | [Scene and UI](scene-and-ui.md) |
| v2 input callback copied from another release | Signature from the pinned header | Compile failure or wrong consumption behavior | [Migration](migration.md) |
| Multiple non-sampler uniform blocks in an Axmol 2 stage | One block per stage | Metal-only shader failure | [Graphics](graphics.md) |
| Custom shader with no batch check | Finalize state, call `updateBatchId()`, measure | Draw-call explosion | [Graphics](graphics.md) |
| Duplicate frame names across atlases | Prefix or preserve subdirectories at pack time | The wrong frame silently winning | [Graphics](graphics.md) |
| Engine tools retained across a branch switch | Re-run the pinned checkout's `setup.ps1` | axslcc/version mismatch | [Setup and build](setup-and-build.md) |
| Engine-submodule edits | Project config or an upstreamable commit | Upgrade-time reconciliation | [Setup and build](setup-and-build.md) |
| Cocos project files in an Axmol port | Fresh Axmol template plus moved code/assets | Stale build assumptions | [Migration](migration.md) |

## Prove the finding

Do not report a rule alone. Show the failing ownership path, coordinate spaces, shader stage,
generator, or migration boundary, then name the smallest check that falsifies the diagnosis.

```text
Good: onMouseMove is assigned a void lambda, but v2.11.4 declares std::function<bool(EventMouse*)>.
      Return the consumption decision; rebuild the target that owns the listener.

Bad: Mouse callback is wrong. Fix the signature.
```

For visuals, proof is the live target on the affected backend. For lifetime, exercise removal and
scene teardown with leak detection. For batching, use measured draw-call counts before and after.
