import pygame, sys
 
pygame.init()
 
WIDTH, HEIGHT = 1500, 900
 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Five In A Row!")

# Tải hình ảnh và thiết lập màu nền
BOARD = pygame.image.load("assets/Board_18x18.png")
X_IMG = pygame.image.load("assets/X.png")
O_IMG = pygame.image.load("assets/O.png")

BG_COLOR = (214, 201, 227)

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
    
to_move = 'X'

SCREEN.fill(BG_COLOR)
SCREEN.blit(BOARD, (0,0))

pygame.display.update()

def render_board(board, ximg, oimg):
    global graphical_board
    for i in range(18):
        for j in range(18):
            if board[i][j] == 'X':
                # Create an X image and rect
                graphical_board[i][j][0] = ximg
                graphical_board[i][j][1] = ximg.get_rect(center=(j*50+25, i*50+25))
            elif board[i][j] == 'O':
                graphical_board[i][j][0] = oimg
                graphical_board[i][j][1] = oimg.get_rect(center=(j*50+25, i*50+25))

def add_XO(board, graphical_board, to_move):
    current_pos = pygame.mouse.get_pos()
    converted_x = (current_pos[0]-1)/899*17
    converted_y = (current_pos[1])/900*17
    
    # Kiểm tra xem vị trí click có nằm trong phạm vi bàn cờ không
    if 0 <= round(converted_x) < 18 and 0 <= round(converted_y) < 18:
        if board[round(converted_y)][round(converted_x)] != 'O' and board[round(converted_y)][round(converted_x)] != 'X':
            board[round(converted_y)][round(converted_x)] = to_move
            if to_move == 'O':
                to_move = 'X'
            else:
                to_move = 'O'
        
        render_board(board, X_IMG, O_IMG)

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
    for i in range(4, 18):
        for j in range(4, 18):  # Bắt đầu từ hàng và cột thích hợp
            if board[i][j] == board[i-1][j-1] == board[i-2][j-2] == board[i-3][j-3] == board[i-4][j-4] != None:
                for k in range(5):
                    if board[i-k][j-k] == 'X':
                        graphical_board[i-k][j-k][0] = pygame.image.load("assets/Winning X.png")
                    else:
                        graphical_board[i-k][j-k][0] = pygame.image.load("assets/Winning O.png")
                for k in range(5):  # Vẽ hình ảnh lên màn hình
                    SCREEN.blit(graphical_board[i-k][j-k][0], graphical_board[i-k][j-k][1])
                pygame.display.update()  # Cập nhật màn hình sau khi thay đổi hình ảnh
                return board[i][j]

    # Kiểm tra hòa
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != 'X' and board[i][j] != 'O':
                    return None
        return "DRAW"





while True:
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
