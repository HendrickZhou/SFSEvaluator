import numpy as np
from matlab_agent import get_eng
import matplotlib.pyplot as plt
import matlab
import open3d as o3d
from math import isnan

def mat2np2d(mat:matlab.double)->np.array:
    """convert 2d matlab matrix to numpy 2d array"""
    eng=get_eng()
    size_mat=eng.size(mat)
    w=size_mat[0][0]
    h=size_mat[0][1]
    result=np.zeros((w,h))
    for i in range(w):
        for j in range(h):
            the_val=mat[i][j]
            if isnan(the_val):
                continue
            result[i][j]=the_val
    return result

class ThreeDObject():
    def __init__(self) -> None:
        self.depth=None
        self.normal=None
        self.K=None
        self.mask=None

    @classmethod
    def from_data(cls, depth:np.array, mask:np.array, normal=None, K=None) -> None:
        new_obj=cls()
        new_obj.depth=depth
        new_obj.K=K
        new_obj.mask=mask
        if normal is None:
            new_obj.normal=new_obj.get_surface_normal(depth,K)

    @classmethod
    def from_file(cls,td_file):
        new_obj=cls()

    def get_depth():
        """get the depth in numpy.ma format, with the mask property applied"""
        ny.

    def get_normal():
        pass

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
    def vis_and_save(self, show_figure=True, save_img=True):
        plt.plot(self.depth)



if __name__=="__main__":
    vis_normal = lambda normal: np.uint8((normal + 1) / 2 * 255)[..., ::-1]

    normal1 = get_surface_normal_by_depth(depth, K)    #  spend time: 60ms
    normal2 = get_normal_map_by_point_cloud(depth, K)  #  spend time: 90m