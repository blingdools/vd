import unittest
import time
from calculator import Timer, quicksort


class TestTimer(unittest.TestCase):

    def setUp(self):
        self.timer = Timer()

    # ── 初始状态 ──────────────────────────────────────────────────────────
    def test_initial_state(self):
        self.assertFalse(self.timer.is_running)
        self.assertEqual(self.timer.get_time(), 0.0)
        self.assertEqual(self.timer.get_formatted_time(), "00:00:00")
        self.assertIsNone(self.timer.get_min_time())
        self.assertEqual(self.timer.get_lap_times(), [])

    # ── start / pause ─────────────────────────────────────────────────────
    def test_start_sets_running(self):
        self.timer.start()
        self.assertTrue(self.timer.is_running)

    def test_start_twice_no_reset(self):
        self.timer.start()
        time.sleep(0.05)
        t1 = self.timer.get_time()
        self.timer.start()          # 第二次 start 应无效
        time.sleep(0.05)
        t2 = self.timer.get_time()
        self.assertGreater(t2, t1)  # 时间仍在增加（不曾重置）

    def test_pause_stops_time(self):
        self.timer.start()
        time.sleep(0.05)
        self.timer.pause()
        t_after_pause = self.timer.get_time()
        time.sleep(0.05)
        self.assertAlmostEqual(self.timer.get_time(), t_after_pause, places=3)

    def test_pause_when_not_running_no_effect(self):
        self.timer.pause()          # 未启动时暂停应无副作用
        self.assertFalse(self.timer.is_running)
        self.assertEqual(self.timer.get_time(), 0.0)

    def test_resume_after_pause(self):
        self.timer.start()
        time.sleep(0.05)
        self.timer.pause()
        frozen = self.timer.get_time()
        self.timer.start()          # 继续
        time.sleep(0.05)
        self.assertGreater(self.timer.get_time(), frozen)

    # ── stop ──────────────────────────────────────────────────────────────
    def test_stop_equivalent_to_pause(self):
        self.timer.start()
        time.sleep(0.05)
        self.timer.stop()
        self.assertFalse(self.timer.is_running)
        frozen = self.timer.get_time()
        time.sleep(0.05)
        self.assertAlmostEqual(self.timer.get_time(), frozen, places=3)

    # ── reset ─────────────────────────────────────────────────────────────
    def test_reset_clears_everything(self):
        self.timer.start()
        time.sleep(0.05)
        self.timer.record_time()
        self.timer.reset()
        self.assertFalse(self.timer.is_running)
        self.assertEqual(self.timer.get_time(), 0.0)
        self.assertIsNone(self.timer.get_min_time())
        self.assertEqual(self.timer.get_lap_times(), [])

    # ── get_formatted_time ────────────────────────────────────────────────
    def test_formatted_time_zero(self):
        self.assertEqual(self.timer.get_formatted_time(), "00:00:00")

    def test_formatted_time_hhmmss(self):
        # 手动设置 elapsed_time 来测试格式化
        self.timer.elapsed_time = 3661.0    # 1h 1m 1s
        self.assertEqual(self.timer.get_formatted_time(), "01:01:01")

    def test_formatted_time_with_ms(self):
        self.timer.elapsed_time = 5.750
        result = self.timer.get_formatted_time(show_ms=True)
        self.assertRegex(result, r"^\d{2}:\d{2}:\d{2}\.\d{3}$")
        self.assertTrue(result.endswith(".750") or result.endswith(".749") or result.endswith(".751"))

    # ── record_time / get_lap_times / get_min_time ────────────────────────
    def test_record_time_appends(self):
        self.timer.elapsed_time = 1.0
        self.timer.record_time()
        self.timer.elapsed_time = 2.0
        self.timer.record_time()
        laps = self.timer.get_lap_times()
        self.assertEqual(len(laps), 2)
        self.assertAlmostEqual(laps[0], 1.0, places=5)
        self.assertAlmostEqual(laps[1], 2.0, places=5)

    def test_record_time_returns_current(self):
        self.timer.elapsed_time = 3.5
        result = self.timer.record_time()
        self.assertAlmostEqual(result, 3.5, places=5)

    def test_get_min_time_single(self):
        self.timer.elapsed_time = 4.0
        self.timer.record_time()
        self.assertAlmostEqual(self.timer.get_min_time(), 4.0, places=5)

    def test_get_min_time_multiple(self):
        for t in [3.0, 1.5, 2.0]:
            self.timer.elapsed_time = t
            self.timer.record_time()
        self.assertAlmostEqual(self.timer.get_min_time(), 1.5, places=5)

    def test_get_min_time_none_when_empty(self):
        self.assertIsNone(self.timer.get_min_time())

    def test_get_lap_times_returns_copy(self):
        self.timer.elapsed_time = 1.0
        self.timer.record_time()
        laps = self.timer.get_lap_times()
        laps.append(999.0)
        self.assertEqual(len(self.timer.get_lap_times()), 1)  # 内部列表未被修改


class TestQuicksort(unittest.TestCase):

    # ── 基本功能 ──────────────────────────────────────────────────────────
    def test_empty_list(self):
        arr = []
        quicksort(arr)
        self.assertEqual(arr, [])

    def test_single_element(self):
        arr = [42]
        quicksort(arr)
        self.assertEqual(arr, [42])

    def test_two_elements_sorted(self):
        arr = [1, 2]
        quicksort(arr)
        self.assertEqual(arr, [1, 2])

    def test_two_elements_unsorted(self):
        arr = [2, 1]
        quicksort(arr)
        self.assertEqual(arr, [1, 2])

    def test_basic_ascending(self):
        arr = [64, 34, 25, 12, 22, 11, 90]
        quicksort(arr)
        self.assertEqual(arr, sorted([64, 34, 25, 12, 22, 11, 90]))

    def test_reverse_flag(self):
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        quicksort(arr, reverse=True)
        self.assertEqual(arr, sorted([3, 1, 4, 1, 5, 9, 2, 6], reverse=True))

    # ── 边界与特殊情况 ────────────────────────────────────────────────────
    def test_already_sorted(self):
        arr = list(range(20))
        quicksort(arr)
        self.assertEqual(arr, list(range(20)))

    def test_reverse_sorted(self):
        arr = list(range(20, 0, -1))
        quicksort(arr)
        self.assertEqual(arr, list(range(1, 21)))

    def test_all_same_elements(self):
        arr = [7] * 15
        quicksort(arr)
        self.assertEqual(arr, [7] * 15)

    def test_duplicates(self):
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        quicksort(arr)
        self.assertEqual(arr, sorted([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]))

    def test_negative_numbers(self):
        arr = [-5, 3, -1, 0, 8, -3]
        quicksort(arr)
        self.assertEqual(arr, [-5, -3, -1, 0, 3, 8])

    def test_floats(self):
        arr = [3.14, 1.41, 2.71, 0.57]
        quicksort(arr)
        self.assertEqual(arr, sorted([3.14, 1.41, 2.71, 0.57]))

    def test_large_list(self):
        import random
        arr = random.sample(range(1000), 500)
        expected = sorted(arr)
        quicksort(arr)
        self.assertEqual(arr, expected)

    def test_small_array_uses_insertion_sort_path(self):
        # 长度 < 10，走插入排序分支
        arr = [9, 3, 7, 1, 5]
        quicksort(arr)
        self.assertEqual(arr, [1, 3, 5, 7, 9])

    def test_in_place_modification(self):
        arr = [5, 2, 8, 1]
        original_id = id(arr)
        quicksort(arr)
        self.assertEqual(id(arr), original_id)  # 同一个列表对象


if __name__ == "__main__":
    unittest.main(verbosity=2)
