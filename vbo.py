import numpy as np


class VBO:
    def __init__(self, ctx):
        self.vbos = {
            'color_cube': ColorCubeVBO(ctx),
            'color_plane': ColorPlaneVBO(ctx),
            'color_capsule': ColorCapsuleVBO(ctx),
        }

    def destroy(self):
        for vbo in self.vbos.values():
            vbo.destroy()


class BaseVBO:
    format = None
    attribs = None

    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = self.ctx.buffer(self.get_vertex_data().astype('f4').tobytes())

    def get_vertex_data(self):
        raise NotImplementedError

    def destroy(self):
        self.vbo.release()


class ColorPlaneVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '3f 3f'
        self.attribs = ['in_normal', 'in_position']

    def get_vertex_data(self):
        positions = [
            (-1, 0, -1), (1, 0, -1), (1, 0, 1), (-1, 0, 1)
        ]
        
        indices = [(0, 2, 1), (0, 3, 2)]
        normals = [(0, 1, 0)] * 6

        def get_data(verts, inds):
            return np.array([verts[i] for tri in inds for i in tri], dtype='f4')

        pos_data = get_data(positions, indices)
        norm_data = np.array(normals, dtype='f4')

        return np.hstack([norm_data, pos_data])


class ColorCubeVBO(BaseVBO):
    format = '3f 3f'
    attribs = ['in_normal', 'in_position']

    def get_vertex_data(self):
        vertices = np.array([
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
            (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1),
        ], dtype='f4')

        faces = [
            ((0, 2, 3), (0, 1, 2), (0, 0, 1)),
            ((1, 7, 2), (1, 6, 7), (1, 0, 0)),
            ((6, 5, 4), (4, 7, 6), (0, 0, -1)),
            ((3, 4, 5), (3, 5, 0), (-1, 0, 0)),
            ((3, 7, 4), (3, 2, 7), (0, 1, 0)),
            ((0, 6, 1), (0, 5, 6), (0, -1, 0)),
        ]

        data = []
        for tri_a, tri_b, normal in faces:
            for tri in (tri_a, tri_b):
                for idx in tri:
                    data.extend(normal)
                    data.extend(vertices[idx])
        return np.array(data, dtype='f4').reshape(-1, 6)


class ColorCapsuleVBO(BaseVBO):
    format = '3f 3f'
    attribs = ['in_normal', 'in_position']

    def get_vertex_data(self):
        """Generate capsule mesh data"""
        segments = 16
        rings = 8
        
        vertices = []
        normals = []
        indices = []
        vertex_index = 0
        
        # Top hemisphere
        for i in range(rings + 1):
            ring_angle = (i / rings) * (np.pi / 2)
            ring_radius = np.sin(ring_angle)
            ring_height = np.cos(ring_angle)
            
            for j in range(segments):
                angle = (j / segments) * 2 * np.pi
                x = ring_radius * np.cos(angle)
                z = ring_radius * np.sin(angle)
                y = ring_height + 1.0
                
                vertices.append((x, y, z))
                normals.append((x, ring_height, z))
                
                if i < rings:
                    if j < segments - 1:
                        idx0 = vertex_index
                        idx1 = vertex_index + 1
                        idx2 = vertex_index + segments
                        idx3 = vertex_index + segments + 1
                        
                        indices.append((idx0, idx2, idx1))
                        indices.append((idx1, idx2, idx3))
                    
                    vertex_index += 1
            
            vertex_index = len(vertices)
        
        # Bottom hemisphere
        top_vert_count = len(vertices)
        for i in range(rings + 1):
            ring_angle = (i / rings) * (np.pi / 2)
            ring_radius = np.sin(ring_angle)
            ring_height = -np.cos(ring_angle)
            
            for j in range(segments):
                angle = (j / segments) * 2 * np.pi
                x = ring_radius * np.cos(angle)
                z = ring_radius * np.sin(angle)
                y = ring_height - 1.0
                
                vertices.append((x, y, z))
                normals.append((x, -ring_height, z))
        
        # Middle cylinder
        for j in range(segments):
            idx0 = (rings) * segments + j
            idx1 = (rings) * segments + ((j + 1) % segments)
            idx2 = top_vert_count + j
            idx3 = top_vert_count + ((j + 1) % segments)
            
            indices.append((idx0, idx2, idx1))
            indices.append((idx1, idx2, idx3))
        
        data = []
        for tri in indices:
            for idx in tri:
                if idx < len(normals):
                    data.extend(normals[idx])
                if idx < len(vertices):
                    data.extend(vertices[idx])
        
        return np.array(data, dtype='f4').reshape(-1, 6) if data else np.array([], dtype='f4').reshape(0, 6)
