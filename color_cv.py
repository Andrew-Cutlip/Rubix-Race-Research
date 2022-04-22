import cv2


class ColorCV:
    def __init__(self) -> None:
        self.stickers = {
            'tile_9': [
                [370, 210], [460, 210], [550, 210],
                [370, 290], [460, 290], [550, 290],
                [370, 380], [460, 380], [550, 380]
            ],
            'prev_9': [
                [10, 10], [30, 10], [50, 10],
                [10, 30], [30, 30], [50, 30],
                [10, 50], [30, 50], [50, 50]
            ],
            'tile_25': [
                [130, 80], [270, 80], [395, 80], [500, 80], [620, 80],
                [130, 180], [270, 180], [395, 180], [500, 180], [620, 180],
                [130, 290], [270, 290], [395, 290], [500, 290], [620, 290],
                [130, 410], [270, 410], [395, 410], [500, 410], [620, 410],
                [130, 530], [270, 530], [395, 530], [500, 530], [620, 530],
            ],
            'prev_25': [
                [20, 10], [40, 10], [60, 10], [80, 10], [100, 10],
                [20, 30], [40, 30], [60, 30], [80, 30], [100, 30],
                [20, 50], [40, 50], [60, 50], [80, 50], [100, 50],
                [20, 70], [40, 70], [60, 70], [80, 70], [100, 70],
                [20, 90], [40, 90], [60, 90], [80, 90], [100, 90]
            ],
        }
        self.color = {
            'W': (255, 255, 255),
            'B': (255, 0, 0),
            'G': (0, 255, 0),
            'Y': (0, 255, 255),
            'R': (0, 0, 255),
            'O': (0, 165, 255),
            'X': (0, 0, 0),
        }
        self.hsv = []
        self.color_tile9 = []
        self.color_tile25 = []

    def colour_detection(self, h, s, v):
        if(h >= 0 and h < 9) and (s >= 50 and s <= 255) and (v >= 70 and v <= 255):
            return 'O'
        elif(h >= 9 and h <= 20) and (s >= 50 and s <= 255) and (v >= 70 and v <= 255):
            return 'O'
        elif(h >= 0 and h <= 180) and (s >= 0 and s <= 35) and (v >= 140 and v <= 255):
            return 'W'
        elif(h > 20 and h <= 35) and (s >= 50 and s <= 255):
            return 'Y'
        elif(h >= 39 and h <= 89) and (s >= 50 and s <= 255):
            return 'G'
        elif(h >= 90 and h <= 128) and (s >= 50 and s <= 255) and (v >= 70 and v <= 255):
            return 'B'
        elif(h >= 159 and h <= 180) and (s >= 50 and s <= 255):
            return 'R'
        else:
            return 'X'

    def draw(self, image, sticker_name):
        for x, y in self.stickers[sticker_name]:
            cv2.rectangle(image, (x, y), (x + 10, y + 10), (255, 255, 0), 2)

    def draw_tile(self, tile, image, sticker_name):
        for i in range(tile):
            self.hsv.append(image[self.stickers[sticker_name][i][1] + 10]
                            [self.stickers[sticker_name][i][0] + 10])

    def draw_prev(self, image, sticker_name):
        a = 0
        for x, y in self.stickers[sticker_name]:
            colour = self.colour_detection(
                self.hsv[a][0], self.hsv[a][1], self.hsv[a][2])
            cv2.rectangle(image, (x, y), (x + 10, y + 10),
                          self.color[colour], -1)
            a += 1
            if(sticker_name == 'prev_9'):
                self.color_tile9.append(colour)
            elif(sticker_name == 'prev_25'):
                self.color_tile25.append(colour)

    def capture_video(self, sticker):
        vid = cv2.VideoCapture(0)
        FRAME = None
        while(True):
            ret, frame = vid.read()
            self.draw(frame, sticker)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                FRAME = frame
                break
        vid.release()
        cv2.destroyAllWindows()
        return frame

    def start(self):
        # print("First Scan the 3*3 solution Cube\n Press q to confirm it")
        # tile_9image = self.capture_video('tile_9')
        # tile_9image_hsv = cv2.cvtColor(tile_9image, cv2.COLOR_BGR2RGB)
        # self.draw_tile(9, tile_9image_hsv, 'tile_9')
        # self.draw_prev(tile_9image, 'prev_9')
        
        print("Scan the 5*5 solution Cube\n Press q to confirm it")
        tile_25image = self.capture_video('tile_25')
        tile_25image_hsv = cv2.cvtColor(tile_25image, cv2.COLOR_BGR2RGB)
        self.draw_tile(25, tile_25image_hsv, 'tile_25')
        self.draw_prev(tile_25image, 'prev_25')
        cv2.imshow("Pattern Image", tile_25image[0:900, 0:900])
        cv2.waitKey(0)
        print("Tile_25",self.color_tile25)


        # img9 = cv2.imread("Images/9_tile_2.png")
        # img25 = cv2.imread("Images/25_tile_3.png")
        # tile_9image = cv2.cvtColor(img9, cv2.COLOR_BGR2RGB)
        # tile_25image = cv2.cvtColor(img25, cv2.COLOR_BGR2RGB)

        # self.draw(img9, 'tile_9')
        # self.draw(img9, 'prev_9')
        # self.draw(img25, 'tile_25')
        # self.draw(img25, 'prev_25')

        # self.draw_tile(9, tile_9image, 'tile_9')
        # self.draw_prev(img9, 'prev_9')
        # hsv = []
        # self.draw_tile(25, tile_25image, 'tile_25')
        # self.draw_prev(img25, 'prev_25')

        # cv2.imshow("Goal State Image", img9[0:900, 0:900])
        # cv2.imshow("Pattern Image", img25[0:900, 0:900])
        
        # print("Tile_9",self.color_tile9)
        # print("Tile_25",self.color_tile25)

        # if cv2.waitKey(0) & 0xFF == 27:
        #     cv2.destroyAllWindows()

ColorCV().start()
