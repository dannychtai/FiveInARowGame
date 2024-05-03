import pygame
import sys

class FiveInARow:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1500, 900
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Five In A Row!")
        self.BOARD = pygame.image.load("assets/Board_18x18.png")
        self.X_IMG = pygame.image.load("assets/X.png")
        self.O_IMG = pygame.image.load("assets/O.png")
        self.WINNING_X_IMG = pygame.image.load("assets/Winning X.png")
        self.WINNING_O_IMG = pygame.image.load("assets/Winning O.png")
        self.BG_COLOR = (255, 250, 205)
        self.board = [[j + 1 + i * 18 for j in range(18)] for i in range(18)]
        self.graphical_board = [[[None, None] for _ in range(18)] for _ in range(18)]
        self.font = pygame.font.Font(None, 72)
        self.sound_XO = pygame.mixer.Sound("assets/effect_click.wav")
        self.sound_XO.set_volume(0.3)
        self.current_player = 'X'  # Người chơi hiện tại
        self.next_player = 'O'     # Người chơi tiếp theo
        self.game_finished = False

    def draw_text(self, text, color, x, y):
        text_obj = self.font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        self.SCREEN.blit(text_obj, text_rect)

    def render_board(self):
        for i in range(18):
            for j in range(18):
                if self.board[i][j] == 'X':
                    self.graphical_board[i][j][0] = self.X_IMG
                    self.graphical_board[i][j][1] = self.X_IMG.get_rect(center=(j*50+25, i*50+25))
                elif self.board[i][j] == 'O':
                    self.graphical_board[i][j][0] = self.O_IMG
                    self.graphical_board[i][j][1] = self.O_IMG.get_rect(center=(j*50+25, i*50+25))

    def play_sound_XO(self):
        self.sound_XO.play()

    def add_XO(self):
        current_pos = pygame.mouse.get_pos()
        converted_x = current_pos[0] // 50
        converted_y = current_pos[1] // 50
        
        if 0 <= converted_x < 18 and 0 <= converted_y < 18:
            if self.board[converted_y][converted_x] != 'O' and self.board[converted_y][converted_x] != 'X':
                self.board[converted_y][converted_x] = self.current_player
                self.play_sound_XO()
                self.current_player, self.next_player = self.next_player, self.current_player  # Đổi lượt chơi

            self.render_board()

            for i in range(18):
                for j in range(18):
                    if self.graphical_board[i][j][0] is not None:
                        self.SCREEN.blit(self.graphical_board[i][j][0], self.graphical_board[i][j][1])
            
            pygame.display.update()

    def check_win(self):
        winning_player = None
        for i in range(18):
            for j in range(14):  # Kiểm tra hàng ngang
                if self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] == self.board[i][j+3] == self.board[i][j+4] != None:
                    winning_player = self.board[i][j]
                    for k in range(5):
                        if winning_player == 'X':
                            self.graphical_board[i][j+k][0] = self.WINNING_X_IMG
                        else:
                            self.graphical_board[i][j+k][0] = self.WINNING_O_IMG
                    for k in range(5):  # Vẽ hình ảnh lên màn hình
                        self.SCREEN.blit(self.graphical_board[i][j+k][0], self.graphical_board[i][j+k][1])
                    pygame.display.update()  # Cập nhật màn hình sau khi thay đổi hình ảnh
                    return winning_player
        for j in range(18):
            for i in range(14):  # Kiểm tra hàng dọc
                if self.board[i][j] == self.board[i+1][j] == self.board[i+2][j] == self.board[i+3][j] == self.board[i+4][j] != None:
                    winning_player = self.board[i][j]
                    for k in range(5):
                        if winning_player == 'X':
                            self.graphical_board[i+k][j][0] = self.WINNING_X_IMG
                        else:
                            self.graphical_board[i+k][j][0] = self.WINNING_O_IMG
                    for k in range(5):  # Vẽ hình ảnh lên màn hình
                        self.SCREEN.blit(self.graphical_board[i+k][j][0], self.graphical_board[i+k][j][1])
                    pygame.display.update()  # Cập nhật màn hình sau khi thay đổi hình ảnh
                    return winning_player
        # Kiểm tra đường chéo chính
        for i in range(14):
            for j in range(14):
                if self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == self.board[i+3][j+3] == self.board[i+4][j+4] != None:
                    winning_player = self.board[i][j]
                    for k in range(5):
                        if winning_player == 'X':
                            self.graphical_board[i+k][j+k][0] = self.WINNING_X_IMG
                        else:
                            self.graphical_board[i+k][j+k][0] = self.WINNING_O_IMG
                    for k in range(5):  # Vẽ hình ảnh lên màn hình
                        self.SCREEN.blit(self.graphical_board[i+k][j+k][0], self.graphical_board[i+k][j+k][1])
                    pygame.display.update()  # Cập nhật màn hình sau khi thay đổi hình ảnh
                    return winning_player
        # Kiểm tra đường chéo phụ
        for i in range(4, 18):
            for j in range(14):
                if self.board[i][j] == self.board[i-1][j+1] == self.board[i-2][j+2] == self.board[i-3][j+3] == self.board[i-4][j+4] != None:
                    winning_player = self.board[i][j]
                    for k in range(5):
                        if winning_player == 'X':
                            self.graphical_board[i-k][j+k][0] = self.WINNING_X_IMG
                        else:
                            self.graphical_board[i-k][j+k][0] = self.WINNING_O_IMG
                    for k in range(5):
                        self.SCREEN.blit(self.graphical_board[i-k][j+k][0], self.graphical_board[i-k][j+k][1])
                    pygame.display.update()
                    return winning_player
        # Kiểm tra hòa
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] != 'X' and self.board[i][j] != 'O':
                    return None
        return "DRAW"


    def run_game(self):
        pygame.mixer.music.load("assets/music_game.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        
        self.SCREEN.fill(self.BG_COLOR)
        self.SCREEN.blit(self.BOARD, (0,0))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.add_XO()
                    
                    if self.game_finished:
                        self.board = [[j + 1 + i * 18 for j in range(18)] for i in range(18)]
                        self.graphical_board = [[[None, None] for _ in range(18)] for _ in range(18)]
                        self.current_player = 'X'
                        self.next_player = 'O'
                        self.SCREEN.fill(self.BG_COLOR)
                        self.SCREEN.blit(self.BOARD, (0,0))
                        self.game_finished = False
                        pygame.display.update()

                    result = self.check_win()
                    if result == "DRAW":
                        self.draw_text("DRAW!", (255, 215, 0), self.WIDTH // 2, self.HEIGHT // 2)
                    elif result is not None:
                        self.draw_text("PLAYER {} WIN!".format(result), (255, 215, 0), self.WIDTH // 2, self.HEIGHT // 2)
                        self.game_finished = True

                    pygame.display.update()

def main():
    game = FiveInARow()
    game.run_game()

if __name__ == "__main__":
    main()
