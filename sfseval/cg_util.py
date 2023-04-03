""" 3D object utility
define the depth object for SFS task
@Author: Hang Zhou
"""

import numpy as np
import numpy.ma as ma
from sfseval.matlab_agent import get_eng

class ThreeDObject():
    """
    3d object for processing the depth_map output

    initialize using from_data
    """
    def __init__(self) -> None:
        self.depth=None
        self.normal=None
        self.K=None
        self.mask=None
        self.d_ma=None
        self.n_ma=None

    @classmethod
    def from_data(cls, depth:np.array, mask:np.array, normal=None, K=None) -> None:
        """ build object from data
        depth: should be a 2d np.array float64
        mask: should be a np.array convertable to bool array, 0 will be False, others are True
              since it's optional in logic, it can be all True
        normal: should be a 2d np.array float64

        the depth image are normalized to 0-1
        """
        new_obj=cls()
        new_obj.depth=depth
        new_obj.K=K
        new_obj.mask=np.invert(ma.make_mask(mask))
        tmask=np.invert(ma.make_mask(mask))
        new_obj.d_ma = ma.array(new_obj.depth, mask=new_obj.mask)
        if normal is None:
            new_obj.normal=new_obj.get_surface_normal_by_depth(depth,K) 
        else:
            new_obj.normal=normal 
        new_obj.n_ma = ma.array(new_obj.normal, mask=np.repeat(tmask[:,:,np.newaxis],3,axis=2))
        ma.set_fill_value(new_obj.d_ma,0)
        ma.set_fill_value(new_obj.n_ma,0)

        new_obj.d_ma=cls.normalize(new_obj.d_ma)
        return new_obj

    @staticmethod
    def normalize(img:np.ma):
        if img is None:
            return
        num_max=ma.max(img)
        num_min=ma.min(img)
        img-=num_min
        img/=num_max
        return img
        

    def get_depth(self):
        """get the depth in numpy.ma format, with the mask property applied"""
        return self.d_ma

    def get_normal(self):
       """get the normal in numpy.ma format, with the mask property applied""" 
       return self.n_ma
    
    def show_depth(self):
        eng=get_eng()
        eng.figure()
        eng.imshow(self.d_ma.filled(),[])

    def show_normal(self):
        eng=get_eng()
        eng.figure()
        eng.imshow(self.n_ma.filled(),[])

    @staticmethod
    def get_surface_normal_by_depth(depth, K=None):
        """
        depth: (h, w) of float, the unit of depth is meter
        K: (3, 3) of float, the depth camere's intrinsic
        """
        K = [[1, 0], [0, 1]] if K is None else K
        fx, fy = K[0][0], K[1][1]

        dz_dv, dz_du = np.gradient(depth)  # u, v mean the pixel coordinate in the image
        # u*depth = fx*x + cx --> du/dx = fx / depth
        du_dx = fx / depth  # x is xyz of camera coordinate
        dv_dy = fy / depth

        dz_dx = dz_du * du_dx
        dz_dy = dz_dv * dv_dy
        # cross-product (1,0,dz_dx)X(0,1,dz_dy) = (-dz_dx, -dz_dy, 1)
        normal_cross = np.dstack((-dz_dx, -dz_dy, np.ones_like(depth)))
        # normalize to unit vector
        normal_unit = normal_cross / np.linalg.norm(normal_cross, axis=2, keepdims=True)
        # set default normal to [0, 0, 1]
        normal_unit[~np.isfinite(normal_unit).all(2)] = [0, 0, 1]
        return normal_unit

    @staticmethod
    def get_normal_map_by_point_cloud(depth, K):
        height, width = depth.shape

        def normalization(data):
            mo_chang = np.sqrt(
                np.multiply(data[:, :, 0], data[:, :, 0])
                + np.multiply(data[:, :, 1], data[:, :, 1])
                + np.multiply(data[:, :, 2], data[:, :, 2])
            )
            mo_chang = np.dstack((mo_chang, mo_chang, mo_chang))
            return data / mo_chang

        x, y = np.meshgrid(np.arange(0, width), np.arange(0, height))
        x = x.reshape([-1])
        y = y.reshape([-1])
        xyz = np.vstack((x, y, np.ones_like(x)))
        pts_3d = np.dot(np.linalg.inv(K), xyz * depth.reshape([-1]))
        pts_3d_world = pts_3d.reshape((3, height, width))
        f = (
            pts_3d_world[:, 1 : height - 1, 2:width]
            - pts_3d_world[:, 1 : height - 1, 1 : width - 1]
        )
        t = (
            pts_3d_world[:, 2:height, 1 : width - 1]
            - pts_3d_world[:, 1 : height - 1, 1 : width - 1]
        )
        normal_map = np.cross(f, t, axisa=0, axisb=0)
        normal_map = normalization(normal_map)
        return normal_map

    ####### visualize #######
    def vis_and_save_depth(self,path):
        eng=get_eng()
        eng.imshow(self.depth,[])
        eng.imwrite(self.get_depth().filled(), path, nargout=0)


if __name__=="__main__":
    # vis_normal = lambda normal: np.uint8((normal + 1) / 2 * 255)[..., ::-1]

    # normal1 = get_surface_normal_by_depth(depth, K)    #  spend time: 60ms
    # normal2 = get_normal_map_by_point_cloud(depth, K)  #  spend time: 90m
    pass