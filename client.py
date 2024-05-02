import pygame
import sys
from network import Network

def run_game():
    pygame.init()
     
    WIDTH, HEIGHT = 1500, 900
     
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Five In A Row!")

    # Tải hình ảnh và thiết lập màu nền
    BOARD = pygame.image.load("assets/Board_18x18.png")
    X_IMG = pygame.image.load("assets/X.png")
    O_IMG = pygame.image.load("assets/O.png")

    BG_COLOR = (255, 250, 205)

    # Tạo bàn cờ 18x18 với các giá trị khởi đầu từ 1 đến 324
    board = [[j + 1 + i * 18 for j in range(18)] for i in range(18)]

    # Tạo graphical_board tương ứng
    graphical_board = [[[None, None] for _ in range(18)] for _ in range(18)]

    # Khởi tạo font và kích thước chữ
    font = pygame.font.Font(None, 72)

    # Hàm để vẽ văn bản lên màn hình
    def draw_text(text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_obj, text_rect)

    # Khởi tạo âm nhạc nền
    pygame.mixer.music.load("assets/music_game.mp3")
    pygame.mixer.music.set_volume(0.2)  # Giảm âm lượng xuống 50%
    pygame.mixer.music.play(-1)  # -1 để lặp lại vô hạn

    global to_move
    to_move = 'X'

    SCREEN.fill(BG_COLOR)
    SCREEN.blit(BOARD, (0,0))

    pygame.display.update()

    def render_board(board, graphical_board, ximg, oimg):
        for i in range(18):
            for j in range(18):
                if board[i][j] == 'X':
                    # Create an X image and rect
                    graphical_board[i][j][0] = ximg
                    graphical_board[i][j][1] = ximg.get_rect(center=(j*50+25, i*50+25))
                elif board[i][j] == 'O':
                    graphical_board[i][j][0] = oimg
                    graphical_board[i][j][1] = oimg.get_rect(center=(j*50+25, i*50+25))

    # Tải âm thanh cho X và O
    sound_XO = pygame.mixer.Sound("assets/effect_click.wav")

    # Điều chỉnh âm lượng của âm thanh
    sound_XO.set_volume(0.3)

    # Hàm để phát âm thanh khi vẽ X hoặc O
    def play_sound_XO():
        sound_XO.play()

    def add_XO(board, graphical_board, to_move):
        current_pos = pygame.mouse.get_pos()
        
        # Tính toán vị trí của ô trên bàn cờ dựa trên kích thước thực sự của bàn cờ và ô
        converted_x = current_pos[0] // 50
        converted_y = current_pos[1] // 50
        
        # Kiểm tra xem vị trí click có nằm trong phạm vi bàn cờ không
        if 0 <= converted_x < 18 and 0 <= converted_y < 18:
            if board[converted_y][converted_x] != 'O' and board[converted_y][converted_x] != 'X':
                board[converted_y][converted_x] = to_move
                play_sound_XO()
                if to_move == 'O':
                    to_move = 'X'
                else:
                    to_move = 'O'

            render_board(board, graphical_board, X_IMG, O_IMG)

            for i in range(18):
                for j in range(18):
                    if graphical_board[i][j][0] is not None:
                        SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
            
            pygame.display.update()  # Cập nhật màn hình sau khi thay đổi hình ảnh

        return board, to_move

    game_finished = False

    def check_win(board):
        for i in range(18):
            for j in range(14):  # Kiểm tra hàng ngang
                if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == board[i][j+4] != None:
                    for k in range(5):
                        if board[i][j+k] == 'X':
                            graphical_board[i][j+k][0] = pygame.image.load("assets/Winning X.png")
                        else:
                            graphical_board[i][j+k][0] = pygame.image.load("assets/Winning O.png")
                    for k in range(5):  # Vẽ hình ảnh lên màn hình
                        SCREEN.blit(graphical_board[i][j+k][0], graphical_board[i][j+k][1])
                    pygame.display.update()  # Cập nhật màn hình sau khi thay đổi hình ảnh
                    return board[i][j]
        for j in range(18):
            for i in range(14):  # Kiểm tra hàng dọc
                if board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] == board[i+4][j] != None:
                    for k in range(5):
                        if board[i+k][j] == 'X':
                            graphical_board[i+k][j][0] = pygame.image.load("assets/Winning X.png")
                        else:
                            graphical_board[i+k][j][0] = pygame.image.load("assets/Winning O.png")
                    for k in range(5):  # Vẽ hình ảnh lên màn hình
                        SCREEN.blit(graphical_board[i+k][j][0], graphical_board[i+k][j][1])
                    pygame.display.update()  # Cập nhật màn hình sau khi thay đổi hình ảnh
                    return board[i][j]
        # Kiểm tra đường chéo chính
        for i in range(14):
            for j in range(14):
                if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == board[i+4][j+4] != None:
                    for k in range(5):
                        if board[i+k][j+k] == 'X':
                            graphical_board[i+k][j+k][0] = pygame.image.load("assets/Winning X.png")
                        else:
                            graphical_board[i+k][j+k][0] = pygame.image.load("assets/Winning O.png")
                    for k in range(5):  # Vẽ hình ảnh lên màn hình
                        SCREEN.blit(graphical_board[i+k][j+k][0], graphical_board[i+k][j+k][1])
                    pygame.display.update()  # Cập nhật màn hình sau khi thay đổi hình ảnh
                    return board[i][j]
        # Kiểm tra đường chéo phụ
                if board[i][j] == board[i-1][j+1] == board[i-2][j+2] == board[i-3][j+3] == board[i-4][j+4] != None:
                    for k in range(5):
                        if board[i-k][j+k] == 'X':
                            graphical_board[i-k][j+k][0] = pygame.image.load("assets/Winning X.png")
                        else:
                            graphical_board[i-k][j+k][0] = pygame.image.load("assets/Winning O.png")
                    for k in range(5):
                        SCREEN.blit(graphical_board[i-k][j+k][0], graphical_board[i-k][j+k][1])
                    pygame.display.update()
                    return board[i][j]
        # Kiểm tra hòa
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != 'X' and board[i][j] != 'O':
                    return None
        return "DRAW"

    run = True
    n = Network()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                board, to_move = add_XO(board, graphical_board, to_move)

                if game_finished:
                    # Tạo bàn cờ 18x18 với các giá trị khởi đầu từ 1 đến 324
                    board = [[j + 1 + i * 18 for j in range(18)] for i in range(18)]

                    # Tạo graphical_board tương ứng
                    graphical_board = [[[None, None] for _ in range(18)] for _ in range(18)]

                    to_move = 'X'

                    SCREEN.fill(BG_COLOR)
                    SCREEN.blit(BOARD, (0,0))

                    game_finished = False

                    pygame.display.update()
                
                # Kiểm tra chiến thắng
                result = check_win(board)
                if result == "DRAW":
                    draw_text("DRAW!", font, (255, 215, 0), SCREEN, WIDTH // 2, HEIGHT // 2)
                elif result is not None:
                    # Hiển thị thông báo chiến thắng lên màn hình
                    draw_text("PLAYER {} WIN!".format(result), font, (255, 215, 0), SCREEN, WIDTH // 2, HEIGHT // 2)
                    game_finished = True
                
                pygame.display.update()

def main():
    run_game()

if __name__ == "__main__":
    main()