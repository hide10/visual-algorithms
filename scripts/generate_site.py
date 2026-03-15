from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path("/home/hide10/algorithm.hide10.com")

CATEGORY_LABELS = {
    "Concepts": "概念",
    "Sorting": "ソート",
    "Searching": "探索",
    "Data Structures": "データ構造",
    "Graphs": "グラフ",
    "Dynamic Programming & Recursion": "動的計画法・再帰",
}

TOP_NAV = [
    ("学習ガイド", "index.html#guide"),
    ("計算量", "complexity/index.html"),
    ("ソート", "index.html#sorting"),
    ("探索", "index.html#searching"),
]


def bars_items(values, states=None):
    states = states or {}
    return [{"value": value, "label": str(value), "state": states.get(i, "default")} for i, value in enumerate(values)]


def cell_items(labels, states=None, subs=None):
    states = states or {}
    subs = subs or {}
    return [{"label": str(label), "sub": subs.get(i, ""), "state": states.get(i, "default")} for i, label in enumerate(labels)]


def cards_items(items):
    return [{"title": title, "text": text, "state": state} for title, text, state in items]


def bubble_sort_frames(values):
    arr = list(values)
    frames = []
    comparisons = 0
    swaps = 0
    passes = 0
    n = len(arr)

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comparisons += 1
            active_states = {j: "active", j + 1: "active"}
            for idx in range(n - i, n):
                active_states[idx] = "sorted"
            frames.append({
                "kind": "bars",
                "line": 2,
                "caption": f"{arr[j]} と {arr[j + 1]} を比べます。",
                "stats": [["比較", str(comparisons)], ["交換", str(swaps)], ["パス", str(passes)]],
                "payload": {"items": bars_items(arr, active_states)},
            })
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
                swap_states = {j: "swap", j + 1: "swap"}
                for idx in range(n - i, n):
                    swap_states[idx] = "sorted"
                frames.append({
                    "kind": "bars",
                    "line": 4,
                    "caption": f"{arr[j]} と {arr[j + 1]} の位置が入れ替わりました。",
                    "stats": [["比較", str(comparisons)], ["交換", str(swaps)], ["パス", str(passes)]],
                    "payload": {"items": bars_items(arr, swap_states)},
                })
        passes += 1
        pass_states = {n - 1 - i: "sorted"}
        for idx in range(n - i, n):
            pass_states[idx] = "sorted"
        frames.append({
            "kind": "bars",
            "line": 5,
            "caption": f"{arr[n - 1 - i]} が右端で確定しました。",
            "stats": [["比較", str(comparisons)], ["交換", str(swaps)], ["パス", str(passes)]],
            "payload": {"items": bars_items(arr, pass_states)},
        })
        if not swapped:
            break

    final_states = {idx: "sorted" for idx in range(n)}
    frames.append({
        "kind": "bars",
        "line": 5,
        "caption": "整列が完了しました。",
        "stats": [["比較", str(comparisons)], ["交換", str(swaps)], ["パス", str(passes)]],
        "payload": {"items": bars_items(arr, final_states)},
    })
    return frames


def selection_sort_frames(values):
    arr = list(values)
    frames = []
    comparisons = 0
    swaps = 0
    passes = 0
    n = len(arr)

    for i in range(n - 1):
        min_index = i
        start_states = {idx: "sorted" for idx in range(i)}
        start_states[min_index] = "swap"
        frames.append({
            "kind": "bars",
            "line": 2,
            "caption": f"{arr[min_index]} をいまの最小候補にします。",
            "stats": [["n", str(n)], ["比較", str(comparisons)], ["交換", str(swaps)], ["パス", str(passes)]],
            "payload": {"items": bars_items(arr, start_states)},
        })
        for j in range(i + 1, n):
            comparisons += 1
            compare_states = {idx: "sorted" for idx in range(i)}
            compare_states[min_index] = "swap"
            compare_states[j] = "active"
            frames.append({
                "kind": "bars",
                "line": 4,
                "caption": f"{arr[j]} と最小候補 {arr[min_index]} を比べます。",
                "stats": [["n", str(n)], ["比較", str(comparisons)], ["交換", str(swaps)], ["パス", str(passes)]],
                "payload": {"items": bars_items(arr, compare_states)},
            })
            if arr[j] < arr[min_index]:
                min_index = j
                update_states = {idx: "sorted" for idx in range(i)}
                update_states[min_index] = "swap"
                frames.append({
                    "kind": "bars",
                    "line": 5,
                    "caption": f"{arr[min_index]} が新しい最小候補になりました。",
                    "stats": [["n", str(n)], ["比較", str(comparisons)], ["交換", str(swaps)], ["パス", str(passes)]],
                    "payload": {"items": bars_items(arr, update_states)},
                })
        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            swaps += 1
            swap_states = {idx: "sorted" for idx in range(i)}
            swap_states[i] = "swap"
            swap_states[min_index] = "swap"
            frames.append({
                "kind": "bars",
                "line": 6,
                "caption": f"最小値 {arr[i]} を先頭へ移動しました。",
                "stats": [["n", str(n)], ["比較", str(comparisons)], ["交換", str(swaps)], ["パス", str(passes)]],
                "payload": {"items": bars_items(arr, swap_states)},
            })
        passes += 1
        sorted_states = {idx: "sorted" for idx in range(i + 1)}
        frames.append({
            "kind": "bars",
            "line": 6,
            "caption": f"{arr[i]} が位置 {i} で確定しました。",
            "stats": [["n", str(n)], ["比較", str(comparisons)], ["交換", str(swaps)], ["パス", str(passes)]],
            "payload": {"items": bars_items(arr, sorted_states)},
        })

    final_states = {idx: "sorted" for idx in range(n)}
    frames.append({
        "kind": "bars",
        "line": 6,
        "caption": "整列が完了しました。",
        "stats": [["n", str(n)], ["比較", str(comparisons)], ["交換", str(swaps)], ["パス", str(passes)]],
        "payload": {"items": bars_items(arr, final_states)},
    })
    return frames


def insertion_sort_frames(values):
    arr = list(values)
    frames = []
    comparisons = 0
    shifts = 0
    passes = 0
    n = len(arr)

    for i in range(1, n):
        key = arr[i]
        j = i - 1
        start_states = {idx: "sorted" for idx in range(i)}
        start_states[i] = "swap"
        frames.append({
            "kind": "bars",
            "line": 2,
            "caption": f"{key} を key として取り出します。",
            "stats": [["n", str(n)], ["比較", str(comparisons)], ["ずらし", str(shifts)], ["整列済み", str(i)]],
            "payload": {"items": bars_items(arr, start_states)},
        })

        while j >= 0:
            comparisons += 1
            compare_states = {idx: "sorted" for idx in range(i)}
            compare_states[j] = "active"
            compare_states[j + 1] = "swap"
            frames.append({
                "kind": "bars",
                "line": 3,
                "caption": f"{arr[j]} と key {key} を比べます。",
                "stats": [["n", str(n)], ["比較", str(comparisons)], ["ずらし", str(shifts)], ["整列済み", str(i)]],
                "payload": {"items": bars_items(arr, compare_states)},
            })
            if arr[j] > key:
                arr[j + 1] = arr[j]
                shifts += 1
                shift_states = {idx: "sorted" for idx in range(i)}
                shift_states[j] = "active"
                shift_states[j + 1] = "swap"
                frames.append({
                    "kind": "bars",
                    "line": 4,
                    "caption": f"{arr[j]} を右へずらします。",
                    "stats": [["n", str(n)], ["比較", str(comparisons)], ["ずらし", str(shifts)], ["整列済み", str(i)]],
                    "payload": {"items": bars_items(arr, shift_states)},
                })
                j -= 1
            else:
                break

        arr[j + 1] = key
        passes += 1
        insert_states = {idx: "sorted" for idx in range(i + 1)}
        frames.append({
            "kind": "bars",
            "line": 5,
            "caption": f"{key} を位置 {j + 1} に差し込みました。",
            "stats": [["n", str(n)], ["比較", str(comparisons)], ["ずらし", str(shifts)], ["整列済み", str(i + 1)]],
            "payload": {"items": bars_items(arr, insert_states)},
        })

    final_states = {idx: "sorted" for idx in range(n)}
    frames.append({
        "kind": "bars",
        "line": 5,
        "caption": "整列が完了しました。",
        "stats": [["n", str(n)], ["比較", str(comparisons)], ["ずらし", str(shifts)], ["整列済み", str(n)]],
        "payload": {"items": bars_items(arr, final_states)},
    })
    return frames


def merge_sort_frames(values):
    arr = list(values)
    frames = []
    comparisons = 0

    def add_frame(line, caption, state_map=None):
        states = state_map or {}
        frames.append({
            "kind": "bars",
            "line": line,
            "caption": caption,
            "stats": [["n", str(len(arr))], ["比較", str(comparisons)]],
            "payload": {"items": bars_items(arr, states)},
        })

    def merge_sort(left, right):
        nonlocal comparisons
        if right - left <= 1:
          return
        mid = (left + right) // 2
        split_states = {idx: "active" for idx in range(left, mid)}
        for idx in range(mid, right):
            split_states[idx] = "swap"
        add_frame(1, f"{left}..{mid - 1} と {mid}..{right - 1} に分けます。", split_states)
        merge_sort(left, mid)
        merge_sort(mid, right)
        temp = []
        i = left
        j = mid
        while i < mid and j < right:
            comparisons += 1
            compare_states = {idx: "active" for idx in range(left, right)}
            compare_states[i] = "active"
            compare_states[j] = "swap"
            add_frame(4, f"{arr[i]} と {arr[j]} を比べて小さい方を先に入れます。", compare_states)
            if arr[i] <= arr[j]:
                temp.append(arr[i])
                i += 1
            else:
                temp.append(arr[j])
                j += 1
        temp.extend(arr[i:mid])
        temp.extend(arr[j:right])
        arr[left:right] = temp
        merged_states = {idx: "sorted" for idx in range(left, right)}
        add_frame(4, f"{left}..{right - 1} が整列済みになりました。", merged_states)

    merge_sort(0, len(arr))
    add_frame(4, "整列が完了しました。", {idx: "sorted" for idx in range(len(arr))})
    return frames


def quick_sort_frames(values):
    arr = list(values)
    frames = []
    comparisons = 0
    swaps = 0

    def add_frame(line, caption, state_map=None):
        states = state_map or {}
        frames.append({
            "kind": "bars",
            "line": line,
            "caption": caption,
            "stats": [["n", str(len(arr))], ["比較", str(comparisons)], ["交換", str(swaps)]],
            "payload": {"items": bars_items(arr, states)},
        })

    def quick_sort(low, high):
        nonlocal comparisons, swaps
        if low >= high:
            if low == high:
                add_frame(4, f"{arr[low]} がこの範囲で確定しました。", {low: "sorted"})
            return
        pivot = arr[high]
        add_frame(1, f"pivot に {pivot} を選びます。", {high: "swap"})
        i = low
        for j in range(low, high):
            comparisons += 1
            state = {high: "swap", j: "active"}
            if i < len(arr):
                state[i] = "frontier"
            add_frame(2, f"{arr[j]} を pivot {pivot} と比べます。", state)
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                swaps += 1
                add_frame(2, f"{arr[i]} を左側グループへ送ります。", {i: "swap", j: "swap", high: "frontier"})
                i += 1
        arr[i], arr[high] = arr[high], arr[i]
        swaps += 1
        add_frame(2, f"pivot {arr[i]} を位置 {i} に置きます。", {i: "sorted"})
        quick_sort(low, i - 1)
        quick_sort(i + 1, high)

    quick_sort(0, len(arr) - 1)
    add_frame(4, "整列が完了しました。", {idx: "sorted" for idx in range(len(arr))})
    return frames


def heap_sort_frames(values):
    arr = list(values)
    frames = []
    comparisons = 0
    swaps = 0
    n = len(arr)
    heap_size = n

    def state_map(*active, sorted_from=None):
        states = {}
        for idx in active:
            if idx is not None and 0 <= idx < len(arr):
                states[idx] = "active"
        if sorted_from is not None:
            for idx in range(sorted_from, len(arr)):
                states[idx] = "sorted"
        return states

    def add_frame(line, caption, states=None):
        frames.append({
            "kind": "bars",
            "line": line,
            "caption": caption,
            "stats": [["n", str(n)], ["比較", str(comparisons)], ["交換", str(swaps)], ["heap", str(heap_size)]],
            "payload": {"items": bars_items(arr, states or {})},
        })

    def heapify(size, root):
        nonlocal comparisons, swaps
        while True:
            largest = root
            left = 2 * root + 1
            right = 2 * root + 2
            if left < size:
                comparisons += 1
                add_frame(4, f"{arr[root]} と左の子 {arr[left]} を比べます。", state_map(root, left, sorted_from=size))
                if arr[left] > arr[largest]:
                    largest = left
            if right < size:
                comparisons += 1
                add_frame(4, f"{arr[largest]} と右の子 {arr[right]} を比べます。", state_map(largest, right, sorted_from=size))
                if arr[right] > arr[largest]:
                    largest = right
            if largest == root:
                break
            arr[root], arr[largest] = arr[largest], arr[root]
            swaps += 1
            add_frame(4, f"{arr[root]} と {arr[largest]} を入れ替えてヒープ条件を回復します。", {**state_map(sorted_from=size), root: "swap", largest: "swap"})
            root = largest

    for start in range(n // 2 - 1, -1, -1):
        add_frame(1, f"位置 {start} から下を max heap に整えます。", state_map(start, sorted_from=heap_size))
        heapify(heap_size, start)

    add_frame(1, "max heap ができました。", {0: "swap"})

    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        swaps += 1
        heap_size = end
        add_frame(2, f"最大値 {arr[end]} を末尾 {end} へ送ります。", {0: "swap", end: "sorted", **state_map(sorted_from=end + 1)})
        heapify(heap_size, 0)

    add_frame(4, "整列が完了しました。", {idx: "sorted" for idx in range(n)})
    return frames


def counting_sort_frames(values):
    arr = list(values)
    frames = []
    max_value = max(arr) if arr else 0
    counts = [0] * (max_value + 1)
    output = []

    def payload(highlight=None):
        highlight = highlight or {}
        items = []
        for index, value in enumerate(arr):
            state = highlight.get(("arr", index), "default")
            items.append({"value": value, "label": str(value), "state": state})
        for value in range(1, len(counts)):
            state = highlight.get(("count", value), "dim")
            items.append({"value": max(1, counts[value]), "label": f"c{value}:{counts[value]}", "state": state})
        for index, value in enumerate(output):
            state = highlight.get(("out", index), "sorted")
            items.append({"value": value, "label": f"o{index}:{value}", "state": state})
        return {"items": items}

    for index, value in enumerate(arr):
        counts[value] += 1
        frames.append({
            "kind": "bars",
            "line": 1,
            "caption": f"{value} を読んで count[{value}] を 1 増やします。",
            "stats": [["n", str(len(arr))], ["読んだ要素", str(index + 1)], ["出力済み", str(len(output))]],
            "payload": payload({("arr", index): "active", ("count", value): "swap"}),
        })

    for value in range(1, len(counts)):
        if counts[value] == 0:
            continue
        frames.append({
            "kind": "bars",
            "line": 2,
            "caption": f"値 {value} は {counts[value]} 個あります。",
            "stats": [["n", str(len(arr))], ["count", f"{value} -> {counts[value]}"], ["出力済み", str(len(output))]],
            "payload": payload({("count", value): "active"}),
        })
        for _ in range(counts[value]):
            output.append(value)
            frames.append({
                "kind": "bars",
                "line": 3,
                "caption": f"{value} を出力列へ並べます。",
                "stats": [["n", str(len(arr))], ["count", f"{value} -> {counts[value]}"], ["出力済み", str(len(output))]],
                "payload": payload({("count", value): "active", ("out", len(output) - 1): "sorted"}),
            })

    frames.append({
        "kind": "bars",
        "line": 3,
        "caption": "整列が完了しました。",
        "stats": [["n", str(len(arr))], ["種類数", str(max_value)], ["出力済み", str(len(output))]],
        "payload": {"items": [{"value": value, "label": str(value), "state": "sorted"} for value in output]},
    })
    return frames


def radix_sort_frames(values):
    arr = list(values)
    frames = []
    max_value = max(arr) if arr else 0
    exp = 1
    pass_count = 0

    def payload(active_indices=None, sorted_indices=None):
        active_indices = set(active_indices or [])
        sorted_indices = set(sorted_indices or [])
        items = []
        for index, value in enumerate(arr):
            digit = (value // exp) % 10
            state = "default"
            if index in active_indices:
                state = "active"
            if index in sorted_indices:
                state = "sorted"
            items.append({"value": value, "label": f"{value}|{digit}", "state": state})
        return {"items": items}

    while max_value // exp > 0:
        pass_count += 1
        buckets = [[] for _ in range(10)]
        for index, value in enumerate(arr):
            digit = (value // exp) % 10
            buckets[digit].append(value)
            frames.append({
                "kind": "bars",
                "line": 1,
                "caption": f"{value} の {exp} の位は {digit} です。",
                "stats": [["n", str(len(arr))], ["桁", str(exp)], ["パス", str(pass_count)]],
                "payload": payload(active_indices={index}),
            })
        rebuilt = []
        for digit, bucket in enumerate(buckets):
            if not bucket:
                continue
            rebuilt.extend(bucket)
            arr[:] = rebuilt + [v for other in buckets[digit + 1:] for v in []] + [v for v in arr if v not in rebuilt]
            frames.append({
                "kind": "bars",
                "line": 2,
                "caption": f"{exp} の位が {digit} のものを前から並べます。",
                "stats": [["n", str(len(arr))], ["桁", str(exp)], ["パス", str(pass_count)]],
                "payload": {"items": [{"value": value, "label": str(value), "state": "sorted" if i < len(rebuilt) else "default"} for i, value in enumerate(rebuilt + [v for b in buckets[digit + 1:] for v in b])]},
            })
        arr[:] = [value for bucket in buckets for value in bucket]
        frames.append({
            "kind": "bars",
            "line": 2,
            "caption": f"{exp} の位で安定に並べ終わりました。",
            "stats": [["n", str(len(arr))], ["桁", str(exp)], ["パス", str(pass_count)]],
            "payload": payload(sorted_indices=set(range(len(arr)))),
        })
        exp *= 10

    frames.append({
        "kind": "bars",
        "line": 2,
        "caption": "整列が完了しました。",
        "stats": [["n", str(len(arr))], ["桁パス", str(pass_count)], ["最大値", str(max_value)]],
        "payload": {"items": [{"value": value, "label": str(value), "state": "sorted"} for value in arr]},
    })
    return frames


GRAPH_BASE = {
    "nodes": [
        {"id": "A", "label": "A", "x": 80, "y": 60},
        {"id": "B", "label": "B", "x": 220, "y": 50},
        {"id": "C", "label": "C", "x": 360, "y": 70},
        {"id": "D", "label": "D", "x": 140, "y": 190},
        {"id": "E", "label": "E", "x": 290, "y": 170},
        {"id": "F", "label": "F", "x": 450, "y": 190},
    ],
    "edges": [
        {"from": "A", "to": "B", "label": "2"},
        {"from": "A", "to": "D", "label": "1"},
        {"from": "B", "to": "C", "label": "3"},
        {"from": "B", "to": "E", "label": "2"},
        {"from": "D", "to": "E", "label": "2"},
        {"from": "E", "to": "C", "label": "1"},
        {"from": "E", "to": "F", "label": "4"},
        {"from": "C", "to": "F", "label": "2"},
    ],
}


TREE_BASE = {
    "nodes": [
        {"id": "8", "label": "8", "x": 270, "y": 40},
        {"id": "3", "label": "3", "x": 150, "y": 120},
        {"id": "10", "label": "10", "x": 390, "y": 120},
        {"id": "1", "label": "1", "x": 90, "y": 210},
        {"id": "6", "label": "6", "x": 210, "y": 210},
        {"id": "14", "label": "14", "x": 450, "y": 210},
    ],
    "edges": [
        {"from": "8", "to": "3"},
        {"from": "8", "to": "10"},
        {"from": "3", "to": "1"},
        {"from": "3", "to": "6"},
        {"from": "10", "to": "14"},
    ],
}


def graph_payload(node_states=None, edge_states=None, labels=True):
    node_states = node_states or {}
    edge_states = edge_states or {}
    nodes = []
    for node in GRAPH_BASE["nodes"]:
        copied = dict(node)
        copied["state"] = node_states.get(node["id"], "default")
        nodes.append(copied)
    edges = []
    for edge in GRAPH_BASE["edges"]:
        copied = dict(edge)
        copied["state"] = edge_states.get((edge["from"], edge["to"]), edge_states.get((edge["to"], edge["from"]), "default"))
        if not labels:
            copied.pop("label", None)
        edges.append(copied)
    return {"nodes": nodes, "edges": edges}


def tree_payload(node_states=None, edge_states=None):
    node_states = node_states or {}
    edge_states = edge_states or {}
    nodes = []
    for node in TREE_BASE["nodes"]:
        copied = dict(node)
        copied["state"] = node_states.get(node["id"], "default")
        nodes.append(copied)
    edges = []
    for edge in TREE_BASE["edges"]:
        copied = dict(edge)
        copied["state"] = edge_states.get((edge["from"], edge["to"]), "default")
        edges.append(copied)
    return {"nodes": nodes, "edges": edges}


PAGES = [
    {
        "slug": "complexity",
        "title": "計算量の概念",
        "nav_title": "計算量",
        "category": "Concepts",
        "eyebrow": "Concept / Complexity",
        "hero_title": "計算量は、\nデータが増えたときに\nどれだけ大変になるか。",
        "description": "計算量は、プログラムの大変さを表す目安です。まずは『Big-O は計算量を書くための記号』だと捉えれば十分です。",
        "pills": ["まずは Big-O", "増え方を見る", "初学者向け導入"],
        "observe": [
            "計算量は処理回数の増え方を見る",
            "Big-O はその書き方のひとつ",
            "小さい入力では差が見えにくい",
        ],
        "legend": [("ゆるやか", "active"), ("急増", "swap"), ("安定", "sorted")],
        "pseudocode_title": "考え方の流れ",
        "pseudocode": [
            "入力サイズ n を大きくして考える",
            "処理回数がどう増えるかを見る",
            "その増え方を Big-O で表す",
            "O(log n), O(n), O(n²) の違いを比べる",
        ],
        "facts": [
            ("計算量", "処理回数の増え方"),
            ("Big-O", "計算量の表し方"),
            ("まず比べるもの", "O(log n), O(n), O(n²)"),
            ("最初の目標", "違いを感覚でつかむ"),
        ],
        "explain": [
            ("ここだけ覚える", "計算量は『どれだけ仕事が増えるか』、Big-O は『その増え方の書き方』です。"),
            ("見方", "まずは『データが2倍になったら、仕事量は何倍くらいになるか』で考えると理解しやすいです。"),
            ("注意", "O(n²) は『n²秒』という意味ではありません。処理回数の増え方を表しています。"),
        ],
        "extra_sections": [
            {
                "eyebrow": "What Is Complexity",
                "title": "計算量は「大変さ」の目安",
                "paragraphs": [
                    "計算量とは、そのプログラムがどれくらいたくさん仕事をするかを表す目安です。",
                    "ここでいう仕事とは、たとえば『何回比べるか』『何回探すか』『何回入れ替えるか』のような回数のことです。",
                    "つまり計算量は、プログラムの速さを直接書くというより、『仕事量がどう増えるか』を見るためのものです。"
                ],
            },
            {
                "eyebrow": "Big-O",
                "title": "Big-O は計算量を書くための記号",
                "paragraphs": [
                    "Big-O は、計算量を書くときによく使う記号です。O(n) や O(n²) のように書きます。",
                    "大切なのは、Big-O 自体がアルゴリズムの名前ではなく、『計算量を表す書き方』だということです。",
                    "最初は『データが増えたとき、仕事量がどんなふうに増えるかを書く記号』と考えれば十分です。"
                ],
            },
            {
                "eyebrow": "Why Growth Matters",
                "title": "なぜ「増え方」を見るのか",
                "paragraphs": [
                    "10件のデータでは、どの方法もすぐ終わるように見えることがあります。",
                    "でも 1000件、10000件と増えていくと、方法によって仕事量の増え方に大きな差が出ます。",
                    "その差を見るために、計算量では『今どれくらい速いか』より『増えたときにどうなるか』を重視します。"
                ],
            },
            {
                "eyebrow": "Concrete Examples",
                "title": "よく出る3つの形",
                "cards": [
                    ("O(log n)", "候補を半分ずつ減らす形です。データが増えても、仕事量は少しずつしか増えません。"),
                    ("O(n)", "1つずつ順に見る形です。データが2倍になると、仕事量もだいたい2倍になります。"),
                    ("O(n²)", "全体を何度も見比べる形です。データが増えると、仕事量が急に大きくなります。")
                ],
            },
            {
                "eyebrow": "How To Read",
                "title": "O(n) や O(n²) はどう読む？",
                "cards": [
                    ("O(1)", "データが増えても、仕事量がほとんど増えない。"),
                    ("O(n)", "データが2倍なら、仕事量もだいたい2倍。"),
                    ("O(n²)", "データが2倍になると、仕事量は4倍くらい。"),
                ],
            },
            {
                "eyebrow": "Important Note",
                "title": "小さい入力では差が見えにくい",
                "paragraphs": [
                    "10件や20件くらいの小さいデータでは、O(n) と O(n²) の差があまり目立たないことがあります。",
                    "しかし、データが増えると O(n²) は急に苦しくなります。だから『今は速かった』だけで判断しないことが大切です。"
                ],
            },
            {
                "eyebrow": "Common Mistakes",
                "title": "初学者が誤解しやすい点",
                "bullets": [
                    "O(n²) は『n² 秒かかる』という意味ではない",
                    "今の入力で速かったことと、大きい入力でも強いことは別",
                    "Big-O は便利だが、平均ケースや定数倍を完全に無視してよいわけではない",
                    "アルゴリズムによっては最良・平均・最悪を分けて考える必要がある"
                ],
            },
        ],
        "pre_visual_sections": [
            {
                "eyebrow": "First Read",
                "title": "最初にこれだけ読めばよい",
                "paragraphs": [
                    "計算量は、プログラムの処理回数がどう増えるかを表します。",
                    "Big-O は、その計算量を書くための記号です。",
                    "最初は O(n) や O(n²) を見て、『データが増えたら仕事量がどう増えるか』を読むことができれば十分です。"
                ],
                "cards": [
                    ("計算量", "処理回数の増え方"),
                    ("Big-O", "計算量の書き方"),
                    ("見るもの", "入力が増えたときの変化")
                ],
            }
        ],
        "frames": [
            {"kind": "cards", "line": 1, "caption": "まずは何を比べるのかを言葉で掴みます。", "stats": [["例", "名簿探索"], ["見たいもの", "増え方"]], "payload": {"items": cards_items([("O(log n)", "半分ずつ絞るので増え方が緩やか", "active"), ("O(n)", "先頭から順に見るのでほぼ比例", "default"), ("O(n²)", "全員を全員と比べるので急増", "swap")])}},
            {"kind": "grid", "line": 2, "caption": "n が大きくなるほど差が開きます。", "stats": [["n", "10 / 100 / 1000"], ["比較の軸", "おおよその回数"]], "payload": {"rows": [[{"text": "式", "state": "default"}, {"text": "10", "state": "default"}, {"text": "100", "state": "default"}, {"text": "1000", "state": "default"}], [{"text": "O(log n)", "state": "active"}, {"text": "約3", "state": "active"}, {"text": "約7", "state": "active"}, {"text": "約10", "state": "active"}], [{"text": "O(n)", "state": "default"}, {"text": "10", "state": "default"}, {"text": "100", "state": "default"}, {"text": "1000", "state": "default"}], [{"text": "O(n²)", "state": "swap"}, {"text": "100", "state": "swap"}, {"text": "10000", "state": "swap"}, {"text": "1000000", "state": "swap"}]]}},
            {"kind": "cards", "line": 4, "caption": "Big-O は『最大でこのくらいの増え方』と読めば入門として十分です。", "stats": [["Big-O", "先に覚える"], ["Big-Theta", "後でよい"]], "payload": {"items": cards_items([("O(f(n))", "最大でこのくらいの増え方", "found"), ("Θ(f(n))", "ちょうどこの増え方", "default"), ("Ω(f(n))", "少なくともこのくらい必要", "default")])}},
        ],
    },
    {
        "slug": "stable-sort",
        "title": "安定ソートとは",
        "nav_title": "安定ソート",
        "category": "Concepts",
        "eyebrow": "Concept / Stable Sort",
        "hero_title": "同じ値の順序を\n保つかどうか。",
        "description": "値が同じ要素に元の順序があるとき、その順序を保つソートを安定ソートと呼びます。複数キーの並べ替えで重要になります。",
        "pills": ["複数キーで重要", "Bubble は安定", "Selection は基本不安定"],
        "observe": ["同じ点数でも出席番号の順が残るかを見る", "値だけでなく元の並びも追う", "教材ではラベル付き要素で示す"],
        "legend": [("元の順序保持", "sorted"), ("順序が崩れる", "swap")],
        "pseudocode_title": "見てほしい視点",
        "pseudocode": ["同じ値をラベル付きで用意する", "ソート後もラベル順が保たれるか見る", "複数条件ソートで使いどころを考える"],
        "facts": [("テーマ", "横断概念"), ("重要場面", "複数キーの整列"), ("安定例", "Bubble / Insertion / Merge"), ("不安定例", "Selection / Heap / Quick の一般実装")],
        "explain": [("何が嬉しいか", "たとえば学年順に並べたあと点数順に並べても、同点内では学年順が残せます。"), ("どう教えるか", "同じ値を色やラベルで区別してから並べ替えると伝わりやすいです。"), ("注意", "不安定ソートでも実装次第で工夫はできますが、基本性質としては区別して教えるのがよいです。")],
        "frames": [
            {"kind": "cells", "line": 1, "caption": "同じ 80 点でも A と B には元の順序があります。", "stats": [["並び", "80A, 60C, 80B, 90D"]], "payload": {"items": cell_items(["80", "60", "80", "90"], {0: "active", 2: "active"}, {0: "A", 1: "C", 2: "B", 3: "D"})}},
            {"kind": "cells", "line": 2, "caption": "安定ソートでは 80A が 80B より前のままです。", "stats": [["安定", "順序保持"]], "payload": {"items": cell_items(["60", "80", "80", "90"], {1: "sorted", 2: "sorted"}, {0: "C", 1: "A", 2: "B", 3: "D"})}},
            {"kind": "cells", "line": 3, "caption": "不安定ソートでは同じ値の順序が崩れることがあります。", "stats": [["不安定", "順序逆転"]], "payload": {"items": cell_items(["60", "80", "80", "90"], {1: "swap", 2: "swap"}, {0: "C", 1: "B", 2: "A", 3: "D"})}},
        ],
    },
    {
        "slug": "recursion",
        "title": "再帰の考え方",
        "nav_title": "再帰",
        "category": "Concepts",
        "eyebrow": "Concept / Recursion",
        "hero_title": "小さい同じ問題に\n分けて、自分を呼ぶ。",
        "description": "再帰は、問題を小さくして同じ形で解く考え方です。停止条件と再帰呼び出しが揃ってはじめて正しく動きます。",
        "pills": ["停止条件が必要", "木で考えると見やすい", "DP とも接続する"],
        "observe": ["どこで止まるか", "1回呼ぶごとに何が小さくなるか", "戻りながら値が組み立つ様子"],
        "legend": [("今いる呼び出し", "active"), ("完了済み", "sorted")],
        "pseudocode_title": "再帰の最小形",
        "pseudocode": ["if 問題が十分小さいなら直接答える", "そうでなければ、少し小さい同じ問題を解く", "小さい答えから元の答えを組み立てる"],
        "facts": [("テーマ", "横断概念"), ("重要", "停止条件"), ("図", "再帰木"), ("関連", "分割統治 / DP")],
        "explain": [("よくある失敗", "停止条件がない、または問題が小さくならないと無限に呼び出します。"), ("教え方", "コードだけでなく呼び出し木を一緒に見ると理解しやすいです。"), ("次の接続", "同じ部分問題を何度も解くとき、メモ化や DP につながります。")],
        "frames": [
            {"kind": "cards", "line": 1, "caption": "まずは停止条件が必要です。", "stats": [["例", "factorial(1)"], ["役割", "これ以上分けない"]], "payload": {"items": cards_items([("停止条件", "n = 1 なら 1 を返す", "found"), ("再帰呼び出し", "n * factorial(n - 1)", "active"), ("組み立て", "小さい答えから戻る", "default")])}},
            {"kind": "tree", "line": 2, "caption": "呼び出しは木として考えると見やすいです。", "stats": [["現在", "factorial(3)"], ["次", "factorial(2)"]], "payload": tree_payload({"8": "default", "3": "active", "1": "sorted", "6": "default", "10": "default", "14": "default"}, {("8", "3"): "active", ("3", "1"): "sorted"})},
            {"kind": "cards", "line": 3, "caption": "戻りながら答えを組み立てます。", "stats": [["戻り", "1 -> 2 -> 6"]], "payload": {"items": cards_items([("factorial(1)", "1 を返す", "sorted"), ("factorial(2)", "2 * 1 = 2", "sorted"), ("factorial(3)", "3 * 2 = 6", "active")])}},
        ],
    },
    {
        "slug": "memoization",
        "title": "メモ化",
        "nav_title": "メモ化",
        "category": "Concepts",
        "eyebrow": "Concept / Memoization",
        "hero_title": "同じ部分問題を\n何度も解かない。",
        "description": "再帰で同じ計算を繰り返すと急に重くなります。メモ化は、一度求めた結果を保存して再利用する方法です。",
        "pills": ["再帰の高速化", "同じ入力を再計算しない", "DP の入口"],
        "observe": ["重複している部分問題を探す", "保存して使い回せる値を見つける", "再帰木がどれだけ減るか見る"],
        "legend": [("未計算", "default"), ("計算中", "active"), ("メモ済み", "sorted")],
        "pseudocode_title": "最小形",
        "pseudocode": ["if メモにあるなら返す", "なければ再帰で求める", "結果をメモに保存する", "保存した結果を返す"],
        "facts": [("テーマ", "横断概念"), ("典型例", "Fibonacci"), ("効果", "重複計算の削減"), ("接続", "Top-down DP")],
        "explain": [("なぜ効くか", "同じ引数で同じ結果が出るなら、2回目以降は再計算不要だからです。"), ("授業の見せ方", "メモなしの再帰木と、メモありの計算済み表を並べると差が出ます。"), ("注意点", "保存領域を使うので、空間計算量とのトレードオフがあります。")],
        "frames": [
            {"kind": "cards", "line": 1, "caption": "メモがなければ毎回計算します。", "stats": [["fib(5)", "重複多数"]], "payload": {"items": cards_items([("fib(5)", "fib(4) + fib(3)", "active"), ("fib(4)", "あとでまた必要", "swap"), ("fib(3)", "こちらも重複", "swap")])}},
            {"kind": "grid", "line": 3, "caption": "一度計算した値を表に保存します。", "stats": [["memo[2]", "1"], ["memo[3]", "2"], ["memo[4]", "3"]], "payload": {"rows": [[{"text": "n", "state": "default"}, {"text": "0", "state": "default"}, {"text": "1", "state": "default"}, {"text": "2", "state": "sorted"}, {"text": "3", "state": "sorted"}, {"text": "4", "state": "sorted"}], [{"text": "fib(n)", "state": "default"}, {"text": "0", "state": "default"}, {"text": "1", "state": "default"}, {"text": "1", "state": "sorted"}, {"text": "2", "state": "sorted"}, {"text": "3", "state": "sorted"}]]}},
            {"kind": "cards", "line": 4, "caption": "次に同じ値が要るときは、表から返します。", "stats": [["再利用", "計算不要"]], "payload": {"items": cards_items([("fib(4)", "表から 3 を返す", "found"), ("fib(3)", "表から 2 を返す", "found"), ("全体", "再帰木がかなり減る", "active")])}},
        ],
    },
]


def add_page(page):
    PAGES.append(page)


add_page({
    "slug": "bubble-sort",
    "title": "Bubble Sort",
    "nav_title": "Bubble Sort",
    "category": "Sorting",
    "eyebrow": "Sorting / Bubble Sort",
    "hero_title": "隣同士を比べて、\n大きい値を右へ送る。",
    "description": "左から隣接要素を比べ、逆順なら交換します。1 パス終わるごとに未確定部分の最大値が右端へ確定します。",
    "pills": ["安定ソート", "in-place", "最悪 O(n²)"],
    "observe": ["比較中の 2 本を見る", "交換が起きる条件を見る", "右端が 1 本ずつ確定する流れを見る"],
    "legend": [("比較中", "active"), ("交換", "swap"), ("確定済み", "sorted")],
    "pseudocode_title": "擬似コード",
    "pseudocode": ["for i = 0 to n - 2", "  for j = 0 to n - 2 - i", "    if a[j] > a[j + 1]", "      swap a[j], a[j + 1]", "  mark last unsorted item as sorted"],
    "facts": [("Best", "O(n) with early exit"), ("Average", "O(n²)"), ("Worst", "O(n²)"), ("Stable", "Yes")],
    "explain": [("なぜ遅いか", "ほぼ毎パスで未整列部分をなめるので、比較回数が二次的に増えます。"), ("でも導入向き", "比較、交換、確定という基本概念がそのまま見えるからです。"), ("見るべき点", "最大値が泡のように右へ浮いていく感覚を掴むと定着します。")],
    "generator": "bubble-sort",
    "default_n": 12,
    "variants": [
        {"label": "n = 5", "frames": bubble_sort_frames([12, 44, 31, 8, 27])},
        {"label": "n = 8", "frames": bubble_sort_frames([44, 12, 31, 8, 27, 52, 19, 3])},
        {"label": "n = 12", "frames": bubble_sort_frames([44, 12, 31, 8, 27, 52, 19, 3, 41, 6, 24, 15])},
    ],
    "frames": bubble_sort_frames([44, 12, 31, 8, 27, 52, 19, 3]),
})

add_page({
    "slug": "selection-sort",
    "title": "Selection Sort",
    "nav_title": "Selection Sort",
    "category": "Sorting",
    "eyebrow": "Sorting / Selection Sort",
    "hero_title": "未整列部分から\n最小値を探して、\n前へ置く。",
    "description": "未整列領域を最後まで見て最小値を選び、先頭と交換します。交換回数は少なめですが、比較回数は基本的に O(n²) です。",
    "pills": ["基本は不安定", "in-place", "比較回数は多い"],
    "observe": ["今の最小候補がどれか", "探索中の位置", "左から 1 つずつ確定する流れ"],
    "legend": [("探索中", "active"), ("最小候補", "swap"), ("確定済み", "sorted")],
    "pseudocode_title": "擬似コード",
    "pseudocode": ["for i = 0 to n - 2", "  minIndex = i", "  for j = i + 1 to n - 1", "    if a[j] < a[minIndex]", "      minIndex = j", "  swap a[i], a[minIndex]"],
    "facts": [("Best", "O(n²)"), ("Average", "O(n²)"), ("Worst", "O(n²)"), ("Stable", "No")],
    "explain": [("Bubble との違い", "その場で何度も交換せず、最後に最小値だけを前へ持ってきます。"), ("交換回数", "各パスで高々 1 回なので少なく見えます。"), ("比較回数", "ただし未整列部分は毎回最後まで見るため、比較回数は減りません。")],
    "generator": "selection-sort",
    "default_n": 12,
    "variants": [
        {"label": "n = 5", "frames": selection_sort_frames([29, 11, 43, 7, 18])},
        {"label": "n = 8", "frames": selection_sort_frames([29, 11, 43, 7, 18, 35, 4, 26])},
        {"label": "n = 12", "frames": selection_sort_frames([29, 11, 43, 7, 18, 35, 4, 26, 51, 9, 32, 14])},
    ],
    "frames": selection_sort_frames([29, 11, 43, 7, 18, 35, 4, 26]),
})

add_page({
    "slug": "insertion-sort",
    "title": "Insertion Sort",
    "nav_title": "Insertion Sort",
    "category": "Sorting",
    "eyebrow": "Sorting / Insertion Sort",
    "hero_title": "整列済みの列へ\n1要素ずつ差し込む。",
    "description": "新しい要素を 1 つ取り出し、左側の整列済み領域の適切な位置へ挿入します。ほぼ整列済みの入力では強いアルゴリズムです。",
    "pills": ["安定ソート", "in-place", "ほぼ整列済みに強い"],
    "observe": ["取り出した key を追う", "左へずらす要素を見る", "整列済み領域がどう広がるか"],
    "legend": [("key", "swap"), ("比較中", "active"), ("整列済み", "sorted")],
    "pseudocode_title": "擬似コード",
    "pseudocode": ["for i = 1 to n - 1", "  key = a[i]", "  while j >= 0 and a[j] > key", "    a[j + 1] = a[j]", "  a[j + 1] = key"],
    "facts": [("Best", "O(n)"), ("Average", "O(n²)"), ("Worst", "O(n²)"), ("Stable", "Yes")],
    "explain": [("どこで効くか", "すでにほぼ整列済みなら、左へ大きく動く要素が少ないため速くなります。"), ("感覚", "カードを手札に差し込む動きに近いです。"), ("Bubble との違い", "交換を連発するより、ずらして最後に挿入する発想です。")],
    "generator": "insertion-sort",
    "default_n": 12,
    "frames": insertion_sort_frames([12, 44, 31, 8, 27, 52, 19, 3, 41, 6, 24, 15]),
})

for slug, title, hero, desc, pills, observe, facts, explain, code, frames in [
    ("merge-sort", "Merge Sort", "半分に分けて解き、\n整列済みの列を\nマージする。", "分割統治の代表例です。半分ずつ再帰的に整列し、最後に 2 つの整列済み配列をマージします。", ["安定ソート", "分割統治", "O(n log n)"], ["分割される様子", "マージ時に何を比較するか", "補助配列が必要な点"], [("Best", "O(n log n)"), ("Average", "O(n log n)"), ("Worst", "O(n log n)"), ("Stable", "Yes")], [("なぜ速いか", "各段で全体を一度なめ、段数は log n 個だからです。"), ("注意点", "配列版では補助領域が必要です。"), ("教え方", "分割の木とマージの流れを分けて見せると整理しやすいです。")], ["split array into halves", "sort left half", "sort right half", "merge two sorted halves"], [
        {"kind": "bars", "line": 1, "caption": "まず配列を半分に分けます。", "stats": [["サイズ", "8 -> 4 + 4"]], "payload": {"items": bars_items([38, 27, 43, 3, 9, 82, 10, 15], {0: "active", 1: "active", 2: "active", 3: "active", 4: "swap", 5: "swap", 6: "swap", 7: "swap"})}},
        {"kind": "cards", "line": 2, "caption": "左右をそれぞれ整列済みにします。", "stats": [["左", "[3, 27, 38, 43]"], ["右", "[9, 10, 15, 82]"]], "payload": {"items": cards_items([("left", "3, 27, 38, 43", "sorted"), ("right", "9, 10, 15, 82", "sorted"), ("phase", "ここから merge", "active")])}},
        {"kind": "bars", "line": 4, "caption": "先頭同士を比べながらマージします。", "stats": [["比較", "3"], ["出力", "3, 9, 10"]], "payload": {"items": bars_items([3, 9, 10, 27, 38, 43, 15, 82], {0: "sorted", 1: "sorted", 2: "sorted", 3: "active", 6: "swap"})}},
    ]),
    ("quick-sort", "Quick Sort", "基準値 pivot で分け、\n左右を再帰的に整列する。", "pivot より小さい群と大きい群に分けていく分割統治です。平均では速いですが、pivot の選び方に偏りが出ると遅くなります。", ["平均 O(n log n)", "in-place 実装可", "pivot が重要"], ["pivot がどれか", "左右にどう分かれるか", "最悪ケースがどんなときか"], [("Best", "O(n log n)"), ("Average", "O(n log n)"), ("Worst", "O(n²)"), ("Stable", "No")], [("平均で速い理由", "分割がある程度均等なら、段数が log n 程度に収まるからです。"), ("最悪", "毎回かなり偏る分割だと二次時間になります。"), ("授業の焦点", "partition の動きが理解の中心です。")], ["choose pivot", "partition into left and right", "sort left part", "sort right part"], [
        {"kind": "bars", "line": 1, "caption": "31 を pivot に選びます。", "stats": [["pivot", "31"]], "payload": {"items": bars_items([44, 12, 31, 8, 27, 52, 19, 3], {2: "swap"})}},
        {"kind": "bars", "line": 2, "caption": "31 より小さい要素を左側へ集めます。", "stats": [["left", "12, 8, 27, 19, 3"], ["right", "44, 52"]], "payload": {"items": bars_items([12, 8, 27, 19, 3, 31, 44, 52], {5: "swap"})}},
        {"kind": "bars", "line": 4, "caption": "左右を同じように再帰的に整列します。", "stats": [["段数", "log n 程度"], ["形", "分割統治"]], "payload": {"items": bars_items([3, 8, 12, 19, 27, 31, 44, 52], {0: "sorted", 1: "sorted", 2: "sorted", 3: "sorted", 4: "sorted", 5: "sorted", 6: "sorted", 7: "sorted"})}},
    ]),
    ("heap-sort", "Heap Sort", "ヒープから最大値を\n順に取り出す。", "二分ヒープを使って最大値を何度も末尾へ送ります。比較的安定した O(n log n) ですが、安定ソートではありません。", ["O(n log n)", "in-place", "ヒープ構造を利用"], ["完全二分木として考える", "親子の大小関係を見る", "根を末尾と交換する流れ"], [("Best", "O(n log n)"), ("Average", "O(n log n)"), ("Worst", "O(n log n)"), ("Stable", "No")], [("流れ", "まずヒープを作り、その後 root を取り出して再ヒープ化します。"), ("見せ方", "木と配列の対応を並べると理解しやすいです。"), ("特徴", "最悪時も O(n log n) を保ちます。")], ["build max heap", "swap root with last element", "shrink heap", "heapify root"], [
        {"kind": "tree", "line": 1, "caption": "まず最大ヒープを作ります。", "stats": [["root", "52"], ["条件", "親 >= 子"]], "payload": tree_payload({"8": "swap", "3": "active", "10": "default", "1": "default", "6": "default", "14": "default"}, {("8", "3"): "active"})},
        {"kind": "bars", "line": 2, "caption": "最大値 52 を末尾へ送ります。", "stats": [["確定", "52"], ["残り", "7"]], "payload": {"items": bars_items([44, 27, 31, 8, 12, 19, 3, 52], {7: "sorted"})}},
        {"kind": "bars", "line": 4, "caption": "根を再びヒープ化して次の最大値を取り出します。", "stats": [["再ヒープ化", "必要"], ["計算量", "log n"]], "payload": {"items": bars_items([31, 27, 19, 8, 12, 3, 44, 52], {0: "active", 6: "sorted", 7: "sorted"})}},
    ]),
    ("counting-sort", "Counting Sort", "値そのものを比較せず、\n個数を数える。", "要素の取りうる値の範囲が狭いときに強いソートです。各値が何回出たかを数え、そこから整列済み列を組み立てます。", ["比較ソートではない", "整数向け", "範囲 k に依存"], ["配列を並べ替える前に数える", "count 配列の意味", "累積和で位置が決まる"], [("Best", "O(n + k)"), ("Average", "O(n + k)"), ("Worst", "O(n + k)"), ("Stable", "実装次第で Yes")], [("なぜ速いか", "比較を繰り返さず、値ごとの個数から位置を求めるからです。"), ("前提", "値の範囲 k が広すぎると不利です。"), ("つながり", "Radix Sort の内部でも使われます。")], ["count each value", "compute prefix sums", "place each item into output"], [
        {"kind": "cells", "line": 1, "caption": "まず各値の出現回数を数えます。", "stats": [["入力", "4 2 2 8 3 3 1"]], "payload": {"items": cell_items([4, 2, 2, 8, 3, 3, 1], {1: "active", 2: "active", 4: "swap", 5: "swap"})}},
        {"kind": "grid", "line": 2, "caption": "count 配列から累積和を作ると、各値の終端位置がわかります。", "stats": [["count", "[1,2,2,1,0,0,0,1]"]], "payload": {"rows": [[{"text": "値", "state": "default"}, {"text": "1", "state": "default"}, {"text": "2", "state": "default"}, {"text": "3", "state": "default"}, {"text": "4", "state": "default"}, {"text": "8", "state": "default"}], [{"text": "個数", "state": "default"}, {"text": "1", "state": "sorted"}, {"text": "2", "state": "sorted"}, {"text": "2", "state": "sorted"}, {"text": "1", "state": "sorted"}, {"text": "1", "state": "sorted"}], [{"text": "累積", "state": "active"}, {"text": "1", "state": "active"}, {"text": "3", "state": "active"}, {"text": "5", "state": "active"}, {"text": "6", "state": "active"}, {"text": "7", "state": "active"}]]}},
        {"kind": "cells", "line": 3, "caption": "出力配列に配置して整列します。", "stats": [["出力", "1 2 2 3 3 4 8"]], "payload": {"items": cell_items([1, 2, 2, 3, 3, 4, 8], {0: "sorted", 1: "sorted", 2: "sorted", 3: "sorted", 4: "sorted", 5: "sorted", 6: "sorted"})}},
    ]),
    ("radix-sort", "Radix Sort", "1 桁ずつ安定に並べて、\n上位桁まで仕上げる。", "各桁を下位から順に安定ソートしていく方法です。桁数が短い整数列などで有効です。", ["下位桁から処理", "安定ソートが必要", "O(d(n + k))"], ["1 の位だけを見る", "10 の位へ進む", "各段で順序がどう保存されるか"], [("Best", "O(d(n + k))"), ("Average", "O(d(n + k))"), ("Worst", "O(d(n + k))"), ("Stable", "Yes if inner sort stable")], [("ポイント", "前の桁で作った順序を崩さないため、内部で安定ソートが必要です。"), ("適用先", "固定長のキーに向きます。"), ("Counting Sort との関係", "各桁の並べ替えに Counting Sort を使うのが典型です。")], ["for each digit from LSD to MSD", "stable sort by that digit"], [
        {"kind": "cells", "line": 1, "caption": "まず 1 の位で並べます。", "stats": [["入力", "170 45 75 90 802 24 2 66"]], "payload": {"items": cell_items([170, 45, 75, 90, 802, 24, 2, 66], {1: "active", 2: "active", 4: "swap", 6: "swap"})}},
        {"kind": "cells", "line": 2, "caption": "1 の位で安定に並べるとこうなります。", "stats": [["1 の位後", "170 90 802 2 24 45 75 66"]], "payload": {"items": cell_items([170, 90, 802, 2, 24, 45, 75, 66], {0: "sorted", 1: "sorted", 2: "sorted"})}},
        {"kind": "cells", "line": 2, "caption": "次に 10 の位で並べると全体が整っていきます。", "stats": [["10 の位後", "802 2 24 45 66 170 75 90"]], "payload": {"items": cell_items([802, 2, 24, 45, 66, 170, 75, 90], {2: "active", 3: "active", 6: "swap"})}},
    ]),
]:
    add_page({
        "slug": slug,
        "title": title,
        "nav_title": title,
        "category": "Sorting",
        "eyebrow": f"Sorting / {title}",
        "hero_title": hero,
        "description": desc,
        "pills": pills,
        "observe": observe,
        "legend": [("注目", "active"), ("重要候補", "swap"), ("確定", "sorted")],
        "pseudocode_title": "擬似コード",
        "pseudocode": code,
        "facts": facts,
        "explain": explain,
        "frames": frames,
    })

for page in PAGES:
    if page["slug"] == "merge-sort":
        page["generator"] = "merge-sort"
        page["default_n"] = 12
        page["hero_title"] = "分けて並べて、\n最後にまとめる。"
        page["frames"] = merge_sort_frames([38, 27, 43, 3, 9, 82, 10, 15, 24, 50, 7, 31])
    elif page["slug"] == "quick-sort":
        page["generator"] = "quick-sort"
        page["default_n"] = 12
        page["hero_title"] = "pivot で分けて、\n左右を整列する。"
        page["frames"] = quick_sort_frames([44, 12, 31, 8, 27, 52, 19, 3, 41, 6, 24, 15])
    elif page["slug"] == "heap-sort":
        page["generator"] = "heap-sort"
        page["default_n"] = 12
        page["frames"] = heap_sort_frames([44, 12, 31, 8, 27, 52, 19, 3, 41, 6, 24, 15])
    elif page["slug"] == "counting-sort":
        page["generator"] = "counting-sort"
        page["default_n"] = 12
        page["frames"] = counting_sort_frames([7, 2, 9, 4, 1, 8, 5, 3, 6, 12, 10, 11])
    elif page["slug"] == "radix-sort":
        page["generator"] = "radix-sort"
        page["default_n"] = 20
        page["frames"] = radix_sort_frames([17, 2, 29, 14, 31, 8, 25, 43, 6, 12, 37, 20])

for slug, title, hero, desc, facts, explain, code, frames in [
    ("linear-search", "Linear Search", "先頭から順に見て、\n見つかるまで進む。", "最も単純な探索です。整列済みでなくても使えますが、最悪では全要素を見る必要があります。", [("Best", "O(1)"), ("Average", "O(n)"), ("Worst", "O(n)"), ("前提", "なし")], [("強み", "整列済みでなくても使えます。"), ("弱み", "大きな入力では候補をまとめて捨てられません。"), ("教え方", "線形に候補が減る感覚を示すのに向いています。")], ["for each item", "  if item == target return index", "return not found"], [
        {"kind": "cells", "line": 1, "caption": "先頭から順に比較します。", "stats": [["target", "19"], ["比較", "1"]], "payload": {"items": cell_items([44, 12, 31, 8, 27, 52, 19, 3], {0: "active"})}},
        {"kind": "cells", "line": 1, "caption": "見つかるまで 1 つずつ進みます。", "stats": [["target", "19"], ["比較", "7"]], "payload": {"items": cell_items([44, 12, 31, 8, 27, 52, 19, 3], {0: "dim", 1: "dim", 2: "dim", 3: "dim", 4: "dim", 5: "dim", 6: "active"})}},
        {"kind": "cells", "line": 2, "caption": "19 を見つけました。", "stats": [["index", "6"], ["比較", "7"]], "payload": {"items": cell_items([44, 12, 31, 8, 27, 52, 19, 3], {6: "found"})}},
    ]),
    ("binary-search", "Binary Search", "真ん中を見て、\n探索範囲を半分に絞る。", "整列済み配列に対して高速に探索する方法です。毎回半分の候補を捨てられるため O(log n) になります。", [("Best", "O(1)"), ("Average", "O(log n)"), ("Worst", "O(log n)"), ("前提", "整列済み")], [("なぜ速いか", "1 回比較するごとに候補が半分になるからです。"), ("前提", "整列されていないと左右どちらを捨てるか判断できません。"), ("比較対象", "Linear Search と並べると差が際立ちます。")], ["low = 0, high = n - 1", "while low <= high", "  mid = floor((low + high) / 2)", "  if a[mid] == target return mid", "  if a[mid] < target then low = mid + 1 else high = mid - 1"], [
        {"kind": "cells", "line": 3, "caption": "まず中央 31 を見ます。", "stats": [["target", "39"], ["mid", "31"]], "payload": {"items": cell_items([3, 8, 12, 17, 21, 26, 31, 39, 44, 50, 58], {5: "dim", 6: "active"})}},
        {"kind": "cells", "line": 5, "caption": "31 < 39 なので右半分だけ残します。", "stats": [["low", "7"], ["high", "10"]], "payload": {"items": cell_items([3, 8, 12, 17, 21, 26, 31, 39, 44, 50, 58], {0: "dim", 1: "dim", 2: "dim", 3: "dim", 4: "dim", 5: "dim", 6: "dim", 8: "active"})}},
        {"kind": "cells", "line": 4, "caption": "次の中央で 39 を見つけます。", "stats": [["index", "7"], ["比較", "2"]], "payload": {"items": cell_items([3, 8, 12, 17, 21, 26, 31, 39, 44, 50, 58], {7: "found", 0: "dim", 1: "dim", 2: "dim", 3: "dim", 4: "dim", 5: "dim", 6: "dim"})}},
    ]),
    ("hash-table", "Hash Table", "キーをハッシュして\nバケットへ置く。", "平均的には高速に探索できますが、衝突が起きると工夫が必要です。教材では衝突解決の考え方まで見せます。", [("Average search", "O(1)"), ("Worst search", "O(n)"), ("鍵", "良いハッシュ"), ("論点", "衝突")], [("平均が速い理由", "狙ったバケットへ直接飛べるからです。"), ("衝突", "同じ場所に複数キーが来ると連鎖や再配置が必要です。"), ("教え方", "衝突前後の見た目の変化を出すと理解しやすいです。")], ["index = hash(key) % tableSize", "if bucket occupied then resolve collision", "store or search in bucket"], [
        {"kind": "cells", "line": 1, "caption": "キーをハッシュして位置を決めます。", "stats": [["key", "21"], ["hash % 7", "0"]], "payload": {"items": cell_items(["0", "1", "2", "3", "4", "5", "6"], {0: "active"})}},
        {"kind": "cells", "line": 2, "caption": "14 と 21 が同じバケットに来て衝突します。", "stats": [["collision", "yes"], ["bucket 0", "14 -> 21"]], "payload": {"items": cell_items(["14,21", "-", "-", "10", "-", "5", "-"], {0: "swap", 3: "sorted", 5: "sorted"})}},
        {"kind": "cells", "line": 3, "caption": "連鎖法なら同じバケット内で探索します。", "stats": [["search 21", "bucket 0 only"]], "payload": {"items": cell_items(["14 -> 21", "-", "-", "10", "-", "5", "-"], {0: "found"})}},
    ]),
]:
    add_page({
        "slug": slug,
        "title": title,
        "nav_title": title,
        "category": "Searching",
        "eyebrow": f"Searching / {title}",
        "hero_title": hero,
        "description": desc,
        "pills": ["探索", "比較教材", "動作イメージ付き"],
        "observe": ["何を比較するか", "候補がどう減るか", "前提条件があるか"],
        "legend": [("注目", "active"), ("発見", "found"), ("除外", "dim")],
        "pseudocode_title": "擬似コード",
        "pseudocode": code,
        "facts": facts,
        "explain": explain,
        "frames": frames,
    })

for slug, title, hero, desc, facts, explain, code, frames, legend in [
    ("stack", "Stack", "後から入れたものを\n先に取り出す。", "LIFO の基本データ構造です。関数呼び出し、undo、式の評価など幅広く出てきます。", [("Push", "O(1)"), ("Pop", "O(1)"), ("特徴", "LIFO"), ("代表用途", "call stack")], [("直感", "積み上げた皿の一番上だけ触れる感覚です。"), ("大事な制約", "先頭や途中は直接取り出しません。"), ("教育用途", "再帰や DFS との接続がしやすいです。")], ["push(x)", "pop()", "peek()"], [
        {"kind": "cells", "line": 1, "caption": "push で上に積みます。", "stats": [["top", "7"]], "payload": {"items": cell_items(["2", "5", "7"], {2: "active"}, {0: "bottom", 2: "top"})}},
        {"kind": "cells", "line": 2, "caption": "pop では一番上だけ取り出せます。", "stats": [["pop", "7"]], "payload": {"items": cell_items(["2", "5"], {1: "found"}, {0: "bottom", 1: "top"})}},
    ], [("top", "active"), ("取り出し", "found")]),
    ("queue", "Queue", "先に入れたものを\n先に取り出す。", "FIFO の基本データ構造です。待ち行列、BFS、ジョブ処理などに出てきます。", [("Enqueue", "O(1)"), ("Dequeue", "O(1)"), ("特徴", "FIFO"), ("代表用途", "BFS")], [("直感", "列に並ぶ感覚です。"), ("出口", "先頭だけ取り出せます。"), ("DFS との対比", "Stack と並べると探索の違いが見えます。")], ["enqueue(x)", "dequeue()", "front()"], [
        {"kind": "cells", "line": 1, "caption": "enqueue で後ろへ追加します。", "stats": [["rear", "9"]], "payload": {"items": cell_items(["3", "6", "9"], {2: "active"}, {0: "front", 2: "rear"})}},
        {"kind": "cells", "line": 2, "caption": "dequeue では先頭が出ます。", "stats": [["dequeue", "3"]], "payload": {"items": cell_items(["6", "9"], {0: "found"}, {0: "front", 1: "rear"})}},
    ], [("front", "found"), ("rear", "active")]),
    ("linked-list", "Linked List", "ノードが次のノードを\n指してつながる。", "配列と違い、要素がメモリ上で連続していなくてもつながれます。挿入・削除の考え方を学ぶ入口になります。", [("Access", "O(n)"), ("Insert after node", "O(1)"), ("Delete after node", "O(1)"), ("構造", "pointer chain")], [("配列との違い", "添字で飛べず、順番にたどります。"), ("強み", "位置がわかっていればつなぎ替えは速いです。"), ("見せ方", "矢印を強調すると理解しやすいです。")], ["node.value", "node.next", "insert after current"], [
        {"kind": "cards", "line": 1, "caption": "各ノードが次を指します。", "stats": [["head", "A"]], "payload": {"items": cards_items([("A", "next -> B", "active"), ("B", "next -> C", "default"), ("C", "next -> null", "default")])}},
        {"kind": "cards", "line": 3, "caption": "B の後ろへ X を挿入します。", "stats": [["操作", "B -> X -> C"]], "payload": {"items": cards_items([("A", "next -> B", "default"), ("B", "next -> X", "active"), ("X", "next -> C", "swap"), ("C", "next -> null", "default")])}},
    ], [("現在ノード", "active"), ("新規ノード", "swap")]),
    ("binary-search-tree", "Binary Search Tree", "左は小さく、右は大きく。", "二分探索木は、各ノードで左部分木の値が小さく、右部分木の値が大きい構造です。探索・挿入の考え方を木として学べます。", [("Search avg", "O(log n)"), ("Search worst", "O(n)"), ("前提", "順序性"), ("注意", "偏ると遅い")], [("速い理由", "各ノードで片側だけ見ればよいからです。"), ("弱点", "偏った木になると線形に近づきます。"), ("次の教材", "AVL や赤黒木へつなげられます。")], ["if x < node then go left", "if x > node then go right", "insert at null child"], [
        {"kind": "tree", "line": 1, "caption": "8 を基準に左か右かを決めます。", "stats": [["target", "6"]], "payload": tree_payload({"8": "active", "3": "frontier", "10": "dim"})},
        {"kind": "tree", "line": 1, "caption": "6 < 8 なので左部分木へ進みます。", "stats": [["current", "3"]], "payload": tree_payload({"8": "visited", "3": "active", "6": "frontier", "1": "dim", "10": "dim", "14": "dim"}, {("8", "3"): "active"})},
        {"kind": "tree", "line": 2, "caption": "3 < 6 なので右へ進み、6 を見つけます。", "stats": [["found", "6"]], "payload": tree_payload({"8": "visited", "3": "visited", "6": "found", "1": "dim", "10": "dim", "14": "dim"}, {("3", "6"): "active"})},
    ], [("現在", "active"), ("通過済み", "visited"), ("発見", "found")]),
    ("heap-structure", "Binary Heap", "完全二分木で\n優先度を管理する。", "ヒープは親子の大小関係だけを保つ構造です。最小値・最大値の取り出しが速く、優先度付きキューの実装に使われます。", [("Peek", "O(1)"), ("Push", "O(log n)"), ("Pop", "O(log n)"), ("用途", "priority queue")], [("BST との違い", "左右全体の順序までは保証しません。"), ("強み", "根に最小または最大が来るので取り出しが速いです。"), ("教え方", "木と配列の対応をセットで見せます。")], ["push into last position", "bubble up", "pop root", "move last to root and bubble down"], [
        {"kind": "tree", "line": 1, "caption": "最小ヒープでは根が最小です。", "stats": [["root", "1"]], "payload": {"nodes": [{"id": "1", "label": "1", "x": 270, "y": 40, "state": "found"}, {"id": "3", "label": "3", "x": 150, "y": 120, "state": "default"}, {"id": "6", "label": "6", "x": 390, "y": 120, "state": "default"}, {"id": "5", "label": "5", "x": 90, "y": 210, "state": "default"}, {"id": "8", "label": "8", "x": 210, "y": 210, "state": "default"}, {"id": "7", "label": "7", "x": 450, "y": 210, "state": "default"}], "edges": [{"from": "1", "to": "3"}, {"from": "1", "to": "6"}, {"from": "3", "to": "5"}, {"from": "3", "to": "8"}, {"from": "6", "to": "7"}]}},
        {"kind": "tree", "line": 2, "caption": "新しい値 2 を挿入し、上へ持ち上げます。", "stats": [["insert", "2"], ["bubble up", "yes"]], "payload": {"nodes": [{"id": "1", "label": "1", "x": 270, "y": 40, "state": "found"}, {"id": "3", "label": "3", "x": 150, "y": 120, "state": "default"}, {"id": "6", "label": "6", "x": 390, "y": 120, "state": "default"}, {"id": "5", "label": "5", "x": 90, "y": 210, "state": "default"}, {"id": "8", "label": "8", "x": 210, "y": 210, "state": "default"}, {"id": "7", "label": "7", "x": 450, "y": 210, "state": "default"}, {"id": "2", "label": "2", "x": 330, "y": 210, "state": "active"}], "edges": [{"from": "1", "to": "3"}, {"from": "1", "to": "6"}, {"from": "3", "to": "5"}, {"from": "3", "to": "8"}, {"from": "6", "to": "2", "state": "active"}, {"from": "6", "to": "7"}]}},
    ], [("root", "found"), ("挿入中", "active")]),
    ("union-find", "Union-Find", "要素が同じ集合かを\n高速に判定する。", "Disjoint Set Union とも呼ばれます。連結成分の管理や Kruskal 法で重要な役割を持ちます。", [("Find", "ほぼ O(1) amortized"), ("Union", "ほぼ O(1) amortized"), ("技法", "path compression"), ("用途", "連結判定")], [("何ができるか", "同じグループかどうかを速く判定できます。"), ("なぜ速いか", "経路圧縮と union by rank によって木が浅く保たれるからです。"), ("関連", "Kruskal 法の理解に直結します。")], ["find(x)", "find(y)", "if roots differ then union them"], [
        {"kind": "cards", "line": 1, "caption": "最初は別々の集合です。", "stats": [["集合", "{A},{B},{C},{D}"]], "payload": {"items": cards_items([("A", "root A", "default"), ("B", "root B", "default"), ("C", "root C", "default"), ("D", "root D", "default")])}},
        {"kind": "cards", "line": 3, "caption": "A と B、C と D を union します。", "stats": [["結果", "{A,B} と {C,D}"]], "payload": {"items": cards_items([("A", "root A", "sorted"), ("B", "parent -> A", "active"), ("C", "root C", "sorted"), ("D", "parent -> C", "active")])}},
        {"kind": "cards", "line": 1, "caption": "find(B) と find(A) は同じ根を返します。", "stats": [["same set?", "yes"]], "payload": {"items": cards_items([("find(A)", "A", "found"), ("find(B)", "A", "found"), ("結論", "同じ集合", "active")])}},
    ], [("注目", "active"), ("同集合", "found")]),
]:
    add_page({
        "slug": slug,
        "title": title,
        "nav_title": title,
        "category": "Data Structures",
        "eyebrow": f"Data Structure / {title}",
        "hero_title": hero,
        "description": desc,
        "pills": ["データ構造", "基礎教材", "可視化"],
        "observe": ["何が制約か", "どこが速いか", "どこが遅いか"],
        "legend": legend,
        "pseudocode_title": "基本操作",
        "pseudocode": code,
        "facts": facts,
        "explain": explain,
        "frames": frames,
    })

for slug, title, hero, desc, facts, explain, code, frames in [
    ("bfs", "BFS", "近い順に広げる探索。", "幅優先探索は、始点からの距離が近い順に探索を進めます。キューを使うのが本質です。", [("Time", "O(V + E)"), ("Space", "O(V)"), ("構造", "Queue"), ("用途", "最短距離(重みなし)")], [("特徴", "1 手先、2 手先という順番で広がります。"), ("見せ方", "frontier を青、訪問済みを灰で出すとわかりやすいです。"), ("用途", "重みなしグラフの最短経路と相性がよいです。")], ["enqueue start", "while queue not empty", "  pop front", "  enqueue unvisited neighbors"], [
        {"kind": "graph", "line": 1, "caption": "A から開始してキューへ入れます。", "stats": [["queue", "[A]"]], "payload": graph_payload({"A": "active"})},
        {"kind": "graph", "line": 4, "caption": "A の隣接 B, D を frontier にします。", "stats": [["queue", "[B, D]"]], "payload": graph_payload({"A": "visited", "B": "frontier", "D": "frontier"}, {("A", "B"): "active", ("A", "D"): "active"})},
        {"kind": "graph", "line": 4, "caption": "次に B から広がり、C と E が frontier になります。", "stats": [["queue", "[D, C, E]"]], "payload": graph_payload({"A": "visited", "B": "visited", "D": "frontier", "C": "frontier", "E": "frontier"}, {("A", "B"): "visited", ("A", "D"): "frontier", ("B", "C"): "active", ("B", "E"): "active"})},
    ]),
    ("dfs", "DFS", "深く行けるだけ進み、\n行き止まりで戻る。", "深さ優先探索は、1 本の道を深く追ってから戻る探索です。再帰またはスタックで実装できます。", [("Time", "O(V + E)"), ("Space", "O(V)"), ("構造", "Stack / Recursion"), ("用途", "全探索, SCC の基礎")], [("特徴", "近さより深さを優先します。"), ("BFS との違い", "順序がかなり変わります。"), ("教え方", "探索木と戻りをセットで見せるとよいです。")], ["visit node", "for each unvisited neighbor", "  dfs(neighbor)"], [
        {"kind": "graph", "line": 1, "caption": "A から始めて 1 本深く追います。", "stats": [["stack", "[A]"]], "payload": graph_payload({"A": "active"})},
        {"kind": "graph", "line": 3, "caption": "A -> B -> C と深く進みます。", "stats": [["path", "A-B-C"]], "payload": graph_payload({"A": "visited", "B": "visited", "C": "active"}, {("A", "B"): "active", ("B", "C"): "active"})},
        {"kind": "graph", "line": 3, "caption": "C から進めないので戻り、別枝 E を探索します。", "stats": [["backtrack", "to B"]], "payload": graph_payload({"A": "visited", "B": "visited", "C": "visited", "E": "active"}, {("A", "B"): "visited", ("B", "C"): "visited", ("B", "E"): "active"})},
    ]),
    ("dijkstra", "Dijkstra", "最短距離が確定した頂点を\n1 つずつ増やす。", "重みが非負のグラフで単一始点最短経路を求めます。いま最も距離が短い候補を優先度付きキューで選びます。", [("Time", "O((V+E) log V)"), ("前提", "非負重み"), ("構造", "Priority Queue"), ("用途", "最短経路")], [("本質", "一番近い未確定頂点から順に確定することです。"), ("BFS との違い", "辺の重みを考慮します。"), ("注意", "負辺がある場合は Bellman-Ford などを使います。")], ["dist[start] = 0", "while pq not empty", "  take node with min dist", "  relax outgoing edges"], [
        {"kind": "graph", "line": 1, "caption": "始点 A の距離を 0 にします。", "stats": [["dist(A)", "0"], ["pq", "(A,0)"]], "payload": graph_payload({"A": "active"})},
        {"kind": "graph", "line": 4, "caption": "A から B と D を緩和します。", "stats": [["dist(B)", "2"], ["dist(D)", "1"]], "payload": graph_payload({"A": "visited", "B": "frontier", "D": "frontier"}, {("A", "B"): "active", ("A", "D"): "active"})},
        {"kind": "graph", "line": 3, "caption": "次に最短の D を確定し、E を更新します。", "stats": [["確定", "D"], ["dist(E)", "3"]], "payload": graph_payload({"A": "visited", "D": "chosen", "E": "frontier", "B": "frontier"}, {("A", "D"): "chosen", ("D", "E"): "active"})},
    ]),
    ("topological-sort", "Topological Sort", "依存関係を壊さずに\n順序を作る。", "有向非巡回グラフの頂点を、辺の向きを保ったまま並べる方法です。タスク依存の可視化に向いています。", [("Time", "O(V + E)"), ("前提", "DAG"), ("方法", "入次数管理"), ("用途", "依存解決")], [("何が嬉しいか", "前提タスクを先に終える順番が得られます。"), ("循環", "閉路があると並べられません。"), ("見せ方", "入次数 0 の頂点がどんどん出てくる流れを見せます。")], ["compute indegrees", "push indegree-0 nodes", "pop and remove outgoing edges"], [
        {"kind": "graph", "line": 1, "caption": "入次数 0 の A から始めます。", "stats": [["in-degree 0", "A"]], "payload": graph_payload({"A": "active", "B": "dim", "C": "dim", "D": "dim", "E": "dim", "F": "dim"})},
        {"kind": "graph", "line": 3, "caption": "A を出力すると B と D の入次数が減ります。", "stats": [["output", "A"], ["next", "B, D"]], "payload": graph_payload({"A": "sorted", "B": "frontier", "D": "frontier"}, {("A", "B"): "active", ("A", "D"): "active"})},
        {"kind": "graph", "line": 3, "caption": "B を出力すると C と E が候補になります。", "stats": [["output", "A, B"], ["next", "D, C, E"]], "payload": graph_payload({"A": "sorted", "B": "sorted", "D": "frontier", "C": "frontier", "E": "frontier"}, {("B", "C"): "active", ("B", "E"): "active"})},
    ]),
    ("prim", "Prim", "木の外へ出る最小辺を\n1 本ずつ足す。", "最小全域木を作るアルゴリズムです。現在の木から外へ伸びる最小の辺を選び続けます。", [("Time", "O(E log V)"), ("目的", "最小全域木"), ("構造", "Priority Queue"), ("比較", "Kruskal")], [("視点", "今ある木を少しずつ広げます。"), ("Kruskal との違い", "辺を全体から選ぶのではなく、木の境界から選びます。"), ("見せ方", "木の中と外を色分けすると良いです。")], ["start from any node", "repeatedly choose minimum edge leaving the tree"], [
        {"kind": "graph", "line": 1, "caption": "A から木を始めます。", "stats": [["tree", "{A}"]], "payload": graph_payload({"A": "chosen"})},
        {"kind": "graph", "line": 2, "caption": "A から外へ出る最小辺 A-D を選びます。", "stats": [["chosen edge", "A-D (1)"]], "payload": graph_payload({"A": "chosen", "D": "frontier"}, {("A", "D"): "chosen", ("A", "B"): "active"})},
        {"kind": "graph", "line": 2, "caption": "次は境界上で最小の A-B を選びます。", "stats": [["tree", "{A, D, B}"]], "payload": graph_payload({"A": "chosen", "D": "chosen", "B": "frontier"}, {("A", "D"): "chosen", ("A", "B"): "chosen", ("D", "E"): "active"})},
    ]),
]:
    add_page({
        "slug": slug,
        "title": title,
        "nav_title": title,
        "category": "Graphs",
        "eyebrow": f"Graph / {title}",
        "hero_title": hero,
        "description": desc,
        "pills": ["グラフ", "ノードとエッジ", "可視化向き"],
        "observe": ["どの頂点が注目か", "候補集合がどう変わるか", "なぜ次の頂点や辺を選ぶか"],
        "legend": [("注目", "active"), ("候補", "frontier"), ("確定", "chosen")],
        "pseudocode_title": "擬似コード",
        "pseudocode": code,
        "facts": facts,
        "explain": explain,
        "frames": frames,
    })

for slug, title, hero, desc, facts, explain, code, frames in [
    ("fibonacci-recursion", "Fibonacci", "同じ部分問題が\n何度も現れる。", "再帰で Fibonacci 数をそのまま求めると、同じ計算を何度も繰り返します。メモ化や DP の必要性を示す代表例です。", [("Naive", "O(2^n)"), ("Memoized", "O(n)"), ("主題", "重複部分問題"), ("接続", "DP")], [("教材価値", "遅さの理由が再帰木ではっきり見えます。"), ("改善", "メモ化で一気に変わります。"), ("説明", "同じ fib(3) が何回出るかを数えるとよいです。")], ["fib(n) = fib(n-1) + fib(n-2)", "base cases: fib(0), fib(1)"], [
        {"kind": "cards", "line": 1, "caption": "fib(5) は fib(4) と fib(3) に分かれます。", "stats": [["root", "fib(5)"]], "payload": {"items": cards_items([("fib(5)", "fib(4) + fib(3)", "active"), ("fib(4)", "さらに分岐", "swap"), ("fib(3)", "こちらも分岐", "swap")])}},
        {"kind": "cards", "line": 1, "caption": "fib(3) が複数回現れます。", "stats": [["重複", "fib(3), fib(2)"]], "payload": {"items": cards_items([("fib(3)", "左枝に出現", "swap"), ("fib(3)", "右枝にも出現", "swap"), ("問題", "同じ計算の繰り返し", "active")])}},
        {"kind": "cards", "line": 2, "caption": "停止条件は簡単でも、木は急激に広がります。", "stats": [["base", "fib(1), fib(0)"]], "payload": {"items": cards_items([("fib(1)", "1", "sorted"), ("fib(0)", "0", "sorted"), ("全体", "指数的に増える", "active")])}},
    ]),
    ("knapsack", "0/1 Knapsack", "入れる / 入れないを\n表で積み上げる。", "容量制約の下で価値の合計を最大化する問題です。DP テーブルを使うと、部分問題の積み重ねで考えられます。", [("Time", "O(nW)"), ("Space", "O(nW)"), ("主題", "DP table"), ("状態", "品物数 × 容量")], [("核心", "各品物について入れるか入れないかを比較します。"), ("見せ方", "行と列の意味を先に固定すると迷いません。"), ("注意", "価値と重さを混同しないこと。")], ["dp[i][w] = max(not take, take if possible)"], [
        {"kind": "grid", "line": 1, "caption": "行は品物、列は容量です。", "stats": [["items", "3"], ["capacity", "5"]], "payload": {"rows": [[{"text": "-", "state": "default"}, {"text": "0", "state": "default"}, {"text": "1", "state": "default"}, {"text": "2", "state": "default"}, {"text": "3", "state": "default"}, {"text": "4", "state": "default"}, {"text": "5", "state": "default"}], [{"text": "item1", "state": "default"}, {"text": "0", "state": "default"}, {"text": "0", "state": "default"}, {"text": "3", "state": "active"}, {"text": "3", "state": "active"}, {"text": "3", "state": "active"}, {"text": "3", "state": "active"}]]}},
        {"kind": "grid", "line": 1, "caption": "新しい品物を入れるか入れないかを比べます。", "stats": [["item2", "weight 2 value 4"]], "payload": {"rows": [[{"text": "容量", "state": "default"}, {"text": "0", "state": "default"}, {"text": "1", "state": "default"}, {"text": "2", "state": "default"}, {"text": "3", "state": "default"}, {"text": "4", "state": "default"}, {"text": "5", "state": "default"}], [{"text": "前行", "state": "default"}, {"text": "0", "state": "default"}, {"text": "0", "state": "default"}, {"text": "3", "state": "default"}, {"text": "3", "state": "default"}, {"text": "3", "state": "default"}, {"text": "3", "state": "default"}], [{"text": "今回", "state": "default"}, {"text": "0", "state": "default"}, {"text": "0", "state": "default"}, {"text": "4", "state": "active"}, {"text": "4", "state": "active"}, {"text": "7", "state": "found"}, {"text": "7", "state": "found"}]]}},
    ]),
    ("lcs", "LCS", "2 つの文字列で\n共通部分列の長さを測る。", "最長共通部分列は、2 つの列に共通して現れる順序付き要素列の最長長を求めます。DP テーブルが典型です。", [("Time", "O(nm)"), ("Space", "O(nm)"), ("主題", "文字列 DP"), ("出力", "長さまたは列")], [("一致したら", "左上 + 1 を使います。"), ("一致しなければ", "上と左の大きい方を取ります。"), ("編集距離との比較", "表の見た目が近いので並べると良いです。")], ["if s[i] == t[j]: dp[i][j] = dp[i-1][j-1] + 1", "else: dp[i][j] = max(top, left)"], [
        {"kind": "grid", "line": 1, "caption": "文字が一致すると左上に 1 を足します。", "stats": [["s", "ABC"], ["t", "ADC"]], "payload": {"rows": [[{"text": "", "state": "default"}, {"text": "A", "state": "default"}, {"text": "D", "state": "default"}, {"text": "C", "state": "default"}], [{"text": "A", "state": "default"}, {"text": "1", "state": "found"}, {"text": "1", "state": "default"}, {"text": "1", "state": "default"}], [{"text": "B", "state": "default"}, {"text": "1", "state": "default"}, {"text": "1", "state": "active"}, {"text": "1", "state": "default"}], [{"text": "C", "state": "default"}, {"text": "1", "state": "default"}, {"text": "1", "state": "default"}, {"text": "2", "state": "found"}]]}},
        {"kind": "cards", "line": 2, "caption": "最後のセルが LCS の長さです。", "stats": [["LCS length", "2"], ["例", "AC"]], "payload": {"items": cards_items([("一致", "A と C が共通", "found"), ("不一致", "B と D では上か左を採用", "active"), ("結論", "長さ 2", "sorted")])}},
    ]),
    ("edit-distance", "Edit Distance", "変換に必要な最小編集回数を\n表で求める。", "1 文字の挿入、削除、置換で文字列を変換する最小コストを求めます。表の各マスで 3 通りを比較します。", [("Time", "O(nm)"), ("Space", "O(nm)"), ("操作", "insert/delete/replace"), ("用途", "文字列類似度")], [("考え方", "各接頭辞同士の最小変換回数を積み上げます。"), ("LCS との違い", "3 方向を比較する点が大きな違いです。"), ("見せ方", "上・左・左上の意味を言語化すると迷いません。")], ["dp[i][j] = min(delete, insert, replace)"], [
        {"kind": "grid", "line": 1, "caption": "上は削除、左は挿入、左上は置換を表します。", "stats": [["from", "cat"], ["to", "cut"]], "payload": {"rows": [[{"text": "", "state": "default"}, {"text": "c", "state": "default"}, {"text": "u", "state": "default"}, {"text": "t", "state": "default"}], [{"text": "c", "state": "default"}, {"text": "0", "state": "found"}, {"text": "1", "state": "default"}, {"text": "2", "state": "default"}], [{"text": "a", "state": "default"}, {"text": "1", "state": "default"}, {"text": "1", "state": "active"}, {"text": "2", "state": "default"}], [{"text": "t", "state": "default"}, {"text": "2", "state": "default"}, {"text": "2", "state": "default"}, {"text": "1", "state": "found"}]]}},
        {"kind": "cards", "line": 1, "caption": "cat -> cut は置換 1 回で済みます。", "stats": [["distance", "1"]], "payload": {"items": cards_items([("delete", "候補 2", "default"), ("insert", "候補 2", "default"), ("replace", "候補 1", "found")])}},
    ]),
    ("hanoi", "Tower of Hanoi", "再帰で円盤を移し、\n手順の構造を学ぶ。", "ハノイの塔は再帰の教材として定番です。大きい円盤を動かす前後に、小さい円盤の塔を丸ごと移す発想が見えます。", [("Moves", "2^n - 1"), ("主題", "再帰構造"), ("制約", "大きい円盤を小さい円盤の上に置けない"), ("教材価値", "高い")], [("再帰の形", "n-1 枚を退避、最大を移動、n-1 枚を戻す、の 3 段構成です。"), ("見せ方", "塔の図がそのまま再帰の構造になります。"), ("計算量", "手数が指数的に増える例としても使えます。")], ["move(n-1, source, spare)", "move largest disc", "move(n-1, spare, target)"], [
        {"kind": "towers", "line": 1, "caption": "最初は 3 枚とも左の塔にあります。", "stats": [["n", "3"], ["目標", "右へ移動"]], "payload": {"rods": [[3, 2, 1], [], []]}},
        {"kind": "towers", "line": 2, "caption": "最大円盤を動かす前に、小さい 2 枚を退避します。", "stats": [["途中", "A -> B"]], "payload": {"rods": [[3], [2, 1], []]}},
        {"kind": "towers", "line": 3, "caption": "最大円盤を右へ移し、最後に小さい 2 枚を重ねます。", "stats": [["完了", "7 手"]], "payload": {"rods": [[], [], [3, 2, 1]]}},
    ]),
]:
    add_page({
        "slug": slug,
        "title": title,
        "nav_title": title,
        "category": "Dynamic Programming & Recursion",
        "eyebrow": f"DP / {title}",
        "hero_title": hero,
        "description": desc,
        "pills": ["DP / 再帰", "表や木で理解", "定番教材"],
        "observe": ["状態が何か", "前の状態をどう使うか", "なぜその漸化式になるか"],
        "legend": [("注目", "active"), ("決定的", "found"), ("確定", "sorted")],
        "pseudocode_title": "擬似コード",
        "pseudocode": code,
        "facts": facts,
        "explain": explain,
        "frames": frames,
    })


def page_template(page):
    root = ".."
    related = related_links(page)
    category_label = CATEGORY_LABELS.get(page["category"], page["category"])
    top_nav = "".join(f'<a href="{root}/{href}">{label}</a>' for label, href in TOP_NAV)
    legend = "".join(
        f'<span class="legend-item"><span class="legend-swatch {state_to_css(state)}"></span>{html.escape(label)}</span>'
        for label, state in page["legend"]
    )
    facts = "".join(
        f'<article class="info-card"><strong>{html.escape(format_fact_label(label))}</strong><p>{html.escape(format_fact_value(value))}</p></article>'
        for label, value in page["facts"]
    )
    explain = "".join(
        f'<article class="info-card"><strong>{html.escape(title)}</strong><p>{html.escape(text)}</p></article>'
        for title, text in page["explain"]
    )
    article_blocks = ""
    intro_section = ""
    for i, section in enumerate(page.get("pre_visual_sections", []), start=1):
        body = ""
        for paragraph in section.get("paragraphs", []):
            body += f"<p>{html.escape(paragraph)}</p>"
        if section.get("bullets"):
            body += "<ul class=\"list-clean\">" + "".join(f"<li>{html.escape(item)}</li>" for item in section["bullets"]) + "</ul>"
        if section.get("cards"):
            body += "<div class=\"card-grid\">" + "".join(
                f'<article class="info-card"><strong>{html.escape(title)}</strong><p>{html.escape(text)}</p></article>'
                for title, text in section["cards"]
            ) + "</div>"
        intro_section += f"""
      <div class="article-block" id="intro-{i}">
        <p class="eyebrow">{html.escape(section["eyebrow"])}</p>
        <h3>{html.escape(section["title"])}</h3>
        {body}
      </div>
"""
    if not intro_section:
        intro_section = f"""
      <div class="article-block">
        <p>{html.escape(page["description"])}</p>
      </div>
"""
    for i, section in enumerate(page.get("extra_sections", []), start=1):
        body = ""
        for paragraph in section.get("paragraphs", []):
            body += f"<p>{html.escape(paragraph)}</p>"
        if section.get("bullets"):
            body += "<ul class=\"list-clean\">" + "".join(f"<li>{html.escape(item)}</li>" for item in section["bullets"]) + "</ul>"
        if section.get("cards"):
            body += "<div class=\"card-grid\">" + "".join(
                f'<article class="info-card"><strong>{html.escape(title)}</strong><p>{html.escape(text)}</p></article>'
                for title, text in section["cards"]
            ) + "</div>"
        article_blocks += f"""
      <div class="article-block" id="extra-{i}">
        <p class="eyebrow">{html.escape(section["eyebrow"])}</p>
        <h3>{html.escape(section["title"])}</h3>
        {body}
      </div>
"""
    pseudocode = "\n".join(
        f'<span class="code-line" data-line="{i + 1}">{html.escape(line)}</span>'
        for i, line in enumerate(page["pseudocode"])
    )
    learn_cards = "".join(
        f'<article class="info-card"><strong>{index}. わかること</strong><p>{html.escape(line)}</p></article>'
        for index, line in enumerate(page["observe"][:3], start=1)
    )
    pills = "".join(f'<span class="pill">{html.escape(pill)}</span>' for pill in page["pills"])
    payload = {"frames": page["frames"]}
    if page.get("generator"):
        payload["generator"] = page["generator"]
        payload["defaultN"] = page.get("default_n", 12)
    if page.get("variants"):
        payload["variants"] = page["variants"]
    data = json.dumps(payload, ensure_ascii=False)
    hero_title = "<br>".join(html.escape(part) for part in page["hero_title"].split("\n"))
    toc_items = [("summary", "このページでわかること")]
    if page.get("pre_visual_sections"):
        toc_items.extend((f"intro-{i}", section["title"]) for i, section in enumerate(page["pre_visual_sections"], start=1))
    else:
        toc_items.append(("article", "概要"))
    toc_items.extend((f"extra-{i}", section["title"]) for i, section in enumerate(page.get("extra_sections", []), start=1))
    toc_items.extend([
        ("howto", page["pseudocode_title"]),
        ("facts", "要点まとめ"),
        ("visualizer", "動きで確認"),
        ("next", "次に見るページ"),
    ])
    toc = "".join(f'<a href="#{anchor}">{html.escape(label)}</a>' for anchor, label in toc_items)
    next_cta = next_links(page)
    visual_hint = html.escape(page["observe"][0]) if page.get("observe") else "アルゴリズムの流れ"
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(page["title"])} | algorithm.hide10.com</title>
  <meta name="description" content="{html.escape(page["description"])}">
  <link rel="stylesheet" href="{root}/styles.css">
</head>
<body>
  <div class="page-shell">
    <header class="site-header">
      <a class="brand" href="{root}/index.html">
        <span class="brand-mark">A</span>
        <span class="brand-copy">
          <strong>algorithm.hide10.com</strong>
          <span>Visual algorithm primer</span>
        </span>
      </a>
      <nav class="nav-links">{top_nav}</nav>
    </header>

    <section class="hero hero-single">
      <div class="panel hero-copy">
        <p class="eyebrow">{html.escape(category_label)} / {html.escape(page["title"])}</p>
        <h1>{hero_title}</h1>
        <p>{html.escape(page["description"])}</p>
        <div class="pill-row">{pills}</div>
      </div>
    </section>

    <section class="panel section toc-section">
      <p class="eyebrow">目次</p>
      <h2>このページの目次</h2>
      <div class="toc-links">{toc}</div>
    </section>

    <section id="summary" class="panel section">
      <p class="eyebrow">このページでわかること</p>
      <h2>先に知っておくポイント</h2>
      <div class="card-grid">{learn_cards}</div>
    </section>

    <section id="article" class="panel section">
      <p class="eyebrow">本文</p>
      <h2>しくみと考え方</h2>
{intro_section}
{article_blocks}
    </section>

    <section id="howto" class="panel section">
      <p class="eyebrow">考え方</p>
      <h2>{html.escape(page["pseudocode_title"])}</h2>
      <div class="code-panel">
        <pre><code>{pseudocode}</code></pre>
      </div>
    </section>

    <section id="facts" class="panel section">
      <p class="eyebrow">要点</p>
      <h2>要点まとめ</h2>
      <div class="card-grid">{facts}</div>
    </section>

    <section class="panel section">
      <p class="eyebrow">補足</p>
      <h2>向いている場面と注意点</h2>
      <div class="card-grid">{explain}</div>
    </section>

    <section id="visualizer" class="panel section">
      <p class="eyebrow">動きで確認</p>
      <h2>最後に動きで確認する</h2>
      <p class="section-lead">ここでは「{visual_hint}」を見ながら、本文で読んだ内容と対応づけます。</p>
      <div class="visualizer-layout">
        <div class="panel bars-panel">
          <div class="toolbar">
            <button id="prevButton" class="button-secondary" type="button">前へ</button>
            <button id="nextButton" class="button-secondary" type="button">次へ</button>
            <button id="playButton" class="button-primary" type="button" data-playing="false">自動再生</button>
            <button id="resetButton" class="button-secondary" type="button">最初へ</button>
            <label for="speedInput">速度
              <input id="speedInput" type="range" min="1" max="100" step="1" value="72">
            </label>
          </div>
          <div id="scene" class="visual-stage"></div>
          <p id="frameCaption" class="visual-caption"></p>
        </div>

        <div>
          <div class="panel stats">
            <div id="dynamicStats" class="stat-grid"></div>
          </div>
          <div class="panel legend" style="margin-top: 18px;">{legend}</div>
        </div>
      </div>
    </section>

    <section id="next" class="panel section">
      <p class="eyebrow">次に見る</p>
      <h2>次に見るページ</h2>
      <p class="section-lead">比較すると違いがわかりやすいページを先に置いています。</p>
      <div class="hero-actions">{next_cta}</div>
    </section>

    <footer class="footer">{related}</footer>
  </div>
  <script>window.PAGE_DATA = {data};</script>
  <script src="{root}/app.js"></script>
</body>
</html>
"""


def state_to_css(state):
    mapping = {
        "active": "is-active",
        "swap": "is-swap",
        "sorted": "is-sorted",
        "found": "is-found",
        "dim": "is-dim",
        "frontier": "is-frontier",
        "visited": "is-visited",
        "chosen": "is-chosen",
    }
    return mapping.get(state, "")


def format_fact_label(label: str) -> str:
    mapping = {
        "Best": "最良時計算量",
        "Average": "平均時計算量",
        "Worst": "最悪時計算量",
        "Stable": "安定ソートか",
        "Time": "時間計算量",
        "Space": "空間計算量",
    }
    return mapping.get(label, label)


def format_fact_value(value: str) -> str:
    mapping = {
        "Yes": "はい",
        "No": "いいえ",
        "O(n) with early exit": "O(n) / 交換がなければ早く終わる",
        "Yes if inner sort stable": "はい / 内部のソートが安定なら",
    }
    return mapping.get(value, value)


def related_links(page):
    category_pages = [p for p in PAGES if p["category"] == page["category"] and p["slug"] != page["slug"]][:2]
    links = " / ".join(f'<a href="../{p["slug"]}/index.html">{html.escape(p["title"])}</a>' for p in category_pages)
    if links:
        return f'関連: {links}'
    return '関連: <a href="../index.html">トップページ</a>'


def next_links(page):
    category_pages = [p for p in PAGES if p["category"] == page["category"]]
    current_index = next((i for i, item in enumerate(category_pages) if item["slug"] == page["slug"]), -1)
    candidates = []
    if page["slug"] == "complexity":
        bubble = next((p for p in PAGES if p["slug"] == "bubble-sort"), None)
        selection = next((p for p in PAGES if p["slug"] == "selection-sort"), None)
        for item in [bubble, selection]:
            if item:
                candidates.append(item)
    elif current_index != -1 and current_index + 1 < len(category_pages):
        candidates.append(category_pages[current_index + 1])

    if not candidates:
        return '<a class="button button-secondary" href="../index.html">トップへ戻る</a>'

    return "".join(
        f'<a class="button button-secondary" href="../{item["slug"]}/index.html">{html.escape(item["title"])}を見る</a>'
        for item in candidates[:2]
    )


def index_template():
    grouped = {}
    for page in PAGES:
      grouped.setdefault(page["category"], []).append(page)
    category_ids = {
        "Concepts": "concepts",
        "Sorting": "sorting",
        "Searching": "searching",
        "Data Structures": "data-structures",
        "Graphs": "graphs",
        "Dynamic Programming & Recursion": "dp-recursion",
    }
    sections = []
    for category, pages in grouped.items():
        cards = "".join(
            f'<article class="info-card"><strong><a href="./{p["slug"]}/index.html">{html.escape(p["title"])}</a></strong><p>{html.escape(p["description"])}</p></article>'
            for p in pages
        )
        sections.append(
            f'<section id="{category_ids.get(category, "")}" class="panel section"><p class="eyebrow">カテゴリ別</p><h2>{html.escape(CATEGORY_LABELS.get(category, category))}</h2><div class="card-grid">{cards}</div></section>'
        )
    total = len(PAGES)
    top_toc = """
      <div class="toc-links">
        <a href="#guide">はじめての4ページ</a>
        <a href="#catalog">カテゴリから探す</a>
        <a href="#concepts">概念</a>
        <a href="#sorting">ソート</a>
        <a href="#searching">探索</a>
      </div>
    """
    guide_cards = """
      <div class="card-grid">
        <article class="info-card"><strong>1. 計算量の概念</strong><p>まず Big-O と計算量の意味を理解します。</p></article>
        <article class="info-card"><strong>2. Bubble Sort</strong><p>比較と交換の基本を動きで確認します。</p></article>
        <article class="info-card"><strong>3. Selection Sort</strong><p>Bubble Sort と何が違うかを見ます。</p></article>
        <article class="info-card"><strong>4. Binary Search</strong><p>O(log n) の感覚をつかみます。</p></article>
      </div>
    """
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>algorithm.hide10.com</title>
  <meta name="description" content="アルゴリズムを視覚で学ぶ静的教材サイト。1 アルゴリズム 1 ページで、動き・擬似コード・計算量を対応づけて理解します。">
  <link rel="stylesheet" href="./styles.css">
</head>
<body>
  <div class="page-shell">
    <header class="site-header">
      <a class="brand" href="./index.html">
        <span class="brand-mark">A</span>
        <span class="brand-copy">
          <strong>algorithm.hide10.com</strong>
          <span>Visual algorithm primer</span>
        </span>
      </a>
      <nav class="nav-links">
        <a href="#guide">学習ガイド</a>
        <a href="./complexity/index.html">計算量</a>
        <a href="#sorting">ソート</a>
        <a href="#searching">探索</a>
      </nav>
    </header>

    <section class="hero hero-single">
      <div class="panel hero-copy">
        <p class="eyebrow">学習サイト</p>
        <h1>アルゴリズムを<br>動きで理解する。</h1>
        <p>説明を読んでから Visualizer で確認する流れに統一した、静的なアルゴリズム教材サイトです。まずは入口の4ページから始めて、その後にカテゴリ別で広げていけます。</p>
        <div class="hero-actions">
          <a class="button button-primary" href="./complexity/index.html">計算量から始める</a>
          <a class="button button-secondary" href="./bubble-sort/index.html">最初の動く教材へ</a>
        </div>
        <div class="pill-row" style="margin-top: 18px;">
          <span class="pill">現在 {total} ページ</span>
          <span class="pill">1アルゴリズム=1HTML</span>
          <span class="pill">GitHub Pages / 独自ドメイン対応</span>
        </div>
      </div>
    </section>
    <section class="panel section toc-section">
      <p class="eyebrow">入口</p>
      <h2>まずどこを見るか</h2>
      {top_toc}
    </section>
    <section id="guide" class="panel section">
      <p class="eyebrow">はじめての人へ</p>
      <h2>最初に見る4ページ</h2>
      <p class="section-lead">この4ページで、計算量、比較ソート、探索の基本まで追えます。</p>
      {guide_cards}
      <div class="hero-actions" style="margin-top:16px;">
        <a class="button button-primary" href="./complexity/index.html">1. 計算量へ</a>
        <a class="button button-secondary" href="./bubble-sort/index.html">2. Bubble Sortへ</a>
      </div>
    </section>
    <section id="catalog" class="panel section toc-section">
      <p class="eyebrow">カテゴリから探す</p>
      <h2>学びたいテーマから入る</h2>
      <p class="section-lead">学習順ではなく、興味のある分野から直接たどるための入口です。</p>
      {top_toc}
    </section>
    {''.join(sections)}
    <footer class="footer">GitHub Pages と <code>algorithm.hide10.com</code> の両方で運用しやすい静的構成です。<code>hide10.com</code> 側へ展開する場合は外側レイアウトに広告を載せ、教材本体はそのまま流用する方針です。</footer>
  </div>
</body>
</html>
"""


def write_pages():
    for page in PAGES:
        target_dir = ROOT / page["slug"]
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "index.html").write_text(page_template(page), encoding="utf-8")
    (ROOT / "index.html").write_text(index_template(), encoding="utf-8")


if __name__ == "__main__":
    write_pages()
