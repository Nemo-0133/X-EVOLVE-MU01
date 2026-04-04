import time

class MutationBridge:
    def __init__(self, mc_core, mutation_engine, cycle_interval=1.0):
        """
        mc_core: 你的 MC-01 instance
        mutation_engine: IEMutationEngine instance
        """
        self.mc = mc_core
        self.mu = mutation_engine
        self.cycle_interval = cycle_interval
        self.running = False

    def run_cycle(self):
        """
        單次循環：
        MC-01 → Snapshot → MU-01 → 回寫
        """
        # 1️⃣ 取得當前狀態
        snapshot = self.mc.debug_snapshot()

        # 2️⃣ 套用變異
        mutations = self.mu.apply_mutation(snapshot)

        # 3️⃣ 將變異寫回 MC-01
        for m in mutations:
            self._inject_into_mc(m)

        # 4️⃣ 對 L2 做 drift（可選）
        drift = self.mu.stochastic_drift(None)
        if drift:
            self._inject_drift(drift)

        return {
            "snapshot": snapshot,
            "mutations": mutations,
            "drift": drift
        }

    def _inject_into_mc(self, mutation):
        """
        將 mutation 寫入 MC-01（當作一筆 L1 記憶）
        """
        # ⚠️ 這裡要對齊你 MC-01 的寫入接口
        self.mc.write(
            content=mutation["content"],
            delta_v=mutation["delta_v"],
            delta_s=mutation["delta_s"],
            source=mutation["type"]
        )

    def _inject_drift(self, drift_data):
        """
        對 L2 記憶做干擾（如果你有 archive API）
        """
        if hasattr(self.mc, "inject_drift"):
            self.mc.inject_drift(drift_data)

    def start(self, cycles=10):
        """
        開始循環運行
        """
        self.running = True
        results = []

        for i in range(cycles):
            result = self.run_cycle()
            results.append(result)

            print(f"[Cycle {i}] →", result)

            time.sleep(self.cycle_interval)

        self.running = False
        return results
