import pygame as pg
from MatrixFunctions import *

class Camera:
	def __init__(self, render, position):
		self.render = render
		self.position = np.array([*position, 1.0])
		self.forward = np.array([0, 0, 1, 1])
		self.up = np.array([0, 1, 0, 1])
		self.right = np.array([1, 0, 0, 1])
		self.h_fov = math.pi / 3
		self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
		self.near_plane = 0.1
		self.far_plane = 100
		self.moving_speed = 0.04
		self.rotation_speed = 0.005
		self.font = pg.font.SysFont('Arial', 20, bold=True)

	def control(self):
		key = pg.key.get_pressed()
		if key[pg.K_a]:
			self.position -= self.right * self.moving_speed
		if key[pg.K_d]:
			self.position += self.right * self.moving_speed
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

	def camera_yaw(self, angle):
		rotate = rotate_y(angle)
		self.forward = self.forward @ rotate
		self.right = self.right @ rotate
		self.up = self.up @ rotate

	def camera_pitch(self, angle):
		rotate = rotate_x(angle)
		
		rx, ry, rz, rw = self.right
		fx, fy, fz, fw = self.forward
		ux, uy, uz, uw = self.up
		mat = np.array([
			[rx, ux, fx, 0],
			[ry, uy, fy, 0],
			[rz, uz, fz, 0],
			[rw, uw, fw, 1]
		])
		
		#inverse = np.linalg.inv(mat)

		mat = mat @ rotate
		
		
		#self.right = [mat[0][0], mat[1][0], mat[2][0], mat[3][0]]
		#self.forward = [mat[0][1], mat[1][1], mat[2][1], mat[3][1]]
		#self.up = [mat[0][1], mat[1][1], mat[2][1], mat[3][2]]

		self.forward = self.forward @ rotate
		self.right = self.right @ rotate
		self.up = self.up @ rotate	

		#inverse = mat.transpose()
		
		#r1 = np.append(inverse[0], [0]),
		#r2 = np.append(inverse[1], [0]),
		#r3 = np.append(inverse[2], [0]),
		#r4 = np.array([0, 0, 0, 1])
		
		#inverse = np.array([r1, r2, r3, r4])
		#print(inverse)
		#self.forward = inverse @ self.forward
		#self.right = inverse @ self.right
		#self.up = inverse @ self.up

	def translate_matrix(self):
		x, y, z, w = self.position
		return np.array([
			[1, 0, 0, 0],
			[0, 1, 0, 0],
			[0, 0, 1, 0],
			[-x, -y, -z, 1]
		])

	def rotate_matrix(self):
		rx, ry, rz, w = self.right
		fx, fy, fz, w = self.forward
		ux, uy, uz, w = self.up
		return np.array([
			[rx, ux, fx, 0],
			[ry, uy, fy, 0],
			[rz, uz, fz, 0],
			[0, 0, 0, 1]
		])



	def camera_matrix(self):

		up_text = self.font.render(f"up: {self.up}", True, (255, 255, 255))
		forward_text = self.font.render(f"forward: {self.forward}", True, (255, 255, 255))
		right_text = self.font.render(f"right: {self.right}", True, (255, 255, 255))

		self.render.screen.blit(up_text, (10, 10))
		self.render.screen.blit(forward_text, (10, 30))
		self.render.screen.blit(right_text, (10, 50))


		return self.translate_matrix() @ self.rotate_matrix()

