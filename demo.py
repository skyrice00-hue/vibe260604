import tkinter as tk
import random
import math

class BreakoutGame:
    def __init__(self, root):
        self.root = root
        self.root.title("블럭깨기 게임")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # 캔버스 생성
        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 게임 변수
        self.ball_x = 400
        self.ball_y = 300
        self.ball_vx = 3
        self.ball_vy = -3
        self.ball_radius = 5
        
        self.paddle_x = 350
        self.paddle_width = 100
        self.paddle_height = 15
        self.paddle_y = 550
        
        self.blocks = [] 
        self.score = 0
        self.game_over = False
        self.game_won = False
        
        # 블럭 생성
        self.create_blocks()
        
        # 이벤트 바인딩
        self.canvas.bind("<Motion>", self.on_mouse_move)
        
        # 게임 루프 시작
        self.game_loop()
    
    def create_blocks(self):
        """게임 시작 시 블럭 생성"""
        self.blocks = []
        colors = ["red", "orange", "yellow", "green", "blue"]
        for row in range(4):
            for col in range(8):
                x = col * 95 + 10
                y = row * 30 + 10
                self.blocks.append({
                    "x": x,
                    "y": y,
                    "width": 90,
                    "height": 25,
                    "color": colors[row % len(colors)],
                    "active": True
                })
    
    def on_mouse_move(self, event):
        """마우스 움직임으로 패들 제어"""
        self.paddle_x = event.x - self.paddle_width // 2
        # 패들이 화면 밖으로 나가지 않도록 제한
        if self.paddle_x < 0:
            self.paddle_x = 0
        if self.paddle_x + self.paddle_width > 800:
            self.paddle_x = 800 - self.paddle_width
    
    def update_ball(self):
        """공의 위치 업데이트"""
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy
        
        # 좌우 벽 충돌
        if self.ball_x - self.ball_radius < 0 or self.ball_x + self.ball_radius > 800:
            self.ball_vx *= -1
        
        # 위 벽 충돌
        if self.ball_y - self.ball_radius < 0:
            self.ball_vy *= -1
        
        # 패들 충돌
        if (self.ball_y + self.ball_radius > self.paddle_y and
            self.ball_y - self.ball_radius < self.paddle_y + self.paddle_height and
            self.ball_x > self.paddle_x and
            self.ball_x < self.paddle_x + self.paddle_width):
            self.ball_vy *= -1
            # 공이 패들 중앙에서의 거리에 따라 각도 조정
            center = self.paddle_x + self.paddle_width // 2
            offset = (self.ball_x - center) / (self.paddle_width // 2)
            self.ball_vx = offset * 5
        
        # 블럭 충돌
        for block in self.blocks:
            if not block["active"]:
                continue
            
            if (self.ball_x > block["x"] and
                self.ball_x < block["x"] + block["width"] and
                self.ball_y > block["y"] and
                self.ball_y < block["y"] + block["height"]):
                block["active"] = False
                self.ball_vy *= -1
                self.score += 10
        
        # 게임 오버 (공이 아래로 떨어짐)
        if self.ball_y > 600:
            self.game_over = True
    
    def draw(self):
        """화면 그리기"""
        self.canvas.delete("all")
        
        # 공 그리기
        self.canvas.create_oval(
            self.ball_x - self.ball_radius,
            self.ball_y - self.ball_radius,
            self.ball_x + self.ball_radius,
            self.ball_y + self.ball_radius,
            fill="white"
        )
        
        # 패들 그리기
        self.canvas.create_rectangle(
            self.paddle_x,
            self.paddle_y,
            self.paddle_x + self.paddle_width,
            self.paddle_y + self.paddle_height,
            fill="cyan",
            outline="white"
        )
        
        # 블럭 그리기
        for block in self.blocks:
            if block["active"]:
                self.canvas.create_rectangle(
                    block["x"],
                    block["y"],
                    block["x"] + block["width"],
                    block["y"] + block["height"],
                    fill=block["color"],
                    outline="white"
                )
        
        # 점수 표시
        self.canvas.create_text(
            10, 10,
            text=f"점수: {self.score}",
            fill="white",
            font=("Arial", 16),
            anchor="nw"
        )
        
        # 게임 오버 표시
        if self.game_over:
            self.canvas.create_text(
                400, 300,
                text="게임 오버!",
                fill="red",
                font=("Arial", 48),
                anchor="center"
            )
            self.canvas.create_text(
                400, 370,
                text=f"최종 점수: {self.score}",
                fill="white",
                font=("Arial", 24),
                anchor="center"
            )
        
        # 게임 승리 표시
        active_blocks = sum(1 for block in self.blocks if block["active"])
        if active_blocks == 0 and not self.game_won:
            self.game_won = True
        
        if self.game_won:
            self.canvas.create_text(
                400, 300,
                text="게임 완료!",
                fill="green",
                font=("Arial", 48),
                anchor="center"
            )
            self.canvas.create_text(
                400, 370,
                text=f"최종 점수: {self.score}",
                fill="white",
                font=("Arial", 24),
                anchor="center"
            )
    
    def game_loop(self):
        """게임 루프"""
        if not self.game_over and not self.game_won:
            self.update_ball()
        
        self.draw()
        
        # 루프 반복 (약 30 FPS)
        self.root.after(33, self.game_loop)

# 게임 실행
if __name__ == "__main__":
    root = tk.Tk()
    game = BreakoutGame(root)
    root.mainloop()
