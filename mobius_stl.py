import numpy as np
import math
from manim import *
from stl import mesh # numpy-stl
import matplotlib.tri as mtri

DEG = np.pi / 180.0

# ---------------- https://raw.githubusercontent.com/3b1b/videos/refs/heads/master/_2024/inscribed_rect/helpers.py ----------------
# # Regular mobius strip
# def alt_mobius_strip_func(u, v):
#     phi = TAU * v
#     vect = rotate_vector(RIGHT, phi / 2, axis=UP)
#     vect = rotate_vector(vect, phi, axis=OUT)
#     ref_point = np.array([np.cos(phi), np.sin(phi), 0])
#     return ref_point + 0.7 * (u - 0.5) * vect

def stereo_project_point(point, axis=0, r=1, max_norm=10000):
    point = np.divide(point * r, point[axis] + r)
    point[axis] = 0
    norm = np.linalg.norm(point)
    if norm > max_norm:
        point *= max_norm / norm
    return point

# Fancy mobius strip
def sudanese_band_func(u, v):
    eta = PI * u
    phi = TAU * v
    z1 = math.sin(eta) * np.exp(complex(0, phi))
    z2 = math.cos(eta) * np.exp(complex(0, phi / 2))
    r4_point = np.array([z1.real, z1.imag, z2.real, z2.imag])
    r4_point[:3] = rotate_vector(r4_point[:3], PI / 3, axis=[1, 1, 1])
    result = stereo_project_point(r4_point, axis=0)[1:]
    result = rotate_vector(result, 60 * DEG, OUT)
    result = rotate_vector(result, 90 * DEG, RIGHT)
    return result
# ---------------------------------------------------------------------------------------------------------------------------------


# Previewing the surface with matplotlib
# def preview_surf(us, vs):
#     xs = np.zeros_like(us)
#     ys = np.zeros_like(us)
#     zs = np.zeros_like(us)

#     for i in range(0, us.shape[0]):
#         for j in range(0, us.shape[1]):
#             coords = sudanese_band_func(us[i][j], vs[i][j])
#             xs[i][j] = coords[0]
#             ys[i][j] = coords[1]
#             zs[i][j] = coords[2]

#     return xs, ys, zs


# # ------------------- https://www.geeksforgeeks.org/rendering-3d-surfaces-using-parametric-equations-in-python/ -------------------

# import matplotlib.pyplot as plt

# # Create a grid of the u and v values
# u = np.linspace(0, 1, 100)
# v = np.linspace(0, 1, 100)
# u, v = np.meshgrid(u, v)

# x, y, z = preview_surf(u, v)
# # Plot the torus
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(x, y, z, color='c', edgecolor='k', alpha=0.6)
# # Labels and title
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.set_title('3D Parametric Surface: Torus')
# # Show the plot
# plt.show()
# # ---------------------------------------------------------------------------------------------------------------------------------


def surf(us, vs):
    xs = np.zeros(us.shape[0])
    ys = np.zeros(us.shape[0])
    zs = np.zeros(us.shape[0])

    for i in range(0, us.shape[0]):
        coords = sudanese_band_func(us[i], vs[i])
        xs[i] = coords[0]
        ys[i] = coords[1]
        zs[i] = coords[2]

    return xs, ys, zs

# ------- https://stackoverflow.com/questions/56545819/is-there-a-way-to-export-an-stl-file-from-a-matplotlib-surface-plot --------
# Create stl

export_resolution = 250 # You can change the mesh resolution here :)

u = np.linspace(0, 1, export_resolution)
v = np.linspace(0, 1, export_resolution)
u, v = np.meshgrid(u, v)

u = u.flatten()
v = v.flatten()

print('Calculating points on mobius strip...')
x, y, z = surf(u, v)

print('Triangulating mesh...')
triang=mtri.Triangulation(u, v)
data = np.zeros(len(triang.triangles), dtype=mesh.Mesh.dtype)
mobius_mesh = mesh.Mesh(data, remove_empty_areas=False)
mobius_mesh.x[:] = x[triang.triangles]
mobius_mesh.y[:] = y[triang.triangles]
mobius_mesh.z[:] = z[triang.triangles]

print('Exporting mesh...')
mobius_mesh.save('mobius_surface.stl') # this stl needs to be edited with something like blender to make it printable (it is just the surface like this)
print('Done!')
# ---------------------------------------------------------------------------------------------------------------------------------
