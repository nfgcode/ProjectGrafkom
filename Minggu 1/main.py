import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Definisi titik-titik kubus
vertices = [
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
    [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]  # Ditambahkan titik ke-8
]

edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

def draw_cube():
    glBegin(GL_QUADS)
    glColor3f(0, 1, 0)  # Hijau
    faces = [
        (0, 1, 2, 3), (4, 5, 6, 7),
        (0, 1, 5, 4), (2, 3, 7, 6),
        (0, 3, 7, 4), (1, 2, 6, 5)
    ]
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()
    
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_mirror(is_concave):
    glColor3f(0.6, 0.6, 0.8)  # Biru muda
    glBegin(GL_QUADS)
    
    # Buat grid melengkung untuk cermin
    grid_size = 10
    for i in range(grid_size):
        for j in range(grid_size):
            # Koordinat dasar
            x1 = 2.5  # Posisi cermin di sumbu x
            y_base = -1 + i * 0.2  # Koordinat y dasar
            z1 = -1 + j * 0.2  # Koordinat z

            # Hitung lengkungan berdasarkan posisi z
            if is_concave:
                # Cermin cekung: kurva ke arah negatif y
                curvature = 0.1 * (z1 - 0) ** 2  # Parabola ke arah negatif y
                y1 = y_base - curvature
            else:
                # Cermin cembung: kurva ke arah positif y
                curvature = 0.1 * (z1 - 0) ** 2  # Parabola ke arah positif y
                y1 = y_base + curvature

            # Titik-titik untuk membuat quad
            x2, y2, z2 = x1, y1 + 0.2, z1
            x3, y3, z3 = x1, y1 + 0.2, z1 + 0.2
            x4, y4, z4 = x1, y1, z1 + 0.2

            # Gambar quad
            glVertex3f(x1, y1, z1)
            glVertex3f(x2, y2, z2)
            glVertex3f(x3, y3, z3)
            glVertex3f(x4, y4, z4)
    
    glEnd()
    
def main():
    pygame.init()
    screen = (800, 600)
    pygame.display.set_mode(screen, DOUBLEBUF | OPENGL)
    gluPerspective(45, (screen[0] / screen[1]), 0.1, 50.0)
    glTranslatef(0, 0, -5)
    
    scale = 1.0
    cube_x = 0.0
    cube_z = -2.0  # Posisi awal kubus
    rotate_x, rotate_y = 0, 0
    is_concave = True  # Cermin awalnya cekung

    keys = {K_LEFT: False, K_RIGHT: False, K_UP: False, K_DOWN: False, K_w: False, K_s: False}
    
    running = True
    while running:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll ke atas
                    scale += 0.1
                elif event.button == 5:  # Scroll ke bawah
                    scale = max(0.1, scale - 0.1)
            elif event.type == pygame.KEYDOWN:
                if event.key in keys:
                    keys[event.key] = True
                if event.key == K_f:  # Flip cermin
                    is_concave = not is_concave
            elif event.type == pygame.KEYUP:
                if event.key in keys:
                    keys[event.key] = False
        
        # Rotasi dengan panah keyboard
        if keys[K_LEFT]:
            rotate_y -= 2
        if keys[K_RIGHT]:
            rotate_y += 2
        if keys[K_UP]:
            rotate_x -= 2
        if keys[K_DOWN]:
            rotate_x += 2
        
        # Geser kubus mendekati atau menjauhi cermin dengan batas
        if keys[K_w] and cube_x < 1.5:  # Batas dekat cermin
            cube_x += 0.05
        if keys[K_s] and cube_x > -1.5:  # Batas jauh dari cermin
            cube_x -= 0.05

        glLoadIdentity()
        gluPerspective(45, (screen[0] / screen[1]), 0.1, 50.0)
        glTranslatef(0, 0, -5)
        glScalef(scale, scale, scale)
        glRotatef(rotate_x, 1, 0, 0)
        glRotatef(rotate_y, 0, 1, 0)
        
        # Gambar Kubus
        glPushMatrix()
        glTranslatef(cube_x, 0, cube_z)
        draw_cube()
        glPopMatrix()
        
        # Gambar Cermin di kanan
        draw_mirror(is_concave)

        pygame.display.flip()
        pygame.time.wait(10)
    
    pygame.quit()

if __name__ == "__main__":
    main()
