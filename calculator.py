import time
from typing import List, Optional


class Timer:
    """
    计时器类
    用于记录和管理时间计数，支持启动、暂停、继续、停止和重置功能，并可记录单圈时间。
    """

    def __init__(self):
        """初始化计时器，设置初始值"""
        self.start_time: float = 0.0
        self.elapsed_time: float = 0.0
        self.is_running: bool = False
        self.min_time: float = float('inf')
        self.lap_times: List[float] = []

    def start(self) -> None:
        """启动计时器"""
        if not self.is_running:
            self.start_time = time.time() - self.elapsed_time
            self.is_running = True

    def pause(self) -> None:
        """暂停计时器"""
        if self.is_running:
            self.elapsed_time = time.time() - self.start_time
            self.is_running = False

    def stop(self) -> None:
        """停止计时器（等同于暂停，语义上表示本次计时会话结束）"""
        self.pause()

    def reset(self) -> None:
        """重置计时器，清除所有记录"""
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.is_running = False
        self.min_time = float('inf')
        self.lap_times = []

    def get_time(self) -> float:
        """获取当前计时时间（秒）"""
        if self.is_running:
            return time.time() - self.start_time
        return self.elapsed_time

    def get_formatted_time(self, show_ms: bool = False) -> str:
        """
        获取格式化的时间字符串

        参数:
            show_ms: 是否显示毫秒，默认 False。
                     False → HH:MM:SS，True → HH:MM:SS.mmm
        """
        total = self.get_time()
        total_seconds = int(total)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        if show_ms:
            ms = int((total - total_seconds) * 1000)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{ms:03d}"
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def get_min_time(self) -> Optional[float]:
        """获取所有单圈记录中的最小时间，若无记录则返回 None"""
        return self.min_time if self.lap_times else None

    def record_time(self) -> float:
        """
        记录当前时间为一圈时间，并更新最小时间记录。

        返回:
            本次记录的时间（秒）
        """
        current_time = self.get_time()
        self.lap_times.append(current_time)
        self.min_time = min(self.lap_times)
        return current_time

    def get_lap_times(self) -> List[float]:
        """获取所有单圈时间记录列表（副本）"""
        return list(self.lap_times)


# ── 快速排序 ────────────────────────────────────────────────────────────────

def _insertion_sort(arr: list, low: int, high: int) -> None:
    """对 arr[low..high] 区间执行插入排序（内部辅助函数）"""
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def _median_of_three(arr: list, low: int, high: int) -> object:
    """三数取中法选择主元，将主元置于 arr[high-1] 并返回主元值"""
    mid = (low + high) // 2
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]
    arr[mid], arr[high - 1] = arr[high - 1], arr[mid]
    return arr[high - 1]


def _quicksort_impl(arr: list, low: int, high: int) -> None:
    """快速排序递归内部函数，对 arr[low..high] 原地排序"""
    if high - low < 10:
        _insertion_sort(arr, low, high)
        return

    pivot = _median_of_three(arr, low, high)

    i = low
    j = high - 1
    while True:
        i += 1
        while arr[i] < pivot:
            i += 1
        j -= 1
        while arr[j] > pivot:
            j -= 1
        if i >= j:
            break
        arr[i], arr[j] = arr[j], arr[i]

    arr[i], arr[high - 1] = arr[high - 1], arr[i]

    _quicksort_impl(arr, low, i - 1)
    _quicksort_impl(arr, i + 1, high)


def quicksort(arr: list, reverse: bool = False) -> None:
    """
    快速排序（原地排序）

    使用三数取中法选择主元，小数组（长度 < 10）自动切换为插入排序。
    平均时间复杂度 O(n log n)，空间复杂度 O(log n)。

    参数:
        arr:     待排序列表，将被原地修改
        reverse: 若为 True 则按降序排序，默认升序
    """
    if len(arr) <= 1:
        return
    _quicksort_impl(arr, 0, len(arr) - 1)
    if reverse:
        arr.reverse()


# ── 主程序：演示 ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    timer = Timer()
    timer.start()
    time.sleep(1)
    timer.record_time()
    time.sleep(1)
    timer.record_time()
    timer.pause()
    print(f"当前时间: {timer.get_formatted_time(show_ms=True)}")
    print(f"单圈记录: {[round(t, 3) for t in timer.get_lap_times()]}")
    print(f"最小单圈: {round(timer.get_min_time(), 3)}")
    timer.reset()
    print(f"重置后:   {timer.get_formatted_time()}")

    data = [64, 34, 25, 12, 22, 11, 90, 3, 7, 45, 18]
    print(f"\n排序前:       {data}")
    quicksort(data)
    print(f"排序后（升序）: {data}")
    quicksort(data, reverse=True)
    print(f"排序后（降序）: {data}")
