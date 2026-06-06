package magearena;

public class Enemy extends Character {
    private static final int RAGE_THRESHOLD = 40;
    private static final int RAGE_DAMAGE_BONUS = 6;

    public Enemy(String name) {
        super(name, 120, 10);
    }

    @Override
    public int attack(Character target) {
        int damage = getAttackPower();
        if (getHealth() <= RAGE_THRESHOLD) {
            damage += RAGE_DAMAGE_BONUS;
        }
        return target.takeDamage(damage);
    }
}
