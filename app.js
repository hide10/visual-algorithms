(function () {
  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function stateClass(state) {
    const map = {
      default: "",
      active: "is-active",
      swap: "is-swap",
      sorted: "is-sorted",
      found: "is-found",
      dim: "is-dim",
      mid: "is-mid",
      candidate: "is-candidate",
      frontier: "is-frontier",
      visited: "is-visited",
      chosen: "is-chosen",
      path: "is-path"
    };
    return map[state] || "";
  }

  function renderBars(payload) {
    const max = Math.max.apply(null, payload.items.map((item) => item.value || 1));
    const count = payload.items.length;
    const denseClass = count > 24 ? "is-dense" : "";
    const gap = count > 60 ? 1 : count > 36 ? 2 : count > 20 ? 4 : 10;
    const showLabels = count <= 20;
    const items = payload.items.map((item) => {
      const cls = ["bar", stateClass(item.state)].filter(Boolean).join(" ");
      const height = ((item.value || 1) / max) * 220 + 28;
      return [
        '<div class="bar-wrap">',
        '<div class="' + cls + '" style="height:' + height + 'px;"></div>',
        showLabels ? '<span class="bar-value">' + escapeHtml(item.label != null ? item.label : item.value) + "</span>" : "",
        "</div>"
      ].join("");
    }).join("");
    return '<div class="bars ' + denseClass + '" style="gap:' + gap + 'px;">' + items + "</div>";
  }

  function shuffledRange(n) {
    const items = [];
    for (let i = 1; i <= n; i += 1) {
      items.push(i);
    }
    for (let i = items.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      const tmp = items[i];
      items[i] = items[j];
      items[j] = tmp;
    }
    return items;
  }

  function bubbleSortFrames(values) {
    const arr = values.slice();
    const frames = [];
    let comparisons = 0;
    let swaps = 0;
    let passes = 0;

    for (let i = 0; i < arr.length - 1; i += 1) {
      let swapped = false;
      for (let j = 0; j < arr.length - 1 - i; j += 1) {
        comparisons += 1;
        const activeStates = {};
        activeStates[j] = "active";
        activeStates[j + 1] = "active";
        for (let idx = arr.length - i; idx < arr.length; idx += 1) {
          activeStates[idx] = "sorted";
        }
        frames.push({
          kind: "bars",
          line: 2,
          caption: arr[j] + " と " + arr[j + 1] + " を比べます。",
          stats: [["n", String(arr.length)], ["比較", String(comparisons)], ["交換", String(swaps)], ["パス", String(passes)]],
          payload: { items: arr.map((value, index) => ({ value, label: String(value), state: activeStates[index] || "default" })) }
        });
        if (arr[j] > arr[j + 1]) {
          const left = arr[j];
          const right = arr[j + 1];
          arr[j] = right;
          arr[j + 1] = left;
          swaps += 1;
          swapped = true;
          const swapStates = {};
          swapStates[j] = "swap";
          swapStates[j + 1] = "swap";
          for (let idx = arr.length - i; idx < arr.length; idx += 1) {
            swapStates[idx] = "sorted";
          }
          frames.push({
            kind: "bars",
            line: 4,
            caption: arr[j] + " と " + arr[j + 1] + " の位置が入れ替わりました。",
            stats: [["n", String(arr.length)], ["比較", String(comparisons)], ["交換", String(swaps)], ["パス", String(passes)]],
            payload: { items: arr.map((value, index) => ({ value, label: String(value), state: swapStates[index] || "default" })) }
          });
        }
      }
      passes += 1;
      const passStates = {};
      for (let idx = arr.length - 1 - i; idx < arr.length; idx += 1) {
        passStates[idx] = "sorted";
      }
      frames.push({
        kind: "bars",
        line: 5,
        caption: arr[arr.length - 1 - i] + " が右端で確定しました。",
        stats: [["n", String(arr.length)], ["比較", String(comparisons)], ["交換", String(swaps)], ["パス", String(passes)]],
        payload: { items: arr.map((value, index) => ({ value, label: String(value), state: passStates[index] || "default" })) }
      });
      if (!swapped) {
        break;
      }
    }

    frames.push({
      kind: "bars",
      line: 5,
      caption: "整列が完了しました。",
      stats: [["n", String(arr.length)], ["比較", String(comparisons)], ["交換", String(swaps)], ["パス", String(passes)]],
      payload: { items: arr.map((value) => ({ value, label: String(value), state: "sorted" })) }
    });
    return frames;
  }

  function selectionSortFrames(values) {
    const arr = values.slice();
    const frames = [];
    let comparisons = 0;
    let swaps = 0;
    let passes = 0;

    for (let i = 0; i < arr.length - 1; i += 1) {
      let minIndex = i;
      const startStates = {};
      for (let idx = 0; idx < i; idx += 1) {
        startStates[idx] = "sorted";
      }
      startStates[minIndex] = "swap";
      frames.push({
        kind: "bars",
        line: 2,
        caption: arr[minIndex] + " をいまの最小候補にします。",
        stats: [["n", String(arr.length)], ["比較", String(comparisons)], ["交換", String(swaps)], ["パス", String(passes)]],
        payload: { items: arr.map((value, index) => ({ value, label: String(value), state: startStates[index] || "default" })) }
      });
      for (let j = i + 1; j < arr.length; j += 1) {
        comparisons += 1;
        const compareStates = {};
        for (let idx = 0; idx < i; idx += 1) {
          compareStates[idx] = "sorted";
        }
        compareStates[minIndex] = "swap";
        compareStates[j] = "active";
        frames.push({
          kind: "bars",
          line: 4,
          caption: arr[j] + " と最小候補 " + arr[minIndex] + " を比べます。",
          stats: [["n", String(arr.length)], ["比較", String(comparisons)], ["交換", String(swaps)], ["パス", String(passes)]],
          payload: { items: arr.map((value, index) => ({ value, label: String(value), state: compareStates[index] || "default" })) }
        });
        if (arr[j] < arr[minIndex]) {
          minIndex = j;
          const updateStates = {};
          for (let idx = 0; idx < i; idx += 1) {
            updateStates[idx] = "sorted";
          }
          updateStates[minIndex] = "swap";
          frames.push({
            kind: "bars",
            line: 5,
            caption: arr[minIndex] + " が新しい最小候補になりました。",
            stats: [["n", String(arr.length)], ["比較", String(comparisons)], ["交換", String(swaps)], ["パス", String(passes)]],
            payload: { items: arr.map((value, index) => ({ value, label: String(value), state: updateStates[index] || "default" })) }
          });
        }
      }
      if (minIndex !== i) {
        const tmp = arr[i];
        arr[i] = arr[minIndex];
        arr[minIndex] = tmp;
        swaps += 1;
        const swapStates = {};
        for (let idx = 0; idx < i; idx += 1) {
          swapStates[idx] = "sorted";
        }
        swapStates[i] = "swap";
        swapStates[minIndex] = "swap";
        frames.push({
          kind: "bars",
          line: 6,
          caption: "最小値 " + arr[i] + " を先頭へ移動しました。",
          stats: [["n", String(arr.length)], ["比較", String(comparisons)], ["交換", String(swaps)], ["パス", String(passes)]],
          payload: { items: arr.map((value, index) => ({ value, label: String(value), state: swapStates[index] || "default" })) }
        });
      }
      passes += 1;
      const sortedStates = {};
      for (let idx = 0; idx <= i; idx += 1) {
        sortedStates[idx] = "sorted";
      }
      frames.push({
        kind: "bars",
        line: 6,
        caption: arr[i] + " が位置 " + i + " で確定しました。",
        stats: [["n", String(arr.length)], ["比較", String(comparisons)], ["交換", String(swaps)], ["パス", String(passes)]],
        payload: { items: arr.map((value, index) => ({ value, label: String(value), state: sortedStates[index] || "default" })) }
      });
    }

    frames.push({
      kind: "bars",
      line: 6,
      caption: "整列が完了しました。",
      stats: [["n", String(arr.length)], ["比較", String(comparisons)], ["交換", String(swaps)], ["パス", String(passes)]],
      payload: { items: arr.map((value) => ({ value, label: String(value), state: "sorted" })) }
    });
    return frames;
  }

  function insertionSortFrames(values) {
    const arr = values.slice();
    const frames = [];
    let comparisons = 0;
    let shifts = 0;

    for (let i = 1; i < arr.length; i += 1) {
      const key = arr[i];
      let j = i - 1;
      const startStates = {};
      for (let idx = 0; idx < i; idx += 1) {
        startStates[idx] = "sorted";
      }
      startStates[i] = "swap";
      frames.push({
        kind: "bars",
        line: 2,
        caption: key + " を key として取り出します。",
        stats: [["n", String(arr.length)], ["比較", String(comparisons)], ["ずらし", String(shifts)], ["整列済み", String(i)]],
        payload: { items: arr.map((value, index) => ({ value, label: String(value), state: startStates[index] || "default" })) }
      });

      while (j >= 0) {
        comparisons += 1;
        const compareStates = {};
        for (let idx = 0; idx < i; idx += 1) {
          compareStates[idx] = "sorted";
        }
        compareStates[j] = "active";
        compareStates[j + 1] = "swap";
        frames.push({
          kind: "bars",
          line: 3,
          caption: arr[j] + " と key " + key + " を比べます。",
          stats: [["n", String(arr.length)], ["比較", String(comparisons)], ["ずらし", String(shifts)], ["整列済み", String(i)]],
          payload: { items: arr.map((value, index) => ({ value, label: String(value), state: compareStates[index] || "default" })) }
        });
        if (arr[j] > key) {
          arr[j + 1] = arr[j];
          shifts += 1;
          const shiftStates = {};
          for (let idx = 0; idx < i; idx += 1) {
            shiftStates[idx] = "sorted";
          }
          shiftStates[j] = "active";
          shiftStates[j + 1] = "swap";
          frames.push({
            kind: "bars",
            line: 4,
            caption: arr[j] + " を右へずらします。",
            stats: [["n", String(arr.length)], ["比較", String(comparisons)], ["ずらし", String(shifts)], ["整列済み", String(i)]],
            payload: { items: arr.map((value, index) => ({ value, label: String(value), state: shiftStates[index] || "default" })) }
          });
          j -= 1;
        } else {
          break;
        }
      }

      arr[j + 1] = key;
      const insertStates = {};
      for (let idx = 0; idx <= i; idx += 1) {
        insertStates[idx] = "sorted";
      }
      frames.push({
        kind: "bars",
        line: 5,
        caption: key + " を位置 " + (j + 1) + " に差し込みました。",
        stats: [["n", String(arr.length)], ["比較", String(comparisons)], ["ずらし", String(shifts)], ["整列済み", String(i + 1)]],
        payload: { items: arr.map((value, index) => ({ value, label: String(value), state: insertStates[index] || "default" })) }
      });
    }

    frames.push({
      kind: "bars",
      line: 5,
      caption: "整列が完了しました。",
      stats: [["n", String(arr.length)], ["比較", String(comparisons)], ["ずらし", String(shifts)], ["整列済み", String(arr.length)]],
      payload: { items: arr.map((value) => ({ value, label: String(value), state: "sorted" })) }
    });
    return frames;
  }

  function mergeSortFrames(values) {
    const arr = values.slice();
    const frames = [];
    let comparisons = 0;

    function push(line, caption, states) {
      frames.push({
        kind: "bars",
        line,
        caption,
        stats: [["n", String(arr.length)], ["比較", String(comparisons)]],
        payload: { items: arr.map((value, index) => ({ value, label: String(value), state: (states && states[index]) || "default" })) }
      });
    }

    function sortRange(left, right) {
      if (right - left <= 1) {
        return;
      }
      const mid = Math.floor((left + right) / 2);
      const splitStates = {};
      for (let i = left; i < mid; i += 1) {
        splitStates[i] = "active";
      }
      for (let i = mid; i < right; i += 1) {
        splitStates[i] = "swap";
      }
      push(1, left + " から " + (right - 1) + " を左右に分けます。", splitStates);
      sortRange(left, mid);
      sortRange(mid, right);
      const temp = [];
      let i = left;
      let j = mid;
      while (i < mid && j < right) {
        comparisons += 1;
        const compareStates = {};
        compareStates[i] = "active";
        compareStates[j] = "swap";
        push(4, arr[i] + " と " + arr[j] + " を比べます。", compareStates);
        if (arr[i] <= arr[j]) {
          temp.push(arr[i]);
          i += 1;
        } else {
          temp.push(arr[j]);
          j += 1;
        }
      }
      while (i < mid) {
        temp.push(arr[i]);
        i += 1;
      }
      while (j < right) {
        temp.push(arr[j]);
        j += 1;
      }
      for (let k = 0; k < temp.length; k += 1) {
        arr[left + k] = temp[k];
      }
      const mergedStates = {};
      for (let idx = left; idx < right; idx += 1) {
        mergedStates[idx] = "sorted";
      }
      push(4, left + " から " + (right - 1) + " が整列済みになりました。", mergedStates);
    }

    sortRange(0, arr.length);
    push(4, "整列が完了しました。", Object.fromEntries(arr.map((_, idx) => [idx, "sorted"])));
    return frames;
  }

  function quickSortFrames(values) {
    const arr = values.slice();
    const frames = [];
    let comparisons = 0;
    let swaps = 0;

    function push(line, caption, states) {
      frames.push({
        kind: "bars",
        line,
        caption,
        stats: [["n", String(arr.length)], ["比較", String(comparisons)], ["交換", String(swaps)]],
        payload: { items: arr.map((value, index) => ({ value, label: String(value), state: (states && states[index]) || "default" })) }
      });
    }

    function sortRange(low, high) {
      if (low >= high) {
        if (low === high) {
          push(4, arr[low] + " がこの範囲で確定しました。", { [low]: "sorted" });
        }
        return;
      }
      const pivot = arr[high];
      push(1, "基準値に " + pivot + " を選びます。", { [high]: "swap" });
      let i = low;
      for (let j = low; j < high; j += 1) {
        comparisons += 1;
        const states = { [j]: "active", [high]: "swap" };
        if (i < arr.length) {
          states[i] = "frontier";
        }
        push(2, arr[j] + " を基準値 " + pivot + " と比べます。", states);
        if (arr[j] < pivot) {
          const tmp = arr[i];
          arr[i] = arr[j];
          arr[j] = tmp;
          swaps += 1;
          push(2, arr[i] + " を左側グループへ送ります。", { [i]: "swap", [j]: "swap", [high]: "frontier" });
          i += 1;
        }
      }
      const tmp = arr[i];
      arr[i] = arr[high];
      arr[high] = tmp;
      swaps += 1;
      push(2, "基準値 " + arr[i] + " を位置 " + i + " に置きます。", { [i]: "sorted" });
      sortRange(low, i - 1);
      sortRange(i + 1, high);
    }

    sortRange(0, arr.length - 1);
    push(4, "整列が完了しました。", Object.fromEntries(arr.map((_, idx) => [idx, "sorted"])));
    return frames;
  }

  function heapSortFrames(values) {
    const arr = values.slice();
    const frames = [];
    const n = arr.length;
    let comparisons = 0;
    let swaps = 0;
    let heapSize = n;

    function push(line, caption, states) {
      frames.push({
        kind: "bars",
        line,
        caption,
        stats: [["n", String(n)], ["比較", String(comparisons)], ["交換", String(swaps)], ["heap", String(heapSize)]],
        payload: { items: arr.map((value, index) => ({ value, label: String(value), state: (states && states[index]) || "default" })) }
      });
    }

    function withSorted(active, sortedFrom) {
      const states = Object.assign({}, active || {});
      if (typeof sortedFrom === "number") {
        for (let i = sortedFrom; i < arr.length; i += 1) {
          states[i] = "sorted";
        }
      }
      return states;
    }

    function heapify(size, root) {
      while (true) {
        let largest = root;
        const left = 2 * root + 1;
        const right = 2 * root + 2;
        if (left < size) {
          comparisons += 1;
          push(4, arr[root] + " と左の子 " + arr[left] + " を比べます。", withSorted({ [root]: "active", [left]: "active" }, size));
          if (arr[left] > arr[largest]) {
            largest = left;
          }
        }
        if (right < size) {
          comparisons += 1;
          push(4, arr[largest] + " と右の子 " + arr[right] + " を比べます。", withSorted({ [largest]: "active", [right]: "active" }, size));
          if (arr[right] > arr[largest]) {
            largest = right;
          }
        }
        if (largest === root) {
          break;
        }
        const tmp = arr[root];
        arr[root] = arr[largest];
        arr[largest] = tmp;
        swaps += 1;
        push(4, arr[root] + " と " + arr[largest] + " を入れ替えてヒープ条件を回復します。", withSorted({ [root]: "swap", [largest]: "swap" }, size));
        root = largest;
      }
    }

    for (let start = Math.floor(n / 2) - 1; start >= 0; start -= 1) {
      push(1, "位置 " + start + " から下を max heap に整えます。", withSorted({ [start]: "active" }, heapSize));
      heapify(heapSize, start);
    }

    push(1, "max heap ができました。", { 0: "swap" });

    for (let end = n - 1; end > 0; end -= 1) {
      const tmp = arr[0];
      arr[0] = arr[end];
      arr[end] = tmp;
      swaps += 1;
      heapSize = end;
      push(2, "最大値 " + arr[end] + " を末尾 " + end + " へ送ります。", withSorted({ 0: "swap", [end]: "sorted" }, end + 1));
      heapify(heapSize, 0);
    }

    push(4, "整列が完了しました。", Object.fromEntries(arr.map((_, idx) => [idx, "sorted"])));
    return frames;
  }

  function countingSortFrames(values) {
    const arr = values.slice();
    const frames = [];
    const maxValue = arr.length ? Math.max.apply(null, arr) : 0;
    const counts = new Array(maxValue + 1).fill(0);
    const output = [];

    function buildItems(highlight) {
      const items = [];
      const marks = highlight || {};
      arr.forEach((value, index) => {
        items.push({ value, label: String(value), state: marks["arr-" + index] || "default" });
      });
      for (let value = 1; value < counts.length; value += 1) {
        items.push({
          value: Math.max(1, counts[value]),
          label: "c" + value + ":" + counts[value],
          state: marks["count-" + value] || "dim"
        });
      }
      output.forEach((value, index) => {
        items.push({ value, label: "o" + index + ":" + value, state: marks["out-" + index] || "sorted" });
      });
      return items;
    }

    arr.forEach((value, index) => {
      counts[value] += 1;
      frames.push({
        kind: "bars",
        line: 1,
        caption: value + " を読んで count[" + value + "] を 1 増やします。",
        stats: [["n", String(arr.length)], ["読んだ要素", String(index + 1)], ["出力済み", String(output.length)]],
        payload: { items: buildItems({ ["arr-" + index]: "active", ["count-" + value]: "swap" }) }
      });
    });

    for (let value = 1; value < counts.length; value += 1) {
      if (!counts[value]) {
        continue;
      }
      frames.push({
        kind: "bars",
        line: 2,
        caption: "値 " + value + " は " + counts[value] + " 個あります。",
        stats: [["n", String(arr.length)], ["count", value + " -> " + counts[value]], ["出力済み", String(output.length)]],
        payload: { items: buildItems({ ["count-" + value]: "active" }) }
      });
      for (let i = 0; i < counts[value]; i += 1) {
        output.push(value);
        frames.push({
          kind: "bars",
          line: 3,
          caption: value + " を出力列へ並べます。",
          stats: [["n", String(arr.length)], ["count", value + " -> " + counts[value]], ["出力済み", String(output.length)]],
          payload: { items: buildItems({ ["count-" + value]: "active", ["out-" + (output.length - 1)]: "sorted" }) }
        });
      }
    }

    frames.push({
      kind: "bars",
      line: 3,
      caption: "整列が完了しました。",
      stats: [["n", String(arr.length)], ["種類数", String(maxValue)], ["出力済み", String(output.length)]],
      payload: { items: output.map((value) => ({ value, label: String(value), state: "sorted" })) }
    });
    return frames;
  }

  function radixSortFrames(values) {
    const arr = values.slice();
    const frames = [];
    const maxValue = arr.length ? Math.max.apply(null, arr) : 0;
    let exp = 1;
    let passCount = 0;

    function digitLabel(value) {
      return String(value) + "|" + Math.floor(value / exp) % 10;
    }

    while (Math.floor(maxValue / exp) > 0) {
      passCount += 1;
      const buckets = Array.from({ length: 10 }, () => []);

      arr.forEach((value, index) => {
        const digit = Math.floor(value / exp) % 10;
        buckets[digit].push(value);
        frames.push({
          kind: "bars",
          line: 1,
          caption: value + " の " + exp + " の位は " + digit + " です。",
          stats: [["n", String(arr.length)], ["桁", String(exp)], ["パス", String(passCount)]],
          payload: { items: arr.map((item, i) => ({ value: item, label: digitLabel(item), state: i === index ? "active" : "default" })) }
        });
      });

      const rebuilt = [];
      for (let digit = 0; digit < buckets.length; digit += 1) {
        if (!buckets[digit].length) {
          continue;
        }
        Array.prototype.push.apply(rebuilt, buckets[digit]);
        frames.push({
          kind: "bars",
          line: 2,
          caption: exp + " の位が " + digit + " のものを前から並べます。",
          stats: [["n", String(arr.length)], ["桁", String(exp)], ["パス", String(passCount)]],
          payload: { items: rebuilt.concat([].concat(...buckets.slice(digit + 1))).map((value, index) => ({ value, label: String(value), state: index < rebuilt.length ? "sorted" : "default" })) }
        });
      }

      for (let i = 0; i < rebuilt.length; i += 1) {
        arr[i] = rebuilt[i];
      }
      frames.push({
        kind: "bars",
        line: 2,
        caption: exp + " の位で安定に並べ終わりました。",
        stats: [["n", String(arr.length)], ["桁", String(exp)], ["パス", String(passCount)]],
        payload: { items: arr.map((value) => ({ value, label: String(value), state: "sorted" })) }
      });
      exp *= 10;
    }

    frames.push({
      kind: "bars",
      line: 2,
      caption: "整列が完了しました。",
      stats: [["n", String(arr.length)], ["桁パス", String(passCount)], ["最大値", String(maxValue)]],
      payload: { items: arr.map((value) => ({ value, label: String(value), state: "sorted" })) }
    });
    return frames;
  }

  function renderCells(payload) {
    const items = payload.items.map((item) => {
      const cls = ["cell", stateClass(item.state)].filter(Boolean).join(" ");
      return [
        '<div class="' + cls + '">',
        '<span class="cell-main">' + escapeHtml(item.label) + "</span>",
        item.sub ? '<span class="cell-sub">' + escapeHtml(item.sub) + "</span>" : "",
        "</div>"
      ].join("");
    }).join("");
    return '<div class="cell-row">' + items + "</div>";
  }

  function renderGraph(payload) {
    const edges = payload.edges.map((edge) => {
      const from = payload.nodes.find((node) => node.id === edge.from);
      const to = payload.nodes.find((node) => node.id === edge.to);
      const cls = ["edge-line", stateClass(edge.state)].filter(Boolean).join(" ");
      const mx = (from.x + to.x) / 2;
      const my = (from.y + to.y) / 2;
      return [
        '<line class="' + cls + '" x1="' + from.x + '" y1="' + from.y + '" x2="' + to.x + '" y2="' + to.y + '"></line>',
        edge.label ? '<text class="edge-label" x="' + mx + '" y="' + my + '">' + escapeHtml(edge.label) + "</text>" : ""
      ].join("");
    }).join("");
    const nodes = payload.nodes.map((node) => {
      const cls = ["graph-node", stateClass(node.state)].filter(Boolean).join(" ");
      return [
        '<g class="' + cls + '">',
        '<circle cx="' + node.x + '" cy="' + node.y + '" r="22"></circle>',
        '<text x="' + node.x + '" y="' + (node.y + 6) + '">' + escapeHtml(node.label) + "</text>",
        "</g>"
      ].join("");
    }).join("");
    return [
      '<div class="graph-scene">',
      '<svg viewBox="0 0 540 280" role="img" aria-label="graph visualization">',
      edges,
      nodes,
      "</svg>",
      "</div>"
    ].join("");
  }

  function renderGrid(payload) {
    const rows = payload.rows.map((row) => {
      const cells = row.map((cell) => {
        const cls = ["grid-cell", stateClass(cell.state)].filter(Boolean).join(" ");
        return '<td class="' + cls + '">' + escapeHtml(cell.text) + "</td>";
      }).join("");
      return "<tr>" + cells + "</tr>";
    }).join("");
    return '<div class="grid-scene"><table class="grid-table"><tbody>' + rows + "</tbody></table></div>";
  }

  function renderTowers(payload) {
    const rods = payload.rods.map((rod) => {
      const discs = rod.map((disc) => {
        return '<div class="disc" style="width:' + (42 + disc * 22) + 'px;">' + disc + "</div>";
      }).join("");
      return '<div class="rod"><div class="rod-stack">' + discs + '</div><div class="rod-base"></div></div>';
    }).join("");
    return '<div class="tower-scene">' + rods + "</div>";
  }

  function renderCards(payload) {
    const cards = payload.items.map((item) => {
      const cls = ["mini-info-card", stateClass(item.state)].filter(Boolean).join(" ");
      return '<article class="' + cls + '"><strong>' + escapeHtml(item.title) + "</strong><p>" + escapeHtml(item.text) + "</p></article>";
    }).join("");
    return '<div class="mini-card-grid">' + cards + "</div>";
  }

  function renderScene(frame) {
    if (frame.kind === "bars") {
      return renderBars(frame.payload);
    }
    if (frame.kind === "cells") {
      return renderCells(frame.payload);
    }
    if (frame.kind === "graph" || frame.kind === "tree") {
      return renderGraph(frame.payload);
    }
    if (frame.kind === "grid") {
      return renderGrid(frame.payload);
    }
    if (frame.kind === "towers") {
      return renderTowers(frame.payload);
    }
    return renderCards(frame.payload);
  }

  function initPage() {
    if (!window.PAGE_DATA) {
      return;
    }

    const data = window.PAGE_DATA;
    const sceneEl = document.getElementById("scene");
    const captionEl = document.getElementById("frameCaption");
    const statsEl = document.getElementById("dynamicStats");
    const codeLines = Array.from(document.querySelectorAll(".code-line"));
    const prevButton = document.getElementById("prevButton");
    const nextButton = document.getElementById("nextButton");
    const playButton = document.getElementById("playButton");
    const resetButton = document.getElementById("resetButton");
    const speedInput = document.getElementById("speedInput");
    const toolbarEl = document.querySelector(".toolbar");

    let currentFrames = data.frames;
    let frameIndex = 0;
    let timerId = null;
    let generatorValues = null;

    function highlight(line) {
      codeLines.forEach((el) => {
        el.classList.toggle("active", Number(el.dataset.line) === Number(line));
      });
    }

    function render() {
      const frame = currentFrames[frameIndex];
      sceneEl.innerHTML = renderScene(frame);
      captionEl.textContent = frame.caption;
      statsEl.innerHTML = (frame.stats || []).map((item) => {
        return '<div class="stat"><span>' + escapeHtml(item[0]) + '</span><strong>' + escapeHtml(item[1]) + "</strong></div>";
      }).join("");
      highlight(frame.line || 0);
      prevButton.disabled = frameIndex === 0;
      nextButton.disabled = frameIndex === currentFrames.length - 1;
    }

    function stop() {
      if (timerId !== null) {
        clearTimeout(timerId);
        timerId = null;
      }
      playButton.textContent = "自動再生";
      playButton.dataset.playing = "false";
    }

    function tick() {
      if (frameIndex >= currentFrames.length - 1) {
        stop();
        return;
      }
      frameIndex += 1;
      render();
      timerId = window.setTimeout(tick, speedToDelay(Number(speedInput.value)));
    }

    function speedToDelay(value) {
      const ratio = value / 100;
      return Math.round(20 + (1 - ratio) * 780);
    }

    prevButton.addEventListener("click", function () {
      stop();
      frameIndex = Math.max(0, frameIndex - 1);
      render();
    });

    nextButton.addEventListener("click", function () {
      stop();
      frameIndex = Math.min(currentFrames.length - 1, frameIndex + 1);
      render();
    });

    resetButton.addEventListener("click", function () {
      stop();
      frameIndex = 0;
      render();
    });

    playButton.addEventListener("click", function () {
      if (playButton.dataset.playing === "true") {
        stop();
        return;
      }
      playButton.textContent = "停止";
      playButton.dataset.playing = "true";
      timerId = window.setTimeout(tick, speedToDelay(Number(speedInput.value)));
    });

    speedInput.addEventListener("input", function () {
      if (playButton.dataset.playing === "true") {
        stop();
        playButton.textContent = "停止";
        playButton.dataset.playing = "true";
        timerId = window.setTimeout(tick, speedToDelay(Number(speedInput.value)));
      }
    });

    if (Array.isArray(data.variants) && data.variants.length > 0 && !data.generator) {
      const label = document.createElement("label");
      label.setAttribute("for", "variantSelect");
      label.innerHTML = 'データ数 <select id="variantSelect"></select>';
      const select = label.querySelector("select");
      data.variants.forEach((variant, index) => {
        const option = document.createElement("option");
        option.value = String(index);
        option.textContent = variant.label;
        select.appendChild(option);
      });
      toolbarEl.appendChild(label);

      const defaultIndex = data.variants.length > 1 ? 1 : 0;
      select.value = String(defaultIndex);

      select.addEventListener("change", function () {
        stop();
        currentFrames = data.variants[Number(select.value)].frames;
        frameIndex = 0;
        render();
      });

      currentFrames = data.variants[defaultIndex].frames;
    }

    if (data.generator === "bubble-sort" || data.generator === "selection-sort" || data.generator === "insertion-sort" || data.generator === "merge-sort" || data.generator === "quick-sort" || data.generator === "heap-sort" || data.generator === "counting-sort" || data.generator === "radix-sort") {
      const wrap = document.createElement("label");
      wrap.setAttribute("for", "sizeInput");
      wrap.innerHTML = 'データ数 <input id="sizeInput" type="range" min="5" max="100" step="1"><span id="sizeValue"></span>';
      const sizeInput = wrap.querySelector("input");
      const sizeValue = wrap.querySelector("span");
      toolbarEl.appendChild(wrap);

      function rebuildFrames(n) {
        generatorValues = shuffledRange(n);
        currentFrames =
          data.generator === "bubble-sort"
            ? bubbleSortFrames(generatorValues)
            : data.generator === "selection-sort"
              ? selectionSortFrames(generatorValues)
              : data.generator === "insertion-sort"
                ? insertionSortFrames(generatorValues)
                : data.generator === "merge-sort"
                  ? mergeSortFrames(generatorValues)
                  : data.generator === "quick-sort"
                    ? quickSortFrames(generatorValues)
                    : data.generator === "heap-sort"
                      ? heapSortFrames(generatorValues)
                      : data.generator === "counting-sort"
                        ? countingSortFrames(generatorValues)
                        : radixSortFrames(generatorValues);
        frameIndex = 0;
        sizeValue.textContent = String(n);
        render();
      }

      sizeInput.value = String(data.defaultN || 12);
      rebuildFrames(Number(sizeInput.value));

      sizeInput.addEventListener("input", function () {
        stop();
        rebuildFrames(Number(sizeInput.value));
      });
    }

    render();
  }

  document.addEventListener("DOMContentLoaded", initPage);
})();
