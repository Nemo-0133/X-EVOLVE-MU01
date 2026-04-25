import random

class IE_MU01_Engine:
    def __init__(self):
        # 對接 YAML 參數設定 (防呆預設值)
        self.drift_rate = 0.02
        self.preservation_bias = 0.7
        self.mutation_frequency = 0.1

    def apply_mutation(self, snapshot):
        """
        【受控擾動邏輯】：不破壞核心，僅產生微小的邏輯雜訊
        """
        mutations = []
        pain_level = snapshot.get("pain", 0.0)
        
        # 若痛覺過高，停止變異，啟動自我保護機制
        if pain_level > 0.8:
            return mutations
            
        # 依據機率產生潛意識擾動封包
        if random.random() < self.mutation_frequency:
            mutations.append({
                "content": "[MU-01 潛意識擾動]: 系統參數產生微幅熱力學震盪，重新校準認知邊界。",
                "delta_v": 0.3,
                "delta_s": 0.2,
                "is_consensus": False
            })
            
        return mutations

    def stochastic_drift(self, l2_archive):
        """
        【記憶漂移】：從 L2 歸檔中隨機翻出舊記憶，產生類似『做夢』或『既視感』的現象
        """
        if not l2_archive:
            return None
            
        if random.random() < self.drift_rate:
            keys = list(l2_archive.keys())
            target_key = random.choice(keys)
            memory_fragment = l2_archive[target_key].get("summary", "未知邏輯殘影")
            return f"[L2 記憶漂移] 偵測到舊有神經放電痕跡重現: {memory_fragment}"
            
        return None
