import cv2
import glob
import os
import sys
import numpy as np
import dlib
__DEBUG__ = False
if __DEBUG__:
    filename_dst = 'data/0.jpg'
    filename_src = 'data/1.jpg'
    filename_out = 'out'
else :
    assert(len(sys.argv) == 4)  #the input should be **.exe src dst out
    filename_src = sys.argv[1]
    filename_dst = sys.argv[2]
    filename_out = sys.argv[3]
img_src = cv2.imread(filename_src)
img_dst = cv2.imread(filename_dst)
assert(img_src is not None and img_dst is not None) #check the input path
img_dst_warped = np.copy(img_dst)

if(__DEBUG__):
    cv2.imshow("src", img_src)
    cv2.imshow("dst", img_dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
basedir = os.path.abspath(os.path.dirname(__file__))
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(os.path.join(basedir, "shape_predictor_68_face_landmarks.dat"))
def get_face_points(img,SHOW=False):
    ret=[]
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    rects = detector(img_gray, 0)
    for i in range(len(rects)): #qwq
        landmarks = np.matrix([[p.x, p.y] for p in predictor(img,rects[i]).parts()])
        for idx, point in enumerate(landmarks):
            # 68点的坐标
            pos = (point[0, 0], point[0, 1])
            ret.append(pos)
            if(SHOW):
                print(idx,pos)
                # 利用cv2.circle给每个特征点画一个圈，共68个
                cv2.circle(img, pos, 1, color=(0, 255, 0))
                # 利用cv2.putText输出1-68
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, str(idx+1), pos, font, 0.8, (0, 0, 255), 1,cv2.LINE_AA)
    if(SHOW):
        cv2.namedWindow("img", 2)
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return ret
#得到68点模型
points_src = get_face_points(img_src.copy(),__DEBUG__)
points_dst = get_face_points(img_dst.copy(),__DEBUG__)
assert(len(points_dst)==68 and len(points_src)==68) #if and only if there is one face in each photo
#求凸包
hull_pt_src = []
hull_pt_dst = []
hull_pt_indices = cv2.convexHull(np.array(points_dst),
                                 returnPoints = False)
hull_pt_indices = hull_pt_indices.flatten()

for idx_pt in hull_pt_indices:
    hull_pt_src.append(points_src[idx_pt])
    hull_pt_dst.append(points_dst[idx_pt])
if(__DEBUG__):
    print(hull_pt_indices)
    print(hull_pt_src)
    print(hull_pt_dst)

#狄洛尼三角剖分

def cal_delaunay_tri(rect, points):
    """计算狄洛尼三角剖分"""

    subdiv = cv2.Subdiv2D(rect);

    # 逐点插入
    for pt in points:
        # subdiv.insert 输入类型：tuple
        subdiv.insert((pt[0],pt[1]))

    lst_tri = subdiv.getTriangleList();

    # 狄洛尼三角网格顶点索引
    lst_delaunay_tri_pt_indices = []

    for tri in lst_tri:
        lst_tri_pts = [(tri[0], tri[1])]
        lst_tri_pts.append((tri[2], tri[3]))
        lst_tri_pts.append((tri[4], tri[5]))

        # 查询三角网格顶点索引
        lst_pt_indices = []
        for tri_pt in lst_tri_pts:

            for idx_pt in range(len(points)):

                if (abs(tri_pt[0] - points[idx_pt][0]) < 1) and \
                    (abs(tri_pt[1] - points[idx_pt][1]) < 1):
                    lst_pt_indices.append(idx_pt)

        lst_delaunay_tri_pt_indices.append(lst_pt_indices)

    return lst_delaunay_tri_pt_indices

size_img_dst = img_dst.shape
rect = (0, 0, size_img_dst[1], size_img_dst[0])
lst_delaunay_tri_pt_indices = cal_delaunay_tri(rect, hull_pt_dst)

size_img_src = img_src.shape
rect = (0, 0, size_img_src[1], size_img_src[0])

src_delaunay_tri_pt_indices = cal_delaunay_tri(rect, hull_pt_src)

# 这里假定凸包上的编号是一一对应的 而三角剖分不是一一对应的
if __DEBUG__:
    print(lst_delaunay_tri_pt_indices)
    print(len(lst_delaunay_tri_pt_indices))
    print(src_delaunay_tri_pt_indices)
    print(len(src_delaunay_tri_pt_indices))

def warp_affine(img_src, tri_src, tri_dst, size):
    # """仿射"""

    # 仿射矩阵
    mat_warp = cv2.getAffineTransform(np.float32(tri_src), np.float32(tri_dst))

    # 仿射变换
    img_dst = cv2.warpAffine(img_src, mat_warp, (size[0], size[1]), None,
                             flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REFLECT_101)

    return img_dst


#----------------------------------------------------------------------
def warp_tri(img_src, img_dst, tri_src, tri_dst, alpha=1) :
    """仿射三角剖分，源图像到目标图像"""

    # 三角区域框
    rect_src = cv2.boundingRect(np.array(tri_src))
    rect_dst = cv2.boundingRect(np.array(tri_dst))

    # 三角形顶点相对于三角区域框的偏移
    tri_src_to_rect = [(item[0] - rect_src[0], item[1] - rect_src[1])
                       for item in tri_src]
    tri_dst_to_rect = [(item[0] - rect_dst[0], item[1] - rect_dst[1])
                       for item in tri_dst]

    # 蒙板
    mask = np.zeros((rect_dst[3], rect_dst[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.array(tri_dst_to_rect), (1, 1, 1), 16, 0)

    # 截取三角区域框中的源图像
    img_src_rect = img_src[rect_src[1] : rect_src[1] + rect_src[3],
                           rect_src[0] : rect_src[0] + rect_src[2]]

    size = (rect_dst[2], rect_dst[3])

    # 三角区域框仿射
    img_src_rect_warpped = warp_affine(img_src_rect, tri_src_to_rect, tri_dst_to_rect, size)

    # 蒙板 * 透明度
    mask *= alpha
    # 目标图像 = 目标图像 * (1 - 蒙板) + 源图像 * 蒙板
    img_dst[rect_dst[1] : rect_dst[1] + rect_dst[3],
            rect_dst[0] : rect_dst[0] + rect_dst[2]] = \
        img_dst[rect_dst[1] : rect_dst[1] + rect_dst[3],
                rect_dst[0] : rect_dst[0] + rect_dst[2]] * (1 - mask) + \
        img_src_rect_warpped * mask

# 狄洛尼三角剖分仿射
for tri_pt_indices in lst_delaunay_tri_pt_indices:

    # 源图像、目标图像三角顶点坐标
    tri_src = [hull_pt_src[tri_pt_indices[idx]] for idx in range(3)]
    tri_dst = [hull_pt_dst[tri_pt_indices[idx]] for idx in range(3)]

    warp_tri(img_src, img_dst_warped, tri_src, tri_dst, 1)

# cv2.imshow("dst",img_dst)
# cv2.waitKey(0)
# cv2.destroyAllWindows(img_dst_warped)
# print(img_dst_warped)

if __DEBUG__:
    cv2.imshow("dst",img_dst_warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 消除肤色差异 泊松
mask = np.zeros(img_dst.shape, dtype=img_dst.dtype)
cv2.fillConvexPoly(mask, np.array(hull_pt_dst), (255, 255, 255))

rect = cv2.boundingRect(np.float32([hull_pt_dst]))

center = (rect[0] + rect[2] // 2, rect[1] + rect[3] // 2)
# NORMAL:
img_dst_src_grad = cv2.seamlessClone(img_dst_warped, img_dst,
                                     mask, center, cv2.NORMAL_CLONE)
# MIXED：
img_dst_mix_grad = cv2.seamlessClone(img_dst_warped, img_dst,
                                     mask, center, cv2.MIXED_CLONE)
# MONOCHROME_TRANSFER
img_dst_mono_grad = cv2.seamlessClone(img_dst_warped, img_dst,
                                     mask, center, cv2.MONOCHROME_TRANSFER)

if __DEBUG__:
    imgs=[img_src, img_dst, img_dst_warped, img_dst_src_grad, img_dst_mix_grad, img_dst_mono_grad]
    for i in range(len(imgs)):
        cv2.imwrite('temp/image'+str(i+1)+'.png',imgs[i])

else:
    # cv2.imwrite(filename_out+"mono.jpg",img_dst_mono_grad )
    # cv2.imwrite(filename_out+"mix.jpg",img_dst_mix_grad)
    cv2.imwrite(filename_out+".jpg",img_dst_src_grad)
print("DONE")