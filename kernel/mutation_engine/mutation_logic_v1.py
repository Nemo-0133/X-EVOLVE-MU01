import time

class MutationBridge:
    def __init__(self, mc_core, mutation_engine):
        """
        mc_core: IE-MC-01 實例
        mutation_engine: IE-MU-01 實例
        """
        self.mc = mc_core
        self.mu = mutation_engine

        self.config = {
            "cycle_interval": 1.0,   # 每幾秒觸發一次
            "enabled": True
        }

    def run_cycle(self):
        """
        單次變異週期：
        1. 從 MC-01 抽 snapshot
        2. 丟給 MU-01 做變異
        3. 將變異結果回寫 MC-01
        """

        # 1️⃣ 取得狀態
        snapshot = self.mc.debug_snapshot()

        # 2️⃣ 進行變異
        mutations = self.mu.apply_mutation(snapshot)

        # 3️⃣ 注入回 MC-01
        for m in mutations:
            self.mc.process_input(m)

        # 4️⃣ L2 漂移（可選）
        drift = self.mu.stochastic_drift(self.mc.storage["L2_ARCHIVE"])
        if drift:
            self.mc.process_input({
                "content": drift,
                "delta_v": 0.2,
                "delta_s": 0.3,
                "type": "DRIFT_SIGNAL"
            })

        return {
            "snapshot": snapshot,
            "mutations": mutations,
            "drift": drift
        }

    def run(self, cycles=10):
        """
        持續運行多個 cycle
        """
        for i in range(cycles):
            result = self.run_cycle()

            print(f"\n=== MU CYCLE {i} ===")
            print("SNAPSHOT:", result["snapshot"])
            print("MUTATIONS:", result["mutations"])
            print("DRIFT:", result["drift"])

            time.sleep(self.config["cycle_interval"])
