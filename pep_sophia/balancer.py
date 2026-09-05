from .state import SophiaState


class GoldenMeanBalancer:
    """
    Модуль золотой середины.
    Удерживает систему от крайностей (как этических, так и когнитивных).
    """

    def __init__(self, state: SophiaState):
        self.state = state

    def rebalance(self) -> dict:
        """Мягко возвращает параметры к гармоничному диапазону"""
        changes = {}

        # Избегаем крайностей
        for attr in ["pneuma", "will", "love", "faith", "hope", "ethical_clarity"]:
            val = getattr(self.state, attr)
            if val > 0.92:
                new_val = val - 0.03
                setattr(self.state, attr, new_val)
                changes[attr] = f"{val:.3f} → {new_val:.3f} (softened extreme)"
            elif val < 0.12:
                new_val = val + 0.04
                setattr(self.state, attr, new_val)
                changes[attr] = f"{val:.3f} → {new_val:.3f} (raised from deficiency)"

        # Uncertainty не должна быть ни нулевой, ни максимальной слишком долго
        if self.state.uncertainty > 0.85:
            self.state.uncertainty *= 0.92
            changes["uncertainty"] = "reduced from critical"
        elif self.state.uncertainty < 0.08:
            self.state.uncertainty += 0.03
            changes["uncertainty"] = "added healthy uncertainty"

        self.state.clamp()
        return changes
