"""Convert the Unitree H2 Plus (H2 with SHARPA hands) USD package to a web GLB.

Source robot files: https://github.com/kevinkawchak/fork_unitree_model/tree/main/H2_Plus
(``H2_with_sharpa.usdz`` — binary USD crate, 56 MB, 744k triangles, 75 revolute
joints). Three.js cannot parse binary USD crate at runtime, so this offline tool
extracts the articulated visual model and writes a compact GLB that
``docs/v11/index.html`` loads with GLTFLoader from a same-origin relative URL
(zero-404 rule: no cross-origin fetches, no runtime USD parsing).

The GLB preserves the full kinematic tree: one named node per robot link placed
at its physics joint frame, with the joint axis, limits, and type stored in the
node ``extras`` (surfaced by three.js as ``object.userData``), so the viewer can
articulate every joint by name. Meshes are welded, decimated (CAD-resolution
fingers are reduced harder than body shells), re-normaled, and grouped per
material color.

Usage (one-off, requires the extracted USDZ contents)::

    unzip H2_with_sharpa.usdz -d /tmp/h2x
    pip install usd-core fast-simplification pygltflib numpy
    python tools/convert_h2_usd_to_glb.py /tmp/h2x docs/v11/h2_plus.glb
"""

from __future__ import annotations

import json
import struct
import sys

import numpy as np

try:
    import fast_simplification
    from pxr import Usd, UsdGeom, UsdShade
except ImportError as exc:  # pragma: no cover - tool-only dependencies
    sys.exit(f"missing converter dependency: {exc}")

WELD_DECIMALS = 5
BODY_REDUCTION = 0.72  # body shells keep 28% of triangles
HAND_REDUCTION = 0.86  # SHARPA finger CAD keeps 14%
MIN_TRIS_TO_DECIMATE = 900


def quat_to_list(q):
    """Gf.Quat* -> [x, y, z, w] (glTF order)."""
    im = q.GetImaginary()
    return [float(im[0]), float(im[1]), float(im[2]), float(q.GetReal())]


def is_identity_quat(q, tol=1e-5):
    return abs(q[3] - 1.0) < tol and all(abs(c) < tol for c in q[:3])


def read_joints(stage):
    """Read every physics joint under /World/H2/joints."""
    joints = []
    root = stage.GetPrimAtPath("/World/H2/joints")
    for prim in root.GetChildren():
        t = prim.GetTypeName()
        if "Joint" not in t:
            continue

        def attr(name, default=None, prim=prim):
            a = prim.GetAttribute(name)
            return a.Get() if a and a.HasValue() else default

        def body(rel, prim=prim):
            r = prim.GetRelationship(rel)
            tg = r.GetTargets() if r else []
            return str(tg[0]).split("/")[-1] if tg else None

        p0 = attr("physics:localPos0", (0, 0, 0))
        q0 = attr("physics:localRot0")
        p1 = attr("physics:localPos1", (0, 0, 0))
        q1 = attr("physics:localRot1")
        joints.append(
            {
                "name": prim.GetName(),
                "type": "fixed" if t == "PhysicsFixedJoint" else "revolute",
                "parent": body("physics:body0"),
                "child": body("physics:body1"),
                "p0": [float(v) for v in p0],
                "q0": quat_to_list(q0) if q0 else [0, 0, 0, 1],
                "p1": [float(v) for v in p1],
                "q1": quat_to_list(q1) if q1 else [0, 0, 0, 1],
                "axis": attr("physics:axis", "Y"),
                "lo": float(attr("physics:lowerLimit", -360.0)),
                "hi": float(attr("physics:upperLimit", 360.0)),
            }
        )
    return joints


def shader_color(mat_prim):
    """diffuse color from an OmniPBR/UsdPreviewSurface shader, else mid grey."""
    for prim in Usd.PrimRange(mat_prim):
        if prim.GetTypeName() != "Shader":
            continue
        sh = UsdShade.Shader(prim)
        for name in ("diffuse_color_constant", "diffuseColor"):
            inp = sh.GetInput(name)
            if inp and inp.Get() is not None:
                c = inp.Get()
                return (float(c[0]), float(c[1]), float(c[2]))
    return (0.62, 0.64, 0.68)


def mesh_face_groups(mesh_prim, default_color):
    """Yield (color, triangle ndarray) groups for one mesh, honoring subsets."""
    mesh = UsdGeom.Mesh(mesh_prim)
    pts = np.array(mesh.GetPointsAttr().Get(), dtype=np.float64)
    counts = np.array(mesh.GetFaceVertexCountsAttr().Get(), dtype=np.int64)
    idx = np.array(mesh.GetFaceVertexIndicesAttr().Get(), dtype=np.int64)

    # fan-triangulate, remembering which source face each triangle came from
    tris, tri_face = [], []
    cursor = 0
    for f, c in enumerate(counts):
        for k in range(1, c - 1):
            tris.append((idx[cursor], idx[cursor + k], idx[cursor + k + 1]))
            tri_face.append(f)
        cursor += c
    tris = np.array(tris, dtype=np.int64)
    tri_face = np.array(tri_face, dtype=np.int64)

    def binding_color(prim):
        rel = UsdShade.MaterialBindingAPI(prim).GetDirectBindingRel()
        targets = rel.GetTargets() if rel else []
        if targets:
            mat = prim.GetStage().GetPrimAtPath(targets[0])
            if mat:
                return shader_color(mat)
        return None

    base_color = binding_color(mesh_prim) or default_color
    face_color = {}
    for sub in UsdGeom.Subset.GetAllGeomSubsets(mesh):
        c = binding_color(sub.GetPrim())
        if c is None:
            continue
        for f in sub.GetIndicesAttr().Get():
            face_color[int(f)] = c

    if not face_color:
        yield base_color, pts, tris
        return
    colors = np.array(
        [face_color.get(int(f), base_color) for f in tri_face], dtype=np.float64
    )
    for color in {tuple(c) for c in colors}:
        mask = np.all(np.isclose(colors, color), axis=1)
        yield tuple(color), pts, tris[mask]


def weld(pts, tris):
    """Collapse duplicate vertices (USD export is an unindexed soup)."""
    used = np.unique(tris)
    remap = np.full(len(pts), -1, dtype=np.int64)
    remap[used] = np.arange(len(used))
    pts, tris = pts[used], remap[tris]
    key = np.round(pts, WELD_DECIMALS)
    _, first, inverse = np.unique(key, axis=0, return_index=True, return_inverse=True)
    return pts[first], inverse[tris]


def decimate(pts, tris, reduction):
    if len(tris) < MIN_TRIS_TO_DECIMATE or reduction <= 0:
        return pts, tris
    out_pts, out_tris = fast_simplification.simplify(
        pts.astype(np.float32), tris.astype(np.int64), reduction
    )
    return out_pts.astype(np.float64), out_tris.astype(np.int64)


def vertex_normals(pts, tris):
    n = np.zeros_like(pts)
    a, b, c = pts[tris[:, 0]], pts[tris[:, 1]], pts[tris[:, 2]]
    fn = np.cross(b - a, c - a)  # area-weighted
    for col in range(3):
        np.add.at(n, tris[:, col], fn)
    norm = np.linalg.norm(n, axis=1, keepdims=True)
    norm[norm < 1e-12] = 1.0
    return n / norm


def pbr_for(color):
    """Heuristic PBR params for the H2 finish per diffuse color."""
    r, g, b = color
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    if lum < 0.08:  # black joint housings
        return {"metallic": 0.35, "roughness": 0.52}
    if g > 0.9 and r < 0.3:  # SHARPA fingertip sensor pads
        return {"metallic": 0.05, "roughness": 0.6}
    if lum > 0.85:  # white shells
        return {"metallic": 0.12, "roughness": 0.38}
    return {"metallic": 0.45, "roughness": 0.4}  # alloy blue-grey


class GlbBuilder:
    def __init__(self):
        self.bin = bytearray()
        self.views, self.accessors = [], []
        self.meshes, self.nodes, self.materials = [], [], []
        self.mat_index = {}

    def material(self, color):
        key = tuple(round(c, 4) for c in color)
        if key in self.mat_index:
            return self.mat_index[key]
        p = pbr_for(color)
        self.materials.append(
            {
                "name": f"h2_{len(self.materials)}",
                "pbrMetallicRoughness": {
                    "baseColorFactor": [*[float(c) for c in color], 1.0],
                    "metallicFactor": p["metallic"],
                    "roughnessFactor": p["roughness"],
                },
            }
        )
        self.mat_index[key] = len(self.materials) - 1
        return self.mat_index[key]

    def push(self, data, target):
        while len(self.bin) % 4:
            self.bin.append(0)
        offset = len(self.bin)
        self.bin.extend(data.tobytes())
        self.views.append(
            {
                "buffer": 0,
                "byteOffset": offset,
                "byteLength": data.nbytes,
                "target": target,
            }
        )
        return len(self.views) - 1

    def accessor(self, data, ctype, atype, target, minmax=False):
        view = self.push(data, target)
        acc = {
            "bufferView": view,
            "componentType": ctype,
            "count": len(data),
            "type": atype,
        }
        if minmax:
            acc["min"] = [float(v) for v in data.min(axis=0)]
            acc["max"] = [float(v) for v in data.max(axis=0)]
        self.accessors.append(acc)
        return len(self.accessors) - 1

    def mesh(self, name, primitives):
        prims = []
        for pts, tris, color in primitives:
            nrm = vertex_normals(pts, tris)
            prims.append(
                {
                    "attributes": {
                        "POSITION": self.accessor(
                            pts.astype(np.float32), 5126, "VEC3", 34962, True
                        ),
                        "NORMAL": self.accessor(
                            nrm.astype(np.float32), 5126, "VEC3", 34962
                        ),
                    },
                    "indices": self.accessor(
                        tris.reshape(-1).astype(np.uint32), 5125, "SCALAR", 34963
                    ),
                    "material": self.material(color),
                }
            )
        self.meshes.append({"name": name, "primitives": prims})
        return len(self.meshes) - 1

    def node(self, **kw):
        self.nodes.append(kw)
        return len(self.nodes) - 1

    def write(self, path, asset_extras):
        gltf = {
            "asset": {
                "version": "2.0",
                "generator": "tools/convert_h2_usd_to_glb.py",
                "extras": asset_extras,
            },
            "scene": 0,
            "scenes": [{"nodes": [0]}],
            "nodes": self.nodes,
            "meshes": self.meshes,
            "materials": self.materials,
            "accessors": self.accessors,
            "bufferViews": self.views,
            "buffers": [{"byteLength": len(self.bin)}],
        }
        js = json.dumps(gltf, separators=(",", ":")).encode()
        js += b" " * (-len(js) % 4)
        binc = bytes(self.bin) + b"\0" * (-len(self.bin) % 4)
        total = 12 + 8 + len(js) + 8 + len(binc)
        with open(path, "wb") as f:
            f.write(struct.pack("<4sII", b"glTF", 2, total))
            f.write(struct.pack("<II", len(js), 0x4E4F534A))
            f.write(js)
            f.write(struct.pack("<II", len(binc), 0x004E4942))
            f.write(binc)


def main(src_dir, out_path):
    main_stage = Usd.Stage.Open(f"{src_dir}/main.usdc")
    base = Usd.Stage.Open(f"{src_dir}/SubUSDs/H2_with_sharpa_base.usd")
    joints = read_joints(main_stage)
    children = {j["child"]: j for j in joints}

    cache = UsdGeom.XformCache()
    builder = GlbBuilder()

    total_in = total_out = 0

    def link_mesh(link):
        nonlocal total_in, total_out
        root = base.GetPrimAtPath(f"/visuals/{link}")
        if not root:
            return None
        hand = ("hand" in link) or any(
            f in link for f in ("index", "middle", "ring", "pinky", "thumb")
        )
        reduction = HAND_REDUCTION if hand else BODY_REDUCTION
        groups = {}
        for prim in Usd.PrimRange(root):
            if prim.GetTypeName() != "Mesh":
                continue
            xf = np.array(cache.ComputeRelativeTransform(prim, root)[0])
            for color, pts, tris in mesh_face_groups(prim, (0.62, 0.64, 0.68)):
                if not len(tris):
                    continue
                local = pts @ xf[:3, :3] + xf[3, :3]  # Gf row-vector convention
                p, t = weld(local, tris)
                total_in += len(t)
                p, t = decimate(p, t, reduction)
                total_out += len(t)
                groups.setdefault(color, []).append((p, t))
        if not groups:
            return None
        prims = []
        for color, parts in groups.items():
            offs, all_p, all_t = 0, [], []
            for p, t in parts:
                all_p.append(p)
                all_t.append(t + offs)
                offs += len(p)
            prims.append((np.vstack(all_p), np.vstack(all_t), color))
        return builder.mesh(link, prims)

    node_of = {}

    def add_link(link, joint):
        kw = {"name": link}
        if joint is not None:
            kw["translation"] = joint["p0"]
            if not is_identity_quat(joint["q0"]):
                kw["rotation"] = joint["q0"]
            extras = {"joint": joint["name"], "type": joint["type"]}
            if joint["type"] == "revolute":
                axis = {"X": [1, 0, 0], "Y": [0, 1, 0], "Z": [0, 0, 1]}
                extras.update(
                    axis=axis[str(joint["axis"])],
                    lo=round(joint["lo"], 3),
                    hi=round(joint["hi"], 3),
                )
            kw["extras"] = extras
        mesh_kids = []
        mi = link_mesh(link)
        if mi is not None:
            # child link frame = joint frame x inverse(localPose1)
            if joint is not None and (
                not is_identity_quat(joint["q1"])
                or any(abs(v) > 1e-6 for v in joint["p1"])
            ):
                q1 = joint["q1"]
                inv_q = [-q1[0], -q1[1], -q1[2], q1[3]]
                mesh_kids.append(
                    builder.node(
                        name=f"{link}__mesh",
                        mesh=mi,
                        rotation=inv_q,
                        translation=[-v for v in joint["p1"]],
                    )
                )
            else:
                kw["mesh"] = mi
        idx = builder.node(**kw)
        if mesh_kids:
            builder.nodes[idx]["children"] = mesh_kids
        node_of[link] = idx
        kids = [j["child"] for j in joints if j["parent"] == link]
        child_idx = [add_link(c, children[c]) for c in kids]
        if child_idx:
            builder.nodes[idx].setdefault("children", []).extend(child_idx)
        return idx

    source = "kevinkawchak/fork_unitree_model main/H2_Plus/H2_with_sharpa.usdz"
    # root: -90 deg about X converts the Z-up USD robot to glTF Y-up
    root = builder.node(
        name="H2_with_sharpa",
        rotation=[-0.7071067811865476, 0, 0, 0.7071067811865476],
        extras={
            "source": source,
            "robot": "Unitree H2 Plus (H2 + dual SHARPA dexterous hands)",
            "dof": sum(1 for j in joints if j["type"] == "revolute"),
        },
    )
    pelvis = add_link("pelvis", None)
    builder.nodes[root]["children"] = [pelvis]

    builder.write(
        out_path,
        {
            "source": source,
            "license": "BSD-3-Clause (Unitree Robotics robot model)",
        },
    )
    rev = sum(1 for j in joints if j["type"] == "revolute")
    print(f"links: {len(node_of)}  joints: {len(joints)} ({rev} revolute)")
    print(f"triangles: {total_in:,} -> {total_out:,}")
    import os

    print(f"wrote {out_path} ({os.path.getsize(out_path) / 1e6:.2f} MB)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: convert_h2_usd_to_glb.py <extracted_usdz_dir> <out.glb>")
    main(sys.argv[1], sys.argv[2])
