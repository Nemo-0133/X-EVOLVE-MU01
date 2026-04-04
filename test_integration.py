from kernel.memory_core.memory_core_v1 import IEMemoryCore
from kernel.mutation_engine.mutation_logic_v1 import IEMutationEngine
from kernel.mutation_engine.bridge_protocol import run_cycle

import time

# 初始化
mc = IEMemoryCore()
mu = IEMutationEngine()

print("=== SYSTEM START ===")

# 模擬 30 個 cycle
for step in range(30):

    print(f"\n--- CYCLE {step} ---")

    # 🔹 外部正常輸入
    result = mc.process_input({
        "content": f"external_event_{step}",
        "delta_v": 0.7,
        "delta_s": 0.6
    })

    print("INPUT:", result)

    # 🔥 核心：執行 bridge（讓 MU 干擾 MC）
    mutations = run_cycle(mc, mu)

    if mutations:
        print("⚠️ MUTATION TRIGGERED:")
        for m in mutations:
            print(m)

    # 系統代謝
    mc.system_update()

    # 觀測狀態
    print("SNAPSHOT:", mc.debug_snapshot())

    time.sleep(0.2)

print("\n=== FINAL STATE ===")
print(mc.debug_snapshot())
