__all__ = [
    "Invalidate"
]

class Invalidate():

    def _after_update(self):
        del self._after_update_id
        self._update()

    def _invalidate(self):
        if hasattr(self, "_after_update_id"):
            return
        self._after_update_id = self.after(100, self._after_update)
