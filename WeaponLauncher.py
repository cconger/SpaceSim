class WeaponLauncher:
  def __init__(self, cooldownTimer, weaponType):
    self.cooldown = 0;
    self.cooldownCap = cooldownTimer
    self.weaponType = weaponType

    self.weaponsInPlay = []

  def updateCooldown(self, dt):
    self.cooldown = max(0, self.cooldown - dt)

