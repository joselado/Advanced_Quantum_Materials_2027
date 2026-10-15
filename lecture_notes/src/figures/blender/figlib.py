"""figlib.py: the Blender helpers shared by the schematic figures of the lecture notes.

A figure script builds one scene with its panels side by side, marks the points where the TikZ
overlay puts its labels with `anchor(name, co)`, and hands its `build()` to `main(build, name)`.
The render has a transparent background with the shadows on a shadow catcher, so it sits on the
white page; no text is rendered, every label comes from `figures/overlays/<name>.tex`. A figure whose panels need different cameras
hands a list of named panels to `main_panels(name, [(panel, build), ...])` instead.

Run with Blender 5.2.2 (the `blender` on the PATH is 2.79):
    DISPLAY=:0 ~/apps/blender-5.2.2-linux-x64/blender -b --factory-startup --python <script> -- still
    DISPLAY=:0 ~/apps/blender-5.2.2-linux-x64/blender -b --factory-startup --python <script> -- final
`still` renders at 50 % with few samples into out/<name>_still.png, `final` at full size into
out/<name>.png; both write out/<name>_anchors.tex, the anchors in units of the image width, and
`anchors` writes only that file.
The shapes and colors are those of the notes of Advanced Computational Methods in Physics, so that
the figures of the two courses read as one family.
"""
import math
import os
import sys

import bpy
import bmesh
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
WIDTH = 2400                                  # final width in px; the height follows the camera
SAMPLES = 256                                 # Cycles samples of a final render, denoised

# Colors of the series (linear RGB)
UP_TIP, UP_TAIL = (1.0, 0.62, 0.12), (0.75, 0.04, 0.02)
DOWN_TIP, DOWN_TAIL = (0.25, 0.75, 1.0), (0.03, 0.12, 0.55)
ELECTRON = (0.10, 0.62, 0.95)                 # the films' cyan, a little deeper so it holds on paper
SITE = (0.06, 0.06, 0.09)
BOND = (0.55, 0.56, 0.60)
TENSOR = (0.02, 0.30, 0.32)                  # tensors of states: a deeper teal than ACCENT[4], which prints as electron cyan
ACCENT = {1: (1.0, 0.55, 0.12), 2: (0.12, 0.75, 0.30), 3: (0.10, 0.62, 0.95),
          4: (0.05, 0.60, 0.60), 5: (0.55, 0.35, 0.95)}



def srgb(r, g, b):
    """Linear RGB of an sRGB color given as 0 to 255 values, so that the scene matches the page."""
    def f(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (f(r), f(g), f(b))


ACCENT_AQM = srgb(31, 78, 121)                # aqmaccent of figures_preamble.tex
SURFACE = srgb(118, 158, 198)                 # a lighter accent for large surfaces, which print dark
BROKEN = srgb(168, 42, 34)                    # aqmbroken: the one anomalous element of a figure

ANCHORS = {}
PREFIX = ['']                                 # set by main_panels, prepended to every anchor name


# ------------------------------------------------------------------------------------------------
# Materials
# ------------------------------------------------------------------------------------------------
def principled(name, rgb, rough=0.4, emit=0.0, alpha=1.0, spec=0.5):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    b = mat.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Specular IOR Level'].default_value = spec
    b.inputs['Emission Color'].default_value = (*rgb, 1)
    b.inputs['Emission Strength'].default_value = emit
    b.inputs['Alpha'].default_value = alpha
    return mat


def gradient_arrow_material(name, tip_rgb, tail_rgb, emit=0.15, rough=0.45, spec=0.4):
    """Arrow colored from tail to tip along its own z axis, as in the films."""
    mat = principled(name, tip_rgb, rough=rough, emit=emit, spec=spec)
    nt = mat.node_tree
    b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value, mr.inputs['From Max'].default_value = -0.5, 0.5
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.inputs['A'].default_value = (*tail_rgb, 1)
    mix.inputs['B'].default_value = (*tip_rgb, 1)
    nt.links.new(tc.outputs['Object'], sep.inputs[0])
    nt.links.new(sep.outputs['Z'], mr.inputs['Value'])
    nt.links.new(mr.outputs['Result'], mix.inputs['Factor'])
    nt.links.new(mix.outputs['Result'], b.inputs['Base Color'])
    nt.links.new(mix.outputs['Result'], b.inputs['Emission Color'])
    return mat


def glow(name, rgb, strength=2.0, alpha=0.35):
    """A soft translucent glow, for an energy cost such as U or V."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = (*rgb, 1)
    em.inputs['Strength'].default_value = strength
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    lw = nt.nodes.new('ShaderNodeLayerWeight')
    lw.inputs['Blend'].default_value = 0.35
    mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value, mr.inputs['From Max'].default_value = 0.0, 1.0
    mr.inputs['To Min'].default_value, mr.inputs['To Max'].default_value = alpha, 0.0
    mix = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(lw.outputs['Facing'], mr.inputs['Value'])
    nt.links.new(mr.outputs['Result'], mix.inputs[0])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs['Surface'])
    return mat


def mat(name, rgb, **kw):
    return bpy.data.materials.get(name) or principled(name, rgb, **kw)


# ------------------------------------------------------------------------------------------------
# Meshes and objects
# ------------------------------------------------------------------------------------------------
def _faces_of(verts):
    return {f for v in verts for f in v.link_faces}


def bm_sphere(bm, center, r, mat_index=0, seg=32, rings=16):
    res = bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=r,
                                    matrix=Matrix.Translation(center))
    for f in _faces_of(res['verts']):
        f.material_index, f.smooth = mat_index, True


def bm_cylinder(bm, p0, p1, r0, r1=None, mat_index=0, seg=24, caps=True):
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    rot = d.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    res = bmesh.ops.create_cone(bm, cap_ends=caps, cap_tris=False, segments=seg, radius1=r0,
                                radius2=r0 if r1 is None else r1, depth=d.length,
                                matrix=Matrix.Translation((p0 + p1) / 2) @ rot)
    for f in _faces_of(res['verts']):
        f.material_index, f.smooth = mat_index, True
    for f in _faces_of(res['verts']):
        if len(f.verts) > 4:                       # the caps stay flat
            f.smooth = False


def mesh_of(name, mats, build_fn):
    bm = bmesh.new()
    build_fn(bm)
    bm.normal_update()
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for m in mats:
        me.materials.append(m)
    return me


def obj(name, data, loc=(0, 0, 0), rot=(0, 0, 0), scale=1.0, coll=None):
    ob = bpy.data.objects.new(name, data)
    (coll or bpy.context.scene.collection).objects.link(ob)
    ob.location, ob.rotation_euler = loc, rot
    ob.scale = (scale, scale, scale) if isinstance(scale, (int, float)) else scale
    return ob


def arrow_mesh(name, m):
    """Unit arrow along +z centered on its origin, the shape of the films."""
    def f(bm):
        bm_cylinder(bm, (0, 0, -0.5), (0, 0, 0.05), 0.045, seg=20)
        bm_cylinder(bm, (0, 0, 0.05), (0, 0, 0.5), 0.185, 0.0, seg=32)
    return mesh_of(name, [m], f)


NEUTRAL_TIP, NEUTRAL_TAIL = (0.42, 0.45, 0.95), (0.08, 0.06, 0.38)


def sz_arrow(name, loc, direction, length=0.8, neutral=False):
    """A spin arrow colored continuously by its z component, mixing the up and down gradients, or
    with one neutral gradient if `neutral`, so that a spin in the plane reads as neither up nor
    down; `loc` is the center of the arrow. Taken from the sibling course."""
    d = Vector(direction).normalized()
    w = (d.z + 1) / 2
    mix = lambda a, b: tuple(w * x + (1 - w) * y for x, y in zip(a, b))
    if neutral:
        tip, tail, key = NEUTRAL_TIP, NEUTRAL_TAIL, 'szarrow_neutral'
    else:
        tip, tail = mix(UP_TIP, DOWN_TIP), mix(UP_TAIL, DOWN_TAIL)
        key = 'szarrow_%.3f' % d.z
    if bpy.data.meshes.get(key) is None:
        arrow_mesh(key, gradient_arrow_material(key, tip, tail))
    return obj(name, bpy.data.meshes[key], loc=loc, rot=d.to_track_quat('Z', 'Y').to_euler(), scale=length)


def spin_arrows():
    if bpy.data.meshes.get('arrow_up') is None:
        arrow_mesh('arrow_up', gradient_arrow_material('arrow_up', UP_TIP, UP_TAIL))
        arrow_mesh('arrow_down', gradient_arrow_material('arrow_down', DOWN_TIP, DOWN_TAIL))
    return bpy.data.meshes['arrow_up'], bpy.data.meshes['arrow_down']


def arrow(name, loc, direction, length=0.8):
    """A spin arrow of the series pointing along `direction` (a vector; up colors if its z >= 0)."""
    up, down = spin_arrows()
    d = Vector(direction).normalized()
    me = up if d.z >= -1e-9 else down
    rot = d.to_track_quat('Z', 'Y').to_euler()
    return obj(name, me, loc=loc, rot=rot, scale=length)


def site(name, loc, r=0.32, h=0.08):
    """A lattice site: a dark disc lying on the floor."""
    m = mat('site', SITE, rough=0.5, spec=0.3)
    return obj(name, mesh_of(name, [m], lambda bm: bm_cylinder(bm, (0, 0, 0), (0, 0, h), r, seg=48)), loc=loc)


def bond(name, p0, p1, r=0.035):
    m = mat('bond', BOND, rough=0.5, spec=0.3)
    return obj(name, mesh_of(name, [m], lambda bm: bm_cylinder(bm, p0, p1, r, seg=16)))


def ball(name, loc, r, rgb=ELECTRON, emit=0.15):
    m = mat('ball_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.3, emit=emit, spec=0.5)
    return obj(name, mesh_of(name, [m], lambda bm: bm_sphere(bm, Vector((0, 0, 0)), r)), loc=loc)


def column(name, loc, height, r=0.24, rgb=ELECTRON):
    m = mat('col_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.35, emit=0.1, spec=0.5)
    return obj(name, mesh_of(name, [m], lambda bm: bm_cylinder(bm, (0, 0, 0), (0, 0, height), r, seg=40)),
               loc=loc)


def ghost(name, rgb, alpha=0.25):
    """A translucent copy of a series color, for a ghost state (a partner, a forbidden state)."""
    m = bpy.data.materials.get(name)
    if m is None:
        m = principled(name, rgb, rough=0.4, emit=0.05, alpha=alpha, spec=0.3)
    return m


def ghost_arrow(name, loc, direction, length=0.8, alpha=0.25):
    """A spin arrow drawn as a translucent ghost in the color of its direction."""
    d = Vector(direction).normalized()
    rgb = UP_TIP if d.z >= -1e-9 else DOWN_TIP
    me = arrow_mesh(name, ghost('ghost_%s_%.2f' % ('up' if d.z >= -1e-9 else 'dn', alpha), rgb, alpha))
    return obj(name, me, loc=loc, rot=d.to_track_quat('Z', 'Y').to_euler(), scale=length)


def bm_rounded_box(bm, center, size, radius, mat_index=0):
    """A box of full sizes `size` with edges rounded by `radius` (a bevel on a cube)."""
    res = bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation(center) @
                                Matrix.Diagonal((*size, 1.0)))
    verts = res['verts']
    edges = list({e for v in verts for e in v.link_edges})
    bmesh.ops.bevel(bm, geom=verts + edges, offset=radius, segments=4, affect='EDGES', profile=0.5)
    for f in _faces_of([v for v in bm.verts]):
        f.material_index, f.smooth = mat_index, True


def tensor(name, loc, size=(0.7, 0.7, 0.7), rgb=None, radius=0.12):
    """A tensor as a rounded cube, in the teal of session 4 unless told otherwise."""
    rgb = ACCENT[4] if rgb is None else rgb
    m = mat('tensor_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.35, emit=0.08, spec=0.5)
    return obj(name, mesh_of(name, [m], lambda bm: bm_rounded_box(bm, Vector((0, 0, 0)), size, radius)), loc=loc)


def leg(name, p0, p1, r=0.05, rgb=BOND):
    """A tensor leg (an index) as a thin rod; a thicker `r` reads as a larger bond dimension."""
    m = mat('leg_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.5, spec=0.3)
    return obj(name, mesh_of(name, [m], lambda bm: bm_cylinder(bm, p0, p1, r, seg=16)))


def cut(name, loc, size=(0.04, 2.0, 2.0), rgb=None, session=4, alpha=0.35):
    """A cut through a system as a thin translucent slab in the session accent, normal along x."""
    rgb = ACCENT[session] if rgb is None else rgb
    m = ghost('cut_%d_%d_%d_%.2f' % (*(int(255 * c) for c in rgb), alpha), rgb, alpha)
    return obj(name, mesh_of(name, [m], lambda bm: bm_rounded_box(bm, Vector((0, 0, 0)), size, 0.015)), loc=loc)


def cup(name, loc, fill, r=0.32, h=0.9, rgb=ELECTRON):
    """An occupation as a glass cup of radius r and height h filled to the fraction `fill` (0 to 1)."""
    glass = ghost('cup_glass2', (0.62, 0.66, 0.76), 0.35)        # dark enough to read on white paper
    obj(name, mesh_of(name, [glass], lambda bm: bm_cylinder(bm, (0, 0, 0), (0, 0, h), r, seg=48, caps=False)),
        loc=loc)
    rim = mat('cup_rim', (0.30, 0.32, 0.38), rough=0.5, spec=0.3)  # a band at the top marks the full height
    obj(name + '_rim', mesh_of(name + '_rim', [rim], lambda bm: bm_cylinder(bm, (0, 0, h - 0.035), (0, 0, h),
                                                                            1.02 * r, seg=48, caps=False)), loc=loc)
    base = mat('site', SITE, rough=0.5, spec=0.3)
    obj(name + '_base', mesh_of(name + '_base', [base], lambda bm: bm_cylinder(bm, (0, 0, 0), (0, 0, 0.03), r,
                                                                             seg=48)), loc=loc)
    if fill > 1e-3:
        column(name + '_fill', (loc[0], loc[1], loc[2] + 0.03), fill * (h - 0.03), r=0.92 * r, rgb=rgb)


def axes_anchors(tag, origin, ends):
    """Anchors for axis arrows drawn in the overlay: <tag>O at the origin and <tag><key> at the end
    of each axis, from a dict like {'x': (x, y, z), 'y': (x, y, z)}."""
    anchor(tag + 'O', origin)
    for key, co in ends.items():
        anchor(tag + key, co)


def anchor(name, co):
    """A point that the TikZ overlay can refer to as (name)."""
    ANCHORS[PREFIX[0] + name] = Vector(co)


# ------------------------------------------------------------------------------------------------
# Curves, axes and level ladders
# ------------------------------------------------------------------------------------------------
def bm_sweep(bm, points, r, seg=16, mat_index=0, end_caps=True):
    """One continuous tube of radius r along a polyline, with rings carried by parallel transport
    and a sphere at each end, built in time linear in the number of points."""
    pts = [Vector(p) for k, p in enumerate(points) if k == 0 or (Vector(p) - Vector(points[k - 1])).length > 1e-9]
    if len(pts) < 2:
        return
    tans = []
    for k in range(len(pts)):
        a, b = pts[max(k - 1, 0)], pts[min(k + 1, len(pts) - 1)]
        tans.append((b - a).normalized())
    n = tans[0].orthogonal().normalized()
    rings = []
    for k, (p, t) in enumerate(zip(pts, tans)):
        if k > 0:
            q = tans[k - 1].rotation_difference(t)
            n = (q @ n).normalized()
        b = t.cross(n)
        rings.append([bm.verts.new(p + r * (math.cos(2 * math.pi * j / seg) * n + math.sin(2 * math.pi * j / seg) * b))
                      for j in range(seg)])
    for ra, rb in zip(rings[:-1], rings[1:]):
        for j in range(seg):
            f = bm.faces.new((ra[j], ra[(j + 1) % seg], rb[(j + 1) % seg], rb[j]))
            f.material_index, f.smooth = mat_index, True
    if end_caps:
        bm_sphere(bm, pts[0], r, mat_index, seg=seg, rings=seg // 2)
        bm_sphere(bm, pts[-1], r, mat_index, seg=seg, rings=seg // 2)


def tube(name, points, r, rgb, emit=0.1, alpha=1.0):
    """A thin tube through a list of points, for every curve of the notes."""
    key = 'tube_%d_%d_%d_%.2f' % (*(int(255 * c) for c in rgb), alpha)
    m = ghost(key, rgb, alpha) if alpha < 1.0 else mat(key, rgb, rough=0.4, emit=emit, spec=0.4)
    return obj(name, mesh_of(name, [m], lambda bm: bm_sweep(bm, points, r)))


def axis(name, p0, p1, r=0.025, head=0.18):
    """An axis as a thin rod in the bond grey with a small cone at its end; its labels are anchors."""
    p0, p1 = Vector(p0), Vector(p1)
    d = (p1 - p0).normalized()
    m = mat('bond', BOND, rough=0.5, spec=0.3)

    def f(bm):
        bm_cylinder(bm, p0, p1 - head * d, r, seg=16)
        bm_cylinder(bm, p1 - head * d, p1, 2.6 * r, 0.0, seg=24)
    return obj(name, mesh_of(name, [m], f))


def profile(name, xs, ys, depth, rgb, y0=0.0, alpha=1.0):
    """A thin slab whose top edge follows ys(xs) above the baseline y0, for a density of states or
    a filled region; it lies in the xz plane at depth 0 and is `depth` thick along y."""
    key = 'prof_%d_%d_%d_%.2f' % (*(int(255 * c) for c in rgb), alpha)
    m = ghost(key, rgb, alpha) if alpha < 1.0 else mat(key, rgb, rough=0.45, emit=0.05, spec=0.3)

    def f(bm):
        front, back = [], []
        bot_f = [bm.verts.new((x, -depth / 2, y0)) for x in xs]
        top_f = [bm.verts.new((x, -depth / 2, y)) for x, y in zip(xs, ys)]
        bot_b = [bm.verts.new((x, depth / 2, y0)) for x in xs]
        top_b = [bm.verts.new((x, depth / 2, y)) for x, y in zip(xs, ys)]
        n = len(xs)
        for i in range(n - 1):
            bm.faces.new((bot_f[i], bot_f[i + 1], top_f[i + 1], top_f[i]))
            bm.faces.new((bot_b[i + 1], bot_b[i], top_b[i], top_b[i + 1]))
            bm.faces.new((top_f[i], top_f[i + 1], top_b[i + 1], top_b[i]))
            bm.faces.new((bot_f[i + 1], bot_f[i], bot_b[i], bot_b[i + 1]))
        bm.faces.new((bot_f[0], top_f[0], top_b[0], bot_b[0]))
        bm.faces.new((top_f[-1], bot_f[-1], bot_b[-1], top_b[-1]))
    return obj(name, mesh_of(name, [m], f))


def surface(name, fn, xr, yr, nx, ny, rgb, alpha=1.0):
    """A smooth mesh of the height function z = fn(x, y) over the rectangle xr by yr."""
    key = 'surf_%d_%d_%d_%.2f' % (*(int(255 * c) for c in rgb), alpha)
    m = ghost(key, rgb, alpha) if alpha < 1.0 else mat(key, rgb, rough=0.4, emit=0.05, spec=0.4)

    def f(bm):
        vs = [[bm.verts.new((xr[0] + (xr[1] - xr[0]) * i / nx, yr[0] + (yr[1] - yr[0]) * j / ny,
                             fn(xr[0] + (xr[1] - xr[0]) * i / nx, yr[0] + (yr[1] - yr[0]) * j / ny)))
               for j in range(ny + 1)] for i in range(nx + 1)]
        for i in range(nx):
            for j in range(ny):
                fc = bm.faces.new((vs[i][j], vs[i + 1][j], vs[i + 1][j + 1], vs[i][j + 1]))
                fc.smooth = True
    return obj(name, mesh_of(name, [m], f))


def marker(name, loc, kind='ball', r=0.12, rgb=ELECTRON):
    """A point on a curve: a ball, a translucent ghost ball, or a cross of two short rods."""
    if kind == 'ball':
        return ball(name, loc, r, rgb)
    if kind == 'ghost':
        m = ghost('ghostball_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, 0.3)
        return obj(name, mesh_of(name, [m], lambda bm: bm_sphere(bm, Vector((0, 0, 0)), r)), loc=loc)
    m = mat('cross_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.4, emit=0.1)
    c, s = Vector(loc), r / math.sqrt(2)

    def f(bm):
        bm_cylinder(bm, c + Vector((-s, 0, -s)), c + Vector((s, 0, s)), 0.25 * r, seg=12)
        bm_cylinder(bm, c + Vector((-s, 0, s)), c + Vector((s, 0, -s)), 0.25 * r, seg=12)
    return obj(name, mesh_of(name, [m], f))


def level(name, x, y, z, length=0.8, r=0.05, rgb=SITE):
    """One level of a single-particle spectrum as a short rod along x centered on (x, y, z), in the
    site color, or in the accent or broken color for a level in a gap."""
    m = mat('level_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.4, emit=0.1, spec=0.4)
    ob = obj(name, mesh_of(name, [m], lambda bm: bm_cylinder(
        bm, (x - length / 2, y, z), (x + length / 2, y, z), r, seg=16)))
    ob.visible_shadow = False                  # a level floats at its energy, its shadow would read as a level
    return ob


SLAB = (0.86, 0.87, 0.90)


def slab(name, center, size, rgb=SLAB, radius=0.03, alpha=1.0):
    """A thin plate with rounded edges, for a basis state, a matrix entry or a unit cell."""
    key = 'slab_%d_%d_%d_%.2f' % (*(int(255 * c) for c in rgb), alpha)
    m = ghost(key, rgb, alpha) if alpha < 1.0 else mat(key, rgb, rough=0.6, spec=0.3)
    return obj(name, mesh_of(name, [m], lambda bm: bm_rounded_box(bm, Vector((0, 0, 0)), size, radius)),
               loc=center)


def rod(name, p0, p1, r=0.03, rgb=BOND):
    m = mat('rod_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.5, spec=0.3)
    return obj(name, mesh_of(name, [m], lambda bm: bm_cylinder(bm, p0, p1, r, seg=16)))


def ghost_ball(name, loc, r, rgb=ELECTRON, alpha=0.25):
    m = ghost('ghostball_%d_%d_%d_%.2f' % (*(int(255 * c) for c in rgb), alpha), rgb, alpha)
    return obj(name, mesh_of(name, [m], lambda bm: bm_sphere(bm, Vector((0, 0, 0)), r)), loc=loc)


def flow(name, points, r=0.03, rgb=(0.16, 0.20, 0.30), head=True):
    """A polyline as a tube with an arrowhead at its end, for a flow or a hop."""
    pts = [Vector(p) for p in points]
    m = mat('rod_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.5, spec=0.3)

    def f(bm):
        d = (pts[-1] - pts[-2]).normalized()
        body = pts[:-1] + [pts[-1] - 0.26 * d] if head else pts
        bm_sweep(bm, body, r, seg=12)
        if head:
            bm_cylinder(bm, pts[-1] - 0.28 * d, pts[-1], 3 * r, 0.0, seg=24)
    return obj(name, mesh_of(name, [m], f))


def ladder(tag, x, y, z0, energies, scale, length=0.8, r=0.03, filled=0, color=None, tol=1e-6):
    """A single-particle spectrum as a column of level rods centered on x at depth y, energy E at
    height z0 + scale * E. Degenerate levels sit side by side, the lowest `filled` levels carry an
    electron ball, and `color(E)` picks the rgb of a level (the site color by default)."""
    es = sorted(energies)
    groups = []
    for e in es:
        if groups and abs(e - groups[-1][0]) < tol:
            groups[-1].append(e)
        else:
            groups.append([e])
    k = 0
    for g, grp in enumerate(groups):
        n = len(grp)
        w = (length - 0.08 * (n - 1)) / n
        for j, e in enumerate(grp):
            xc = x - length / 2 + w / 2 + j * (w + 0.08)
            rgb = SITE if color is None else color(e)
            level(f'{tag}_l{g}_{j}', xc, y, z0 + scale * e, length=w, r=r, rgb=rgb)
            if k < filled:
                b = ball(f'{tag}_e{g}_{j}', (xc, y, z0 + scale * e + r + 0.07), 0.07)
                b.visible_shadow = False
            k += 1


def phasor(name, loc, angle, length=0.8, rgb=None, z_tilt=0.0):
    """A complex number as an arrow lying in the horizontal plane, centered on loc and pointing at
    `angle` (radians from +x), in the accent color: a phase, not a spin."""
    rgb = ACCENT_AQM if rgb is None else rgb
    key = 'phasor_%d_%d_%d' % tuple(int(255 * c) for c in rgb)
    if bpy.data.meshes.get(key) is None:
        arrow_mesh(key, mat(key, rgb, rough=0.4, emit=0.1, spec=0.4))
    d = Vector((math.cos(angle), math.sin(angle), z_tilt)).normalized()
    return obj(name, bpy.data.meshes[key], loc=loc, rot=d.to_track_quat('Z', 'Y').to_euler(), scale=length)


def vector_arrow(name, p0, p1, r=0.035, rgb=None, head=0.22):
    """A straight arrow from p0 to p1 with a cone at p1, for a bond vector or a phasor sum."""
    rgb = ACCENT_AQM if rgb is None else rgb
    p0, p1 = Vector(p0), Vector(p1)
    d = (p1 - p0).normalized()
    m = mat('rod_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.45, emit=0.08, spec=0.4)

    def f(bm):
        bm_cylinder(bm, p0, p1 - head * d, r, seg=16)
        bm_cylinder(bm, p1 - head * d, p1, 2.6 * r, 0.0, seg=24)
    return obj(name, mesh_of(name, [m], f))


def revolution(name, fn, R, rgb, loc=(0, 0, 0), nr=60, nth=96, r0=0.0, alpha=1.0):
    """A surface of revolution z = fn(r) for r0 <= r <= R around loc, for a cone, a paraboloid or a
    radial density."""
    key = 'rev_%d_%d_%d_%.2f' % (*(int(255 * c) for c in rgb), alpha)
    m = ghost(key, rgb, alpha) if alpha < 1.0 else mat(key, rgb, rough=0.4, emit=0.05, spec=0.4)

    def f(bm):
        rs = [r0 + (R - r0) * i / nr for i in range(nr + 1)]
        rings = [[bm.verts.new((r * math.cos(2 * math.pi * j / nth), r * math.sin(2 * math.pi * j / nth),
                                fn(r))) for j in range(nth)] for r in rs]
        for a, b in zip(rings[:-1], rings[1:]):
            for j in range(nth):
                fc = bm.faces.new((a[j], a[(j + 1) % nth], b[(j + 1) % nth], b[j]))
                fc.smooth = True
    return obj(name, mesh_of(name, [m], f), loc=loc)


def disc_surface(name, fn, R, rgb, nr=80, nth=160, alpha=1.0):
    """A surface z = fn(x, y) over the disc of radius R around the origin, on a polar mesh, for a
    droplet or any height field that is round by nature."""
    key = 'surf_%d_%d_%d_%.2f' % (*(int(255 * c) for c in rgb), alpha)
    m = ghost(key, rgb, alpha) if alpha < 1.0 else mat(key, rgb, rough=0.4, emit=0.05, spec=0.4)

    def f(bm):
        center = bm.verts.new((0, 0, fn(0, 0)))
        rings = []
        for i in range(1, nr + 1):
            r = R * i / nr
            rings.append([bm.verts.new((r * math.cos(2 * math.pi * j / nth), r * math.sin(2 * math.pi * j / nth),
                                        fn(r * math.cos(2 * math.pi * j / nth), r * math.sin(2 * math.pi * j / nth))))
                          for j in range(nth)])
        for j in range(nth):
            bm.faces.new((center, rings[0][j], rings[0][(j + 1) % nth])).smooth = True
        for a, b in zip(rings[:-1], rings[1:]):
            for j in range(nth):
                bm.faces.new((a[j], b[j], b[(j + 1) % nth], a[(j + 1) % nth])).smooth = True
    return obj(name, mesh_of(name, [m], f))


def dos(name, x0, y, z0, es, gs, ez, gx, depth=0.12, rgb=None, alpha=1.0):
    """A density of states as a thin slab standing next to a band: energy up (height z0 + ez * E),
    the density along +x from x0 (gx per unit of g)."""
    rgb = ACCENT_AQM if rgb is None else rgb
    ob = profile(name, [-ez * e for e in es], [gx * g for g in gs], depth, rgb, alpha=alpha)
    ob.rotation_euler = (0, math.pi / 2, 0)       # local x (minus the energy) becomes world z
    ob.location = (x0, y, z0)
    return ob


def honeycomb(fits, bond=1.0):
    """Sites of a honeycomb lattice with first-neighbor distance `bond`, kept where fits(x, y) is
    true: returns the A sites, the B sites and the first-neighbor bonds as pairs of points."""
    s3 = math.sqrt(3)
    a1, a2 = (s3 * bond, 0.0), (s3 * bond / 2, 1.5 * bond)
    A, B = [], []
    for i in range(-12, 13):
        for j in range(-12, 13):
            x, y = i * a1[0] + j * a2[0], i * a1[1] + j * a2[1]
            if fits(x, y):
                A.append((x, y))
            if fits(x, y + bond):
                B.append((x, y + bond))
    bonds = [(a, b) for a in A for b in B if abs(math.dist(a, b) - bond) < 1e-6]
    return A, B, bonds


def gradient_x_material(name, rgb0, rgb1, x0, x1, rough=0.5):
    """A material whose color goes from rgb0 at x = x0 to rgb1 at x = x1 in object coordinates."""
    m = principled(name, rgb0, rough=rough, spec=0.3)
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value, mr.inputs['From Max'].default_value = x0, x1
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.inputs['A'].default_value = (*rgb0, 1)
    mix.inputs['B'].default_value = (*rgb1, 1)
    nt.links.new(tc.outputs['Object'], sep.inputs[0])
    nt.links.new(sep.outputs['X'], mr.inputs['Value'])
    nt.links.new(mr.outputs['Result'], mix.inputs['Factor'])
    nt.links.new(mix.outputs['Result'], b.inputs['Base Color'])
    return m


# ------------------------------------------------------------------------------------------------
# Studio, camera and render
# ------------------------------------------------------------------------------------------------
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    ANCHORS.clear()


def studio(floor_size=80.0, shadows=True):
    """White world, a large soft key light, a fill, and a shadow catcher floor at z = 0; a flat view
    from above passes shadows=False, since a shadow seen from above reads as a halo."""
    sc = bpy.context.scene
    w = bpy.data.worlds.new('world')
    w.use_nodes = True
    bg = w.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (0.92, 0.93, 0.96, 1)
    bg.inputs['Strength'].default_value = 0.55
    sc.world = w
    key = bpy.data.lights.new('key', 'AREA')
    key.energy, key.size, key.shape = 2600.0, 6.0, 'SQUARE'
    k = obj('key', key, loc=(-8.0, -10.0, 14.0))
    k.rotation_euler = (Vector((0, 0, 0)) - k.location).to_track_quat('-Z', 'Y').to_euler()
    fill = bpy.data.lights.new('fill', 'AREA')
    fill.energy, fill.size = 700.0, 18.0
    f = obj('fill', fill, loc=(10.0, -12.0, 6.0))
    f.rotation_euler = (Vector((0, 0, 0)) - f.location).to_track_quat('-Z', 'Y').to_euler()
    m = principled('floor', (1, 1, 1), rough=0.9, spec=0.0)
    fl = obj('floor', mesh_of('floor', [m], lambda bm: bmesh.ops.create_grid(
        bm, x_segments=1, y_segments=1, size=floor_size / 2)))
    fl.is_shadow_catcher = True
    fl.hide_render = not shadows


def camera(target, elev=32.0, azim=0.0, ortho=12.0, aspect=2.4):
    """Orthographic camera looking at `target` from the front (-y), raised by `elev` degrees."""
    sc = bpy.context.scene
    cam = bpy.data.cameras.new('cam')
    cam.type, cam.ortho_scale = 'ORTHO', ortho
    cam.clip_end = 200.0
    e, a = math.radians(elev), math.radians(azim)
    d = Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)))
    c = obj('cam', cam, loc=Vector(target) + 40.0 * d)
    c.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    sc.camera = c
    sc.render.resolution_x = WIDTH
    sc.render.resolution_y = int(round(WIDTH / aspect))
    return c


def setup_render(pct, samples):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    if os.environ.get('FIGLIB_GPU'):              # FIGLIB_GPU=OPTIX (or CUDA) renders on the card
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = os.environ['FIGLIB_GPU']
        prefs.get_devices()
        for d in prefs.devices:
            d.use = d.type == prefs.compute_device_type
        sc.cycles.device = 'GPU'
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.render.film_transparent = True
    sc.render.resolution_percentage = pct
    sc.view_settings.view_transform = 'Standard'
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'


def write_anchors(path):
    """Anchors as TikZ coordinates in units of the image width, origin at the bottom left."""
    sc = bpy.context.scene
    bpy.context.view_layer.update()            # the camera's matrix_world is stale until this
    ratio = sc.render.resolution_y / sc.render.resolution_x
    with open(path, 'w') as fh:
        fh.write('%% written by figlib.py; x and y in units of the image width\n')
        for name, co in ANCHORS.items():
            p = world_to_camera_view(sc, sc.camera, co)
            fh.write('\\coordinate (%s) at (%.4f\\figw,%.4f\\figw);\n' % (name, p.x, p.y * ratio))


def _render(stem, mode):
    os.makedirs(OUT, exist_ok=True)
    pct, samples, suffix = (50, 48, '_still') if mode == 'still' else (100, SAMPLES, '')
    setup_render(pct, samples)
    write_anchors(os.path.join(OUT, stem + '_anchors.tex'))
    if mode == 'anchors':
        return
    sc = bpy.context.scene
    sc.render.filepath = os.path.join(OUT, stem + suffix + '.png')
    bpy.ops.render.render(write_still=True)
    print('wrote', sc.render.filepath)


def main_panels(name, panels):
    """Render each (panel, build) on its own into out/<name>_<panel>.png, with its anchors in
    out/<name>_<panel>_anchors.tex named <panel><anchor>, so that the overlay places them per scope.
    Panel names after the mode render only those panels, as in `final a`."""
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['still']
    mode, only = argv[0], argv[1:]
    for panel, build in panels:
        if only and panel not in only:
            continue
        reset()
        PREFIX[0] = panel
        build()
        _render(name + '_' + panel, mode)
    PREFIX[0] = ''


def main(build, name):
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['still']
    reset()
    build()
    _render(name, argv[0])
