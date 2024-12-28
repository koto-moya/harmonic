import numpy as np
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore 
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtCore import Qt, Signal
import pyqtgraph as pg
from noise import snoise3
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import random
from PySide6.QtCore import QTimer, QTime



class Nyx(gl.GLViewWidget):
    clicked = Signal()

    # Constants for Readability
    TIME_INCREMENT = 0.04
    COLORMAP_SPEED = 0.07
    TRANSITION_SPEED = 0.01
    BASE_RADIUS = 7
    TUBE_RADIUS = 4
    BASE_NOISE_INTENSITY = 1.2
    DEFAULT_NUM_POINTS = 30
    MIN_POINTS = 12
    MAX_POINTS = 30
    INACTIVITY_INTERVAL_MS = 100  # 1 second

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(50, 50)
        self.setFixedSize(50, 50)

        self.setup_surface_format()
        self.setup_initial_parameters()
        self.setup_mesh_and_colormap()
        self.setup_timers()
        self.setMouseTracking(True)
        self.mouse_disabled = False
        self.last_mouse_move = QTime.currentTime()

    def setup_surface_format(self):
        format = QSurfaceFormat()
        format.setSamples(0)
        QSurfaceFormat.setDefaultFormat(format)
        self.setBackgroundColor("#2d2b2b")
        self.setCameraPosition(distance=20)

    def setup_initial_parameters(self):
        # Visual Parameters
        self.idle_time = 120000
        self.num_points = self.DEFAULT_NUM_POINTS
        self.radius = self.BASE_RADIUS
        self.tube_radius = self.TUBE_RADIUS
        self.noise_intensity = self.BASE_NOISE_INTENSITY
        self.noise_scale = 0.2

        # Animation/Timing
        self.time = 0.0
        self.time_increment = self.TIME_INCREMENT
        self.colormap_time = 0
        self.colormap_speed = self.COLORMAP_SPEED

        # Transition Parameters
        self.transition_phase = 0
        self.transition_speed = self.TRANSITION_SPEED
        self.transition_active = False
        self.reverse_transition = False

        # Point Reduction
        self.vortex_center = 1
        self.points_decrease_rate = 1
        self.min_points = self.MIN_POINTS
        self.max_points = self.MAX_POINTS

    def setup_mesh_and_colormap(self):
        phi = np.linspace(0, 2 * np.pi, self.num_points, endpoint=False)
        theta = np.linspace(0, np.pi, self.num_points)
        self.phi, self.theta = np.meshgrid(phi, theta)

        self.spike_mesh = gl.GLMeshItem(computeNormals=False)
        self.spike_mesh.setGLOptions('additive')
        self.addItem(self.spike_mesh)
        self.faces = self.generate_faces(self.num_points)

        original_cmap = cm.get_cmap('inferno')
        self.plasma_colormap = self.truncate_colormap(original_cmap, 0.0, 0.4)

    def setup_timers(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateData)
        self.timer.start(8)

        self.reduce_intensity_timer = QTimer()
        self.reduce_intensity_timer.start(100)

        if not self.transition_active:
            self.inactivity_timer = QTimer(self)
            self.inactivity_timer.timeout.connect(self.reduce_points_due_to_inactivity)
            self.inactivity_timer.start(self.INACTIVITY_INTERVAL_MS)
    def mousePressEvent(self, event):
        if not self.mouse_disabled:
            self.activate_transition()
            self.adjustNoise(event)
            super().mousePressEvent(event)
            self.clicked.emit()

    def activate_transition(self):
        self.num_points = 15
        self.noise_intensity = self.BASE_NOISE_INTENSITY * 10
        self.radius = 3
        self.transition_active = True
        self.reverse_transition = False
        self.mouse_disabled = True
        self.update_colormap(0.6)

    def wheelEvent(self, event):
        # Disable wheel interaction
        event.ignore()

    def adjustNoise(self, event):
        # Adjust noise based on mouse proximity to center
        distance_from_center = np.linalg.norm(
            np.array([event.position().x(), event.position().y()]) -
            np.array([self.width() / 2, self.height() / 2])
        )
        normalized_distance = distance_from_center / np.sqrt(
            (self.width() / 2) ** 2 + (self.height() / 2) ** 2
        )
        self.noise_intensity = self.BASE_NOISE_INTENSITY + 2 * np.clip(1.0 - normalized_distance, 0.0, 1.0)

    def mouseReleaseEvent(self, event):
        self.adjustNoise(event)
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        self.reset_points()
        self.last_mouse_move = QTime.currentTime()
        self.adjustNoise(event)
        super().mouseMoveEvent(event)

    def reset_points(self):
        if self.num_points < self.max_points:
            self.num_points = min(self.num_points + self.points_decrease_rate, self.max_points)
            self.faces = self.generate_faces(self.num_points)
            self.update_colormap(0.6)

    def update_colormap(self, max_val):
        original_cmap = cm.get_cmap('inferno')
        self.plasma_colormap = self.truncate_colormap(original_cmap, 0.0, max_val)

    def updateData(self):
        self.time += self.time_increment
        x, y, z = self.generate_dynamic_radius()
        vertices = np.column_stack((x.flatten(), y.flatten(), z.flatten()))
        colors = self.generate_colors(vertices)
        self.spike_mesh.setMeshData(vertexes=vertices, faces=self.faces, vertexColors=colors)

    def generate_dynamic_radius(self):
        sphere_x, sphere_y, sphere_z = self.calculate_sphere()
        torus_x, torus_y, torus_z = self.calculate_torus()

        # Apply transition between sphere and torus
        x, y, z = self.apply_transition(sphere_x, sphere_y, sphere_z, torus_x, torus_y, torus_z)

        noise = self.calculate_noise(x, y, z)
        return x, y, z + self.noise_intensity * noise

    def calculate_sphere(self):
        x = self.BASE_RADIUS * np.sin(self.theta) * np.cos(self.phi)
        y = self.BASE_RADIUS * np.sin(self.theta) * np.sin(self.phi)
        z = self.BASE_RADIUS * np.cos(self.theta)
        return x, y, z

    def calculate_torus(self):
        x = (self.radius + self.tube_radius * np.cos(self.theta)) * np.cos(self.phi)
        y = (self.radius + self.tube_radius * np.cos(self.theta)) * np.sin(self.phi)
        z = self.tube_radius * np.sin(self.theta)
        return x, y, z

    def apply_transition(self, sphere_x, sphere_y, sphere_z, torus_x, torus_y, torus_z):
        if self.transition_active:
            self.noise_intensity = self.BASE_NOISE_INTENSITY * 2
            self.transition_phase += self.transition_speed * (1 if not self.reverse_transition else -1)
            self.transition_phase = np.clip(self.transition_phase, 0, 1)
            
            if self.transition_phase in [0, 1]:
                self.transition_active = False

        factor = 0.5 * (1 - np.cos(np.pi * self.transition_phase))
        x = (1 - factor) * sphere_x + factor * torus_x
        y = (1 - factor) * sphere_y + factor * torus_y
        z = (1 - factor) * sphere_z + factor * torus_z
        return x, y, z

    def calculate_noise(self, x, y, z):
        noise = np.zeros_like(self.theta)
        for i, j in np.ndindex(self.theta.shape):
            noise[i, j] = snoise3(
                x[i, j] * self.noise_scale,
                y[i, j] * self.noise_scale,
                z[i, j] * self.noise_scale + self.time,
                octaves=1,
                persistence=0.5,
                lacunarity=1.5
            )
        return noise

    def generate_colors(self, vertices):
        self.colormap_time += self.colormap_speed
        r = np.linalg.norm(vertices, axis=1)
        theta = np.arccos(vertices[:, 2] / r)  # Polar angle
        phi = np.arctan2(vertices[:, 1], vertices[:, 0])  # Azimuthal angle
        
        colors = np.zeros((len(vertices), 4))
        
        # Calculate vortex and swirl intensity for each vertex
        for i, (t, p) in enumerate(zip(theta, phi)):
            vortex_intensity = self.calculate_vortex_intensity(t, p)
            swirl_factor = self.apply_swirl_pattern(t, p)
            
            # Combine intensities
            final_intensity = vortex_intensity * swirl_factor
            colors[i] = self.plasma_colormap(final_intensity % 1)
        
        return colors

    def calculate_vortex_intensity(self, theta, phi):
        vortex_centers = [(np.pi / self.vortex_center, 0), (2 * np.pi / 3, np.pi / 2)]
        vortex_radius = 1
        intensity = 0
        
        for v_t, v_p in vortex_centers:
            dist = np.sqrt((theta - v_t) ** 2 + (phi - v_p) ** 2)
            intensity += np.exp(-dist ** 2 / (2 * vortex_radius ** 2))  # Gaussian decay
        
        return intensity

    def apply_swirl_pattern(self, theta, phi):
        return (
            np.sin(3 * phi + self.colormap_time + 5 * theta) * 0.5 +
            np.cos(phi + self.colormap_time + 2 * theta) +
            0.5 - np.cos(phi + self.colormap_time + 2)
        )

    def truncate_colormap(self, cmap, min_val=0.0, max_val=1.0, n=256):
        new_cmap = cmap(np.linspace(min_val, max_val, n))
        return ListedColormap(new_cmap)

    def update_colormap(self, max_val):
        original_cmap = cm.get_cmap('inferno')
        self.plasma_colormap = self.truncate_colormap(original_cmap, 0.0, max_val)


    def scale_animation(self, scaling_factor):
        self.time_increment = self.TIME_INCREMENT * scaling_factor/3
        self.noise_intensity = self.BASE_NOISE_INTENSITY / scaling_factor
        self.transition_speed = self.TRANSITION_SPEED * scaling_factor

    def adjust_colormap_for_inactivity(self, scaling_factor):
        new_max_val = 0.5 - 0.4 * scaling_factor  # Scale from 0.5 to 0.1
        new_max_val = max(0.1, new_max_val)  # Ensure it doesn't go below 0.1
        self.update_colormap(new_max_val)


    def generate_faces(self, num_points):
        faces = np.zeros(((num_points - 1) * num_points * 2, 3), dtype=int)
        idx = 0

        for i in range(num_points - 1):
            for j in range(num_points):
                idx_next = (j + 1) % num_points
                idx_down = (i + 1) * num_points + j
                idx_down_next = (i + 1) * num_points + idx_next

                # Upper triangle
                faces[idx] = [i * num_points + j, i * num_points + idx_next, idx_down]
                idx += 1

                # Lower triangle
                faces[idx] = [i * num_points + idx_next, idx_down_next, idx_down]
                idx += 1

        return faces

    def mousePressEvent(self, event):
        if not self.mouse_disabled and not self.transition_active:
            self.activate_transition()
            super().mousePressEvent(event)
            self.clicked.emit()

    def reset_points(self):
        if self.num_points < self.max_points:
            self.num_points = min(self.num_points + self.points_decrease_rate, self.max_points)
            self.faces = self.generate_faces(self.num_points)
            self.update_colormap(0.6)

    def reduce_points_due_to_inactivity(self):
        self.elapsed_time = self.last_mouse_move.msecsTo(QTime.currentTime())
        
        if self.elapsed_time > self.idle_time:  # 10 seconds of inactivity
            if self.num_points > self.min_points:
                self.num_points = max(self.num_points - self.points_decrease_rate, self.min_points)
                self.faces = self.generate_faces(self.num_points)
                
                scaling_factor = self.num_points / self.max_points
                self.scale_animation(scaling_factor)
                self.adjust_colormap_for_inactivity(scaling_factor)
                self.updateData()

    def activate_transition(self):
        self.num_points = 15
        self.noise_intensity = self.BASE_NOISE_INTENSITY * 10
        self.radius = 3
        self.transition_active = True
        self.reverse_transition = False
        self.mouse_disabled = True
        self.update_colormap(0.6)

        # Stop inactivity timer during transition
        self.inactivity_timer.stop()
        self.timer.start(8)

    def resetToSphere(self):
        self.reverse_transition = True
        self.transition_active = True
        self.mouse_disabled = False
        self.num_points = self.DEFAULT_NUM_POINTS

        # Restart inactivity timer when transition ends
        self.last_mouse_move = QTime.currentTime()
        self.inactivity_timer.start(self.INACTIVITY_INTERVAL_MS)


    def resizeEvent(self, event):
        self.faces = self.generate_faces(self.num_points)
        new_size = event.size()
        self.resize(new_size.width(), new_size.height())
        super().resizeEvent(event)

