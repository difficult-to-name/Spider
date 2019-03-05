import time
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# 登陆需要的账号密码
account = '13631789679'
password = 'a757664220'


# Seleniun对象的初始化
class CrackGeetest():

    def __init__(self):
        self.url = 'https://passport.bilibili.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 5)
        self.account = account
        self.password = password

    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.browser.get(self.url)
        account = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        password.clear()
        account.clear()
        # account.send_keys(self.account)
        # password.send_keys(self.password)

    def get_position(self):
        """
        获取图像位置
        :param self:
        :return: 图像位置元组
        """
        # 等待验证码滑块加载
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gt_bg')))
        time.sleep(1)
        location = img.location
        size = img.size
        print('图像大小:', size)
        top, bottom, left, right = location['y'], location['y'] + size['height'], \
                                   location['x'], location['x'] + size['width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_verify_image(self):
        """
        获取图像
        :param self:
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码图像位置:', top, left, bottom, right)

        # 获取网页截图
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))  # 裁剪需左上角和右下角坐标
        return captcha

    def get_slider(self):
        """
        获取滑动按钮
        :param self:
        :return:滑动按钮
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'gt_slider_knob')))
        return slider

    def get_offset(self, image1, image2):
        """
        :param image1: 完整图片
        :param image2: 带缺口图片
        :return:缺口位置
        """
        # 设置检测偏移量为65，避开滑块，检测缺口
        left = 65
        for x in range(left, image1.size[0]):
            for y in range(image1.size[1] - 30):
                if not self.is_equal_pixel(image1, image2, x, y):
                    left = x
                    print('(%s,%s)点的RGB值不同' % (x, y))
                    print('检测到缺口')
                    return left
        return left

    def is_equal_pixel(self, image1, image2, x, y):
        """
        判断两图像素点是否一致
        :param image1: 完整图片
        :param image2: 带缺口图片
        :param x: 横坐标
        :param y: 纵坐标
        :return:
        """
        # 取两图的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        # 设置对比阈值
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold \
                and abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            print(pixel1, pixel2)
            return False

    def get_track(self, distance):
        """
        根据偏移量计算移动轨迹
        :param distance:偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 3 / 5
        # 计算间隔
        t = 0.2
        # 当前速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为+2
                a = 2
            else:
                # 加速度为-3, 此时将时间间隔设置为0.1，可有效降低拖动速度，增加成功率
                a = -3
                t = 0.1
            # 当前速度
            v0 = v
            v = v0 + a * t
            # 移动距离
            move = v0 * t + 0.5 * a * t ** 2
            # 当前位移
            current = current + move
            # 加入轨迹
            track.append(round(move))

        return track

    def move_to_gap(self, slider, track):
        """
        移动滑块至缺口处
        :param slider: 滑块
        :param track: 轨迹
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def login(self):
        """
        验证通过后登录
        :param self:
        :return: None
        """
        account = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        account.send_keys(self.account)
        password.send_keys(self.password)
        submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn')))
        submit.click()
        time.sleep(5)
        print('登录成功')

    def main(self):

        # 打开浏览器，获取网页
        self.open()
        # 将鼠标放在按钮上，加载图片
        slider = self.get_slider()
        ActionChains(self.browser).move_to_element(slider).perform()
        time.sleep(1)
        # 获取原图
        image1 = self.get_verify_image()
        # image1.show()
        # 获取带缺口的图片
        slider.click()
        image2 = self.get_verify_image()
        # image2.show()
        # 计算缺口位置
        gap = self.get_offset(image1, image2)
        print('缺口位置:', gap)
        # 计算轨迹
        track = self.get_track(gap - 6)
        self.move_to_gap(slider, track)

        try:
            success = self.wait.until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, 'gt_info_type'), '验证通过'))
            print('验证通过')
            # 验证通过后登录
            self.login()
        except TimeoutException:
            # 失败则重试
            self.main()


if __name__ == '__main__':
    crack = CrackGeetest()
    crack.main()