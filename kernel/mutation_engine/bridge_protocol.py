import time

class MemoryMutationBridge:
    def __init__(self, memory_core, mutation_engine):
        self.memory = memory_core
        self.mutator = mutation_engine
        self.cycle_count = 0

    def run_cycle(self):
        """
        一個完整循環：
        1. 從 MC01 抽取狀態
        2. 丟給 MU01 做變異
        3. 再寫回 MC01
        """

        # 1️⃣ 抽取狀態
        snapshot = self.memory.export_state()

        # 2️⃣ 套用變異
        mutations = self.mutator.apply_mutation(snapshot)

        # 3️⃣ 寫回記憶核心
        for m in mutations:
            self.memory.process_input(m)

        self.cycle_count += 1

        return {
            "cycle": self.cycle_count,
            "mutations_applied": len(mutations),
            "pain": round(snapshot["PAIN_LEVEL"], 3),
            "tolerance": round(snapshot["TOLERANCE"], 3)
        }

    def run_loop(self, cycles=10, delay=0.5):
        """
        自動執行多個循環（模擬「潛意識持續干擾」）
        """
        for _ in range(cycles):
            result = self.run_cycle()
            print(result)
            time.sleep(delay)
