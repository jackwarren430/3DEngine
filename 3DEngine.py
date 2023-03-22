import pygame as pg
import numpy as np
from Object3D import *
from Camera import *
from Projection import *


class SoftwareRender:
	def __init__(self):
		pg.init()
		self.RES = self.WIDTH, self.HEIGHT = 1300, 700
		self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
		self.FPS = 60
		self.screen = pg.display.set_mode(self.RES)
		self.clock = pg.time.Clock()
		self.create_objects()


	def create_objects(self):
		self.camera = Camera(self, [-5, 5, -50])
		self.projection = Projection(self)
		self.object = self.get_object_from_file('./objects/lego_man.obj')

	def get_object_from_file(self, filename):
		vertex, faces = [], []
		with open(filename) as f:
			for line in f:
				if line.startswith('v '):
					vertex.append([float(i) for i in line.split()[1:]] + [1])
				elif line.startswith('f'):
					faces_ = line.split()[1:]
					faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
		return Object3D(self, vertex, faces)


	def draw(self):
		self.screen.fill(pg.Color('darkslategray'))
		self.object.draw()

	def run(self):
		while True:
			self.draw()
			#self.object.control()
			self.camera.control()
			#self.object.rotate_x(self.camera.rotation_speed / 2)
			for i in pg.event.get():
				if i.type == pg.QUIT: exit()
			pg.display.set_caption(str(self.clock.get_fps()))
			pg.display.flip()
			self.clock.tick(self.FPS)

if __name__ == '__main__':
	app = SoftwareRender()
	app.run()



