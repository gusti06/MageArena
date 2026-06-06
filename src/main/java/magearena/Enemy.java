package magearena;

public class Enemy extends Character {
    public Enemy(String name) {
        super(name, 120, 10);
    }

    @Override
    public int attack(Character target) {
        int damage = getAttackPower();
        if (getHealth() <= 40) {
            damage += 6;
        }
        return target.takeDamage(damage);
    }
}
