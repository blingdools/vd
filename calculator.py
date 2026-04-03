import time

class Timer:
    """
    计时器类
    用于记录和管理时间计数，支持启动、暂停、停止和重置功能。
    """
    
    def __init__(self):
        """初始化计时器，设置初始值"""
        self.start_time = 0      # 计时器启动时的时间戳
        self.elapsed_time = 0    # 已经过的时间（秒）
        self.is_running = False  # 计时器是否正在运行
        self.min_time = float('inf')  # 记录最小的计时时间
    
    def start(self):
        """启动计时器"""
        if not self.is_running:
            self.start_time = time.time() - self.elapsed_time
            self.is_running = True
    
    def pause(self):
        """暂停计时器"""
        if self.is_running:
            self.elapsed_time = time.time() - self.start_time
            self.is_running = False
    
    def reset(self):
        """重置计时器"""
        self.start_time = 0
        self.elapsed_time = 0
        self.is_running = False
        self.min_time = float('inf')
    
    def get_time(self):
        """获取当前计时时间（秒）"""
        if self.is_running:
            return time.time() - self.start_time
        return self.elapsed_time
    
    def get_formatted_time(self):
        """获取格式化的时间字符串 (HH:MM:SS)"""
        total_seconds = int(self.get_time())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def get_min_time(self):
        """获取最小的计时时间"""
        return self.min_time if self.min_time != float('inf') else 0
    
    def record_time(self):
        """记录当前时间为最小值（如果比现有最小值更小）"""
        current_time = self.get_time()
        if current_time < self.min_time:
            self.min_time = current_time
        return self.min_time


# 主程序：演示计时器的使用
if __name__ == "__main__":
    timer = Timer()
    timer.start()
    time.sleep(2)
    print(timer.get_formatted_time())  # 00:00:02
    timer.pause()
    timer.record_time()
    print(f"最小时间: {timer.get_min_time()}")  # 约2.0
    timer.reset()
    print(timer.get_formatted_time())  # 00:00:00