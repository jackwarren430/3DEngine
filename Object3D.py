import pygame as pg
from MatrixFunctions import *
from numba import njit

@njit(fastmath=True)
def any_func(arr, a, b):
	return np.any((arr == a) | (arr == b))


class Object3D:
	def __init__(self, render, vertexes, faces):
		self.render = render
		self.vertexes = np.array([np.array(v) for v in vertexes])
		self.faces = np.array([np.array(f) for f in faces])
		
		self.font = pg.font.SysFont('Arial', 20, bold=True)
		self.color_faces = [(pg.Color('orange'), face) for face in self.faces]
		self.movemen_flag, self.draw_vertexes = True, False
		self.label = ''
		self.moving_speed = 0.0001

	def draw(self):
		self.screen_projection()

	def screen_projection(self):
		vertexes = self.vertexes @ self.render.camera.camera_matrix() # transforming vectors into "camera space"
		vertexes = vertexes @ self.render.projection.projection_matrix # transforming vectors into "clop space""
		vertexes /= vertexes[:, -1].reshape(-1, 1) # "normalizing"
		vertexes[(vertexes > 2) | (vertexes < -2)] = 0
		vertexes = vertexes @ self.render.projection.to_screen_matrix # screen res
		vertexes = vertexes[:, :2]

		for index, color_face in enumerate(self.color_faces):
			color, face = color_face
			polygon = vertexes[face]
			if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
				pg.draw.polygon(self.render.screen, color, polygon, 1)
				if self.label:
					text = self.font.render(self.label[index], True, pg.Color('white'))
					self.render.screen.blit(text, polygon[-1])

		if self.draw_vertexes:
			for vertex in vertexes:
				if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
					pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 2)

	def control(self):
		pos = self.vertexes[0]
		key = pg.key.get_pressed()
		if key[pg.K_a]:
			pos[1] += self.moving_speed
			self.translate(pos[:-1])
		if key[pg.K_d]:
			pos[1] -= self.moving_speed
			self.translate(pos[:-1])
		if key[pg.K_w]:
			self.position += self.forward * self.moving_speed
		if key[pg.K_s]:
			self.position -= self.forward * self.moving_speed
		if key[pg.K_q]:
			self.position += self.up * self.moving_speed
		if key[pg.K_e]:
			self.position -= self.up * self.moving_speed

		if key[pg.K_LEFT]:
			self.camera_yaw(-self.rotation_speed)
		if key[pg.K_RIGHT]:
			self.camera_yaw(self.rotation_speed)
		if key[pg.K_UP]:
			self.camera_pitch(-self.rotation_speed)
		if key[pg.K_DOWN]:
			self.camera_pitch(self.rotation_speed)


	def translate(self, pos):
		self.vertexes = self.vertexes @ translate(pos)

	def scale(self, scale_to):
		self.vertexes = self.vertexes @ scale(scale_to)

	def rotate_x(self, angle):
		self.vertexes = self.vertexes @ rotate_x(angle)

	def rotate_y(self, angle):
		self.vertexes = self.vertexes @ rotate_y(angle)

	def rotate_z(self, angle):
		self.vertexes = self.vertexes @ rotate_z(angle)


class Axes(Object3D):
	def __init__(self, render):
		super().__init__(render)
		self.vertexes = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
		self.faces = np.array([(0, 1), (0, 2), (0, 3)])
		self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
		self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
		self.draw_vertexes = False
		self.label = 'xyz'



